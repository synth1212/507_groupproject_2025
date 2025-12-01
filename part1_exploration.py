# Database Connection & Data Exploration


# -------------------
# 1.1 Database Setup
# -------------------


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


# --------------------------------------
# 1.2 Data Quality Assessment Questions
# --------------------------------------


# -------------------------------------------------
# 1. How many unique athletes are in the database?


print("\n--- 1. Unique Athletes ---")
query_unique_athletes = """
SELECT COUNT(DISTINCT playername) AS unique_athletes
FROM research_experiment_refactor_test;
"""
result_unique = pd.read_sql(query_unique_athletes, engine)
print(result_unique)


# -------------------------------------------------------------
# 2. How many different sports/teams are represented?
print("\n--- 2. Number of Teams/Sports ---")
query_teams = f"""
SELECT COUNT(DISTINCT team) AS num_teams
FROM research_experiment_refactor_test;
"""
print(pd.read_sql(query_teams, engine))


# -------------------------------------------------
# 3. What is the date range of available data?
print("\n--- 3. Date Range of Available Data ---")
query_date_range = """
SELECT
    MIN(timestamp) AS earliest_date,
    MAX(timestamp) AS latest_date
FROM research_experiment_refactor_test;
"""
result_date_range = pd.read_sql(query_date_range, engine)
print(result_date_range)


# ------------------------------------------------------------------
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


# ---------------------------------------------------------
# 5. Are there any athletes with missing or invalid names?
print("\n--- 5. Missing or Invalid Player Names ---")
query_missing_names = f"""
SELECT COUNT(*) AS missing_or_invalid_names
FROM research_experiment_refactor_test
WHERE playername IS NULL
   OR playername = ''
   OR playername LIKE 'NULL';
"""
print(pd.read_sql(query_missing_names, engine))


# -----------------------------------------------------------------------
# 6. How many athletes have data from multiple sources (2 or 3 systems)?
print("\n--- 6. Athletes With Data From 2 or More Sources ---")
query_multisource = f"""
SELECT playername,
       COUNT(DISTINCT data_source) AS num_sources
FROM research_experiment_refactor_test
GROUP BY playername
HAVING num_sources >= 2
ORDER BY num_sources DESC;
"""
print(pd.read_sql(query_multisource, engine))


# -------------------------------------------------------------
# Summary Report
# -------------------------------------------------------------


print("\n=== Summary Report ===")
print("Table: research_experiment_refactor_test")


# 1. Unique Athletes
result_unique = pd.read_sql(query_unique_athletes, engine)
print("1. Unique athletes:")
print(result_unique)


# 2. Unique Teams
result_teams = pd.read_sql(query_teams, engine)
print("\n2. Unique teams/sports:")
print(result_teams)


# 3. Date Range
result_date_range = pd.read_sql(query_date_range, engine)
print("\n3. Date range:")
print(result_date_range)


# 4. Data sources
result_sources = pd.read_sql(query_sources, engine)
print("\n4. Data sources:")
print(result_sources)


# 5. Missing or invalid names
result_missing = pd.read_sql(query_missing_names, engine)
print("\n5. Missing or invalid player names:")
print(result_missing)


# 6. Multi-source athletes
result_multisource = pd.read_sql(query_multisource, engine)
print("\n6. Athletes with data from multiple systems:")
print(result_multisource)


# Summary Per Source
query_source_summary = """
SELECT
    data_source,
    COUNT(*) AS record_count,
    MIN(timestamp) AS earliest_date,
    MAX(timestamp) AS latest_date
FROM research_experiment_refactor_test
GROUP BY data_source
ORDER BY record_count DESC;
"""


# -------------------------------------------------------------
# Save Summary CSV
# -------------------------------------------------------------


summary_csv = {
    "Unique Athletes": result_unique.iloc[0,0],
    "Unique Teams": result_teams.iloc[0,0],
    "Date Start": result_date_range.iloc[0,0],
    "Date End": result_date_range.iloc[0,1],
    "Top Source": result_sources.sort_values("record_count", ascending=False).iloc[0,0],
    "Missing/Invalid Names": result_missing.iloc[0,0],
    "Multi-Source Athletes": result_multisource.iloc[0,0],
}


pd.DataFrame([summary_csv]).to_csv("part1_summary.csv", index=False)
print("\n Saved summary CSV: part1_summary.csv")


engine.dispose()


# ------------------------------------
# 1.3 Data Quality Assessment Findings
# ------------------------------------


print("\n--- 1.3 Top 10 Metrics Per Data Source ---")


# Function to get top 10 metrics for a data_source
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
