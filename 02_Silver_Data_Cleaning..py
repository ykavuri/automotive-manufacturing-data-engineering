# Databricks notebook source
bronze_df = spark.table("bronze_manufacturing")

print("Total Bronze Records:", bronze_df.count())

display(bronze_df.limit(5))


clean_df = bronze_df.dropDuplicates(["production_id"])

print("Before cleaning:", bronze_df.count())
print("After cleaning:", clean_df.count())


from pyspark.sql.functions import col, sum as spark_sum

clean_df.select([
    spark_sum(col(c).isNull().cast("int")).alias(c)
    for c in clean_df.columns
]).show()

valid_df = clean_df.filter(
    (col("units_produced") > 0) &
    (col("defect_count") >= 0) &
    (col("defect_count") <= col("units_produced"))
)

print("Valid records:", valid_df.count())


valid_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("silver_manufacturing")

print("Silver table saved successfully!")