"""
Unit tests for example service
"""
import pytest
from backend.api.services.example_service import ExampleService

@pytest.fixture
def example_service():
    return ExampleService()

def test_process_data(example_service):
    """Test data processing"""
    input_data = {"key": "value"}
    result = example_service.process_data(input_data)
    
    assert result["processed"] is True
    assert result["data"] == input_data

def test_validate_input(example_service):
    """Test input validation"""
    valid_data = {"name": "test", "value": 10}
    assert example_service.validate_input(valid_data) is True
