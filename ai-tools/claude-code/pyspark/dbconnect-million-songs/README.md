# Databricks Connect Million Songs Example

A complete example demonstrating modern Databricks development practices using **Databricks Connect** for local development and **Delta Live Tables (DLT)** for data ingestion pipelines. This project uses the Million Songs dataset to showcase:

- Local PySpark development with remote Databricks compute
- Delta Live Tables pipeline deployment using Databricks Asset Bundles
- Bronze layer data ingestion with Auto Loader
- Comprehensive testing with pytest

## Project Overview

This project demonstrates an end-to-end data pipeline workflow:

1. **Bronze Layer**: DLT pipeline ingests raw CSV data from the Million Songs dataset into a Unity Catalog bronze table
2. **Local Development**: Query and analyze the bronze table using Databricks Connect from your local machine
3. **Testing**: Validate data quality and schema using pytest

## Project Structure

```
dbconnect-million-songs/
   src/
      dbconnect_million_songs/  # Main package
         __init__.py
         config.py             # Spark session management
         data.py               # Data access functions
      main.py                   # Entry point script
   pipelines/
      dlt_pipeline.py           # Delta Live Tables pipeline
   tests/
      __init__.py
      test_data.py              # Test suite
   docs/                         # Documentation
   scripts/                      # Development scripts
   data/                         # Sample data (if needed)
   databricks.yml               # Databricks Asset Bundle config
   pyproject.toml               # Project configuration
   .gitignore                   # Git exclusions
   README.md
```

## Features

- **Databricks Connect**: Local development with remote Databricks compute
- **Delta Live Tables**: Declarative ETL pipeline for bronze layer ingestion
- **Databricks Asset Bundles**: Infrastructure-as-code for pipeline deployment
- **Auto Loader**: Incremental ingestion of CSV files with schema inference
- **Unity Catalog**: Governed data storage in catalog.schema.table format
- **Serverless Compute**: No cluster management required
- **Test Suite**: pytest-based testing examples with data quality validation

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- [Databricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
- Access to a Databricks workspace with Unity Catalog enabled
- Permissions to create catalogs, schemas, and tables

## Quick Start

### 1. Authenticate with Databricks

```bash
databricks auth login --profile DEFAULT --host https://your-workspace.databricks.com
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Deploy the DLT Pipeline

The `databricks.yml` file defines a Databricks Asset Bundle that deploys the DLT pipeline:

```bash
# Validate the bundle configuration
databricks bundle validate

# Deploy the pipeline to your workspace
databricks bundle deploy

# Run the pipeline to create the bronze table
databricks bundle run million_songs_bronze
```

This will create the table `jules_catalog.millionsongs.songs_raw_bronze` (update catalog/schema names as needed).

### 4. Run the Application

Once the pipeline has created the bronze table, query it locally:

```bash
uv run src/main.py
```

Expected output:
```
Starting Million Songs Data Analysis...
==================================================
✓ Connected to Databricks
✓ Loaded Million Songs data from bronze table: 31,389 records

Sample Million Songs:
--------------------------------------------------
[Sample data displayed here]

Analysis complete!
```

### 5. Run Tests

```bash
uv run pytest tests/ -v
```

## Databricks Asset Bundle Configuration

The `databricks.yml` file defines the infrastructure for deploying the DLT pipeline:

```yaml
bundle:
  name: million-songs-pipeline

resources:
  pipelines:
    million_songs_bronze:
      name: million-songs-bronze-pipeline
      catalog: jules_catalog          # Unity Catalog name
      schema: millionsongs            # Schema name within the catalog
      libraries:
        - file:
            path: ./pipelines/dlt_pipeline.py  # DLT pipeline code
      clusters:
        - label: default
          num_workers: 1               # Single worker for this small dataset
      channel: CURRENT                 # Use current release channel
      photon: true                     # Enable Photon for performance
      continuous: false                # Run as triggered (not streaming)
      development: true                # Development mode for easier debugging
```

### Key Configuration Elements

- **bundle.name**: Unique identifier for the bundle
- **resources.pipelines**: Defines DLT pipelines to deploy
- **catalog/schema**: Unity Catalog location for tables (`catalog.schema.table`)
- **libraries**: Path to the DLT pipeline Python file
- **clusters**: Compute configuration (workers, instance types)
- **photon**: Enables Databricks Photon engine for faster processing
- **continuous**: `false` = triggered mode, `true` = streaming mode
- **development**: `true` enables development mode with faster iteration

### Customizing for Your Environment

Before deploying, update these values in `databricks.yml`:

1. **catalog**: Change `jules_catalog` to your Unity Catalog name
2. **schema**: Change `millionsongs` to your desired schema name
3. Update the table name in `src/dbconnect_million_songs/data.py`:
   ```python
   return spark.read.table("your_catalog.your_schema.songs_raw_bronze")
   ```

## Delta Live Tables Pipeline

The DLT pipeline (`pipelines/dlt_pipeline.py`) defines the bronze table:

```python
@dlt.table(
    name="songs_raw_bronze",
    comment="Raw data from Million Song Dataset",
    table_properties={"quality": "bronze"}
)
def songs_raw_bronze() -> DataFrame:
    return (
        spark.readStream
        .format("cloudFiles")  # Auto Loader
        .option("cloudFiles.format", "csv")
        .option("header", "false")
        .option("delimiter", "\t")
        .schema(...)  # Explicit schema definition
        .load("/databricks-datasets/songs/data-001")
        .withColumn("ingestion_timestamp", current_timestamp())
        .withColumn("source_system", lit("/databricks-datasets/songs/data-001"))
    )
```

### Pipeline Features

- **Auto Loader (cloudFiles)**: Incrementally processes new files as they arrive
- **Schema Evolution**: Explicit schema prevents breaking changes
- **Metadata Columns**: Adds `ingestion_timestamp` and `source_system` for lineage tracking
- **Tab-Delimited CSV**: Handles the Million Songs dataset format

## Usage

### Basic Usage

```python
from dbconnect_million_songs.config import get_spark
from dbconnect_million_songs.data import get_songs

# Get Spark session
spark = get_spark()

# Query songs data from bronze table
df = get_songs(spark)
df.show(10)

# Perform analysis
popular_songs = df.filter(df.year > 2000).orderBy(df.tempo.desc())
popular_songs.show()
```

### Querying the Bronze Table

The bronze table contains the following columns:

- `artist_id`: Unique identifier for the artist
- `artist_name`: Name of the artist
- `artist_latitude`, `artist_longitude`, `artist_location`: Geographic data
- `duration`: Song duration in seconds
- `title`: Song title
- `release`: Album/release name
- `year`: Release year (0 = unknown)
- `tempo`: Tempo in BPM
- `time_signature`: Time signature
- `key`, `key_confidence`: Musical key information
- `loudness`: Average loudness in dB
- `song_hotness`: Popularity metric
- `ingestion_timestamp`: When the record was ingested
- `source_system`: Source path of the data

## Development

### Project Structure Rules

This project follows strict structure rules defined in `../.claude/CLAUDE.md`:

- **Source code** → `/src/dbconnect_million_songs/` (reusable modules) and `/src/` (entry points)
- **Pipelines** → `/pipelines/` (DLT pipeline code)
- **Tests** → `/tests/` (mirrors src structure)
- **Documentation** → `/docs/`
- **Scripts** → `/scripts/` (setup/dev only)
- **Data** → `/data/` (internal data only)

### Adding New Features

1. Add modules to `src/dbconnect_million_songs/`
2. Create corresponding tests in `tests/`
3. Update `src/dbconnect_million_songs/__init__.py` exports
4. Run tests: `uv run pytest tests/`
5. Update documentation

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

The application uses the DEFAULT Databricks profile by default. This can be customized in `src/dbconnect_million_songs/config.py`.

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

## Troubleshooting

### Pipeline Fails with "Table Not Found"

Make sure the DLT pipeline has completed successfully:
```bash
databricks pipelines get <pipeline-id>
```

Check the pipeline status at the URL provided when you run `databricks bundle run`.

### Import Errors

The `dlt` module is only available in the Databricks runtime, not locally. The project structure separates:
- `pipelines/dlt_pipeline.py` - Uses `dlt` decorator (runs on Databricks)
- `src/dbconnect_million_songs/data.py` - No `dlt` import (runs locally)

### Authentication Issues

Ensure you're authenticated with the DEFAULT profile:
```bash
databricks auth login --profile DEFAULT
```

## Resources

- [Databricks Connect Docs](https://docs.databricks.com/dev-tools/databricks-connect.html)
- [Delta Live Tables](https://docs.databricks.com/delta-live-tables/index.html)
- [Databricks Asset Bundles](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Auto Loader](https://docs.databricks.com/ingestion/auto-loader/index.html)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)

## License

MIT License
