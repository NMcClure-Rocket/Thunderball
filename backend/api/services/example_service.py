"""
Example service with business logic
"""

import logging

logger = logging.getLogger(__name__)


class ExampleService:
    """Handles business logic for examples"""

    def __init__(self):
        pass

    def process_data(self, data: dict) -> dict:
        """Process data with business logic"""
        logger.info("Processing data...")
        # Add your business logic here
        return {"processed": True, "data": data}

    def validate_input(self, data: dict) -> bool:
        """Validate input data"""
        # Add validation logic
        return True
