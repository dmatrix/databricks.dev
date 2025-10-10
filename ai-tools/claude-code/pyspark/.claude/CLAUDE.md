
# Project Structure Rules for Databricks Projects

## Directory Organization

### Root Level

**REQUIRED DIRECTORIES:**

- `/src/project_name_placeholder/` - Main package code
- `/src/` - Main notebook code (.ipynb) and Python files that will be called directly
- `/tests/` - Test files
- `/docs/` - Documentation
- `/scripts/` - Development and setup scripts ONLY
- `/data/` - Internal data ONLY (no scripts)
- Configuration files (setup.py, requirements.txt, etc.)

**Standard Project Structure:**
```
project-name/
├── src/
│   ├── project_name/           # Main package code
│   │   ├── __init__.py
│   │   └── *.py               # Python modules
│   ├── *.py                   # Python files called directly
│   └── *.ipynb                # Notebooks called directly
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── docs/
│   └── *.md
├── scripts/
│   └── *.sh, *.py             # Setup/dev scripts ONLY
├── data/
│   └── *.csv, *.json          # Internal data ONLY
├── .cursor/
│   └── rules/
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

### Scripts Location

**CRITICAL RULES:**
- ALL scripts must be in `/scripts/`
- NEVER put scripts in `/data/`, unless they are data generation scripts
- NO OTHER DIRECTORIES ALLOWED

## File Naming Conventions

### Python Files
- Use **snake_case** for all Python files: `data_processor.py`, `taxi_analytics.py`
- Prefix test files with `test_`: `test_data_processor.py`
- Use descriptive names that indicate purpose: `transform_taxi_data.py` not `utils.py`
- Avoid generic names like `helper.py`, `common.py`, `misc.py`

### Notebooks  
- Use descriptive names with hyphens: `01-data-exploration.ipynb`
- Number notebooks if they have a logical sequence: `01-`, `02-`, `03-`
- Place in `/src/` if called directly, or in `/src/project_name/` if part of package

### Directories
- Use **snake_case** for directory names
- Only use the approved directories: `/src/`, `/tests/`, `/docs/`, `/scripts/`, `/data/`
- NO additional directories at root level without explicit approval

## Code Organization Rules

### Source Code Location

**`/src/project_name/` - Main Package Code**
- All reusable Python modules
- Functions and classes imported by other code
- Library-style code
- Must have `__init__.py`

Example structure:
```python
src/project_name/
├── __init__.py
├── config.py           # Configuration
├── transforms.py       # Data transformations
├── models.py          # Data models/schemas
└── utils.py           # Utility functions
```

**`/src/` - Directly Called Files**
- Python files that are executed directly
- Notebooks (.ipynb) for analysis or workflows
- Entry point scripts
- Job definitions

Example:
```
src/
├── main.py                    # Entry point script
├── data_pipeline.py          # Direct execution
└── analysis_notebook.ipynb   # Databricks notebook
```

### Test Organization

**`/tests/` - All Test Files**
- Mirror the structure of `/src/`
- Must have `__init__.py`
- Use `test_` prefix for all test files
- One test file per source file

Example:
```
tests/
├── __init__.py
├── test_main.py
├── test_transforms.py
└── test_utils.py
```

## File Placement Rules

### `/src/` - Source Code
- **Package code**: `/src/project_name/*.py` (reusable modules)
- **Direct execution files**: `/src/*.py` (entry points)
- **Notebooks**: `/src/*.ipynb` (analysis, workflows)

### `/tests/` - Test Files Only
- All test files with `test_` prefix
- Must have `__init__.py`
- Mirror `/src/` structure
- Test fixtures and mock data (small files only)

### `/scripts/` - Development & Setup Scripts ONLY
- Setup scripts (setup.sh, deploy.sh)
- Development utilities
- CI/CD scripts
- Build scripts
- **NEVER put data processing code here** (that goes in `/src/`)

### `/data/` - Internal Data ONLY
- Sample data files
- Test datasets (small)
- Configuration data
- **NO SCRIPTS** (except data generation scripts)
- This is for data files, not code

### `/docs/` - Documentation
- Markdown files
- Architecture diagrams
- API documentation
- User guides

### Root Directory - Configuration Only
- `pyproject.toml`, `requirements.txt`, `uv.lock`
- `README.md`, `LICENSE`, `.gitignore`
- `.cursor/`, `.github/` directories
- **NO Python modules or scripts in root**

## Import Organization

**Always use this import order:**

1. Standard library imports
2. Third-party library imports  
3. Local application imports

**Use absolute imports** (not relative):

```python
# Good
from project_name.config import get_spark
from project_name.transforms import process_taxi_data

# Bad
from ..config import get_spark
from .transforms import process_taxi_data
```

**Example:**
```python
# Standard library
import os
from typing import Optional

# Third-party
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, when

# Local
from project_name.config import get_spark
from project_name.transforms import process_taxi_data
```

## Configuration Files

### Root Configuration Files
- `pyproject.toml` - Project metadata and dependencies
- `requirements.txt` - Pinned dependencies (generated by uv)
- `uv.lock` - Lock file (generated by uv)
- `.gitignore` - Git exclusions
- `README.md` - Project documentation

### Cursor Configuration
- `.cursor/rules/` - All Cursor rules files (`.mdc` files)

## Documentation

### Required Files
- `README.md` - Project overview, setup instructions, usage
- Put in root directory

### Extended Documentation
- Place in `/docs/` directory
- Use markdown files
- Examples: `docs/api.md`, `docs/architecture.md`

## Environment and Secrets

### NEVER Commit
- `.env` files
- `.databricks/` directory
- Credentials or tokens
- Local configuration overrides

### Secret Management
- Use environment variables
- Use Databricks secrets
- Document required secrets in README

## Version Control

### ALWAYS Commit
- Source code in `/src/`
- Tests in `/tests/`
- Documentation in `/docs/`
- Scripts in `/scripts/`
- Configuration files: `pyproject.toml`, `.gitignore`, `README.md`
- Cursor rules in `.cursor/rules/`
- `uv.lock`

### NEVER Commit
- Virtual environments: `.venv/`, `venv/`
- Compiled Python: `*.pyc`, `__pycache__/`
- Environment files: `.env`, `.databricks/`
- Large data files (use `/data/` for small samples only)
- Credentials or secrets
- Build artifacts

### Recommended .gitignore
```gitignore
# Python
__pycache__/
*.py[cod]
.Python
.venv/
venv/

# Databricks
.databricks/

# Environment
.env
.env.local

# IDE (keep .cursor/rules/)
.vscode/
.idea/

# Data (except test fixtures)
data/*.csv
data/*.parquet
!data/sample*.json

# OS
.DS_Store
```

## Critical Rules Summary

### Directory Structure
✅ **REQUIRED**: `/src/`, `/tests/`, `/docs/`, `/scripts/`, `/data/`  
❌ **FORBIDDEN**: Any other directories at root level

### Scripts Placement
✅ **ALL scripts** → `/scripts/`  
❌ **NEVER** → `/data/` (unless data generation)  
❌ **NO OTHER LOCATIONS**

### Source Code
✅ **Package modules** → `/src/project_name/`  
✅ **Direct execution** → `/src/` (notebooks, entry points)  
❌ **NEVER in root**

### Tests
✅ **ALL tests** → `/tests/`  
✅ **Mirror structure** of `/src/`  
✅ **test_ prefix** required

### Data Files  
✅ **Internal data only** → `/data/`  
❌ **NO SCRIPTS** in `/data/`  
❌ **NO LARGE FILES** (use external storage)

## Anti-Patterns

❌ Code files in root directory  
❌ Scripts in `/data/` directory  
❌ Tests mixed with source code  
❌ Creating unauthorized directories  
❌ Generic names like `utils.py`, `helper.py` in root  

✅ Clear separation: src, tests, scripts, data, docs  
✅ Descriptive, specific file names  
✅ Consistent structure across projects  
✅ Follow the rules strictly

# Python Development Rules for Databricks Projects

## General Python Guidelines

- Use the DRY principle, composition over inheritance, pure functions when possible
- 
- Use Python 3.11+ features and syntax
- Follow PEP 8 style guidelines for code formatting
- Use type hints for all function signatures and class attributes
- Write descriptive docstrings for all public functions, classes, and modules
- Keep functions focused and under 50 lines when possible
- Use descriptive variable names that convey intent

## Testing (Critical)
- **pytest only** (no unittest) - all tests must be in `/tests/` directory with `__init__.py` file
- Test Driven Development (TDD) approach: write/update test for all modified code
- All tests must pass before task completion

## Dependency Management

- ALWAYS use `uv` for package management (never pip, poetry, or conda)
- Add dependencies to `pyproject.toml` under `[project.dependencies]`
- Run `uv sync` after adding new dependencies
- Generate `requirements.txt` with `uv pip compile pyproject.toml -o requirements.txt`
- Pin dependency versions for reproducibility

## Testing Framework

- ALWAYS use `pytest` for testing (NEVER unittest)
- Place all tests in a `tests/` directory at the project root
- Name test files with `test_` prefix (e.g., `test_main.py`)
- Name test functions descriptively: `test_<what_is_being_tested>_<expected_outcome>`
- Use pytest fixtures for reusable test data and setup
- Create one happy path test with multiple assertions per function
- Create one failure/edge case test per function
- Use `pytest.raises()` for exception testing
- Keep tests independent and idempotent

Example:
```python
def test_get_taxis_returns_dataframe_with_expected_columns():
    spark = get_spark()
    df = get_taxis(spark)
    
    assert df is not None
    assert "tpep_pickup_datetime" in df.columns
    assert df.count() > 0
```

## Project Structure

**Note:** Detailed project structure rules are defined in `project-structure-rules.mdc`.

**Quick Reference:**
- Source code → `/src/project_name/` (package) and `/src/` (scripts, notebooks)
- Tests → `/tests/` (mirror src structure)
- Scripts → `/scripts/` (setup, dev scripts only)
- Data → `/data/` (internal data only, no scripts)
- Docs → `/docs/`

## Code Quality

- Use `ruff` for linting and formatting
- Run linter before committing code
- Fix all linter errors and warnings
- Avoid code duplication - extract common logic into functions
- Use list comprehensions for simple iterations
- Use context managers (`with` statements) for resource management

## Error Handling
 - Specfic exception types, validate inputs early
 - f-strings, comprehensions, context-managers
- Use specific exception types (never bare `except:`)
- Provide informative error messages
- Log errors with context information
- Handle expected errors gracefully
- Let unexpected errors bubble up with clear stack traces

Example:
```python
try:
    df = spark.read.table("samples.nyctaxi.trips")
except Exception as e:
    raise ValueError(f"Failed to read table: {e}") from e
```

## Documentation

- Write docstrings in Google style format
- Include type hints in docstrings when helpful
- Document all parameters and return values
- Provide usage examples in docstrings for complex functions
- Keep README.md up to date with setup and usage instructions

Example:
```python
def get_taxis(spark: SparkSession) -> DataFrame:
    """Retrieve NYC taxi trip data from Databricks sample tables.
    
    Args:
        spark: An active SparkSession instance
        
    Returns:
        DataFrame containing NYC taxi trip records with columns:
        - tpep_pickup_datetime
        - tpep_dropoff_datetime
        - trip_distance
        - fare_amount
        - pickup_zip
        - dropoff_zip
        
    Raises:
        ValueError: If the table cannot be accessed
        
    Example:
        >>> spark = get_spark()
        >>> df = get_taxis(spark)
        >>> df.show(5)
    """
    return spark.read.table("samples.nyctaxi.trips")
```

## Databricks-Specific Guidelines

- Use `DatabricksSession` instead of standard `SparkSession`
- Configure with DEFAULT profile for consistency with AI tools
- Use `.serverless(False)` or `.serverless(True)` explicitly
- Handle connection errors gracefully with informative messages
- Use DataFrame API over SQL when possible for better type safety
- Import PySpark functions explicitly: `from pyspark.sql.functions import col, when`

## Imports

- Group imports in this order:
  1. Standard library imports
  2. Third-party library imports
  3. Local application imports
- Use absolute imports over relative imports
- Sort imports alphabetically within each group
- Avoid wildcard imports (`from module import *`)

Example:
```python
# Standard library
from typing import Optional

# Third-party
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, when, avg

# Local
from my_project.config import settings
```

## Version Control

- Write clear, descriptive commit messages
- Commit logical units of work
- Don't commit generated files (.pyc, __pycache__, .venv)
- Keep .gitignore updated
- Review diffs before committing

## Performance

- Use DataFrame operations over collect() when possible
- Avoid unnecessary data shuffling
- Cache DataFrames that are reused multiple times
- Use appropriate partition sizes
- Profile code to identify bottlenecks before optimizing

## Security

- Never hardcode credentials or secrets
- Use environment variables or secret management systems
- Don't commit sensitive information to version control
- Use authentication profiles (DEFAULT) for Databricks access

---
globs: **/test_*.py,**/tests/**/*.py
alwaysApply: false
---
# Testing Rules for Databricks Projects

## Test Function Limits

**CRITICAL**: When creating test functions, create **MAXIMUM 2 tests per function being tested**.

Avoid creating Test Classes; stick to test functions

### Test Pattern

For each function being tested, create:

1. **One happy path test** with multiple assertions covering normal cases
2. **One edge case/failure test** with multiple assertions covering error conditions

### Multiple Assertions Strategy

✅ **DO**: Combine related checks in a single test function
```python
def test_get_taxis_returns_valid_dataframe():
    """Test that get_taxis returns a DataFrame with correct structure and data."""
    spark = get_spark()
    df = get_taxis(spark)
    
    # Multiple assertions in one test
    assert df is not None, "DataFrame should not be None"
    assert isinstance(df, DataFrame), "Should return DataFrame type"
    assert df.count() > 0, "DataFrame should contain records"
    assert "trip_distance" in df.columns, "Should have trip_distance column"
    assert "fare_amount" in df.columns, "Should have fare_amount column"
    assert df.filter(df.trip_distance < 0).count() == 0, "No negative distances"
```

❌ **DON'T**: Create separate test for each assertion
```python
# BAD - Too many tests for one function
def test_get_taxis_returns_dataframe():
    df = get_taxis(get_spark())
    assert df is not None

def test_get_taxis_has_columns():
    df = get_taxis(get_spark())
    assert "trip_distance" in df.columns

def test_get_taxis_has_records():
    df = get_taxis(get_spark())
    assert df.count() > 0

# This creates 3+ tests for one function - WRONG!
```

### Test Organization

**For a single function under test:**

```python
def test_function_name_happy_path():
    """Test normal/expected behavior with multiple validations."""
    # Setup
    result = function_under_test(valid_input)
    
    # Multiple assertions for happy path
    assert result is not None
    assert result.expected_property == expected_value
    assert len(result.collection) > 0
    assert result.validates_correctly()
```

```python
def test_function_name_edge_cases():
    """Test error conditions and edge cases with multiple validations."""
    # Test multiple edge cases in one function
    
    # Edge case 1: Empty input
    with pytest.raises(ValueError):
        function_under_test(None)
    
    # Edge case 2: Invalid input
    with pytest.raises(ValueError):
        function_under_test(invalid_value)
    
    # Edge case 3: Boundary condition
    result = function_under_test(boundary_value)
    assert result.handled_correctly
```

## Real Example from Project

```python
def test_get_taxis_returns_dataframe():
    """Test that get_taxis returns a DataFrame with expected structure."""
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_taxis
    
    spark = get_spark()
    df = get_taxis(spark)
    
    # Verify DataFrame is not None
    assert df is not None
    
    # Verify expected columns exist (multiple assertions)
    expected_columns = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "trip_distance",
        "fare_amount",
        "pickup_zip",
        "dropoff_zip"
    ]
    
    for col in expected_columns:
        assert col in df.columns, f"Expected column '{col}' not found"
    
    # Verify DataFrame has data
    assert df.count() > 0, "DataFrame should contain records"


def test_get_taxis_has_mostly_positive_fare_amounts():
    """Test that most fare amounts are positive (edge cases)."""
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_taxis
    
    spark = get_spark()
    df = get_taxis(spark)
    
    # Multiple validations in one test
    total_count = df.count()
    negative_fares = df.filter(df.fare_amount < 0).count()
    positive_ratio = (total_count - negative_fares) / total_count
    
    # At least 99% of fares should be non-negative
    assert positive_ratio >= 0.99, f"Expected at least 99% positive fares"
    assert negative_fares < 100, "Too many negative fares"
```

## Why This Approach?

### Benefits:
✅ **Efficiency**: Fewer test functions means faster test execution  
✅ **Clarity**: Related assertions grouped together are easier to understand  
✅ **Maintenance**: Less code duplication, easier to update  
✅ **Speed**: Spark session initialization happens only once per test  

### When to Break This Rule:
Only create more than 2 tests if:
- The function has **completely different execution paths** (e.g., different algorithms based on input type)
- The function is **critical** and requires extensive integration testing
- **Explicitly requested** by the developer

## Summary

🎯 **Key Rule**: **2 tests maximum per function**  
📝 **Strategy**: **Multiple assertions per test**  
✅ **Result**: **Comprehensive coverage with minimal test count**