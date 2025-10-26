# Video Script: Local Development with Databricks Connect and Claude Code
## 15-Minute Technical Demo

**Target Audience:** Data engineers and developers familiar with Python and Databricks
**Goal:** Demonstrate how to use Claude Code in Cursor for local PySpark development with remote Databricks execution

---

## [0:00 - 0:45] Introduction & Setup Overview (45 seconds)

**[Screen: Title slide with "Local Development, Remote Execution" theme]**

**Narrator:**
"Hi everyone! Today I'm going to show you how to develop PySpark applications locally using Claude Code in Cursor, while executing your code on remote Databricks compute. This workflow gives you the best of both worlds: the speed and familiarity of local development with the power and scalability of Databricks.

We'll explore two complete projects: a NYC Taxi analysis for basic queries, and a Million Songs pipeline demonstrating Delta Live Tables deployment. By the end, you'll understand how to set up your environment, use AI-assisted coding, run tests locally, and deploy production pipelines—all from your IDE."

**[Screen: Show both project folder structures side-by-side]**

---

## [0:45 - 2:15] Prerequisites & Authentication (90 seconds)

**[Screen: Terminal showing installation commands]**

**Narrator:**
"Let's start with the prerequisites. You'll need three things: Python 3.11 or higher, the uv package manager, and the Databricks CLI.

First, authenticate with your Databricks workspace using the CLI. This is critical—we're setting up the DEFAULT profile, which allows Claude Code to seamlessly connect without managing credentials."

**[Terminal commands shown:]**
```bash
# Install Databricks CLI (if not already installed)
brew install databricks

# Authenticate with DEFAULT profile
databricks auth login --profile DEFAULT --host https://your-workspace.databricks.com
```

**Narrator:**
"When you run this command, it opens your browser for OAuth authentication. Once you complete the authentication, the CLI stores your credentials securely. The DEFAULT profile is special—it's the profile that Databricks Connect uses automatically, making your AI assistant's generated code work without modification.

Now let's look at our project structure. Both projects follow the same modern Python layout: source code in the src directory, tests mirroring that structure, pipelines for DLT code, and configuration managed through pyproject.toml."

**[Screen: Show directory tree of both projects]**

---

## [2:15 - 4:30] NYC Taxi Project: Simple Query Development (2:15 minutes)

**[Screen: Open Cursor with dbconnect-nyc-example project]**

**Narrator:**
"Let's start with the simpler project—NYC Taxi data analysis. I'm opening this in Cursor with Claude Code enabled. The key files here are config.py for Spark session management and data.py for our data access functions.

Watch how we use Claude Code to generate a new analysis function. I'm going to use one of the pre-written prompts from our vibe coding documentation."

**[Screen: Open docs/vibe_coding_nyc_taxi_prompts.md, highlight Prompt #2: Busiest Pickup Locations]**

**Narrator:**
"Here's our prompt library—12 ready-to-use prompts for common taxi analyses. Let's pick 'Busiest Pickup Locations.' I'm copying this prompt..."

**[Copy prompt text]**

**Prompt text shown:**
```
"Create a function `get_busiest_pickup_locations` that finds which zip codes
have the most pickups. Group by pickup_zip, aggregate count of trips as
trip_count, order by trip count descending."
```

**[Screen: Open Claude Code chat in Cursor, paste prompt]**

**Narrator:**
"I paste it into Claude Code and add context: 'Add this function to data.py following the existing pattern.' Watch what happens..."

**[Screen: Claude Code generates the function]**

**Generated code shown:**
```python
def get_busiest_pickup_locations(spark: SparkSession) -> DataFrame:
    """Find the busiest pickup locations by zip code.

    Returns:
        DataFrame with columns:
        - pickup_zip: ZIP code
        - trip_count: Number of trips from this location
    """
    df = get_taxis(spark)
    return (
        df.groupBy("pickup_zip")
        .agg(count("*").alias("trip_count"))
        .orderBy(col("trip_count").desc())
    )
```

**Narrator:**
"Claude generated a complete function with type hints, a Google-style docstring, and proper imports. It followed the project's existing patterns automatically. Now let's update main.py to call this function."

**[Screen: Ask Claude to update main.py]**

**Narrator:**
"I tell Claude: 'Update main.py to display the top 10 busiest pickup locations.' It updates the file instantly, adding the import and the display logic."

**[Screen: Show updated main.py with new section]**

**Narrator:**
"Notice how Claude Code understands the project structure—it knows where functions live, how they're imported, and the coding style to match. Now let's run it."

**[Terminal shown:]**
```bash
cd dbconnect-nyc-example
uv run python src/main.py
```

**[Screen: Output showing connecting to Databricks, then data results]**

**Narrator:**
"The code runs locally on my machine but executes on Databricks serverless compute. You can see it connected, loaded over 22 million taxi records, and produced our busiest pickup locations in seconds. The data never leaves Databricks—only the results come back to your local machine."

---

## [4:30 - 7:00] Testing with pytest and uv (2:30 minutes)

**[Screen: Open tests/test_data.py]**

**Narrator:**
"Now let's talk about testing. Professional data projects need tests, and Claude Code makes this easy. Our testing philosophy is simple: exactly two tests per function—one happy path with multiple assertions, one edge case test.

Let me ask Claude to generate tests for our new function."

**[Screen: Claude Code chat]**

**Prompt shown:**
```
"Generate exactly 2 pytest tests for get_busiest_pickup_locations:
1) happy path validating DataFrame structure and data,
2) edge case test. Add to tests/test_data.py."
```

**[Screen: Claude generates tests]**

**Generated tests shown:**
```python
def test_get_busiest_pickup_locations_returns_valid_dataframe():
    """Test that get_busiest_pickup_locations returns valid structure."""
    spark = get_spark()
    df = get_busiest_pickup_locations(spark)

    # Verify DataFrame is not None
    assert df is not None, "DataFrame should not be None"

    # Verify expected columns
    assert "pickup_zip" in df.columns
    assert "trip_count" in df.columns

    # Verify data exists
    assert df.count() > 0, "Should have pickup locations"

    # Verify ordering (descending by trip_count)
    counts = df.select("trip_count").collect()
    assert counts[0][0] >= counts[-1][0], "Should be ordered descending"


def test_get_busiest_pickup_locations_data_quality():
    """Test data quality of busiest pickup locations."""
    spark = get_spark()
    df = get_busiest_pickup_locations(spark)

    # All trip counts should be positive
    negative_counts = df.filter(col("trip_count") <= 0).count()
    assert negative_counts == 0, "All trip counts should be positive"

    # Pickup zips should not be null
    null_zips = df.filter(col("pickup_zip").isNull()).count()
    assert null_zips == 0, "Pickup zips should not be null"
```

**Narrator:**
"Perfect! Claude generated comprehensive tests that validate structure, data quality, and ordering. Now here's the magic—we run tests using uv, which automatically manages a virtual environment with all dependencies."

**[Terminal shown:]**
```bash
uv run pytest tests/test_data.py -v
```

**[Screen: pytest output showing tests passing]**

**Output shown:**
```
tests/test_data.py::test_get_busiest_pickup_locations_returns_valid_dataframe PASSED
tests/test_data.py::test_get_busiest_pickup_locations_data_quality PASSED

============================== 2 passed in 12.34s ==============================
```

**Narrator:**
"Both tests passed! Notice uv automatically created a virtual environment, installed databricks-connect and all dependencies, and ran the tests against our remote Databricks workspace. This is crucial: our tests validate real data quality, not mocked data.

The test execution happens locally, but Spark operations run on Databricks. This gives us real confidence that our code works with production data and infrastructure."

**[Screen: Show .venv directory created by uv]**

**Narrator:**
"You can see uv created a .venv directory with an isolated Python environment. This ensures consistent dependencies across your team without manual pip installs or conda environments. It's fast, reliable, and works seamlessly with Claude Code."

---

## [7:00 - 10:30] Million Songs Project: DLT Pipeline Development (3:30 minutes)

**[Screen: Switch to dbconnect-million-songs project in Cursor]**

**Narrator:**
"Now let's level up with the Million Songs project. This demonstrates a complete data pipeline workflow: Delta Live Tables for ingestion, Databricks Asset Bundles for deployment, and local development for analysis.

The architecture is simple but powerful: a DLT pipeline ingests raw CSV data into a Unity Catalog bronze table, then we query that table locally using Databricks Connect."

**[Screen: Show pipelines/dlt_pipeline.py]**

**Narrator:**
"Here's our DLT pipeline. This file runs on Databricks, not locally, so it uses the dlt decorator. Let me highlight the key parts."

**[Code shown with annotations:]**
```python
@dlt.table(
    name="songs_raw_bronze",
    comment="Raw data from Million Song Dataset",
    table_properties={"quality": "bronze"}
)
def songs_raw_bronze() -> DataFrame:
    return (
        spark.readStream
        .format("cloudFiles")           # Auto Loader for incremental ingestion
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("delimiter", "\t")
        .schema("""...""")              # Explicit schema prevents drift
        .load("/databricks-datasets/songs/data-001")
        .withColumn("ingestion_timestamp", current_timestamp())
        .withColumn("source_system", lit("/databricks-datasets/songs/data-001"))
    )
```

**Narrator:**
"This is a bronze layer ingest using Auto Loader—Databricks' intelligent incremental file loader. We're reading tab-delimited CSV files, applying an explicit schema, and adding metadata columns for lineage tracking. The dlt.table decorator handles all the Delta table creation and streaming orchestration.

Now, I had a problem with this code earlier. Let me show you how Claude Code helped me debug it."

**[Screen: Claude Code chat, scroll to earlier conversation]**

**Earlier conversation shown:**
```
User: "What seems to be two problems with dlt_pipeline.py?"

Claude: "I've identified two problems:
1. Missing spark variable (line 41) - spark is used but never imported
2. Inconsistent header configuration (line 44) - header is 'false' but
   should be 'true' for CSV with headers"
```

**Narrator:**
"Claude Code analyzed the file and immediately identified two issues: the missing spark variable and incorrect CSV header configuration. It then generated fixes with proper imports and correct configuration. This kind of context-aware debugging is incredibly valuable—Claude understands both PySpark patterns and DLT-specific requirements.

Now let's deploy this pipeline using Databricks Asset Bundles."

**[Screen: Show databricks.yml]**

**Configuration shown:**
```yaml
bundle:
  name: million-songs-pipeline

resources:
  pipelines:
    million_songs_bronze:
      name: million-songs-bronze-pipeline
      catalog: jules_catalog
      schema: millionsongs
      libraries:
        - file:
            path: ./pipelines/dlt_pipeline.py
      clusters:
        - label: default
          num_workers: 1
      channel: CURRENT
      photon: true
      continuous: false
      development: true
```

**Narrator:**
"This YAML file is infrastructure as code. It defines our pipeline name, Unity Catalog location, the Python file to deploy, and cluster configuration. The beauty is that everything is version controlled and reproducible.

Let's deploy it."

**[Terminal shown:]**
```bash
# Validate configuration
databricks bundle validate
```

**Output:**
```
Name: million-songs-pipeline
Target: default
Workspace:
  User: jules@databricks.com
  Path: /Workspace/Users/jules@databricks.com/.bundle/million-songs-pipeline/default

Validation OK!
```

**Narrator:**
"Validation passed. Now we deploy."

**[Terminal:]**
```bash
databricks bundle deploy
```

**Output:**
```
Uploading bundle files to /Workspace/Users/jules@databricks.com/.bundle/...
Deploying resources...
Updating deployment state...
Deployment complete!
```

**Narrator:**
"The pipeline is deployed to our workspace. Now we run it."

**[Terminal:]**
```bash
databricks bundle run million_songs_bronze
```

**Output:**
```
Update URL: https://e2-dogfood.staging.cloud.databricks.com/#joblist/pipelines/...
2025-10-15T15:21:18.729Z update_progress INFO "Update f0f84d is WAITING_FOR_RESOURCES."
```

**Narrator:**
"The pipeline is running! It's waiting for compute resources, then it will start ingesting data. The CLI gave us a URL to monitor progress in real-time.

While that's running, let me show you the local development side. Once the pipeline creates the bronze table, we can query it from our local machine."

**[Screen: Open src/dbconnect_million_songs/data.py]**

**Code shown:**
```python
def get_songs(spark: SparkSession) -> DataFrame:
    """Retrieve Million Songs data from bronze table in catalog."""
    try:
        return spark.read.table("jules_catalog.millionsongs.songs_raw_bronze")
    except Exception as e:
        raise Exception(
            f"Failed to read Million Songs data from bronze table. "
            f"Ensure you have access to jules_catalog.millionsongs.songs_raw_bronze. "
            f"Error: {e}"
        ) from e
```

**Narrator:**
"This function reads from the Unity Catalog table created by our DLT pipeline. Notice there's no dlt import here—this is pure Databricks Connect code that runs locally. The separation is clean: pipelines directory for DLT code that runs on Databricks, src directory for local development code."

---

## [10:30 - 12:30] Running Tests and Validating Data Quality (2:00 minutes)

**[Screen: Open tests/test_data.py for million songs project]**

**Narrator:**
"Let's look at the tests for this project. Again, we follow the two-test pattern."

**[Code shown:]**
```python
def test_get_songs_returns_valid_dataframe():
    """Test that get_songs returns a DataFrame with correct structure."""
    spark = get_spark()
    df = get_songs(spark)

    assert df is not None, "DataFrame should not be None"
    assert df.count() > 0, "DataFrame should contain records"

    expected_columns = ["artist_id", "artist_name", "duration",
                       "release", "tempo", "title", "year"]
    for col in expected_columns:
        assert col in df.columns, f"Expected column '{col}' not found"


def test_get_songs_data_quality():
    """Test data quality checks for edge cases."""
    spark = get_spark()
    df = get_songs(spark)

    total_count = df.count()

    # Check that most durations are positive
    negative_durations = df.filter(df.duration < 0).count()
    positive_duration_ratio = (total_count - negative_durations) / total_count
    assert positive_duration_ratio >= 0.95

    # Check that valid years are reasonable
    valid_year_count = df.filter(df.year > 0).count()
    unreasonable_years = df.filter(
        (df.year > 0) & ((df.year < 1900) | (df.year > 2026))
    ).count()

    if valid_year_count > 0:
        reasonable_year_ratio = (valid_year_count - unreasonable_years) / valid_year_count
        assert reasonable_year_ratio >= 0.95
```

**Narrator:**
"These tests validate both structure and data quality. The second test is particularly interesting—it checks that 95% of songs have positive durations and reasonable years. This catches real-world data quality issues.

Let's run these tests using uv."

**[Terminal shown:]**
```bash
cd dbconnect-million-songs
uv run pytest tests/test_data.py -v
```

**[Output shown:]**
```
============================= test session starts ==============================
platform darwin -- Python 3.11.13, pytest-8.4.2, pluggy-1.6.0
collecting ... collected 2 items

tests/test_data.py::test_get_songs_returns_valid_dataframe PASSED        [ 50%]
tests/test_data.py::test_get_songs_data_quality PASSED                   [100%]

============================== 2 passed in 28.82s ==============================
```

**Narrator:**
"Perfect! Both tests passed. Notice the execution time—28 seconds. That's because uv set up the environment, installed dependencies, connected to Databricks, and ran quality checks on over 31,000 records. All of this happened seamlessly.

The beauty of this workflow is that we're testing against real production data in Unity Catalog. There are no mocks, no fake data. We're validating that our code works with the actual data our pipeline ingested."

**[Screen: Show terminal with successful test output]**

**Narrator:**
"These tests run in CI/CD pipelines too. You can integrate this into GitHub Actions or GitLab CI to validate every pull request against your development Databricks workspace. It's true test-driven development for data engineering."

---

## [12:30 - 14:15] Best Practices & Workflow Patterns (1:45 minutes)

**[Screen: Split screen showing both projects]**

**Narrator:**
"Let's summarize the key patterns that make this workflow so powerful.

**First: Project structure.** Both projects follow the same layout—src for local code, pipelines for DLT code, tests mirroring src, and docs for reference material. This consistency makes projects easy to understand and maintain."

**[Highlight project structure diagrams]**

**Narrator:**
"**Second: Separation of concerns.** Code that uses the dlt decorator lives in the pipelines directory and runs on Databricks. Code for local analysis lives in src and uses Databricks Connect. This separation is clean and prevents import errors.

**Third: Testing strategy.** Two tests per function—no more, no less. One validates the happy path with multiple assertions, one tests edge cases. This keeps test suites maintainable while ensuring comprehensive coverage."

**[Screen: Show testing rules in action]**

**Narrator:**
"**Fourth: AI-assisted development with Claude Code.** The vibe coding approach works because we provide structured prompts. Look at the NYC taxi prompts—they specify the function name, expected output structure, and even the business insight. This gives Claude Code enough context to generate production-quality code.

When Claude makes mistakes, ask it to debug. We saw this with the DLT pipeline—Claude identified the missing import and configuration error immediately."

**[Screen: Show vibe_coding_nyc_taxi_prompts.md]**

**Narrator:**
"**Fifth: Infrastructure as code with Asset Bundles.** The databricks.yml file version controls your pipeline configuration. You can deploy to dev, staging, and prod environments just by changing the target. Everything is reproducible and auditable.

**Sixth: Use uv for dependency management.** Forget pip, forget conda. uv is fast, creates isolated environments automatically, and works seamlessly with both Claude Code and Databricks Connect. One command—uv run—and everything just works."

**[Screen: Show pyproject.toml with dependencies]**

**Narrator:**
"**Finally: The DEFAULT profile pattern.** By authenticating with the DEFAULT profile, you eliminate credential management in code. Claude Code's generated code works immediately because Databricks Connect finds the credentials automatically. This is especially important for AI coding assistants that shouldn't have access to your credentials."

---

## [14:15 - 15:00] Closing & Next Steps (45 seconds)

**[Screen: Summary slide with key points]**

**Narrator:**
"To wrap up, we've covered the complete workflow for local PySpark development with remote Databricks execution:

1. Authenticate once with the DEFAULT profile
2. Use Claude Code to generate functions from structured prompts
3. Run code locally with uv that executes on Databricks serverless compute
4. Test against real data with pytest and uv
5. Deploy pipelines as code using Databricks Asset Bundles
6. Maintain clean separation between local and pipeline code

This workflow gives you the speed of local development with the power of Databricks. You get instant feedback, real data quality testing, and seamless deployment—all from your IDE.

Both example projects are available on GitHub with complete documentation, ready-to-use prompts, and working code. Try them out, customize the prompts for your datasets, and experience the future of data engineering development.

Thanks for watching, and happy coding!"

**[Screen: Fade to GitHub repository URLs and resources]**

**Resources shown:**
- GitHub: github.com/databricks/dbconnect-examples
- Docs: docs.databricks.com/dev-tools/databricks-connect.html
- Claude Code: claude.ai/claude-code
- uv: docs.astral.sh/uv/

**[End]**

---

## Technical Notes for Video Production

### Screen Recordings Needed:
1. Terminal: Authentication flow (databricks auth login)
2. Cursor: Both project folder structures side-by-side
3. Cursor: Claude Code generating busiest_pickup_locations function
4. Terminal: Running main.py showing output
5. Cursor: Claude Code generating pytest tests
6. Terminal: Running pytest with uv showing passes
7. Cursor: DLT pipeline code with annotations
8. Cursor: Claude Code debugging session (earlier conversation)
9. Terminal: Bundle validate, deploy, and run commands
10. Browser: Quick shot of Databricks UI showing running pipeline
11. Cursor: data.py showing Unity Catalog table read
12. Terminal: pytest running for Million Songs with passing tests
13. Screen capture: Both project structures for best practices section

### Timing Breakdown:
- Intro: 45s
- Prerequisites: 90s
- NYC Project Demo: 135s
- Testing Demo: 150s
- DLT Pipeline Demo: 210s
- Testing DLT: 120s
- Best Practices: 105s
- Closing: 45s
**Total: 900 seconds (15 minutes)**

### Graphics/Overlays:
1. Title cards for each section
2. Code highlights and annotations (arrows, boxes)
3. Split-screen for comparing projects
4. Progress bar during longer operations
5. Resource URLs at end

### Audio Cues:
- Upbeat background music (low volume)
- Keyboard typing sounds during code generation (subtle)
- Terminal beep sounds for successful commands
- Transition sounds between major sections
