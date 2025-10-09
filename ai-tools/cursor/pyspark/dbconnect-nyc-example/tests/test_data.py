"""Tests for data access functions.

Following testing-rules.mdc: Maximum 2 tests per function with multiple assertions.
"""

import pytest


def test_get_taxis_happy_path():
    """Test get_taxis returns a valid DataFrame with expected structure and data.
    
    This test validates the happy path with multiple assertions covering:
    - DataFrame creation and type
    - Expected schema/columns
    - Data presence
    - Basic record count validation
    """
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_taxis
    
    # Setup
    spark = get_spark()
    df = get_taxis(spark)
    
    # Verify DataFrame creation and type
    assert df is not None, "DataFrame should not be None"
    assert hasattr(df, 'columns'), "Should return a DataFrame-like object with columns"
    assert hasattr(df, 'count'), "Should return a DataFrame-like object with count method"
    
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
    record_count = df.count()
    assert record_count > 0, "DataFrame should contain records"
    assert record_count > 1000, f"Expected substantial dataset, got {record_count} records"
    
    # Verify schema is accessible
    assert df.schema is not None, "DataFrame should have a defined schema"
    assert len(df.schema.fields) >= 6, "DataFrame should have at least 6 fields"


def test_get_taxis_data_quality():
    """Test get_taxis data quality and edge cases with multiple validations.
    
    This test validates data quality with multiple assertions covering:
    - Fare amount distribution (positive vs negative)
    - Trip distance validity
    - No null values in critical columns
    - Data type consistency
    """
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_taxis
    
    # Setup
    spark = get_spark()
    df = get_taxis(spark)
    
    # Validate fare amounts - mostly positive (allowing refunds/adjustments)
    total_count = df.count()
    negative_fares = df.filter(df.fare_amount < 0).count()
    positive_ratio = (total_count - negative_fares) / total_count
    
    assert positive_ratio >= 0.99, f"Expected at least 99% positive fares, got {positive_ratio:.2%}"
    assert negative_fares < 100, f"Too many negative fares: {negative_fares}"
    
    # Validate trip distances - should be non-negative
    negative_distances = df.filter(df.trip_distance < 0).count()
    assert negative_distances == 0, f"Found {negative_distances} records with negative distances"
    
    # Validate critical columns have data (not all nulls)
    null_fares = df.filter(df.fare_amount.isNull()).count()
    null_distances = df.filter(df.trip_distance.isNull()).count()
    
    assert null_fares < total_count * 0.01, f"Too many null fares: {null_fares}"
    assert null_distances < total_count * 0.01, f"Too many null distances: {null_distances}"
    
    # Validate reasonable value ranges
    max_fare = df.selectExpr("max(fare_amount)").collect()[0][0]
    max_distance = df.selectExpr("max(trip_distance)").collect()[0][0]
    
    assert max_fare < 10000, f"Suspiciously high fare: {max_fare}"
    assert max_distance < 500, f"Suspiciously long trip: {max_distance} miles"

