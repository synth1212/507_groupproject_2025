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
    
* The `requirement.txt` file should consist of:

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
├── part1_exploration.py          # Data exploration & quality checks (Part 1)
├── part2_cleaning.py             # Cleaning, long→wide transform, derived metrics (Part 2)
├── part3_visualization.py        # (Optional) Plots/dashboards (if created)
├── part4_flags.py                # Performance monitoring flag system (Part 4)
├── requirements.txt              # Python dependencies
├── test.env / .env               # Local DB credentials (not committed to Git ideally)
├── README.md                     # Project documentation (this file)
└── output/
    ├── part2_missing_values_summary_overall.csv
    ├── part2_wide_format_examples.csv
    └── part4_flagged_athletes.csv
```

## Screenshots (Evidence of Setup)

- Part 1 – Exploration (Kalin Yuen)  
  ![Part 1 – First 10 Rows](screenshots/kalin.png)
