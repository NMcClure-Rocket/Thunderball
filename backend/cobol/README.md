# COBOL Programs

This directory contains all COBOL source programs and related files.

## Directory Structure

- **src/** - COBOL source programs (.cbl, .cob files)
- **copybooks/** - COBOL copybooks (shared data structures)
- **jcl/** - JCL scripts for executing COBOL programs
- **build/** - Compiled load modules (output directory)

## Development Workflow

### 1. Writing COBOL Programs

Place your COBOL source files in the `src/` directory.

### 2. Copybooks

Place shared data structures and includes in the `copybooks/` directory.

### 3. Compilation

Use the build script to compile COBOL programs:
```bash
../../infrastructure/scripts/build_cobol.sh
```

Compiled modules will be placed in the `build/` directory.

### 4. Execution

COBOL programs can be executed via:
- JCL scripts in the `jcl/` directory
- Python wrapper in `../api/adapters/cobol_runner.py`

## Integration with Python

The Python backend can call COBOL programs through the CobolRunner adapter.
See `../api/adapters/cobol_runner.py` for implementation details.

## Testing

Test COBOL programs using the integration tests in `../../tests/backend/integration/`.
