# Databricks notebook source
import random
import csv
from datetime import datetime, timedelta

random.seed(42)

plants = ["Kentucky", "Texas", "Indiana", "Mississippi"]
models = ["Camry", "RAV4", "Corolla", "Highlander", "Tacoma"]

records = []

for i in range(10000):
    production_date = datetime(2026, 1, 1) + timedelta(
        days=random.randint(0, 280)
    )

    units = random.randint(50, 300)
    defects = random.randint(0, int(units * 0.08))

    records.append((
        f"P{i+1:05d}",
        production_date.strftime("%Y-%m-%d"),
        random.choice(plants),
        random.choice(models),
        units,
        defects
    ))

columns = [
    "production_id",
    "production_date",
    "plant",
    "model",
    "units_produced",
    "defect_count"
]

df = spark.createDataFrame(records, columns)

display(df.limit(10))

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("manufacturing_source")









