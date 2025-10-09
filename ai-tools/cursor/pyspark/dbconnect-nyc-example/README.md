# Databricks Connect NYC Taxi Example

A minimal PySpark application demonstrating best practices for Databricks development using Databricks Connect and serverless compute. Features queries on the NYC taxi sample dataset.

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
├── docs/
│   └── vibe_coding_nyc_taxi_prompts.md  # 12 query examples
├── scripts/                    # Development scripts
├── data/                       # Sample data (if needed)
├── pyproject.toml             # Project configuration
├── requirements.txt           # Pinned dependencies
└── README.md
```

## Features

- **Databricks Connect**: Local development with remote Databricks compute
- **Serverless Compute**: No cluster management required
- **DEFAULT Profile**: Seamless authentication for AI tools
- **NYC Taxi Dataset**: Query sample data for demonstrations
- **Test Suite**: pytest-based testing examples
- **Query Library**: 12 interesting query patterns in docs/

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
uv run src/main.py
```

Expected output:
```
NYC Taxi Trips Sample Data:
+--------------------+---------------------+-------------+-----------+----------+-----------+
|tpep_pickup_datetime|tpep_dropoff_datetime|trip_distance|fare_amount|pickup_zip|dropoff_zip|
+--------------------+---------------------+-------------+-----------+----------+-----------+
...
```

### 4. Run Tests

```bash
uv run pytest tests/
```

## Usage

### Import as a Package

```python
from dbconnect_nyc_example import get_spark, get_taxis

# Get Spark session
spark = get_spark()

# Query taxi data
df = get_taxis(spark)
df.show(10)
```

### Explore Query Examples

Check out `docs/vibe_coding_nyc_taxi_prompts.md` for 12 interesting query patterns including:

1. Average Fare Per Mile
2. Busiest Pickup Locations
3. Peak Hours Analysis
4. Popular Routes
5. Trip Distance Distribution
6. Day of Week Patterns
7. Trip Duration Analysis
8. Fare Comparisons
9. Speed Analysis
10. Weekend vs Weekday
11. Time Period Comparison
12. Hourly Revenue Potential

## Development

### Project Structure Rules

This project follows strict structure rules defined in `../.cursor/rules/project-structure-rules.mdc`:

- **Source code** → `/src/dbconnect_nyc_example/` (reusable modules) and `/src/` (entry points)
- **Tests** → `/tests/` (mirrors src structure)
- **Documentation** → `/docs/`
- **Scripts** → `/scripts/` (setup/dev only)
- **Data** → `/data/` (internal data only)

### Adding New Features

1. Add modules to `src/dbconnect_nyc_example/`
2. Create corresponding tests in `tests/`
3. Update `src/dbconnect_nyc_example/__init__.py` exports
4. Run tests: `uv run pytest tests/`
5. Update documentation

### Code Quality

This project uses:
- **pytest** for testing (never unittest)
- **uv** for dependency management (never pip/conda)
- **Type hints** for all functions
- **Google-style docstrings**
- **PEP 8** code style

See `../.cursor/rules/python-dev.mdc` for detailed coding standards.

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
- [Cursor with Databricks Guide](https://dustinvannoy.com/2025/09/29/cursor-with-databricks-ai-enhanced-development/)

## License

See [LICENSE](../../../../LICENSE) for details.

