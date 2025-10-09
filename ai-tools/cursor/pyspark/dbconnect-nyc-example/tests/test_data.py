"""Tests for data access functions."""

import pytest
from pyspark.sql import SparkSession


def test_get_taxis_returns_dataframe():
    """Test that get_taxis returns a DataFrame with expected structure."""
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_taxis
    
    spark = get_spark()
    df = get_taxis(spark)
    
    # Verify DataFrame is not None
    assert df is not None
    
    # Verify expected columns exist
    expected_columns = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "trip_distance",
        "fare_amount",
        "pickup_zip",
        "dropoff_zip"
    ]
    
    for col in expected_columns:
        assert col in df.columns, f"Expected column '{col}' not found in DataFrame"
    
    # Verify DataFrame has data
    assert df.count() > 0, "DataFrame should contain records"


def test_get_taxis_has_mostly_positive_fare_amounts():
    """Test that most fare amounts are positive (allowing for refunds/adjustments)."""
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_taxis
    
    spark = get_spark()
    df = get_taxis(spark)
    
    total_count = df.count()
    negative_fares = df.filter(df.fare_amount < 0).count()
    positive_ratio = (total_count - negative_fares) / total_count
    
    # At least 99% of fares should be non-negative
    assert positive_ratio >= 0.99, f"Expected at least 99% positive fares, got {positive_ratio:.2%}"

