## Strava to BigQuery Data Pipeline
An automated end-to-end ETL pipeline that fetches fitness activities from the Strava API and stores them in Google BigQuery for further analysis.

# Overview
This project was created to practice working with real-world data and to centralize my Strava activities in one place for future analysis.

# Tech Stack

Language: Python 3.10+
Cloud Provider: Google Cloud Platform (GCP)
Data Warehouse: Google BigQuery
Automation: Cloud Scheduler & Cloud Run
API: Strava REST API 
Version Control: Git

# Architecture

Trigger: Google Cloud Scheduler sends HTTP request on a daily basis.
Extraction: A Python script (Cloud Function) authenticates via OAuth 2.0, refreshes tokens, and requests new activities from Strava API.
Transformation: Data is cleaned and flattened into a structured format suitable for BigQuery.
Loading: The processed data is appended to a BigQuery table.

# Key Features

Token Management: Automatic OAuth 2.0 token refresh logic to ensure uninterrupted service.
Incremental Loading: The script is designed to fetch only the latest activities to avoid duplicates.
Serverless: The entire pipeline runs on GCP serverless infrastructure, meaning zero maintenance and minimal cost.

# Future Work (WIP)

Looker Studio - to visualize monthly progress.
Explanatory data analysis - Deep dive into personal metrics to identify patterns in training volume
Clustering activities - Applying Machine Learning to categorize activities based on intensity, heart rate zones or other features.

# How to Run (Optional)

Clone the repo.
Install dependencies: pip install -r requirements.txt
Set up your Strava API credentials in GCP secretmanager
Deploy to GCP using gcloud CLI.
