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


def test_get_taxis_with_fare_per_mile_happy_path():
    """Test get_taxis_with_fare_per_mile returns valid DataFrame with calculated field.
    
    This test validates the happy path with multiple assertions covering:
    - DataFrame creation with new average_fare_per_mile column
    - All original columns preserved
    - Data presence and record count
    - Descending order by fare per mile
    - Calculated values are reasonable and rounded to 2 decimals
    """
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_taxis_with_fare_per_mile
    
    # Setup
    spark = get_spark()
    df = get_taxis_with_fare_per_mile(spark)
    
    # Verify DataFrame creation
    assert df is not None, "DataFrame should not be None"
    assert hasattr(df, 'columns'), "Should return a DataFrame-like object with columns"
    
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
        assert col in df.columns, f"Original column '{col}' should be preserved"
    
    # Verify DataFrame has data
    record_count = df.count()
    assert record_count > 0, "DataFrame should contain records"
    assert record_count > 1000, f"Expected substantial dataset, got {record_count} records"
    
    # Verify ordering (descending by average_fare_per_mile)
    # Get first few non-null values to check ordering
    top_fares = df.filter(df.average_fare_per_mile.isNotNull()).limit(10).collect()
    assert len(top_fares) > 0, "Should have records with calculated fare per mile"
    
    # Check that values are in descending order
    for i in range(len(top_fares) - 1):
        current = top_fares[i]["average_fare_per_mile"]
        next_val = top_fares[i + 1]["average_fare_per_mile"]
        assert current >= next_val, f"Values should be in descending order: {current} >= {next_val}"
    
    # Verify values are rounded to 2 decimal places
    sample_with_values = df.filter(df.average_fare_per_mile.isNotNull()).limit(20).collect()
    for row in sample_with_values:
        value = row["average_fare_per_mile"]
        # Check that value has at most 2 decimal places
        decimal_str = str(value).split('.')
        if len(decimal_str) > 1:
            assert len(decimal_str[1]) <= 2, f"Value {value} should be rounded to 2 decimal places"
    
    # Verify calculated values are reasonable (not infinity or extreme values)
    max_fare_per_mile = df.filter(df.average_fare_per_mile.isNotNull()) \
        .selectExpr("max(average_fare_per_mile)").collect()[0][0]
    assert max_fare_per_mile < 10000, f"Suspiciously high fare per mile: {max_fare_per_mile}"


def test_get_taxis_with_fare_per_mile_edge_cases():
    """Test get_taxis_with_fare_per_mile handles edge cases correctly with try_divide.
    
    This test validates edge cases with multiple assertions covering:
    - Zero-distance trips have None for average_fare_per_mile (try_divide behavior)
    - Non-zero distance trips have calculated values
    - Calculation accuracy (fare / distance) rounded to 2 decimals
    - No division by zero errors
    - Proper handling of null values
    """
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_taxis_with_fare_per_mile
    
    # Setup
    spark = get_spark()
    df = get_taxis_with_fare_per_mile(spark)
    
    # Verify zero-distance trips have None for average_fare_per_mile (try_divide returns NULL)
    zero_distance_trips = df.filter(df.trip_distance == 0)
    if zero_distance_trips.count() > 0:
        zero_distance_with_calc = zero_distance_trips.filter(
            df.average_fare_per_mile.isNotNull()
        ).count()
        assert zero_distance_with_calc == 0, \
            f"Zero-distance trips should have None for fare per mile with try_divide, found {zero_distance_with_calc}"
    
    # Verify non-zero distance trips have calculated values
    non_zero_trips = df.filter((df.trip_distance > 0) & (df.fare_amount.isNotNull()))
    non_zero_count = non_zero_trips.count()
    
    if non_zero_count > 0:
        non_zero_with_calc = non_zero_trips.filter(df.average_fare_per_mile.isNotNull()).count()
        calc_ratio = non_zero_with_calc / non_zero_count
        assert calc_ratio >= 0.95, \
            f"Expected at least 95% of non-zero distance trips to have calculated fare per mile, got {calc_ratio:.2%}"
    
    # Verify calculation accuracy on a sample (accounting for rounding to 2 decimals)
    sample_trips = df.filter(
        (df.trip_distance > 0) & 
        (df.fare_amount.isNotNull()) &
        (df.average_fare_per_mile.isNotNull())
    ).limit(100).collect()
    
    assert len(sample_trips) > 0, "Should have sample trips for validation"
    
    for trip in sample_trips[:10]:  # Validate first 10
        expected = round(trip["fare_amount"] / trip["trip_distance"], 2)
        actual = trip["average_fare_per_mile"]
        # Should match exactly since both are rounded to 2 decimals
        assert abs(expected - actual) < 0.01, \
            f"Calculation error: expected {expected}, got {actual}"
    
    # Verify no extreme outliers in positive fare per mile values
    positive_fares = df.filter(df.average_fare_per_mile > 0)
    if positive_fares.count() > 0:
        avg_fare_per_mile = positive_fares.selectExpr("avg(average_fare_per_mile)").collect()[0][0]
        assert avg_fare_per_mile < 1000, \
            f"Average fare per mile seems too high: {avg_fare_per_mile}"
    
    # Verify null handling - trips with null fare or distance should handle gracefully
    total_count = df.count()
    null_calc = df.filter(df.average_fare_per_mile.isNull()).count()
    null_ratio = null_calc / total_count
    # Most trips should have a calculated value
    assert null_ratio < 0.05, \
        f"Too many null calculated values: {null_ratio:.2%} of trips"


def test_get_busiest_pickup_locations_happy_path():
    """Test get_busiest_pickup_locations returns valid aggregated DataFrame.
    
    This test validates the happy path with multiple assertions covering:
    - DataFrame creation with correct columns
    - Proper aggregation by pickup_zip
    - Trip count calculation
    - Descending order by trip count
    - Data presence and reasonable values
    """
    from pyspark.sql.functions import col
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_busiest_pickup_locations
    
    # Setup
    spark = get_spark()
    df = get_busiest_pickup_locations(spark)
    
    # Verify DataFrame creation
    assert df is not None, "DataFrame should not be None"
    assert hasattr(df, 'columns'), "Should return a DataFrame-like object with columns"
    
    # Verify expected columns exist
    assert "pickup_zip" in df.columns, "Should have pickup_zip column"
    assert "trip_count" in df.columns, "Should have trip_count column"
    
    # Verify only these two columns exist (aggregation should reduce columns)
    assert len(df.columns) == 2, f"Should have exactly 2 columns, got {len(df.columns)}"
    
    # Verify DataFrame has data
    location_count = df.count()
    assert location_count > 0, "DataFrame should contain pickup locations"
    assert location_count < 1000, f"Too many unique zip codes: {location_count}"
    
    # Verify ordering (descending by trip_count)
    top_locations = df.limit(10).collect()
    assert len(top_locations) > 0, "Should have records"
    
    # Check that trip counts are in descending order
    for i in range(len(top_locations) - 1):
        current_count = top_locations[i]["trip_count"]
        next_count = top_locations[i + 1]["trip_count"]
        assert current_count >= next_count, \
            f"Trip counts should be in descending order: {current_count} >= {next_count}"
    
    # Verify all trip counts are positive
    assert df.filter(col("trip_count") <= 0).count() == 0, "All trip counts should be positive"
    
    # Verify the busiest location has a reasonable number of trips
    max_trips = df.selectExpr("max(trip_count)").collect()[0][0]
    assert max_trips > 100, f"Expected busiest location to have >100 trips, got {max_trips}"
    assert max_trips < 100000, f"Suspiciously high trip count: {max_trips}"


def test_get_busiest_pickup_locations_edge_cases():
    """Test get_busiest_pickup_locations handles edge cases correctly.
    
    This test validates edge cases with multiple assertions covering:
    - Null pickup_zip handling
    - All zip codes have positive counts
    - No duplicate zip codes (proper grouping)
    - Sum of trip_counts matches original data
    - Data distribution is reasonable
    """
    from pyspark.sql.functions import col
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_busiest_pickup_locations, get_taxis
    
    # Setup
    spark = get_spark()
    df = get_busiest_pickup_locations(spark)
    original_df = get_taxis(spark)
    
    # Verify no duplicate zip codes (proper grouping)
    total_locations = df.count()
    distinct_zips = df.select("pickup_zip").distinct().count()
    assert total_locations == distinct_zips, \
        f"Found duplicate zip codes: {total_locations} rows but {distinct_zips} distinct zips"
    
    # Verify sum of trip_counts equals original row count
    aggregated_total = df.selectExpr("sum(trip_count)").collect()[0][0]
    original_total = original_df.count()
    assert aggregated_total == original_total, \
        f"Trip count mismatch: aggregated {aggregated_total} vs original {original_total}"
    
    # Check if null pickup_zip exists and is handled
    null_zip_count = df.filter(col("pickup_zip").isNull()).count()
    if null_zip_count > 0:
        # Verify null zip has a valid trip count
        null_trips = df.filter(col("pickup_zip").isNull()).select("trip_count").collect()
        assert len(null_trips) == 1, "Should have at most one row for null zip"
        assert null_trips[0]["trip_count"] > 0, "Null zip should have positive trip count"
    
    # Verify distribution - top 10 locations should account for reasonable portion
    top_10_sum = df.limit(10).selectExpr("sum(trip_count)").collect()[0][0]
    top_10_ratio = top_10_sum / original_total
    assert top_10_ratio > 0.1, f"Top 10 locations should have >10% of trips, got {top_10_ratio:.2%}"
    assert top_10_ratio < 0.9, f"Top 10 locations shouldn't dominate (>90%), got {top_10_ratio:.2%}"
    
    # Verify minimum trip count (even least popular location should have some trips)
    min_trips = df.selectExpr("min(trip_count)").collect()[0][0]
    assert min_trips > 0, f"All locations should have at least 1 trip, min is {min_trips}"
    
    # Verify data types
    schema = df.schema
    trip_count_field = [f for f in schema.fields if f.name == "trip_count"][0]
    assert trip_count_field.dataType.typeName() in ["long", "integer", "bigint"], \
        f"trip_count should be numeric type, got {trip_count_field.dataType.typeName()}"


def test_get_peak_hours_happy_path():
    """Test get_peak_hours returns valid aggregated DataFrame with hourly statistics.
    
    This test validates the happy path with multiple assertions covering:
    - DataFrame creation with correct columns
    - Proper aggregation by hour (0-23)
    - Trip count, average fare, and average distance calculations
    - Chronological order by hour
    - Data presence and reasonable values
    """
    from pyspark.sql.functions import col
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_peak_hours
    
    # Setup
    spark = get_spark()
    df = get_peak_hours(spark)
    
    # Verify DataFrame creation
    assert df is not None, "DataFrame should not be None"
    assert hasattr(df, 'columns'), "Should return a DataFrame-like object with columns"
    
    # Verify expected columns exist
    assert "hour" in df.columns, "Should have hour column"
    assert "trip_count" in df.columns, "Should have trip_count column"
    assert "avg_fare" in df.columns, "Should have avg_fare column"
    assert "avg_distance" in df.columns, "Should have avg_distance column"
    
    # Verify only these four columns exist
    assert len(df.columns) == 4, f"Should have exactly 4 columns, got {len(df.columns)}"
    
    # Verify DataFrame has data for all 24 hours
    hour_count = df.count()
    assert hour_count > 0, "DataFrame should contain hour records"
    assert hour_count <= 24, f"Should have at most 24 hours, got {hour_count}"
    assert hour_count >= 1, "Should have at least 1 hour of data"
    
    # Verify ordering (chronological by hour)
    all_hours = df.collect()
    assert len(all_hours) > 0, "Should have records"
    
    # Check that hours are in ascending order
    for i in range(len(all_hours) - 1):
        current_hour = all_hours[i]["hour"]
        next_hour = all_hours[i + 1]["hour"]
        assert current_hour < next_hour, \
            f"Hours should be in ascending order: {current_hour} < {next_hour}"
    
    # Verify hour range (0-23)
    first_hour = all_hours[0]["hour"]
    last_hour = all_hours[-1]["hour"]
    assert first_hour >= 0, f"First hour should be >= 0, got {first_hour}"
    assert last_hour <= 23, f"Last hour should be <= 23, got {last_hour}"
    
    # Verify all trip counts are positive
    assert df.filter(col("trip_count") <= 0).count() == 0, "All trip counts should be positive"
    
    # Verify average values are reasonable
    max_avg_fare = df.selectExpr("max(avg_fare)").collect()[0][0]
    max_avg_distance = df.selectExpr("max(avg_distance)").collect()[0][0]
    
    assert max_avg_fare > 0, "Average fare should be positive"
    assert max_avg_fare < 1000, f"Suspiciously high average fare: {max_avg_fare}"
    assert max_avg_distance > 0, "Average distance should be positive"
    assert max_avg_distance < 100, f"Suspiciously high average distance: {max_avg_distance} miles"
    
    # Verify values are rounded to 2 decimal places
    sample_hours = df.limit(5).collect()
    for row in sample_hours:
        avg_fare = row["avg_fare"]
        avg_distance = row["avg_distance"]
        
        # Check decimal places for avg_fare
        if avg_fare is not None:
            decimal_str = str(avg_fare).split('.')
            if len(decimal_str) > 1:
                assert len(decimal_str[1]) <= 2, f"avg_fare {avg_fare} should be rounded to 2 decimal places"
        
        # Check decimal places for avg_distance
        if avg_distance is not None:
            decimal_str = str(avg_distance).split('.')
            if len(decimal_str) > 1:
                assert len(decimal_str[1]) <= 2, f"avg_distance {avg_distance} should be rounded to 2 decimal places"


def test_get_peak_hours_edge_cases():
    """Test get_peak_hours handles edge cases and validates aggregation correctness.
    
    This test validates edge cases with multiple assertions covering:
    - All hours have positive trip counts
    - Average values are within reasonable ranges
    - No duplicate hours (proper grouping)
    - Aggregation totals make sense
    - Data types are correct
    """
    from pyspark.sql.functions import col
    from dbconnect_nyc_example.config import get_spark
    from dbconnect_nyc_example.data import get_peak_hours, get_taxis
    
    # Setup
    spark = get_spark()
    df = get_peak_hours(spark)
    original_df = get_taxis(spark)
    
    # Verify no duplicate hours (proper grouping)
    total_hours = df.count()
    distinct_hours = df.select("hour").distinct().count()
    assert total_hours == distinct_hours, \
        f"Found duplicate hours: {total_hours} rows but {distinct_hours} distinct hours"
    
    # Verify sum of trip_counts matches original row count
    aggregated_total = df.selectExpr("sum(trip_count)").collect()[0][0]
    original_total = original_df.count()
    assert aggregated_total == original_total, \
        f"Trip count mismatch: aggregated {aggregated_total} vs original {original_total}"
    
    # Verify all hours have reasonable trip counts (no outliers too extreme)
    min_trips = df.selectExpr("min(trip_count)").collect()[0][0]
    max_trips = df.selectExpr("max(trip_count)").collect()[0][0]
    
    assert min_trips > 0, f"All hours should have at least 1 trip, min is {min_trips}"
    assert max_trips > min_trips, "Should have variation in trip counts across hours"
    
    # Verify average fare is within reasonable bounds for all hours
    min_avg_fare = df.filter(col("avg_fare").isNotNull()).selectExpr("min(avg_fare)").collect()[0][0]
    max_avg_fare = df.filter(col("avg_fare").isNotNull()).selectExpr("max(avg_fare)").collect()[0][0]
    
    assert min_avg_fare > 0, f"Minimum average fare should be positive, got {min_avg_fare}"
    assert max_avg_fare < 500, f"Maximum average fare seems too high: {max_avg_fare}"
    assert max_avg_fare > min_avg_fare, "Should have variation in average fares"
    
    # Verify average distance is within reasonable bounds
    min_avg_distance = df.filter(col("avg_distance").isNotNull()).selectExpr("min(avg_distance)").collect()[0][0]
    max_avg_distance = df.filter(col("avg_distance").isNotNull()).selectExpr("max(avg_distance)").collect()[0][0]
    
    assert min_avg_distance >= 0, f"Minimum average distance should be non-negative, got {min_avg_distance}"
    assert max_avg_distance < 50, f"Maximum average distance seems too high: {max_avg_distance} miles"
    
    # Verify no null values in critical columns
    null_hours = df.filter(col("hour").isNull()).count()
    null_trip_counts = df.filter(col("trip_count").isNull()).count()
    
    assert null_hours == 0, f"Should have no null hours, found {null_hours}"
    assert null_trip_counts == 0, f"Should have no null trip counts, found {null_trip_counts}"
    
    # Verify data types
    schema = df.schema
    hour_field = [f for f in schema.fields if f.name == "hour"][0]
    trip_count_field = [f for f in schema.fields if f.name == "trip_count"][0]
    
    assert hour_field.dataType.typeName() in ["integer", "int", "long", "bigint"], \
        f"hour should be integer type, got {hour_field.dataType.typeName()}"
    assert trip_count_field.dataType.typeName() in ["long", "integer", "bigint"], \
        f"trip_count should be numeric type, got {trip_count_field.dataType.typeName()}"

