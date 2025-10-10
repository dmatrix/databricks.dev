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
│           └── dbconnect-nyc-example/    # NYC Taxi example with Claude Code
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

---

**What Both Examples Demonstrate:**
- Connect to Databricks using Databricks Connect
- Use serverless compute for data processing
- Query sample data (NYC taxi trips)
- Work with DataFrames in PySpark
- Perform aggregations and time-series analysis

**Common Features:**
- Uses `uv` for fast dependency management
- Configured for the DEFAULT authentication profile
- 12 query patterns available (3 implemented, 9 ready for development)
- Follows strict project structure rules for AI-assisted development
- Clean, minimal setup for quick starts
- Comprehensive test suite with pytest

**Quick Start (either example):**
```bash
# Choose your AI tool:
cd ai-tools/cursor/pyspark/dbconnect-nyc-example     # For Cursor
# OR
cd ai-tools/claude-code/pyspark/dbconnect-nyc-example # For Claude Code

# Authenticate with Databricks
databricks auth login --profile DEFAULT --host https://your-workspace.databricks.com

# Install dependencies and run
uv sync
uv run python src/main.py

# Run tests
uv run pytest tests/ -v
```

**Example Output:**
```
NYC Taxi Peak Hours Analysis:
+----+----------+--------+------------+
|hour|trip_count|avg_fare|avg_distance|
+----+----------+--------+------------+
|18  |1455      |11.77   |2.45        | ← Peak demand at 6 PM
|7   |801       |11.55   |2.75        | ← Morning rush
|4   |250       |14.73   |4.24        | ← Highest fares (early morning)
...
```

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

### Official Documentation
- **Databricks Connect Docs**: https://docs.databricks.com/dev-tools/databricks-connect.html
- **PySpark Documentation**: https://spark.apache.org/docs/latest/api/python/

## Contributing

This repository is for educational and demonstration purposes. Feel free to fork and adapt the examples for your own use cases.

## License

See [LICENSE](LICENSE) for details.