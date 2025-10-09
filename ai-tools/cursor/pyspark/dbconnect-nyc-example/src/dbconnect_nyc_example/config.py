"""Configuration and Spark session management."""

from pyspark.sql import SparkSession


def get_spark() -> SparkSession:
    """Get or create a Spark session.
    
    Uses DatabricksSession when databricks-connect is available,
    otherwise falls back to standard SparkSession.
    
    Returns:
        SparkSession: An active Spark session instance
        
    Example:
        >>> spark = get_spark()
        >>> spark.version
    """
    try:
        from databricks.connect import DatabricksSession
        return DatabricksSession.builder.getOrCreate()
    except ImportError:
        return SparkSession.builder.getOrCreate()

