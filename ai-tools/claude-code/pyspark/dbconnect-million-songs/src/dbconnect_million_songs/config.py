"""Spark session configuration for Databricks Connect."""

from databricks.connect import DatabricksSession
from pyspark.sql import SparkSession


def get_spark() -> SparkSession:
    """Get or create a Databricks Spark session.

    Uses the DEFAULT Databricks authentication profile and serverless compute.
    The DEFAULT profile should be configured using:
    databricks auth login --profile DEFAULT --host https://your-workspace.databricks.com

    Returns:
        SparkSession: An active Databricks Spark session

    Raises:
        Exception: If unable to connect to Databricks workspace

    Example:
        >>> spark = get_spark()
        >>> spark.sql("SELECT 1 AS test").show()
    """
    try:
        return DatabricksSession.builder.getOrCreate()
    except Exception as e:
        raise Exception(
            f"Failed to create Databricks session. "
            f"Ensure you've authenticated with: "
            f"databricks auth login --profile DEFAULT --host <your-workspace-url>. "
            f"Error: {e}"
        ) from e
