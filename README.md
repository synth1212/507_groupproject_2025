# 507_groupproject_2025
- This project analyzes longitudinal jump testing data from Stony Brook University Athletics. Using Hawkins force-plate metrics, we explore how force- and velocity-based variables relate to jump height and use those insights to build simple performance-monitoring tools.

## Group Members & Roles:
- Cynthia Chen
    - Role: Team Lead
- Rozelle Thompson 
    - Role: Developer
- Carson Chin
    - Role: Developer
- Kalin Yuen
    - Role: Developer
- Tanveer Kaur
    - Role: Researcher

## Database Overview
The athletics database contains performance data from multiple tracking systems integrated into a single unified table.

### Main Table:
**`research_experiment_refactor_test`** - Single unified table containing all performance metrics from three data sources:
- Hawkins (force plates)
- Kinexon (GPS/accelerometry)
- Vald (strength testing)

### Table Schema:

| Column | Type | Description |
|--------|------|-------------|
| **id** | BIGINT | Unique record identifier (auto-increment) |
| **playername** | VARCHAR(255) | Anonymized player identifier (e.g., PLAYER_001, PLAYER_002) |
| **timestamp** | DATETIME | Date and time of the measurement/session |
| **device** | VARCHAR(50) | Specific device/equipment used for measurement |
| **metric** | VARCHAR(255) | Name of the performance metric being measured |
| **value** | DECIMAL(20,6) | Numeric value of the metric |
| **team** | VARCHAR(255) | Sport/team affiliation (e.g., Football, Soccer, Basketball) |
| **session_type** | VARCHAR(255) | Type of session (e.g., Practice, Game, Training) - only relevant for Kinexon |
| **session_description** | TEXT | Detailed description of the session |
| **function_description** | VARCHAR(255) | Movement or exercise description |
| **data_source** | VARCHAR(50) | Original data source (Hawkins, Kinexon, or Vald) |
| **created_at** | TIMESTAMP | Record creation timestamp |

## Setup Instructions (how to install dependencies)
1. In your machine terminal, create a virtual environment by:

```
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows PowerShell
```

2. Install requirements for this project by running this in the terminal 

```
pip install -r requirements.txt
```
    
* The `requirements.txt` file should consist of:

```python
pandas
sqlalchemy
pymysql
matplotlib.pyplot
seaborn
numpy
```
## Setting Up Your GitHub Repository

1. **Create .gitignore file** (to protect sensitive data):
   
```
# Environment variables and credentials
.env
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb_checkpoints/

# Data files (if you download data locally)
*.csv
!*part4_flagged_athletes.csv # Allow csv files to be staged and commited
*.pkl
*.xlsx
!*_example.csv  # Allow example files

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```
## Database Connection Instructions

1. Copy and paste this code to load your environment variables
   
```
   sql_username = os.getenv('username')
    sql_password = os.getenv('password')
    sql_host = os.getenv('hostname')
    sql_database = os.getenv('database')
```
2. Build the connection URL string with this code:

```
    url_string = f"mysql+pymysql://{sql_username}:{sql_password}@{sql_host}:3306/{sql_database}"
```

3. Create the database engine: 

```
    engine = create_engine("mysql+pymysql://ahistudent:researcher@shtm-fallprev.mysql.database.azure.com:3306/sbu_athletics")
```

## Project Structure Overview

```
507_groupproject_2025/
├── README.md (with group member names, roles, and contributions)
├── references.md (full bibliography in APA or similar format)
├── .env.example (template for database credentials - DO NOT include actual credentials)
├── .gitignore (exclude .env, data files, etc.)
├── part1_exploration.py
├── part1_summary.pdf
├── part1_literature_review.pdf (NEW - your metric selection and lit review)
├── part2_cleaning.py
├── part3_viz_individual.ipynb
├── part3_viz_comparison.ipynb
├── part4_flags.py
├── part4_flagged_athletes.csv
├── part4_flag_justification.pdf (NEW - explain your thresholds)
├── part4_research_synthesis.pdf (NEW - replaces sport_analysis.pdf)
└── final_presentation.pdf
```

## Screenshots (Evidence of Setup)

* Part 1 – Exploration (Kalin Yuen)  
  ![Part 1 – First 10 Rows](screenshots/kalin.png)

* Part 1 – Exploration (Cynthia Chen)
    ![Part 1 – First 10 Rows](screenshots/cynthia.jpg)

* Part 1 – Exploration (Tanveer Kaur)
    ![Part 1 – First 10 Rows](screenshots/tanveer.png)

* Part 1 - Exploration (Rozelle Thompson)
    ![Part 1 – First 10 Rows](screenshots/rozelle.png)

