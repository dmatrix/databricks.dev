"""Main entry point for dbconnect-nyc-example.

Demonstrates querying NYC taxi data from Databricks using Databricks Connect.
"""

from dbconnect_nyc_example.config import get_spark
from dbconnect_nyc_example.data import get_taxis


def main():
    """Run the example application."""
    spark = get_spark()
    df = get_taxis(spark)
    
    print("NYC Taxi Trips Sample Data:")
    df.show(5)
    
    print(f"\nTotal records: {df.count()}")
    print("Hello from dbconnect-nyc-example!")


if __name__ == "__main__":
    main()
