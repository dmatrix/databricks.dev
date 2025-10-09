# Suggested Queries for NYC Taxi Dataset

This document contains interesting queries you can use to garner insights from the `samples.nyctaxi.trips` dataset.

---

## 1. Busiest Pickup Locations

**Prompt:** "Find which zip codes have the most pickups and show the top 10"

```python
def get_busiest_pickup_locations(spark: SparkSession) -> DataFrame:
  from pyspark.sql.functions import count, col
  
  return (spark.read.table("samples.nyctaxi.trips")
    .groupBy("pickup_zip")
    .agg(count("*").alias("trip_count"))
    .orderBy(col("trip_count").desc())
  )
```

**Insight:** Identifies the most popular pickup locations in NYC.

---

## 2. Peak Hours Analysis

**Prompt:** "Show me the busiest hours of the day with average fare and distance"

```python
def get_peak_hours(spark: SparkSession) -> DataFrame:
  from pyspark.sql.functions import hour, count, avg, col
  
  return (spark.read.table("samples.nyctaxi.trips")
    .withColumn("hour", hour("tpep_pickup_datetime"))
    .groupBy("hour")
    .agg(
      count("*").alias("trip_count"),
      avg("fare_amount").alias("avg_fare"),
      avg("trip_distance").alias("avg_distance")
    )
    .orderBy("hour")
  )
```

**Insight:** Reveals patterns in taxi usage throughout the day, useful for understanding demand.

---

## 3. Most Popular Routes

**Prompt:** "What are the most common pickup-dropoff route combinations?"

```python
def get_popular_routes(spark: SparkSession) -> DataFrame:
  from pyspark.sql.functions import count, avg, col
  
  return (spark.read.table("samples.nyctaxi.trips")
    .groupBy("pickup_zip", "dropoff_zip")
    .agg(
      count("*").alias("trip_count"),
      avg("fare_amount").alias("avg_fare"),
      avg("trip_distance").alias("avg_distance")
    )
    .orderBy(col("trip_count").desc())
  )
```

**Insight:** Shows the most traveled routes, which could inform driver positioning strategies.

---

## 4. Trip Distance Distribution

**Prompt:** "Analyze trips by distance buckets (0-1, 1-3, 3-5, 5-10, 10+ miles)"

```python
def get_trip_distance_buckets(spark: SparkSession) -> DataFrame:
  from pyspark.sql.functions import when, col, count, avg
  
  return (spark.read.table("samples.nyctaxi.trips")
    .withColumn("distance_bucket", 
      when(col("trip_distance") < 1, "0-1 miles")
      .when(col("trip_distance") < 3, "1-3 miles")
      .when(col("trip_distance") < 5, "3-5 miles")
      .when(col("trip_distance") < 10, "5-10 miles")
      .otherwise("10+ miles")
    )
    .groupBy("distance_bucket")
    .agg(
      count("*").alias("trip_count"),
      avg("fare_amount").alias("avg_fare")
    )
    .orderBy("trip_count")
  )
```

**Insight:** Understand the distribution of trip lengths and their relationship to fares.

---

## 5. Day of Week Patterns

**Prompt:** "How do trips vary by day of the week?"

```python
def get_day_of_week_patterns(spark: SparkSession) -> DataFrame:
  from pyspark.sql.functions import dayofweek, count, avg, col
  
  return (spark.read.table("samples.nyctaxi.trips")
    .withColumn("day_of_week", dayofweek("tpep_pickup_datetime"))
    .groupBy("day_of_week")
    .agg(
      count("*").alias("trip_count"),
      avg("fare_amount").alias("avg_fare"),
      avg("trip_distance").alias("avg_distance")
    )
    .orderBy("day_of_week")
  )
```

**Insight:** Identify weekday vs weekend patterns in taxi usage (1=Sunday, 7=Saturday).

---

## 6. Trip Duration Analysis

**Prompt:** "Calculate trip durations and group them into time buckets"

```python
def get_trip_duration_analysis(spark: SparkSession) -> DataFrame:
  from pyspark.sql.functions import unix_timestamp, col, avg, count, when
  
  return (spark.read.table("samples.nyctaxi.trips")
    .withColumn("duration_minutes", 
      (unix_timestamp("tpep_dropoff_datetime") - 
       unix_timestamp("tpep_pickup_datetime")) / 60
    )
    .filter(col("duration_minutes") > 0)
    .withColumn("duration_bucket",
      when(col("duration_minutes") < 10, "0-10 min")
      .when(col("duration_minutes") < 20, "10-20 min")
      .when(col("duration_minutes") < 30, "20-30 min")
      .otherwise("30+ min")
    )
    .groupBy("duration_bucket")
    .agg(
      count("*").alias("trip_count"),
      avg("fare_amount").alias("avg_fare"),
      avg("trip_distance").alias("avg_distance")
    )
  )
```

**Insight:** Understand trip duration patterns and how they correlate with distance and fare.

---

## 7. Expensive vs Cheap Trips

**Prompt:** "Compare characteristics of high-fare vs low-fare trips using quartiles"

```python
def get_fare_comparison(spark: SparkSession) -> DataFrame:
  from pyspark.sql.functions import col, percentile_approx, avg, when, count
  
  df = spark.read.table("samples.nyctaxi.trips")
  
  # Get percentiles
  percentiles = df.select(
    percentile_approx("fare_amount", 0.25).alias("q1"),
    percentile_approx("fare_amount", 0.75).alias("q3")
  ).collect()[0]
  
  return (df.withColumn("fare_category",
      when(col("fare_amount") < percentiles["q1"], "Low")
      .when(col("fare_amount") > percentiles["q3"], "High")
      .otherwise("Medium")
    )
    .groupBy("fare_category")
    .agg(
      count("*").alias("trip_count"),
      avg("trip_distance").alias("avg_distance"),
      avg("fare_amount").alias("avg_fare")
    )
  )
```

**Insight:** Reveals what distinguishes expensive trips from cheap ones.

---

## 8. Speed Analysis

**Prompt:** "Calculate average speed (mph) for trips and identify patterns"

```python
def get_speed_analysis(spark: SparkSession) -> DataFrame:
  from pyspark.sql.functions import unix_timestamp, col, avg, count, when
  
  return (spark.read.table("samples.nyctaxi.trips")
    .withColumn("duration_hours", 
      (unix_timestamp("tpep_dropoff_datetime") - 
       unix_timestamp("tpep_pickup_datetime")) / 3600
    )
    .filter((col("duration_hours") > 0) & (col("trip_distance") > 0))
    .withColumn("avg_speed_mph", col("trip_distance") / col("duration_hours"))
    .filter(col("avg_speed_mph") < 100)  # Filter outliers
    .withColumn("speed_bucket",
      when(col("avg_speed_mph") < 10, "0-10 mph (Heavy Traffic)")
      .when(col("avg_speed_mph") < 20, "10-20 mph (Moderate)")
      .when(col("avg_speed_mph") < 30, "20-30 mph (Good Flow)")
      .otherwise("30+ mph (Highway)")
    )
    .groupBy("speed_bucket")
    .agg(
      count("*").alias("trip_count"),
      avg("fare_amount").alias("avg_fare"),
      avg("trip_distance").alias("avg_distance")
    )
  )
```

**Insight:** Understand traffic patterns through average travel speeds.

---

## 9. Weekend vs Weekday Analysis

**Prompt:** "Compare weekend vs weekday trip patterns"

```python
def get_weekend_vs_weekday(spark: SparkSession) -> DataFrame:
  from pyspark.sql.functions import dayofweek, when, col, count, avg
  
  return (spark.read.table("samples.nyctaxi.trips")
    .withColumn("day_type",
      when(dayofweek("tpep_pickup_datetime").isin([1, 7]), "Weekend")
      .otherwise("Weekday")
    )
    .groupBy("day_type")
    .agg(
      count("*").alias("trip_count"),
      avg("fare_amount").alias("avg_fare"),
      avg("trip_distance").alias("avg_distance")
    )
  )
```

**Insight:** Reveals differences in taxi usage between weekdays and weekends.

---

## 10. Late Night vs Rush Hour

**Prompt:** "Compare late night trips vs rush hour trips"

```python
def get_time_period_comparison(spark: SparkSession) -> DataFrame:
  from pyspark.sql.functions import hour, when, col, count, avg
  
  return (spark.read.table("samples.nyctaxi.trips")
    .withColumn("hour", hour("tpep_pickup_datetime"))
    .withColumn("time_period",
      when((col("hour") >= 7) & (col("hour") <= 9), "Morning Rush")
      .when((col("hour") >= 17) & (col("hour") <= 19), "Evening Rush")
      .when((col("hour") >= 22) | (col("hour") <= 4), "Late Night")
      .otherwise("Off-Peak")
    )
    .groupBy("time_period")
    .agg(
      count("*").alias("trip_count"),
      avg("fare_amount").alias("avg_fare"),
      avg("trip_distance").alias("avg_distance")
    )
    .orderBy(col("trip_count").desc())
  )
```

**Insight:** Shows how trip characteristics differ across different times of day.

---

## How to Use These Queries

1. Copy any function into your `main.py` file
2. Update the `main()` function to call your chosen query function
3. Run with `uv run main.py`

Example:
```python
def main():
    get_peak_hours(get_spark()).show(24)  # Show all 24 hours
```

## Tips for Exploration

- Use `.show(n)` to display more rows (default is 20)
- Use `.show(n, truncate=False)` to see full values without truncation
- Chain multiple operations for deeper analysis
- Export results with `.toPandas()` for visualization
- Use `.explain()` to see the query execution plan
