# GitHub API Data Pipeline Project

## Overview

This project is a data pipeline built with Python, PostgreSQL, and dbt using data from the GitHub REST API.

The pipeline collects GitHub user, repository, commit, and issue data, stores it in PostgreSQL, and transforms the raw data into structured tables for analysis and reporting.

The project focuses on:

* API ingestion and pagination
* JSON flattening and transformation
* Incremental-style repository ingestion
* Relational data modeling
* dbt staging and marts
* PostgreSQL data warehousing concepts

---

# Tech Stack

## Languages

* Python
* SQL

## Tools & Frameworks

* PostgreSQL
* dbt
* Jupyter Notebook
* Git / GitHub
* psycopg2
* requests

---

# Architecture

```text
GitHub REST API
        ↓
Python Ingestion Pipeline
        ↓
PostgreSQL Raw Staging Tables
        ↓
dbt Staging Models
        ↓
Fact / Dimension Models
        ↓
Analytics Marts
```

---

# Project Structure

```text
github-pipeline-project/
│
├── github_pipeline.ipynb
├── github_pipeline.html
├── README.md
│
├── src/
│   ├── api_helpers.py
│   ├── config.py
│   ├── db_helpers.py
│   ├── pipeline.py
│   └── transformations.py
│
├── sql/
│   └── 01_create_tables.sql
│
└── github_pipeline_dbt/
    ├── dbt_project.yml
    └── models/
        ├── staging/
        │   ├── stg_users.sql
        │   ├── stg_repos.sql
        │   ├── stg_commits.sql
        │   └── stg_issues.sql
        │
        └── marts/
            ├── dim_users.sql
            ├── dim_users.yml
            ├── dim_repos.sql
            ├── dim_repos.yml
            ├── fact_commits.sql
            ├── fact_commits.yml
            ├── fact_issues.sql
            └── fact_issues.yml

```

---

# Features

## GitHub REST API Ingestion

The pipeline ingests:

* Users
* Repositories
* Commits
* Issues

using authenticated GitHub REST API requests.

The project handles:

* Pagination
* Rate limiting delays
* HTTP error handling
* Incremental repository ingestion
* Nested JSON structures

---

## Data Transformation

Nested GitHub API data is flattened and cleaned for analytics and reporting.

Examples include:

* Commit metadata
* Repository permissions
* Reactions
* Labels
* Assignees
* Milestones

Repeated nested structures are stored as JSONB where appropriate.

---

## PostgreSQL Staging Layer

Raw API data is loaded into PostgreSQL staging tables before transformation.

The staging layer serves as the ingestion boundary between:

* raw API extraction
* downstream dbt transformations

---

## dbt Modeling

dbt is used to:

* clean and standardize staging data
* cast timestamps and normalize fields
* build fact and dimension tables
* create analytics marts
* test data quality

---

# Example Metrics

The marts layer includes repository and commit activity metrics such as:

* Total commits
* Active commit days
* Average commits per active day
* Unique contributors
* Commit activity span
* Issue metrics and engagement statistics

---

# Example Pipeline Output

Example ingestion volumes from a single pipeline run:

```text
Users:   60
Repos:   530
Commits: 7643
Issues:  423
```

Additional incremental repository ingestion for first 60 users ingested:

```text
Repos:   244
Commits: 3659
Issues:  155
```

---

# Notebook Preview

If GitHub has issues rendering the notebook preview, use the HTML export instead:

```text
https://htmlpreview.github.io/?https://github.com/rancy1313/github-pipeline-project/blob/main/github_pipeline.html
```

---

# Future Improvements

Potential future enhancements:

Potential future enhancements:

* Add summary marts such as `repo_activity_summary`
* Load modeled data into a cloud data warehouse such as BigQuery
* Build a Power BI dashboard for repository and issue activity
* Improve incremental ingestion and API retry handling

---

# Learning Objectives

This project was designed to strengthen practical experience with:

* Data engineering workflows
* API ingestion pipelines
* Data modeling
* Incremental loading strategies
* dbt development
* PostgreSQL

---

# Author

Rancel Hernandez
