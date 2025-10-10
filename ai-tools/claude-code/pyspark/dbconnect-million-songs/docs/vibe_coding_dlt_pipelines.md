# Vibe Coding Prompts for DLT Medallion Pipeline

This document contains incremental prompts for building a Delta Live Tables (DLT) medallion architecture pipeline using the Million Songs dataset. The pipeline progresses through Bronze (raw), Silver (cleaned), and Gold (aggregated) layers.

**Usage:** Follow the prompts in order to build a complete data pipeline that demonstrates DLT best practices with incremental processing, data quality checks, and expectations.

---

## Prerequisites

Before starting, ensure you have:
- Access to a Databricks workspace
- The Million Songs dataset available in AutoLoader in CloudFormat CSV at `/databricks-datasets/songs/data-001`
- Basic understanding of Delta Live Tables and medallion architecture

---

## Pipeline Architecture Overview

```
Bronze Layer (Raw)
    ↓
Silver Layer (Cleaned & Validated)
    ↓
Gold Layer (Aggregated & Analytics-Ready)
```

---

## Phase 1: Bronze Layer - Raw Data Ingestion

### Prompt 1.1: Create Bronze Table

**Prompt:** "Create a DLT bronze table called `songs_raw_bronze` that incrementally ingests data from `/databricks-datasets/songs/data-001`. Include metadata columns for ingestion timestamp and source system. Use streaming read for incremental processing."

**Expected Implementation:**
- Function decorated with `@dlt.table`, with arguments name=songs_raw_bronze, and commment=Raw data from a subset of the Million Song Dataset; a collection of features and metadata for contemprary music tracks. 
- Streaming source: `spark.readStream.format("cloudFiles")
- the resulting table should be saved in the catalog path=jules_catalog.millionsongs
- Add columns:
  - `ingestion_timestamp`: current timestamp when record was ingested
  - `source_system`: literal value "samples.songs.millionsongs"
- Return: Streaming DataFrame with all original columns plus metadata

**Purpose:** Create the raw data layer that serves as the source of truth, preserving all data as-is from the source system.

**Key Concepts:**
- Bronze tables store raw, unmodified data
- Streaming enables incremental processing
- Metadata tracking for lineage and debugging

---

## Phase 2: Silver Layer - Data Cleaning & Quality

### Prompt 2.1: Create Silver Table with Data Quality

**Prompt:** "Create a DLT silver table called `silver_songs_cleaned` that reads from `bronze_songs` and applies data quality rules. Add expectations to validate: 1) duration is positive, 2) year is between 1900-2030, 3) artist_name is not null. Use quarantine pattern for invalid records. Add a `quality_check_timestamp` column."

**Expected Implementation:**
- Function decorated with `@dlt.table`
- Read from: `dlt.read_stream("bronze_songs")`
- Expectations with violation actions:
  - `@dlt.expect_or_drop("valid_duration", "duration > 0")`
  - `@dlt.expect_or_drop("valid_year", "year >= 1900 AND year <= 2030")`
  - `@dlt.expect_or_drop("valid_artist", "artist_name IS NOT NULL")`
- Add `quality_check_timestamp`: current timestamp
- Filter out null or empty titles
- Return: Cleaned streaming DataFrame

**Purpose:** Ensure data quality through validation rules and filter out invalid records.

**Key Concepts:**
- Silver tables contain cleaned, validated data
- DLT expectations enforce data quality
- `expect_or_drop` removes invalid records
- Quarantine pattern isolates bad data

---

### Prompt 2.2: Create Silver Quarantine Table

**Prompt:** "Create a DLT table called `silver_songs_quarantine` that captures all records that failed silver layer validations. Include the original record plus columns for: failure reason, validation timestamp, and all failed validation rules."

**Expected Implementation:**
- Function decorated with `@dlt.table`
- Read from: `bronze_songs`
- Anti-join with `silver_songs_cleaned` to find failed records
- Add columns:
  - `quarantine_timestamp`: when record was quarantined
  - `failed_validations`: array of failed rule names
  - `failure_reason`: concatenated string of failure reasons
- Return: DataFrame with failed records and metadata

**Purpose:** Track and analyze records that don't meet quality standards for investigation and improvement.

**Key Concepts:**
- Quarantine tables preserve rejected data
- Enable root cause analysis of data quality issues
- Support data quality monitoring and metrics

---

### Prompt 2.3: Enrich Silver Table with Derived Columns

**Prompt:** "Create a DLT silver table called `silver_songs_enriched` that reads from `silver_songs_cleaned` and adds derived columns: 1) `duration_minutes` (duration converted to minutes, rounded to 2 decimals), 2) `decade` (derived from year), 3) `tempo_category` (Slow: <100, Medium: 100-140, Fast: >140), 4) `is_modern` (boolean: year >= 2000)."

**Expected Implementation:**
- Function decorated with `@dlt.table`
- Read from: `dlt.read_stream("silver_songs_cleaned")`
- Derived columns:
  - `duration_minutes`: `round(duration / 60, 2)`
  - `decade`: `floor(year / 10) * 10`
  - `tempo_category`: CASE expression based on tempo
  - `is_modern`: `year >= 2000`
- Return: Enriched streaming DataFrame

**Purpose:** Add business-friendly derived attributes that support analytics without complex calculations in queries.

**Key Concepts:**
- Silver enrichment adds value through transformations
- Derived columns improve query performance
- Business logic encoded once at ingestion

---

## Phase 3: Gold Layer - Analytics-Ready Aggregations

### Prompt 3.1: Create Artist Summary Gold Table

**Prompt:** "Create a DLT gold table called `gold_artist_summary` that aggregates songs by artist. Include metrics: total songs, average duration (minutes), earliest year, latest year, decades active, most common tempo category. Use complete mode for full refresh."

**Expected Implementation:**
- Function decorated with `@dlt.table`
- Read from: `dlt.read("silver_songs_enriched")` (batch read for aggregation)
- Group by: `artist_id`, `artist_name`
- Aggregations:
  - `total_songs`: count
  - `avg_duration_minutes`: average of duration_minutes, rounded to 2 decimals
  - `earliest_year`: min year
  - `latest_year`: max year
  - `decades_active`: count distinct decades
  - `most_common_tempo_category`: mode of tempo_category
- Order by: total_songs descending
- Return: Aggregated DataFrame

**Purpose:** Provide artist-level analytics for music catalog analysis and artist profiling.

**Key Concepts:**
- Gold tables serve specific analytics use cases
- Batch processing for complex aggregations
- Pre-aggregated for query performance

---

### Prompt 3.2: Create Decade Trends Gold Table

**Prompt:** "Create a DLT gold table called `gold_decade_trends` that analyzes musical trends by decade. Include metrics: song count, average tempo, average duration, top 3 artists by song count, percentage of modern songs (year >= 2000)."

**Expected Implementation:**
- Function decorated with `@dlt.table`
- Read from: `dlt.read("silver_songs_enriched")`
- Group by: `decade`
- Aggregations:
  - `song_count`: count
  - `avg_tempo`: average tempo, rounded to 2 decimals
  - `avg_duration_minutes`: average duration_minutes, rounded to 2 decimals
  - `top_artists`: collect top 3 artists by song count (use window functions or array_agg)
  - `pct_modern_songs`: percentage where is_modern = true
- Order by: decade ascending
- Return: Aggregated DataFrame

**Purpose:** Identify musical trends over time for historical analysis and pattern recognition.

**Key Concepts:**
- Time-based aggregations reveal trends
- Complex aggregations (top N) using window functions
- Percentage calculations for comparative analysis

---

### Prompt 3.3: Create Tempo Analysis Gold Table

**Prompt:** "Create a DLT gold table called `gold_tempo_analysis` that analyzes songs by tempo category. Include metrics: song count, average year, average duration, most active decade, top 5 artists in each category."

**Expected Implementation:**
- Function decorated with `@dlt.table`
- Read from: `dlt.read("silver_songs_enriched")`
- Group by: `tempo_category`
- Aggregations:
  - `song_count`: count
  - `avg_year`: average year, rounded to integer
  - `avg_duration_minutes`: average duration_minutes, rounded to 2 decimals
  - `most_active_decade`: mode of decade
  - `top_artists`: top 5 artists by song count in category
  - `pct_of_total`: percentage of total songs
- Order by: song_count descending
- Return: Aggregated DataFrame

**Purpose:** Understand tempo distribution and preferences across the music catalog.

**Key Concepts:**
- Category-based analysis for segmentation
- Percentage of total for relative importance
- Nested aggregations for top N within groups

---

### Prompt 3.4: Create Year-over-Year Growth Gold Table

**Prompt:** "Create a DLT gold table called `gold_yoy_growth` that shows year-over-year growth in song releases. Calculate metrics: songs per year, YoY growth count, YoY growth percentage, cumulative total, 3-year moving average."

**Expected Implementation:**
- Function decorated with `@dlt.table`
- Read from: `dlt.read("silver_songs_enriched")`
- Group by: `year`
- Calculate:
  - `songs_released`: count
  - `yoy_growth`: songs_released - lag(songs_released, 1) over (order by year)
  - `yoy_growth_pct`: (yoy_growth / lag(songs_released, 1)) * 100, rounded to 2 decimals
  - `cumulative_total`: sum(songs_released) over (order by year rows unbounded preceding)
  - `moving_avg_3yr`: avg(songs_released) over (order by year rows between 2 preceding and current row)
- Filter: year between 1950 and 2020 (focus on modern era)
- Order by: year ascending
- Return: Time series DataFrame

**Purpose:** Track music industry growth patterns and identify expansion or contraction periods.

**Key Concepts:**
- Window functions for time series analysis
- Year-over-year comparisons reveal trends
- Moving averages smooth volatility
- Cumulative metrics show total growth

---

## Phase 4: Data Quality Monitoring

### Prompt 4.1: Create Data Quality Metrics Gold Table

**Prompt:** "Create a DLT gold table called `gold_data_quality_metrics` that tracks data quality metrics across the pipeline. Include: total records by layer (bronze/silver/gold), records dropped at silver, quarantine rate, average processing lag, data freshness timestamp."

**Expected Implementation:**
- Function decorated with `@dlt.table`
- Read from multiple tables:
  - `bronze_songs`: count total ingested
  - `silver_songs_cleaned`: count total cleaned
  - `silver_songs_quarantine`: count total quarantined
  - `gold_artist_summary`: count total aggregated
- Calculate:
  - `bronze_record_count`: count from bronze
  - `silver_record_count`: count from silver cleaned
  - `quarantine_record_count`: count from quarantine
  - `drop_rate_pct`: (quarantine / bronze) * 100
  - `silver_pass_rate_pct`: (silver / bronze) * 100
  - `pipeline_timestamp`: current timestamp
- Return: Single-row summary DataFrame

**Purpose:** Monitor pipeline health and data quality trends for operational excellence.

**Key Concepts:**
- Quality metrics enable observability
- Cross-layer metrics reveal data loss
- Timestamps track freshness and latency

---

## Phase 5: Advanced Gold Tables

### Prompt 5.1: Create Artist Similarity Gold Table

**Prompt:** "Create a DLT gold table called `gold_artist_similarity` that finds similar artists based on shared musical characteristics (decade, tempo category, average duration). For each artist, find top 5 most similar artists with similarity score."

**Expected Implementation:**
- Function decorated with `@dlt.table`
- Read from: `dlt.read("gold_artist_summary")`
- Self-join on artists
- Calculate similarity score based on:
  - Decade overlap (count of shared decades)
  - Tempo category match (bonus points for same most_common_tempo_category)
  - Duration similarity (lower absolute difference = higher score)
- For each artist, rank similar artists and take top 5
- Return: DataFrame with artist pairs and similarity scores

**Purpose:** Enable recommendation systems and artist discovery features.

**Key Concepts:**
- Self-joins for entity comparison
- Similarity scoring using multiple dimensions
- Window functions for top N selection

---

### Prompt 5.2: Create Comprehensive Song Catalog Gold Table

**Prompt:** "Create a DLT gold table called `gold_song_catalog` that creates a comprehensive, denormalized view combining song details with artist summaries and trend data. Include all song attributes plus artist rank, decade trend info, and quality flags."

**Expected Implementation:**
- Function decorated with `@dlt.table`
- Join multiple tables:
  - `silver_songs_enriched` (base)
  - `gold_artist_summary` (artist metrics)
  - `gold_decade_trends` (decade context)
- Add computed columns:
  - `artist_popularity_rank`: rank artist by total songs
  - `is_decade_top_tempo`: boolean if song's tempo matches decade's most common
  - `relative_duration`: song duration vs decade average
- Return: Denormalized, wide DataFrame optimized for queries

**Purpose:** Provide a single, performant table for ad-hoc analytics and BI tools.

**Key Concepts:**
- Denormalization trades storage for query performance
- Star schema flattening for analytics
- Pre-computed flags reduce query complexity

---

## How to Implement This Pipeline

### Step 1: Set Up DLT Pipeline
```python
# Create a new Python file: pipelines/million_songs_pipeline.py
import dlt
from pyspark.sql import functions as F
from pyspark.sql import DataFrame
```

### Step 2: Implement Tables in Order
Follow the prompts sequentially:
1. Start with Bronze layer (Prompt 1.1)
2. Build Silver layer (Prompts 2.1-2.3)
3. Create Gold aggregations (Prompts 3.1-3.4)
4. Add monitoring (Prompt 4.1)
5. Enhance with advanced tables (Prompts 5.1-5.2)

### Step 3: Create DLT Pipeline in Databricks
```json
{
  "name": "Million Songs Medallion Pipeline",
  "storage": "/mnt/delta/million_songs",
  "target": "million_songs_db",
  "libraries": [
    {
      "notebook": {
        "path": "/Workspace/pipelines/million_songs_pipeline"
      }
    }
  ],
  "clusters": [
    {
      "label": "default",
      "autoscale": {
        "min_workers": 1,
        "max_workers": 5
      }
    }
  ]
}
```

### Step 4: Run and Monitor
1. Start the DLT pipeline in Databricks
2. Monitor data quality metrics
3. Validate expectations are being enforced
4. Review quarantine table for rejected records

---

## Best Practices for DLT Pipelines

### Data Quality
- **Use expectations liberally**: Validate critical fields at ingestion
- **Implement quarantine pattern**: Never lose data, always investigate failures
- **Monitor metrics**: Track drop rates, freshness, and processing lag

### Performance
- **Leverage streaming**: Use streaming reads for incremental processing where possible
- **Partition gold tables**: Partition by commonly filtered columns (year, decade)
- **Z-order optimization**: Z-order gold tables by frequently joined columns

### Maintainability
- **Comment expectations**: Explain why each expectation exists
- **Version control**: Store DLT notebooks in git
- **Use meaningful names**: Table names should describe content and layer clearly

### Testing
- **Unit test transformations**: Test complex logic before deploying to DLT
- **Validate with sample data**: Run pipeline on small datasets first
- **Monitor quarantine**: Set alerts for high quarantine rates

---

## Pipeline Evolution

As your pipeline matures, consider:

1. **Change Data Capture (CDC)**: Implement SCD Type 2 for tracking historical changes
2. **Data Lineage**: Document dependencies between tables
3. **Cost Optimization**: Tune cluster sizing and autoscaling
4. **Data Retention**: Implement archival policies for old partitions
5. **Access Control**: Apply table-level and column-level security
6. **Data Sharing**: Use Delta Sharing for secure data distribution

---

## Troubleshooting Common Issues

### Pipeline Failures
- Check expectations: Are they too strict?
- Review quarantine table: What patterns exist in rejected records?
- Validate source data: Has schema changed?

### Performance Issues
- Check cluster size: May need more workers
- Review query plans: Look for expensive operations
- Optimize partitioning: Partition by query patterns

### Data Quality Issues
- Add more expectations: Identify gaps in validation
- Strengthen upstream: Fix issues at source
- Implement alerting: Notify on quality degradation

---

## Additional Resources

- [Delta Live Tables Documentation](https://docs.databricks.com/delta-live-tables/index.html)
- [Medallion Architecture Guide](https://www.databricks.com/glossary/medallion-architecture)
- [DLT Expectations Reference](https://docs.databricks.com/delta-live-tables/expectations.html)
- [Streaming in DLT](https://docs.databricks.com/delta-live-tables/streaming.html)
