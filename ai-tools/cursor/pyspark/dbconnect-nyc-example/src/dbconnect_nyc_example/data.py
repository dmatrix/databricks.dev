"""Data access functions for NYC taxi dataset."""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, try_divide, round as spark_round, count, hour, avg


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


def get_taxis_with_fare_per_mile(spark: SparkSession) -> DataFrame:
    """Retrieve NYC taxi trip data with average fare per mile calculated.
    
    Calculates the average fare per mile for each trip using try_divide to safely
    handle zero-distance trips (which return None). Values are rounded to 2 decimal
    places. Results are ordered by fare per mile in descending order, showing the
    most expensive trips first.
    
    Args:
        spark: An active SparkSession instance
        
    Returns:
        DataFrame containing NYC taxi trip records with additional column:
        - average_fare_per_mile: fare_amount / trip_distance rounded to 2 decimals
          (None if distance is 0)
        
        All original columns are preserved, including:
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
        >>> df = get_taxis_with_fare_per_mile(spark)
        >>> df.show(10)
        
    Note:
        Short trips typically have higher per-mile rates due to base fares
        and minimum charges. The try_divide function safely handles zero-distance
        trips by returning None instead of throwing division by zero errors.
        Values are rounded to 2 decimal places for readability.
    """
    return (spark.read.table("samples.nyctaxi.trips")
        .withColumn("average_fare_per_mile",
            spark_round(try_divide(col("fare_amount"), col("trip_distance")), 2)
        )
        .orderBy(col("average_fare_per_mile").desc())
    )


def get_busiest_pickup_locations(spark: SparkSession) -> DataFrame:
    """Retrieve the busiest pickup locations by zip code.
    
    Groups NYC taxi trips by pickup zip code and counts the number of trips
    from each location. Results are ordered by trip count in descending order
    to show the most popular pickup locations first.
    
    Args:
        spark: An active SparkSession instance
        
    Returns:
        DataFrame with columns:
        - pickup_zip: The zip code of the pickup location
        - trip_count: Number of trips that originated from this zip code
        
        Results are ordered by trip_count descending (busiest first)
        
    Raises:
        ValueError: If the table cannot be accessed
        
    Example:
        >>> from dbconnect_nyc_example.config import get_spark
        >>> spark = get_spark()
        >>> df = get_busiest_pickup_locations(spark)
        >>> df.show(10)
        
    Note:
        This analysis helps identify high-demand areas which can inform:
        - Driver positioning strategies
        - Demand forecasting
        - Resource allocation
        
        Null pickup_zip values are included in the aggregation.
    """
    return (spark.read.table("samples.nyctaxi.trips")
        .groupBy("pickup_zip")
        .agg(count("*").alias("trip_count"))
        .orderBy(col("trip_count").desc())
    )


def get_peak_hours(spark: SparkSession) -> DataFrame:
    """Analyze the busiest hours of the day with average fare and distance.
    
    Extracts the hour from pickup datetime and groups trips by hour of day (0-23).
    Calculates trip count, average fare, and average distance for each hour.
    Results are ordered chronologically by hour.
    
    Args:
        spark: An active SparkSession instance
        
    Returns:
        DataFrame with columns:
        - hour: Hour of day (0-23) extracted from pickup datetime
        - trip_count: Number of trips during this hour
        - avg_fare: Average fare amount during this hour (rounded to 2 decimals)
        - avg_distance: Average trip distance during this hour (rounded to 2 decimals)
        
        Results are ordered by hour (chronological order)
        
    Raises:
        ValueError: If the table cannot be accessed
        
    Example:
        >>> from dbconnect_nyc_example.config import get_spark
        >>> spark = get_spark()
        >>> df = get_peak_hours(spark)
        >>> df.show(24)
        
    Note:
        This analysis reveals patterns in taxi usage throughout the day:
        - Peak demand times (morning/evening rush hours)
        - Off-peak periods
        - Optimal driver scheduling windows
        - Demand cycles and pricing opportunities
        
        Useful for understanding when to deploy more drivers and when 
        customers are willing to pay higher fares.
    """
    return (spark.read.table("samples.nyctaxi.trips")
        .withColumn("hour", hour(col("tpep_pickup_datetime")))
        .groupBy("hour")
        .agg(
            count("*").alias("trip_count"),
            spark_round(avg(col("fare_amount")), 2).alias("avg_fare"),
            spark_round(avg(col("trip_distance")), 2).alias("avg_distance")
        )
        .orderBy(col("hour"))
    )

