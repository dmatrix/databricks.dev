# databricks.dev

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Databricks](https://img.shields.io/badge/Databricks-Connect-FF3621?logo=databricks)](https://docs.databricks.com/dev-tools/databricks-connect.html)
[![PySpark](https://img.shields.io/badge/PySpark-3.5+-E25A1C?logo=apachespark)](https://spark.apache.org/docs/latest/api/python/)
[![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

A collection of AI-assisted development tools and examples for working with Databricks.

## Overview

This repository contains practical examples and tools for developing with Databricks using modern AI coding assistants like Cursor and Claude Code. The focus is on demonstrating best practices for local development with Databricks Connect and PySpark.

## Repository Structure

```
databricks.dev/
├── ai-tools/
│   ├── cursor/
│   │   └── pyspark/
│   │       ├── .cursor/                  # Cursor IDE rules
│   │       └── dbconnect-nyc-example/    # NYC Taxi example with Databricks Connect
│   └── claude-code/
│       └── pyspark/
│           ├── dbconnect-nyc-example/    # NYC Taxi example with Claude Code
│           └── dbconnect-million-songs/  # Million Songs SPD pipeline example
├── LICENSE
└── README.md
```

## Projects

### Databricks Connect NYC Taxi Example

This repository includes two implementations of the same NYC Taxi example project, each tailored for different AI coding assistants:

#### 🎯 For Cursor Users
**Location:** [ai-tools/cursor/pyspark/dbconnect-nyc-example/](ai-tools/cursor/pyspark/dbconnect-nyc-example/)

A minimal PySpark application demonstrating Databricks Connect with Cursor IDE. Features:
- Cursor IDE rules (`.cursor/rules/`) for Python development, project structure, and testing
- 12 vibe coding prompts for generating NYC taxi analysis functions
- 3 implemented functions with comprehensive tests
- Complete documentation for AI-assisted development

[📖 Read the Cursor example README](ai-tools/cursor/pyspark/dbconnect-nyc-example/README.md)

#### 🤖 For Claude Code Users
**Location:** [ai-tools/claude-code/pyspark/dbconnect-nyc-example/](ai-tools/claude-code/pyspark/dbconnect-nyc-example/)

The same NYC Taxi example optimized for Claude Code. Features:
- Claude Code configuration (`.claude/`) with project-specific rules
- 12 vibe coding prompts ready for use with Claude Code
- Same data analysis capabilities as the Cursor version
- Streamlined for VS Code + Claude Code workflow

[📖 Read the Claude Code example README](ai-tools/claude-code/pyspark/dbconnect-nyc-example/README.md)

**Quick Start (NYC Taxi):**
```bash
# Choose your AI tool:
cd ai-tools/cursor/pyspark/dbconnect-nyc-example     # For Cursor
# OR
cd ai-tools/claude-code/pyspark/dbconnect-nyc-example # For Claude Code

# 1. Authenticate with Databricks
databricks auth login --profile DEFAULT --host https://your-workspace.databricks.com

# 2. Install dependencies
uv sync

# 3. Run the application
uv run python src/main.py

# 4. Run tests
uv run pytest tests/ -v
```

**Expected Output:**
```
Starting NYC Taxi Data Analysis...
==================================================
✓ Connected to Databricks
✓ Loaded NYC taxi data: 22,699,369 records

Sample NYC Taxi Trips:
--------------------------------------------------
+-------------------+-------------+-----------+-----------+------------+
|tpep_pickup_datetime|trip_distance|fare_amount|pickup_zip |dropoff_zip |
+-------------------+-------------+-----------+-----------+------------+
|2016-02-14 16:52:13|2.25         |9.0        |10282      |10171       |
|2016-02-04 18:44:19|8.04         |26.0       |10110      |10023       |
|2016-02-17 17:13:57|0.72         |5.5        |10103      |10022       |
...

Fare Per Mile Analysis (Top 10 by fare/mile):
--------------------------------------------------
+-------------+-----------+---------------------+-----------+------------+
|trip_distance|fare_amount|average_fare_per_mile|pickup_zip |dropoff_zip |
+-------------+-----------+---------------------+-----------+------------+
|0.01         |52.0       |5200.00              |10282      |10282       |
|0.03         |107.5      |3583.33              |10019      |10019       |
...

Analysis complete!
```

**What the NYC Taxi Examples Demonstrate:**
- Connect to Databricks using Databricks Connect
- Use serverless compute for data processing
- Query sample data (NYC taxi trips from `samples.nyctaxi.trips`)
- Work with DataFrames in PySpark
- Perform aggregations, filtering, and time-series analysis
- AI-assisted development with pre-written prompts

**Next Steps:**
- Explore the [12 vibe coding prompts](ai-tools/claude-code/pyspark/dbconnect-nyc-example/docs/vibe_coding_nyc_taxi_prompts.md) for generating new analysis functions
- Use your AI assistant to implement additional patterns (9 prompts ready to use)
- Run tests with `uv run pytest tests/ -v` to validate your code

---

### Million Songs Spark Declarative Pipelines Example

**Location:** [ai-tools/claude-code/pyspark/dbconnect-million-songs/](ai-tools/claude-code/pyspark/dbconnect-million-songs/)

A comprehensive example demonstrating Spark Declarative Pipelines (SPD) with Databricks Asset Bundles. Features:
- **Spark Declarative Pipelines**: Declarative ETL pipeline for bronze layer data ingestion
- **Databricks Asset Bundles**: Infrastructure-as-code deployment with `databricks.yml`
- **Auto Loader**: Incremental CSV ingestion with schema inference
- **Unity Catalog**: Governed data storage in catalog.schema.table format
- **Local Development**: Query SPD-created tables using Databricks Connect
- **Complete Testing**: pytest suite with data quality validation

**What This Example Demonstrates:**
- Deploy SPD pipelines using `databricks bundle deploy`
- Ingest data from the Million Songs dataset into a bronze table
- Use Auto Loader (cloudFiles) for incremental processing
- Query Unity Catalog tables from your local environment
- Test data quality and schema compliance

[📖 Read the Million Songs README](ai-tools/claude-code/pyspark/dbconnect-million-songs/README.md)

**Quick Start:**
```bash
cd ai-tools/claude-code/pyspark/dbconnect-million-songs

# Deploy the SPD pipeline
databricks bundle validate
databricks bundle deploy
databricks bundle run million_songs_spd

# Query the bronze table locally
uv sync
uv run src/main.py

# Run tests
uv run pytest tests/ -v
```

---

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
- Access to a Databricks workspace

## Authentication

The examples use Databricks CLI authentication profiles. Set up your profile:

```bash
databricks auth login --profile DEFAULT --host https://your-workspace.databricks.com
```

## Resources

### AI-Assisted Development

#### For Cursor Users
- **Cursor with Databricks: AI Enhanced Development**: [Comprehensive guide by Dustin Vannoy](https://dustinvannoy.com/2025/09/29/cursor-with-databricks-ai-enhanced-development/) on leveraging Cursor IDE with Databricks Connect, including setup, Cursor rules, and MCP integration
- **Cursor Rules**: Check out [ai-tools/cursor/pyspark/.cursor/rules/](ai-tools/cursor/pyspark/.cursor/rules/) for Python development and project structure rules
- **Vibe Coding Prompts**: See [ai-tools/cursor/pyspark/dbconnect-nyc-example/docs/vibe_coding_nyc_taxi_prompts.md](ai-tools/cursor/pyspark/dbconnect-nyc-example/docs/vibe_coding_nyc_taxi_prompts.md) for 12 interesting query patterns

#### For Claude Code Users
- **Claude Code Configuration**: Check out [ai-tools/claude-code/pyspark/dbconnect-nyc-example/.claude/](ai-tools/claude-code/pyspark/dbconnect-nyc-example/.claude/) for project-specific rules
- **Vibe Coding Prompts**: See [ai-tools/claude-code/pyspark/dbconnect-nyc-example/docs/vibe_coding_nyc_taxi_prompts.md](ai-tools/claude-code/pyspark/dbconnect-nyc-example/docs/vibe_coding_nyc_taxi_prompts.md) for 12 interesting query patterns
  - 3 implemented and tested (Average Fare Per Mile, Busiest Pickup Locations, Peak Hours Analysis)
  - 9 ready for AI-assisted development
- **SPD Pipeline Example**: See [ai-tools/claude-code/pyspark/dbconnect-million-songs/](ai-tools/claude-code/pyspark/dbconnect-million-songs/) for Spark Declarative Pipelines and Databricks Asset Bundles

### Official Documentation
- **Databricks Connect Docs**: https://docs.databricks.com/dev-tools/databricks-connect.html
- **PySpark Documentation**: https://spark.apache.org/docs/latest/api/python/

## Contributing

This repository is for educational and demonstration purposes. Feel free to fork and adapt the examples for your own use cases.

## License

See [LICENSE](LICENSE) for details.