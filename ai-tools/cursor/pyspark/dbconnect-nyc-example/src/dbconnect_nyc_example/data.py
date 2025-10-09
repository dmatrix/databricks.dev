"""Data access functions for NYC taxi dataset."""

from pyspark.sql import SparkSession, DataFrame


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
        >>> from dbconnect_nyc_example.config import get_spark
        >>> spark = get_spark()
        >>> df = get_taxis(spark)
        >>> df.show(5)
    """
    return spark.read.table("samples.nyctaxi.trips")

