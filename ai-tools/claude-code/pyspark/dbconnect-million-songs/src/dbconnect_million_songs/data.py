"""Data access functions for Million Songs dataset."""

from pyspark.sql import DataFrame, SparkSession

 
def get_songs(spark: SparkSession) -> DataFrame:
    """Retrieve Million Songs data from bronze table in catalog.

    Args:
        spark: An active SparkSession instance

    Returns:
        DataFrame containing Million Songs records with columns:
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

    Raises:
        Exception: If the table cannot be accessed

    Example:
        >>> spark = get_spark()
        >>> df = get_songs(spark)
        >>> df.show(5)
    """
    try:
        return spark.read.table("jules_catalog.millionsongs.songs_raw_bronze")
    except Exception as e:
        raise Exception(
            f"Failed to read Million Songs data from bronze table. "
            f"Ensure you have access to jules_catalog.millionsongs.songs_raw_bronze table. "
            f"Error: {e}"
        ) from e
