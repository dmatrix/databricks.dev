# Vibe Coding Prompts for NYC Taxi Dataset

This document contains prompts for generating interesting queries to analyze the `samples.nyctaxi.trips` dataset. Each prompt is designed to be used with AI code generation tools to create PySpark DataFrame transformations.

**Usage:** Copy a prompt and use it to generate code that will be added to `src/dbconnect_nyc_example/data.py` and called from `src/main.py`.

---

## 1. Average Fare Per Mile

**Prompt:** "Create a function `get_taxis_with_fare_per_mile` that returns NYC taxi trips with average fare per mile calculated. Handle zero-distance trips by setting their fare per mile to None. Use try_divide funciton for division, compute values rounding up to 2 decimal places. Order results by fare per mile descending."

**Expected Output:**
- New column: `average_fare_per_mile` (fare_amount / trip_distance)
- Zero-distance trips should have None for fare per mile
- Results ordered by fare per mile (highest first)
- All original columns preserved

**Insight:** Shows cost efficiency of trips - short trips typically have higher per-mile rates due to base fares and minimum charges.

---

## 2. Busiest Pickup Locations

**Prompt:** "Create a function `get_busiest_pickup_locations` that finds which zip codes have the most pickups."

**Expected Output:**
- Group by: `pickup_zip`
- Aggregate: count of trips as `trip_count`
- Order by: trip count descending (busiest first)

**Insight:** Identifies the most popular pickup locations in NYC - useful for understanding demand patterns.

---

## 3. Peak Hours Analysis

**Prompt:** "Create a function `get_peak_hours` that shows the busiest hours of the day with average fare and distance."

**Expected Output:**
- Extract hour from `tpep_pickup_datetime`
- Group by: hour of day (0-23)
- Aggregates: trip count, average fare, average distance
- Order by: hour (chronological)

**Insight:** Reveals patterns in taxi usage throughout the day - useful for understanding demand cycles and optimal driver scheduling.

---

## 4. Most Popular Routes

**Prompt:** "Create a function `get_popular_routes` that finds the most common pickup-dropoff route combinations."

**Expected Output:**
- Group by: `pickup_zip` and `dropoff_zip`
- Aggregates: trip count, average fare, average distance for each route
- Order by: trip count descending (most popular first)

**Insight:** Shows the most traveled routes - could inform driver positioning strategies and demand forecasting.

---

## 5. Trip Distance Distribution

**Prompt:** "Create a function `get_trip_distance_buckets` that analyzes trips by distance buckets: 0-1, 1-3, 3-5, 5-10, and 10+ miles."

**Expected Output:**
- New column: `distance_bucket` with ranges (0-1 miles, 1-3 miles, 3-5 miles, 5-10 miles, 10+ miles)
- Group by: distance bucket
- Aggregates: trip count, average fare per bucket
- Order by: trip count

**Insight:** Understand the distribution of trip lengths and their relationship to fares - most trips are short urban rides.

---

## 6. Day of Week Patterns

**Prompt:** "Create a function `get_day_of_week_patterns` that shows how trips vary by day of the week."

**Expected Output:**
- Extract day of week from `tpep_pickup_datetime` (1=Sunday, 7=Saturday)
- Group by: day of week
- Aggregates: trip count, average fare, average distance
- Order by: day of week (chronological)

**Insight:** Identify weekday vs weekend patterns in taxi usage - typically more commuter traffic on weekdays, leisure on weekends.

---

## 7. Trip Duration Analysis

**Prompt:** "Create a function `get_trip_duration_analysis` that calculates trip durations in minutes and groups them into time buckets: 0-10, 10-20, 20-30, and 30+ minutes."

**Expected Output:**
- Calculate duration_minutes from pickup to dropoff timestamps
- Filter out negative or zero durations
- Create duration buckets: 0-10 min, 10-20 min, 20-30 min, 30+ min
- Group by: duration bucket
- Aggregates: trip count, average fare, average distance

**Insight:** Understand trip duration patterns and how they correlate with distance and fare - helps identify traffic conditions.

---

## 8. Expensive vs Cheap Trips

**Prompt:** "Create a function `get_fare_comparison` that compares characteristics of high-fare vs low-fare trips using quartiles to categorize them."

**Expected Output:**
- Calculate 25th percentile (Q1) and 75th percentile (Q3) of fare amounts
- Categorize trips: Low (below Q1), Medium (Q1-Q3), High (above Q3)
- Group by: fare category
- Aggregates: trip count, average distance, average fare

**Insight:** Reveals what distinguishes expensive trips from cheap ones - typically longer distances or premium time periods.

---

## 9. Speed Analysis

**Prompt:** "Create a function `get_speed_analysis` that calculates average speed in mph for trips and identifies traffic patterns."

**Expected Output:**
- Calculate duration in hours from timestamps
- Calculate average speed: distance / duration_hours
- Filter: positive durations and distances, speed < 100 mph (remove outliers)
- Create speed buckets: 0-10 mph (Heavy Traffic), 10-20 mph (Moderate), 20-30 mph (Good Flow), 30+ mph (Highway)
- Group by: speed bucket
- Aggregates: trip count, average fare, average distance

**Insight:** Understand traffic patterns through average travel speeds - reveals congestion times and highway vs city driving.

---

## 10. Weekend vs Weekday Analysis

**Prompt:** "Create a function `get_weekend_vs_weekday` that compares weekend vs weekday trip patterns."

**Expected Output:**
- Extract day of week from pickup datetime
- Create day_type: Weekend (Sunday=1, Saturday=7) or Weekday (all others)
- Group by: day_type
- Aggregates: trip count, average fare, average distance

**Insight:** Reveals differences in taxi usage between weekdays and weekends - commuter vs leisure patterns.

---

## 11. Late Night vs Rush Hour

**Prompt:** "Create a function `get_time_period_comparison` that compares trips across different time periods: morning rush, evening rush, late night, and off-peak."

**Expected Output:**
- Extract hour from pickup datetime
- Create time_period categories:
  - Morning Rush: 7-9 AM
  - Evening Rush: 5-7 PM
  - Late Night: 10 PM - 4 AM
  - Off-Peak: all other times
- Group by: time_period
- Aggregates: trip count, average fare, average distance
- Order by: trip count descending

**Insight:** Shows how trip characteristics differ across different times of day - rush hour = shorter trips, late night = longer distances.

---

## 12. Hourly Revenue Potential

**Prompt:** "Create a function `get_hourly_revenue_potential` that calculates potential hourly revenue by combining trip frequency and average fares."

**Expected Output:**
- Extract hour from pickup datetime
- Group by: hour
- Aggregates:
  - trip_count: number of trips per hour
  - avg_fare: average fare per hour
  - total_revenue_potential: trip_count × avg_fare (rounded to 2 decimals)
- Order by: total revenue potential descending

**Insight:** Identifies the most profitable hours for drivers by combining trip volume with average fares - helps optimize driver schedules for maximum earnings.

---

## How to Use These Prompts

### Step 1: Choose a Prompt
Select any prompt from above that interests you.

### Step 2: Generate the Code
Use the prompt with your AI assistant to generate:
1. The function implementation in `src/dbconnect_nyc_example/data.py`
2. Update `src/main.py` to call your new function
3. Create pytest tests following the testing-rules (2 tests max per function)

### Step 3: Run and Verify
```bash
# Run the implementation
uv run python src/main.py

# Run the tests
uv run pytest tests/test_data.py -v
```

## Tips for Better Prompts

- Start with "Create a function `function_name`..." for clarity
- Specify the expected output structure (columns, aggregations, ordering)
- Mention edge cases that need handling (null values, zeros, outliers)
- Request proper docstrings following Google style format
- Ask for type hints on function signatures

## Display Tips

- Use `.show(n)` to display more rows (default is 20)
- Use `.show(n, truncate=False)` to see full values without truncation
- Use `.toPandas()` for visualization in notebooks
- Use `.explain()` to see the query execution plan
