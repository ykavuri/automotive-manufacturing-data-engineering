# Databricks notebook source
silver_df = spark.table("silver_manufacturing")

print("Silver records:", silver_df.count())

display(silver_df.limit(5))

from pyspark.sql.functions import sum

plant_production = silver_df.groupBy("plant").agg(
    sum("units_produced").alias("total_vehicles")
)

display(plant_production)

sorted_production = plant_production.orderBy(
    "total_vehicles",
    ascending=False
)

display(sorted_production)


from pyspark.sql.functions import sum, round

plant_quality = silver_df.groupBy("plant").agg(
    sum("units_produced").alias("total_vehicles"),
    sum("defect_count").alias("total_defects")
)

plant_quality = plant_quality.withColumn(
    "defect_rate",
    round(
        (plant_quality["total_defects"] / plant_quality["total_vehicles"]) * 100,
        2
    )
)

display(plant_quality)

quality_ranking = plant_quality.orderBy(
    "defect_rate",
    ascending=False
)

display(quality_ranking)

plant_quality.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_plant_quality")

print("Gold plant quality table saved successfully!")

model_production = silver_df.groupBy("model").agg(
    sum("units_produced").alias("total_vehicles")
)

model_production = model_production.orderBy(
    "total_vehicles",
    ascending=False
)

display(model_production)


model_production.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_model_production")

print("Gold model production table saved successfully!")


from pyspark.sql.functions import to_date

date_df = silver_df.withColumn(
    "production_date",
    to_date("production_date", "yyyy-MM-dd")
)

date_df.printSchema()

from pyspark.sql.functions import month

monthly_df = date_df.withColumn(
    "production_month",
    month("production_date")
)

display(
    monthly_df.select(
        "production_date",
        "production_month",
        "units_produced"
    ).limit(10)
)

monthly_production = monthly_df.groupBy("production_month").agg(
    sum("units_produced").alias("total_vehicles")
)

monthly_production = monthly_production.orderBy("production_month")

display(monthly_production)

monthly_production.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("gold_monthly_production")

print("Gold monthly production table saved successfully!")