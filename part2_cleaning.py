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
## 2.1.3 Identify athletes who haven't been tested in the last 6 months (for your selected metrics)
# ----------------------------------------------------------------------------------------------------------------------
print("\n--- 2.1.3 Athletes NOT tested in last 6 months (selected metrics) ---")

selected_metrics_213 = [
    "Peak Velocity(m/s)",
    "Jump Height(m)",
    "Peak Propulsive Force(N)",
    "System Weight(N)",
    "Propulsive Net Impulse(N.s)",
]

# Build placeholders: %s, %s, ...
placeholders_213 = ",".join(["%s"] * len(selected_metrics_213))

query_not_tested = f"""
SELECT
    playername,
    team,
    MAX(`timestamp`) AS last_test
FROM research_experiment_refactor_test
WHERE metric IN ({placeholders_213})
GROUP BY playername, team
HAVING MAX(`timestamp`) < DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
ORDER BY last_test;
"""

athletes_not_tested_6m = pd.read_sql(
    query_not_tested,
    engine,
    params=tuple(selected_metrics_213)   # tuple, not list (SQLAlchemy quirk)
)

print(athletes_not_tested_6m)

# Optional: save to CSV
athletes_not_tested_6m.to_csv(
    "part2_athletes_not_tested_last_6_months.csv",
    index=False
)
print("\nSaved list to 'part2_athletes_not_tested_last_6_months.csv'")

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
selected_metrics = [
    'Peak Velocity(m/s)',
    'Jump Height(m)',
    'Peak Propulsive Force(N)',
    'System Weight(N)',
    'Propulsive Net Impulse(N.s)'
]

def make_player_wide(player_name, metrics=selected_metrics):
    """
    Returns a wide-format DataFrame for one athlete:
      - one row per timestamp (test session)
      - one column per selected metric
      - missing values left as NaN (can be filled if desired)
    """
    # Build IN (...) list for SQL
    metrics_sql = ",".join(f"'{m}'" for m in metrics)

    query = f"""
        SELECT
            playername,
            `timestamp`,
            metric,
            value
        FROM research_experiment_refactor_test
        WHERE playername = '{player_name}'
          AND metric IN ({metrics_sql})
        ORDER BY `timestamp`;
    """

    df_long = pd.read_sql(query, engine)

    # Pivot from long → wide:
    # index = timestamp, columns = metric, values = value
    df_wide = (
        df_long
        .pivot_table(
            index="timestamp",
            columns="metric",
            values="value",
            aggfunc="mean"      # in case there are duplicates per timestamp/metric
        )
        .reset_index()
        .sort_values("timestamp")
    )

    # Ensure all selected metrics are present as columns
    for m in metrics:
        if m not in df_wide.columns:
            df_wide[m] = pd.NA

    return df_wide


# ---- Test the function on at least 3 different athletes from different teams ----
three_athletes = pd.read_sql("""
    SELECT team, playername
    FROM research_experiment_refactor_test
    GROUP BY team, playername
    ORDER BY team
    LIMIT 3;
""", engine)

print(three_athletes)

test_players = [
    "PLAYER_012",  
    "PLAYER_018",  
    "PLAYER_035"   
]

for p in test_players:
    print(f"\nWide-format data for {p}")
    wide_df = make_player_wide(p)
    print(wide_df.head())   # show first few rows
# ----------------------------
print("\n--- 2.3 Derived Metric: team means, % difference, top/bottom 5 ---")

def derived_metric_for_team(metric_name):
    """
    Computes team mean, percent difference from team mean,
    and identifies top/bottom 5 performers for a given metric.
    """

    # 1) Pull data
    query = """
        SELECT
            team,
            playername,
            `timestamp`,
            value
        FROM research_experiment_refactor_test
        WHERE metric = %s
    """

    # NOTE: params must be tuples, not lists
    df = pd.read_sql(query, engine, params=(metric_name,))

    if df.empty:
        print(f"No rows found for metric: {metric_name}")
        return df, None, None, None

    # Remove null values
    df = df.dropna(subset=["value"])

    # 2) Compute team means
    team_means = (
        df.groupby("team")["value"]
          .mean()
          .reset_index()
          .rename(columns={"value": "team_mean"})
    )

    # Attach team means back to each measurement
    df_detail = df.merge(team_means, on="team", how="left")

    # 3) % difference from team mean
    df_detail["pct_diff_from_team_mean"] = (
        100.0 * (df_detail["value"] - df_detail["team_mean"]) / df_detail["team_mean"]
    )

    # 4) Athlete-level summary
    summary = (
        df_detail.groupby(["team", "playername"])["pct_diff_from_team_mean"]
        .mean()
        .reset_index()
        .rename(columns={"pct_diff_from_team_mean": "avg_pct_diff_from_team"})
    )

    # Optional: z-score within each team
    summary["z_score_within_team"] = (
        summary.groupby("team")["avg_pct_diff_from_team"]
        .transform(lambda x: (x - x.mean()) / x.std(ddof=0))
    )

    # 5) Top & bottom 5 performers per team
    top5 = (
        summary.sort_values(["team", "avg_pct_diff_from_team"], ascending=[True, False])
        .groupby("team")
        .head(5)
    )

    bottom5 = (
        summary.sort_values(["team", "avg_pct_diff_from_team"], ascending=[True, True])
        .groupby("team")
        .head(5)
    )

    return df_detail, summary, top5, bottom5


# ===== Example usage =====
metric_to_use = "Jump Height(m)"

detail, summary, top5_jump, bottom5_jump = derived_metric_for_team(metric_to_use)

print("\nSummary:")
print(summary.head())

print("\nTop 5 performers:")
print(top5_jump)

print("\nBottom 5 performers:")
print(bottom5_jump)
