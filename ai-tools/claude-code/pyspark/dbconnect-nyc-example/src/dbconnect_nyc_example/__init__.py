"""Databricks Connect NYC Taxi Example.

A minimal PySpark application demonstrating Databricks Connect usage
with the NYC taxi sample dataset.
"""

from dbconnect_nyc_example.config import get_spark
from dbconnect_nyc_example.data import get_taxis

__version__ = "0.1.0"

__all__ = ["get_spark", "get_taxis"]
