# pip install pymysql sqlalchemy pandas python-dotenv

import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv ## Load Libraries and Connect to SQL Database
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
engine = create_engine("mysql+pymysql://ahistudent:researcher@shtm-fallprev.mysql.database.azure.com:3306/sbu_athletics")

""" Your Task:
1. Based on your literature review, define 2-3 clinically/performance-relevant thresholds:
    * Examples: metric declined by X% compared to baseline
    * Metric below/above published risk threshold
    * Athlete hasn't been tested in >30 days
    * Left/right asymmetry if using bilateral metrics
    * Deviation from team norms
2. Justify your thresholds using evidence from your literature review
3. Create a script that identifies athletes meeting your flag criteria
4. Output a CSV with: playername, team, flag reason, metric value, last test date
"""

# -------------------------------------------
# Threshold (based on research literature)
# -------------------------------------------
# threshold 1: women jump height
women_jump_height_threshold = 0.30 # meters

# threshold 2: women peak propulsive force
women_peak_propulsive_force_threshold = 1200 # newtons

print("Based on research literature for female collegiate athletes:")
print(f"Jump height < {women_jump_height_threshold} m = low explosive capacity")
print(f"Peak propulsive force < {women_peak_propulsive_force_threshold} N = low force production")

# load 2 metrics jump height & peak propulsive force
metrics = ("Jump Height(m)", "Peak Propulsive Force(N)")

query = f"""
SELECT
    playername,
    team,
    metric,
    value,
    timestamp
FROM research_experiment_refactor_test
WHERE metric IN {metrics}
"""

initial_df = pd.read_sql(query, engine)
initial_df.head()

# create a wide layout to rename table column names as well
df = initial_df.pivot_table( # this is also so we can see both test in on table
    index=["playername", "team", "timestamp"],
    columns="metric",
    values="value"
).reset_index()

df.head()

# get most recent test result of players
idx_recent = df.groupby(["playername", "team"])["timestamp"].idxmax()
recent_tests = df.loc[idx_recent].copy()

recent_tests.head()

flags = []

for _, row in recent_tests.iterrows():

    name = row["playername"]
    team = row["team"]
    test_date = row["timestamp"]

    # ------ JUMP HEIGHT THRESHOLD ------
    if pd.notna(row["Jump Height(m)"]):
        if row["Jump Height(m)"] < women_jump_height_threshold:
            flags.append({
                "playername": name,
                "team": team,
                "flag_reason": "Jump Height < 0.30 m (below performance standard)",
                "metric": "Jump Height(m)",
                "metric_value": row["Jump Height(m)"],
                "last_test_date": test_date
            })

    # ------ PEAK PROPULSIVE FORCE THRESHOLD ------
    if pd.notna(row["Peak Propulsive Force(N)"]):
        if row["Peak Propulsive Force(N)"] < women_peak_propulsive_force_threshold:
            flags.append({
                "playername": name,
                "team": team,
                "flag_reason": "Peak Propulsive Force < 1200 N (below performance standard)",
                "metric": "Peak Propulsive Force(N)",
                "metric_value": row["Peak Propulsive Force(N)"],
                "last_test_date": test_date
            })

flags_df = pd.DataFrame(flags)
flags_df

# save to csv
flags_df.to_csv("part4_flagged_athletes.csv", index=False)

print("Saved to part4_flagged_athletes.csv")
flags_df