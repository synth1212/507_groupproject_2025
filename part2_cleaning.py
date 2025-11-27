# 2. Data Cleaning & Transformation

# --------------------------
# 2.1 Missing Data Analysis
# --------------------------

# -----------------------------------------------------------------------------
## 2.1.1 Identify which of your selected metrics have the most NULL or zero values
# -----------------------------------------------------------------------------
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
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

query_focused = """
SELECT
    metric,
    COUNT(*) as total_records,
    SUM(CASE WHEN value IS NULL THEN 1 ELSE 0 END) as null_count,
    SUM(CASE WHEN value = 0 THEN 1 ELSE 0 END) as zero_count,
    SUM(CASE WHEN value IS NULL OR value = 0 THEN 1 ELSE 0 END) as null_or_zero_count,
    ROUND(100.0 * SUM(CASE WHEN value IS NULL OR value = 0 THEN 1 ELSE 0 END) / COUNT(*), 2) as null_zero_percentage
FROM research_experiment_refactor_test
WHERE metric IN (
    'Peak Velocity(m/s)',
    'Jump Height(m)',
    'Peak Propulsive Force(N)',
    'System Weight(N)',
    'Propulsive Net Impulse(N.s)'
)
GROUP BY metric
ORDER BY null_zero_percentage DESC
"""

df_null_focused =pd.read_sql(query_focused, engine)

print("="*80)
print("NULL/Zero Analysis - Sorted from HIGHEST to LOWEST percentage:")
print("="*80)
print(df_null_focused.to_string(index=False))

### To save to a CSV summary 
missing_summary = df_null_focused.sort_values("null_zero_percentage", ascending=False)

missing_summary.to_csv("part2_missing_values_summary_overall.csv", index=False)
print("\nSaved overall missing values summary to 'part2_missing_values_summary_overall.csv'")

# ----------------------------------------------------------------------------------------------------------------------
## 2.1.2 For each sport/team, calculate what percentage of athletes have at least 5 measurements for your selected metrics
# ----------------------------------------------------------------------------------------------------------------------
print("\n--- 2. Percentage of athletes with >=5 measurements for selected metrics, by team ---")

# our selected metrics
print("\n--- 2. Percentage of athletes with >=5 measurements for selected metrics, by team ---")

query_pct = """
SELECT
    team,
    COUNT(*) AS total_athletes,
    SUM(CASE WHEN n_measurements >= 5 THEN 1 ELSE 0 END) AS athletes_5_plus,
    ROUND(100.0 * SUM(CASE WHEN n_measurements >= 5 THEN 1 ELSE 0 END) / COUNT(*), 2)
        AS pct_athletes_5_plus
FROM (
    SELECT
        team,
        playername,
        COUNT(*) AS n_measurements
    FROM research_experiment_refactor_test
    WHERE metric IN (
        'Peak Velocity(m/s)',
        'Jump Height(m)',
        'Peak Propulsive Force(N)',
        'System Weight(N)',
        'Propulsive Net Impulse(N.s)'
    )
    GROUP BY team, playername
) AS per_athlete
GROUP BY team
ORDER BY team;
"""

result_pct = pd.read_sql(query_pct, engine)
print(result_pct)
# ----------------------------------------------------------------------------------------------------------------------
## 2.1.3 For each sport/team, calculate what percentage of athletes have at least 5 measurements for your selected metrics
# ----------------------------------------------------------------------------------------------------------------------
print("\n--- 2. Percentage of athletes with >=5 measurements for selected metrics, by team ---")

query_pct = """
SELECT
    team,
    COUNT(*) AS total_athletes,
    SUM(CASE WHEN n_measurements >= 5 THEN 1 ELSE 0 END) AS athletes_5_plus,
    ROUND(
        100.0 * SUM(CASE WHEN n_measurements >= 5 THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS pct_athletes_5_plus
FROM (
    SELECT
        team,
        playername,
        COUNT(*) AS n_measurements
    FROM research_experiment_refactor_test
    WHERE metric IN (
        'Peak Velocity(m/s)',
        'Jump Height(m)',
        'Peak Propulsive Force(N)',
        'System Weight(N)',
        'Propulsive Net Impulse(N.s)'
    )
    GROUP BY team, playername
) AS per_athlete
GROUP BY team
ORDER BY team;
"""

result_pct = pd.read_sql(query_pct, engine)
print(result_pct)
# ----------------------------------------------------------------------------------------------------------------------
## 2.1.4 Determine if you have sufficient data to answer your research question
# ----------------------------------------------------------------------------------------------------------------------
dataset_strength_paragraph = """
The SBU Athletics dataset is unusually strong for applied sport science research 
because it combines a large-scale, multi-year sample with consistent longitudinal 
tracking of key biomechanical performance metrics. Most published research on 
jump mechanics is constrained by small sample sizes (10–30 athletes), limited 
testing sessions, or isolated laboratory trials. In contrast, this dataset 
contains over 32,000 jump-related measurements across dozens of teams, with many 
athletes exceeding the five-measurement threshold needed for stable force–time 
analysis. The breadth of the dataset — covering peak force, propulsive impulse, 
peak velocity, system weight, and jump height — allows for integrated modeling 
of mechanical output, neuromuscular performance, and load-based variability.

Additionally, the high frequency and repeated-measures structure of the dataset 
enable evaluation of within-athlete trends across training cycles, competitive 
seasons, and recovery periods. This level of temporal density is rarely available 
in applied settings and provides exceptional power to investigate how force-based 
and velocity-based metrics interact to predict jump height. The diversity of teams 
and athlete groups further enhances generalizability and supports cross-sport 
comparisons. Together, these features make the dataset uniquely valuable for answering 
complex research questions about performance readiness, fatigue, asymmetry, and 
injury risk in elite collegiate populations.
"""
print(dataset_strength_paragraph)

# ----------------------------------
# 2.2 Data Transformation Challenge
# ----------------------------------

# ----------------------------
# 2.3 Create a Derived Metric
# ----------------------------
