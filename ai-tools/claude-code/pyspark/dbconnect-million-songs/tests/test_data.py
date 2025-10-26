"""Tests for data access functions."""

from dbconnect_million_songs.config import get_spark
from dbconnect_million_songs.data import get_songs


def test_get_songs_returns_valid_dataframe():
    """Test that get_songs returns a DataFrame with correct structure and data."""
    spark = get_spark()
    df = get_songs(spark)

    # Verify DataFrame is not None
    assert df is not None, "DataFrame should not be None"

    # Verify it's a DataFrame type (works with both PySpark and Databricks Connect)
    assert hasattr(df, 'schema') and hasattr(df, 'count'), "Should return DataFrame type"

    # Verify DataFrame has data
    assert df.count() > 0, "DataFrame should contain records"

    # Verify expected columns exist
    expected_columns = [
        "artist_id",
        "artist_name",
        "duration",
        "release",
        "tempo",
        "time_signature",
        "title",
        "year"
    ]

    for col in expected_columns:
        assert col in df.columns, f"Expected column '{col}' not found"


def test_get_songs_data_quality():
    """Test data quality checks for edge cases."""
    spark = get_spark()
    df = get_songs(spark)

    total_count = df.count()

    # Check that most durations are positive
    negative_durations = df.filter(df.duration < 0).count()
    positive_duration_ratio = (total_count - negative_durations) / total_count
    assert positive_duration_ratio >= 0.95, "At least 95% of songs should have non-negative duration"

    # Check that valid years (non-zero) are reasonable (between 1900 and current year + 1)
    # Note: Many songs have year = 0 indicating unknown year
    valid_year_count = df.filter(df.year > 0).count()
    unreasonable_years = df.filter((df.year > 0) & ((df.year < 1900) | (df.year > 2026))).count()

    if valid_year_count > 0:
        reasonable_year_ratio = (valid_year_count - unreasonable_years) / valid_year_count
        assert reasonable_year_ratio >= 0.95, "At least 95% of non-zero years should be reasonable (1900-2026)"

    # Verify data types
    schema_dict = {field.name: str(field.dataType) for field in df.schema.fields}
    assert "string" in schema_dict["artist_name"].lower(), "artist_name should be string type"
    assert "string" in schema_dict["title"].lower(), "title should be string type"
