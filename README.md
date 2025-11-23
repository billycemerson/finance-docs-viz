# Data Engineering Project: Financial Data Pipeline

## Project Overview

This project is a ETL (Extract, Transform, Load) pipeline that automates the process of extracting financial data from PDF reports, cleaning and transforming it, and loading it into a PostgreSQL database.

Use Case: Extracting bank financial statements from PDF files and storing them in a structured database for analysis.

---

## Project Idea

The pipeline solves a common data engineering challenge: unstructured data in PDFs into structured data in a database.

1. Extract: Automatically scan PDF files and extract tables and metadata
2. Transform: Clean column names, normalize numeric values, and create proper date formats
3. Load: Insert clean data into a database while avoiding duplicates
4. Serving: Use Looker Studio for dashboard

This follows the industry-standard ETL pattern used by data engineers daily.

