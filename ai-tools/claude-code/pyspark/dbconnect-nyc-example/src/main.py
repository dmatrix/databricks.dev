"""Main entry point for NYC taxi data analysis."""

from dbconnect_nyc_example.config import get_spark
from dbconnect_nyc_example.data import get_taxis, get_taxis_with_fare_per_mile


def main() -> None:
    """Run NYC taxi data analysis.

    Retrieves and displays sample NYC taxi trip data using Databricks Connect.
    """
    print("Starting NYC Taxi Data Analysis...")
    print("=" * 50)

    # Get Spark session
    spark = get_spark()
    print("✓ Connected to Databricks")

    # Get taxi data
    df = get_taxis(spark)
    print(f"✓ Loaded NYC taxi data: {df.count():,} records")

    # Display sample data
    print("\nSample NYC Taxi Trips:")
    print("-" * 50)
    df.select(
        "tpep_pickup_datetime",
        "trip_distance",
        "fare_amount",
        "pickup_zip",
        "dropoff_zip"
    ).show(10, truncate=False)

    # Display fare per mile analysis
    print("\nFare Per Mile Analysis (Top 10 by fare/mile):")
    print("-" * 50)
    fare_per_mile_df = get_taxis_with_fare_per_mile(spark)
    fare_per_mile_df.select(
        "trip_distance",
        "fare_amount",
        "average_fare_per_mile",
        "pickup_zip",
        "dropoff_zip"
    ).show(10, truncate=False)

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()
