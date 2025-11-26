# 1.2 Data Quality Assessment Questions 

## Load Libraries and Connect to SQL Database
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

## Load Variables from .env file
load_dotenv('test.env')

## Get SQL Connection Variables
sql_username = os.getenv('username')
sql_password = os.getenv('password')
sql_host = os.getenv('hostname')
sql_database = os.getenv('database')

sql_username

## with SSL off
url_string = f"mysql+pymysql://{sql_username}:{sql_password}@{sql_host}:3306/{sql_database}"

## Create the connection
conn = create_engine(url_string)

engine = create_engine(
     "mysql+pymysql://ahistudent:researcher@shtm-fallprev.mysql.database.azure.com:3306/sbu_athletics"
)

## Sample Query
sql_toexecute = """
select *
from research_experiment_refactor_test
limit 50;
"""

## Execute Query and print results
response = pd.read_sql(sql_toexecute, engine)
print(response)


# 1. How many unique athletes are in the database?
print("\n--- 1. Unique Athletes ---")
query_unique_athletes = """
SELECT COUNT(DISTINCT playername) AS unique_athletes
FROM research_experiment_refactor_test;
"""
result_unique = pd.read_sql(query_unique_athletes, engine)
print(result_unique)

# 2. How many different sports/teams are represented? (Carson)
pdf = pd.read_sql("SELECT * FROM research_experiment_refactor_test LIMIT 5;", engine)
print(pdf.columns)
print(pdf.head())


print("\n--- 2. Different Sports/Teams ---")
query_unique_teams = """
SELECT COUNT(DISTINCT team) AS unique_teams
FROM research_experiment_refactor_test;
"""
result_teams = pd.read_sql(query_unique_teams, engine)
print(result_teams)

# 3. What is the date range of available data?

# 4. Which data source (Hawkins/Kinexon/Vald) has the most records?
print("\n--- 4. Records Per Data Source ---")
query_sources = f"""
SELECT data_source,
       COUNT(*) AS record_count
FROM research_experiment_refactor_test
GROUP BY data_source
ORDER BY record_count DESC;
"""
print(pd.read_sql((query_sources), engine))
# 5. Are there any athletes with missing or invalid names?

# 6. How many athletes have data from multiple sources (2 or 3 systems)?

#1.3 Metric Discovery & Selection

print("\n--- 1.3 Top 10 Metrics Per Data Source ---")

# Helper: function to get top 10 metrics for a data_source
def top10_metrics_for_source(source):
    query = f"""
    SELECT metric,
           COUNT(*) AS metric_count
    FROM research_experiment_refactor_test
    WHERE data_source = '{source}'
    GROUP BY metric
    ORDER BY metric_count DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

# a) Top 10 metrics for each data source
print("\nTop 10 metrics - Hawkins")
top_hawkins = top10_metrics_for_source("hawkins")
print(top_hawkins)

print("\nTop 10 metrics - Kinexon")
top_kinexon = top10_metrics_for_source("kinexon")
print(top_kinexon)

print("\nTop 10 metrics - Vald")
top_vald = top10_metrics_for_source("vald")
print(top_vald)

# b) How many unique metrics exist across all data sources?
print("\n--- Unique Metrics Across All Sources ---")
query_unique_metrics = """
SELECT COUNT(DISTINCT metric) AS unique_metrics
FROM research_experiment_refactor_test;
"""
unique_metrics = pd.read_sql(query_unique_metrics, engine)
print(unique_metrics)

# c) For each data source, show date range and record count for its TOP 10 metrics
print("\n--- Date Range & Record Count for Top 10 Metrics (per source) ---")

def date_range_for_top_metrics(source):
    query = f"""
    SELECT
        metric,
        MIN(`timestamp`) AS first_timestamp,
        MAX(`timestamp`) AS last_timestamp,
        COUNT(*) AS record_count
    FROM research_experiment_refactor_test
    WHERE data_source = '{source}'
      AND metric IN (
          SELECT metric
          FROM research_experiment_refactor_test
          WHERE data_source = '{source}'
          GROUP BY metric
          ORDER BY COUNT(*) DESC
          LIMIT 10
      )
    GROUP BY metric
    ORDER BY record_count DESC;
    """
    return pd.read_sql(query, engine)

print("\nHawkins - Top metrics date range & counts")
print(date_range_for_top_metrics("hawkins"))

print("\nKinexon - Top metrics date range & counts")
print(date_range_for_top_metrics("kinexon"))

print("\nVald - Top metrics date range & counts")
print(date_range_for_top_metrics("vald"))