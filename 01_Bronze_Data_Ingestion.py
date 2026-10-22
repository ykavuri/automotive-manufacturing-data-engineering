# Databricks notebook source
data = [
    ("Toyota", "Camry", 150),
    ("Toyota", "RAV4", 200),
    ("Toyota", "Corolla", 175)
]

columns = ["manufacturer", "model", "units_produced"]

df = spark.createDataFrame(data, columns)

display(df)


source_df = spark.table("manufacturing_source")

print("Total records:", source_df.count())

display(source_df.limit(10))

source_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("bronze_manufacturing")

bronze_df = spark.table("bronze_manufacturing")

print("Bronze records:", bronze_df.count())    