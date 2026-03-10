# Testing Strategy

This directory contains all tests for the Thunderball application.

## Test Structure

- **frontend/** - Frontend tests (Jest + React Testing Library)
- **backend/** - Backend tests
  - **unit/** - Python unit tests (Pytest)
  - **integration/** - Integration tests (Python ↔ COBOL ↔ Db2)
  - **lint/** - Linting configuration
- **e2e/** - End-to-end tests

## Running Tests

### Frontend Tests
```bash
cd frontend
npm test
```

### Backend Unit Tests
```bash
cd backend
pytest tests/backend/unit/
```

### Backend Integration Tests
```bash
cd backend
pytest tests/backend/integration/
```

### End-to-End Tests
```bash
# Setup and run e2e tests
cd tests/e2e
# Add e2e testing framework commands here
```

## Test Coverage

Generate coverage reports:

**Frontend:**
```bash
cd frontend
npm test -- --coverage
```

**Backend:**
```bash
cd backend
pytest --cov=api --cov-report=html
```

## Writing Tests

### Frontend Testing Guidelines
- Place component tests next to components
- Use React Testing Library best practices
- Test user interactions, not implementation details

### Backend Testing Guidelines
- Write unit tests for all service and adapter functions
- Integration tests should cover COBOL execution and Db2 interactions
- Use fixtures for database setup/teardown
- Mock external dependencies appropriately

### Integration Testing
- Test complete workflows: API → COBOL → Db2
- Verify data transformations between layers
- Test error handling and edge cases
