"""
Utility functions
"""
import hashlib
from datetime import datetime
from typing import Any

def generate_id(input_str: str) -> str:
    """Generate a unique ID from input string"""
    return hashlib.sha256(input_str.encode()).hexdigest()[:16]

def format_timestamp(dt: datetime) -> str:
    """Format datetime to ISO string"""
    return dt.isoformat()

def validate_config(config: dict) -> bool:
    """Validate configuration dictionary"""
    required_keys = ['app', 'database', 'api']
    return all(key in config for key in required_keys)
