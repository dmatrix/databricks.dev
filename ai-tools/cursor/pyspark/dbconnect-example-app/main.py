from pyspark.sql import SparkSession, DataFrame

def get_spark() -> SparkSession:
  try:
    from databricks.connect import DatabricksSession
    return DatabricksSession.builder.getOrCreate()
  except ImportError:
    return SparkSession.builder.getOrCreate()
    
def get_taxis(spark: SparkSession) -> DataFrame:
  return spark.read.table("samples.nyctaxi.trips")
    

def main():

    get_taxis(get_spark()).show(5)
    
    print("Hello from dbconnect-example-app!")


if __name__ == "__main__":
    main()
