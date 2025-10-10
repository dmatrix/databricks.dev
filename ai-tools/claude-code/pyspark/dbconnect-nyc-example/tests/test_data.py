"""Tests for data access functions."""

import pytest

from dbconnect_nyc_example.config import get_spark
from dbconnect_nyc_example.data import get_taxis, get_taxis_with_fare_per_mile


def test_get_taxis_returns_valid_dataframe():
    """Test that get_taxis returns a DataFrame with correct structure and data."""
    spark = get_spark()
    df = get_taxis(spark)

    # Verify DataFrame is not None
    assert df is not None, "DataFrame should not be None"

    # Verify it's a DataFrame type (works with both PySpark and Databricks Connect)
    assert hasattr(df, 'schema') and hasattr(df, 'count'), "Should return DataFrame type"

    # Verify DataFrame has data
    assert df.count() > 0, "DataFrame should contain records"

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
        assert col in df.columns, f"Expected column '{col}' not found"


def test_get_taxis_data_quality():
    """Test data quality checks for edge cases."""
    spark = get_spark()
    df = get_taxis(spark)

    total_count = df.count()

    # Check that most trip distances are positive
    negative_distances = df.filter(df.trip_distance < 0).count()
    positive_distance_ratio = (total_count - negative_distances) / total_count
    assert positive_distance_ratio >= 0.95, "At least 95% of trips should have non-negative distance"

    # Check that most fare amounts are reasonable
    negative_fares = df.filter(df.fare_amount < 0).count()
    positive_fare_ratio = (total_count - negative_fares) / total_count
    assert positive_fare_ratio >= 0.95, "At least 95% of trips should have non-negative fare"

    # Verify data types
    schema_dict = {field.name: str(field.dataType) for field in df.schema.fields}
    assert "timestamp" in schema_dict["tpep_pickup_datetime"].lower(), "Pickup should be timestamp"
    assert "timestamp" in schema_dict["tpep_dropoff_datetime"].lower(), "Dropoff should be timestamp"


def test_get_taxis_with_fare_per_mile_returns_valid_dataframe():
    """Test that get_taxis_with_fare_per_mile returns correct structure and calculations."""
    spark = get_spark()
    df = get_taxis_with_fare_per_mile(spark)

    # Verify DataFrame is not None and has data
    assert df is not None, "DataFrame should not be None"
    assert hasattr(df, 'schema') and hasattr(df, 'count'), "Should return DataFrame type"
    assert df.count() > 0, "DataFrame should contain records"

    # Verify new column exists
    assert "average_fare_per_mile" in df.columns, "Should have average_fare_per_mile column"

    # Verify all original columns are preserved
    expected_columns = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "trip_distance",
        "fare_amount",
        "pickup_zip",
        "dropoff_zip"
    ]
    for col in expected_columns:
        assert col in df.columns, f"Expected column '{col}' not found"

    # Verify ordering (first row should have highest fare per mile that's not None)
    first_row = df.select("average_fare_per_mile").first()
    assert first_row is not None, "Should have at least one row"
    assert first_row[0] is not None, "First row should not be None (ordered desc nulls last)"

    # Verify calculation correctness for non-zero distance trips
    sample_data = df.filter(df.trip_distance > 0).limit(10).collect()
    for row in sample_data:
        if row.average_fare_per_mile is not None:
            expected = round(row.fare_amount / row.trip_distance, 2)
            assert row.average_fare_per_mile == expected, f"Fare per mile calculation incorrect"


def test_get_taxis_with_fare_per_mile_handles_edge_cases():
    """Test that get_taxis_with_fare_per_mile handles zero-distance and null cases."""
    spark = get_spark()
    df = get_taxis_with_fare_per_mile(spark)

    # Verify zero-distance trips have None for fare per mile
    zero_distance_trips = df.filter(df.trip_distance == 0).select("average_fare_per_mile")
    if zero_distance_trips.count() > 0:
        for row in zero_distance_trips.collect():
            assert row.average_fare_per_mile is None, "Zero-distance trips should have None fare per mile"

    # Verify rounding to 2 decimal places
    non_null_fares = df.filter(df.average_fare_per_mile.isNotNull()).select("average_fare_per_mile").limit(100).collect()
    for row in non_null_fares:
        fare_str = str(row.average_fare_per_mile)
        if '.' in fare_str:
            decimal_places = len(fare_str.split('.')[1])
            assert decimal_places <= 2, f"Should be rounded to max 2 decimal places, got {decimal_places}"

    # Verify ordering (descending nulls last)
    all_fares = df.select("average_fare_per_mile").limit(100).collect()
    non_null_fares_list = [row.average_fare_per_mile for row in all_fares if row.average_fare_per_mile is not None]

    # Check descending order for non-null values
    if len(non_null_fares_list) > 1:
        for i in range(len(non_null_fares_list) - 1):
            assert non_null_fares_list[i] >= non_null_fares_list[i + 1], "Should be ordered descending"
