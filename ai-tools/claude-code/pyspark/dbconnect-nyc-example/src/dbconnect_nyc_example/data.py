"""Data access functions for NYC taxi dataset."""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, round as sql_round, try_divide


def get_taxis(spark: SparkSession) -> DataFrame:
    """Retrieve NYC taxi trip data from Databricks sample tables.

    Args:
        spark: An active SparkSession instance

    Returns:
        DataFrame containing NYC taxi trip records with columns:
        - tpep_pickup_datetime: Pickup timestamp
        - tpep_dropoff_datetime: Dropoff timestamp
        - trip_distance: Trip distance in miles
        - fare_amount: Fare amount in dollars
        - pickup_zip: Pickup location ZIP code
        - dropoff_zip: Dropoff location ZIP code

    Raises:
        Exception: If the table cannot be accessed

    Example:
        >>> spark = get_spark()
        >>> df = get_taxis(spark)
        >>> df.show(5)
    """
    try:
        return spark.read.table("samples.nyctaxi.trips")
    except Exception as e:
        raise Exception(
            f"Failed to read NYC taxi data. "
            f"Ensure you have access to samples.nyctaxi.trips table. "
            f"Error: {e}"
        ) from e


def get_taxis_with_fare_per_mile(spark: SparkSession) -> DataFrame:
    """Return NYC taxi trips with average fare per mile calculated.

    Calculates fare per mile for each trip, handling zero-distance trips
    by setting their fare per mile to None. Results are ordered by fare
    per mile in descending order.

    Args:
        spark: An active SparkSession instance

    Returns:
        DataFrame containing all original columns plus:
        - average_fare_per_mile: Fare amount divided by trip distance,
          rounded to 2 decimal places. None for zero-distance trips.

    Raises:
        Exception: If the table cannot be accessed

    Example:
        >>> spark = get_spark()
        >>> df = get_taxis_with_fare_per_mile(spark)
        >>> df.select("trip_distance", "fare_amount", "average_fare_per_mile").show(10)
    """
    df = get_taxis(spark)

    # Calculate fare per mile using try_divide (returns None for division by zero)
    # Round to 2 decimal places
    df_with_fare_per_mile = df.withColumn(
        "average_fare_per_mile",
        sql_round(try_divide(col("fare_amount"), col("trip_distance")), 2)
    )

    # Order by fare per mile descending (nulls last)
    return df_with_fare_per_mile.orderBy(col("average_fare_per_mile").desc_nulls_last())
