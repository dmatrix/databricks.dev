"""Spark session configuration for Databricks Connect."""

import os
from databricks.connect import DatabricksSession
from pyspark.sql import SparkSession


def get_spark(cluster_id: str | None = None) -> SparkSession:
    """Get or create a Databricks Spark session.

    Uses the DEFAULT Databricks authentication profile.
    The DEFAULT profile should be configured using:
    databricks auth login --profile DEFAULT --host https://your-workspace.databricks.com

    Args:
        cluster_id: Optional cluster ID to use. If not provided, checks DATABRICKS_CLUSTER_ID
                   environment variable, otherwise uses serverless compute.

    Returns:
        SparkSession: An active Databricks Spark session

    Raises:
        Exception: If unable to connect to Databricks workspace

    Example:
        >>> spark = get_spark()  # Uses serverless or env var
        >>> spark = get_spark(cluster_id="your-cluster-id")  # Uses specific cluster
        >>> spark.sql("SELECT 1 AS test").show()
    """
    try:
        builder = DatabricksSession.builder

        # Use cluster_id if provided, otherwise check environment variable
        target_cluster_id = cluster_id or os.getenv("DATABRICKS_CLUSTER_ID")

        if target_cluster_id:
            return builder.clusterId(target_cluster_id).getOrCreate()
        else:
            # Use serverless compute as fallback
            return builder.serverless(True).getOrCreate()
    except Exception as e:
        raise Exception(
            f"Failed to create Databricks session. "
            f"Ensure you've authenticated with: "
            f"databricks auth login --profile DEFAULT --host <your-workspace-url>. "
            f"Error: {e}"
        ) from e
