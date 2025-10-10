# Databricks Connect NYC Taxi Example

A minimal PySpark application demonstrating best practices for Databricks development using Databricks Connect and serverless or classic compute. Features queries on the NYC taxi sample dataset.

## Project Structure

```
dbconnect-nyc-example/
├── src/
│   ├── dbconnect_nyc_example/  # Main package
│   │   ├── __init__.py
│   │   ├── config.py           # Spark session management
│   │   └── data.py             # Data access functions
│   └── main.py                 # Entry point script
├── tests/
│   ├── __init__.py
│   └── test_data.py            # Test suite
├── docs/                       # Documentation
├── scripts/                    # Development scripts
├── data/                       # Sample data (if needed)
├── pyproject.toml             # Project configuration
├── .gitignore                 # Git exclusions
└── README.md
```

## Features

- **Databricks Connect**: Local development with remote Databricks compute
- **Serverless Compute**: No cluster management required
- **DEFAULT Profile**: Seamless authentication for AI tools
- **NYC Taxi Dataset**: Query sample data for demonstrations
- **Test Suite**: pytest-based testing examples

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
- Access to a Databricks workspace

## Quick Start

### 1. Authenticate with Databricks

```bash
databricks auth login --profile DEFAULT --host https://your-workspace.databricks.com
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Run the Application

```bash
uv run python src/main.py
```

### 4. Run Tests

```bash
uv run pytest tests/
```

## Usage

### Basic Usage

```python
from dbconnect_nyc_example.config import get_spark
from dbconnect_nyc_example.data import get_taxis

# Get Spark session
spark = get_spark()

# Query taxi data
df = get_taxis(spark)
df.show(10)
```

## Development

### Project Structure Rules

This project follows strict structure rules defined in `../.claude/CLAUDE.md`:

- **Source code** -> `/src/dbconnect_nyc_example/` (reusable modules) and `/src/` (entry points)
- **Tests** -> `/tests/` (mirrors src structure)
- **Documentation** -> `/docs/`
- **Scripts** -> `/scripts/` (setup/dev only)
- **Data** -> `/data/` (internal data only)

### Adding New Features

1. Add modules to `src/dbconnect_nyc_example/`
2. Create corresponding tests in `tests/`
3. Update `src/dbconnect_nyc_example/__init__.py` exports
4. Run tests: `uv run pytest tests/`
5. Update documentation

### Vibe Coding - Extending with AI

This project includes ready-to-use prompts for generating new NYC taxi data analysis functions. See [docs/vibe_coding_nyc_taxi_prompts.md](docs/vibe_coding_nyc_taxi_prompts.md) for:

- **12 pre-written prompts** for common taxi data analyses (fare analysis, peak hours, popular routes, etc.)
- **Step-by-step instructions** for generating functions, tests, and integrating them into the project
- **Best practices** for prompt engineering with AI coding assistants

Example workflow:
```bash
# 1. Choose a prompt from docs/vibe_coding_nyc_taxi_prompts.md
# 2. Use it with your AI assistant to generate the function in src/dbconnect_nyc_example/data.py
# 3. Generate corresponding tests in tests/test_data.py
# 4. Run: uv run python src/main.py
# 5. Test: uv run pytest tests/test_data.py -v
```

### Testing

Following the testing rules, each function has **exactly 2 tests**:
1. **Happy path test** - Multiple assertions covering normal operation
2. **Edge case test** - Multiple assertions covering error conditions

Run tests:
```bash
# Run all tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_data.py -v
```

### Code Quality

This project uses:
- **pytest** for testing (never unittest)
- **uv** for dependency management (never pip/conda)
- **Type hints** for all functions
- **Google-style docstrings**
- **PEP 8** code style

## Configuration

The application uses the DEFAULT Databricks profile by default. This can be customized in `src/dbconnect_nyc_example/config.py`.

### Serverless Compute

By default, the application uses `getOrCreate()` which will connect using your DEFAULT profile settings. To explicitly use serverless compute, modify the config:

```python
return DatabricksSession.builder.profile("DEFAULT").serverless(True).getOrCreate()
```

### Specify Cluster ID

To use a specific cluster instead of serverless:

```python
return DatabricksSession.builder.profile("DEFAULT").clusterId("your-cluster-id").getOrCreate()
```

## Resources

- [Databricks Connect Docs](https://docs.databricks.com/dev-tools/databricks-connect.html)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)

## License

MIT License
