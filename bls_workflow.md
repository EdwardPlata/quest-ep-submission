# QuestWorkflow Documentation

## Overview
`QuestWorkflow` is a Python class designed to automate the process of web scraping and data uploading. It fetches data from a specified base URL, processes it, and uploads the results to an AWS S3 bucket.

## Features
- URL Generation: Automatically generate a list of URLs to scrape from a given base URL.
- Data Fetching: Retrieve data from the generated URLs.
- Data Uploading: Process the fetched data and upload it to a specified AWS S3 bucket.

## Requirements
- Python 3
- Libraries: `boto3`, `requests`, `beautifulsoup4`, `pandas`
- An AWS account with S3 access
- `.env` file with AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION)

## Installation
Ensure you have the required libraries installed:
```bash
pip install boto3 requests beautifulsoup4 pandas python-dotenv
```


## Usage

### Setting Up
1. Place your AWS credentials in a `.env` file:
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region
2. Import and initialize the `QuestWorkflow` class with your base URL and bucket name:
```python
from quest_workflow import QuestWorkflow

workflow = QuestWorkflow("http://example.com", "your-s3-bucket-name")
```

### Running the Workflow
Execute the workflow to scrape data and upload it to your S3 bucket:
```python
workflow.run()

## Class Methods
- `generate_urls()`: Returns a list of URLs to scrape based on the base URL.
- `fetch_data(urls)`: Takes a list of URLs and returns the fetched data.
- `fetch_and_upload_data(urls_list)`: Processes and uploads the data from the given URLs to the S3 bucket.
- `run()`: Orchestrates the entire workflow.

## Logging
The class uses Python's `logging` module to log significant events and errors. Configure the logging as per your requirement.
