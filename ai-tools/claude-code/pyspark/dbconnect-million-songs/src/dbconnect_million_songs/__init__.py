"""Databricks Connect Million Songs Example.

A minimal PySpark application demonstrating Databricks Connect usage
with the Million Songs dataset.
"""

from dbconnect_million_songs.config import get_spark
from dbconnect_million_songs.data import get_songs

__version__ = "0.1.0"

__all__ = ["get_spark", "get_songs"]
