# 2. Data Cleaning & Transformation

# --------------------------
# 2.1 Missing Data Analysis
# --------------------------

# -----------------------------------------------------------------------------
## 1. Identify which of your selected metrics have the most NULL or zero values
# -----------------------------------------------------------------------------
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

df_null_focused = pd.read_sql(query_focused, engine)

print("="*80)
print("NULL/Zero Analysis - Sorted from HIGHEST to LOWEST percentage:")
print("="*80)
print(df_null_focused.to_string(index=False))

# ----------------------------------------------------------------------------------------------------------------------
## 2. For each sport/team, calculate what percentage of athletes have at least 5 measurements for your selected metrics
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------
# 2.2 Data Transformation Challenge
# ----------------------------------

# ----------------------------
# 2.3 Create a Derived Metric
# ----------------------------
