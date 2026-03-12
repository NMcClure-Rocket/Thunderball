#utilities/logger.py
import logging
import logging.config
import yaml
import os
#from utilities.config import YamlReader

#Ensures logging security so that malicious user cannot define a new path
ALLOWED_LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))

#Create private SmartLogger wrapper class that optimizes the logging by only calling if the yaml
#is set to that level or above. Stacklevel is set to 2 to ensure the original call's file will be
#output and not the wrapper.
class _SmartLogger:
    '''
    This class optimizes the speed of the loggers by discarding logs below the currently set
    sensitivity. To change this, disable the SmartLogger variable in the log config
    '''
    def __init__(self, name):
        self._logger = logging.getLogger(name)

    def debug(self, msg, *args, **kwargs):
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(msg, *args, stacklevel = 2, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self._logger.isEnabledFor(logging.INFO):
            self._logger.info(msg, *args, stacklevel = 2, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self._logger.isEnabledFor(logging.WARNING):
            self._logger.warning(msg, *args, stacklevel = 2, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self._logger.isEnabledFor(logging.ERROR):
            self._logger.error(msg, *args, stacklevel = 2, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, stacklevel = 2, **kwargs)

    #Allows traceback
    def exception(self, msg, *args, **kwargs):
        self._logger.exception(msg, *args, stacklevel = 2, **kwargs)

#Create singleton Logger factory to ensure only one Logger is allocated.
class LoggerFactory:
    '''
    This class is a static singleton that produces a single logger of each type (security and general).
    Depending on the logger config SmartLogger will be turned on, which saves memory and optimizes speed
    '''
    _initialized = False
    _general_logger = None
    _security_logger = None
    _use_smart_logger = True #Default; change in config!

    @staticmethod
    def _is_safe_log_path(path: str) -> bool:
        '''
        Checks a given tag against the ALLOWED_LOG_DIR path

        Args:
            path (str): the file path to check

        Returns:
            is_safe (bool): a boolean that determines if the path starts with the ALLOWED_LOG_DIR
        '''
        abs_path = os.path.abspath(path)
        is_safe = abs_path.startswith(ALLOWED_LOG_DIR)
        return is_safe

    @staticmethod
    def initialize() -> None:
        '''
        Initialize the LoggerFactory, create or connect logging files, and read the logging config to set
        certain variables. If it is initialized, do nothing
        '''
        if LoggerFactory._initialized:
            return
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        #Ensure the proper files are in place; if not, create them
        logs_dir = os.path.join(base_dir, 'logs')
        os.makedirs(logs_dir, exist_ok=True)

        general_log_path = os.path.join(logs_dir, 'general.log')
        security_log_path = os.path.join(logs_dir, 'security.log')
        for path in [general_log_path, security_log_path]:
            if not os.path.exists(path):
                with open(path, 'w'):
                    pass

        config_path = os.path.join(base_dir, 'configs', 'logging_config.yaml')
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        LoggerFactory._use_smart_logger = config.get("use_smart_logger", True)

        #Set the absolute path of the log files inside the config file
        for _, handler in config.get("handlers", {}).items():
            if "filename" in handler and "{LOG_DIR}" in handler["filename"]:
                resolved_path = handler["filename"].replace("{LOG_DIR}", logs_dir)
                if not LoggerFactory._is_safe_log_path(resolved_path):
                    raise ValueError(f"Unsafe log path detected: {resolved_path}")
                handler["filename"] = resolved_path

        logging.config.dictConfig(config)
        LoggerFactory._initialized = True

    @staticmethod
    def get_general_logger() -> logging.Logger:
        '''
        Returns the general logger. First initalizes LoggerFactory if not already initialized

        Returns:
            general_logger (logging.Logger): the logger for the general.log file
        '''
        LoggerFactory.initialize()
        if LoggerFactory._general_logger is None:
            if LoggerFactory._use_smart_logger:
                LoggerFactory._general_logger = _SmartLogger("generalLogger")
            else:
                LoggerFactory._general_logger = logging.getLogger("generalLogger")
        return LoggerFactory._general_logger

    @staticmethod
    def get_security_logger() -> logging.Logger:
        '''
        Returns the security logger. First initalizes LoggerFactory if not already initialized

        Returns:
            security_logger (logging.Logger): the logger for the security.log file
        '''
        LoggerFactory.initialize()
        if LoggerFactory._security_logger is None:
            if LoggerFactory._use_smart_logger:
                LoggerFactory._security_logger = _SmartLogger("securityLogger")
            else:
                LoggerFactory._security_logger = logging.getLogger("securityLogger")
        return LoggerFactory._security_logger