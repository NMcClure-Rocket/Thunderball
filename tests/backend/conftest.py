"""
Pytest configuration for backend tests.
Adds the backend directory to sys.path so that `from api.xxx import ...` works.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))
