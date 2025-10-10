"""Main entry point for Million Songs data analysis."""

from dbconnect_million_songs.config import get_spark
from dbconnect_million_songs.data import get_songs


def main() -> None:
    """Run Million Songs data analysis.

    Retrieves and displays sample Million Songs data from the bronze table
    using Databricks Connect.
    """
    print("Starting Million Songs Data Analysis...")
    print("=" * 50)

    # Get Spark session
    spark = get_spark()
    print("✓ Connected to Databricks")

    # Get songs data from bronze table
    df = get_songs(spark)
    print(f"✓ Loaded Million Songs data from bronze table: {df.count():,} records")

    # Display sample data
    print("\nSample Million Songs:")
    print("-" * 50)
    df.select(
        "artist_name",
        "title",
        "year",
        "duration",
        "tempo"
    ).show(10, truncate=False)

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
