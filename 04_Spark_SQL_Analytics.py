# Databricks notebook source
# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM gold_plant_quality;
# MAGIC
# MAGIC SELECT
# MAGIC plant,
# MAGIC total_vehicles,
# MAGIC total_defects,
# MAGIC defect_rate
# MAGIC FROM gold_plant_quality
# MAGIC WHERE defect_rate > 3.80
# MAGIC ORDER BY defect_rate DESC;
# MAGIC
# MAGIC SELECT
# MAGIC     SUM(total_vehicles) AS total_vehicles_produced,
# MAGIC     SUM(total_defects) AS total_defects,
# MAGIC     ROUND(
# MAGIC         SUM(total_defects) * 100.0 / SUM(total_vehicles),
# MAGIC         2
# MAGIC     ) AS overall_defect_rate
# MAGIC FROM gold_plant_quality;
# MAGIC
# MAGIC
# MAGIC
# MAGIC CREATE OR REPLACE TABLE gold_overall_kpis
# MAGIC USING DELTA
# MAGIC AS
# MAGIC SELECT
# MAGIC     SUM(total_vehicles) AS total_vehicles_produced,
# MAGIC     SUM(total_defects) AS total_defects,
# MAGIC     ROUND(
# MAGIC         SUM(total_defects) * 100.0 / SUM(total_vehicles),
# MAGIC         2
# MAGIC     ) AS overall_defect_rate
# MAGIC FROM gold_plant_quality;
# MAGIC