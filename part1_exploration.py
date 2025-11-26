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

# 5. Are there any athletes with missing or invalid names?

# 6. How many athletes have data from multiple sources (2 or 3 systems)?

