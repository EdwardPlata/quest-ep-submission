import boto3
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import pandas as pd
import io
from typing import List
import logging

class QuestWorkflow:
    """
    A class to encapsulate the workflow of generating URLs, fetching data from these URLs,
    and uploading the data to an S3 bucket.
    """

    def __init__(self, base_url: str, bucket_name: str):
        """
        Initializes the QuestWorkflowClass with the base URL and the bucket name.

        Parameters:
        base_url (str): The base URL for scraping data.
        bucket_name (str): The name of the S3 bucket where data will be uploaded.
        """
        self.base_url = base_url
        self.bucket_name = bucket_name
        load_dotenv()  # Load environment variables

    def generate_urls(self) -> List[str]:
        """Generates a list of URLs to scrape data from."""
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(self.base_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a')
            urls = [link.get('href') for link in links if link.get('href')]
            return [urljoin(self.base_url, url) for url in urls]
        else:
            logging.error(f"Failed to fetch HTML from {self.base_url}")
            return []

    def fetch_data(self, urls: List[str]) -> dict:
        """Fetches data from a list of URLs."""
        data = {}
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        for url in urls:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data[url] = response.text
            else:
                logging.error(f"Failed to fetch data from {url}")
            time.sleep(1)  # Delay between requests

        return data

    def fetch_and_upload_data(self, urls_list: List[str]) -> None:
        """Fetches data from URLs and uploads it to an S3 bucket."""
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )

        for url in urls_list:
            data = self.fetch_data([url])
            if data:
                for url, content in data.items():
                    dataframe = pd.DataFrame(content.split('\n'))
                    dataframe = dataframe[0].str.split('\t', expand=True)
                    csv_buffer = io.StringIO()
                    dataframe.to_csv(csv_buffer, index=False)
                    s3_key = 'landing-zone/' + url.split('/')[-1].replace('.txt', '.csv')
                    s3.put_object(Body=csv_buffer.getvalue(), Bucket=self.bucket_name, Key=s3_key)
                    logging.info(f"Uploaded dataset from {url} to {self.bucket_name}/{s3_key}")
            else:
                logging.error(f"Failed to fetch data from {url}")

    def run(self):
        """Executes the workflow."""
        urls_list = self.generate_urls()
        if urls_list:
            self.fetch_and_upload_data(urls_list)
        else:
            logging.error("No URLs generated to fetch data.")