"""Delta Live Tables pipeline for Million Songs dataset.

This pipeline creates a bronze table by ingesting data from the Million Songs dataset
using Auto Loader (cloudFiles) for incremental processing.
"""

import dlt
from pyspark.sql import DataFrame
from pyspark.sql.functions import current_timestamp, lit


@dlt.table(
    name="songs_raw_bronze",
    comment="Raw data from a subset of the Million Song Dataset; a collection of features and metadata for contemporary music tracks.",
    table_properties={
        "quality": "bronze",
        "pipelines.autoOptimize.managed": "true"
    }
)
def songs_raw_bronze() -> DataFrame:
    """Create DLT bronze table for Million Songs data with incremental ingestion.

    Uses Auto Loader (cloudFiles) to incrementally ingest CSV files from
    /databricks-datasets/songs/data-001. Adds metadata columns for lineage
    tracking and debugging.

    Returns:
        Streaming DataFrame containing Million Songs records with columns:
        - artist_id: Unique identifier for the artist
        - artist_name: Name of the artist
        - duration: Song duration in seconds
        - release: Album/release name
        - tempo: Tempo in BPM
        - time_signature: Time signature
        - title: Song title
        - year: Release year
        - ingestion_timestamp: Timestamp when record was ingested
        - source_system: Source path of the data
    """
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "false")
        .option("inferSchema", "false")
        .option("delimiter", "\t")
        .schema("""
            artist_id STRING,
            artist_latitude DOUBLE,
            artist_longitude DOUBLE,
            artist_location STRING,
            artist_name STRING,
            duration DOUBLE,
            end_of_fade_in DOUBLE,
            key INT,
            key_confidence DOUBLE,
            loudness DOUBLE,
            release STRING,
            song_hotness DOUBLE,
            song_id STRING,
            start_of_fade_out DOUBLE,
            tempo DOUBLE,
            time_signature INT,
            time_signature_confidence DOUBLE,
            title STRING,
            year INT,
            partial_sequence STRING
        """)
        .load("/databricks-datasets/songs/data-001")
        .withColumn("ingestion_timestamp", current_timestamp())
        .withColumn("source_system", lit("/databricks-datasets/songs/data-001"))
    )
