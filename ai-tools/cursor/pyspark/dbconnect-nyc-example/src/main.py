"""Main entry point for dbconnect-nyc-example.

Demonstrates querying NYC taxi data from Databricks using Databricks Connect.
"""

from dbconnect_nyc_example.config import get_spark
from dbconnect_nyc_example.data import get_peak_hours


def main():
    """Run the example application."""
    spark = get_spark()
    df = get_peak_hours(spark)
    
    print("NYC Taxi Peak Hours Analysis:")
    df.show(24, truncate=False)
    
    print(f"\nTotal hours analyzed: {df.count()}")
    print("\nInsight: Reveals patterns in taxi usage throughout the day - useful for understanding demand cycles and optimal driver scheduling.")


if __name__ == "__main__":
    main()
