import requests
import os
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime

class BLSDataFetcher:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.download_dir = 'downloaded_data'

    def download_front_page(self, retries=3):
        for i in range(retries):
            response = requests.get(self.base_url, headers=self.headers)
            if response.status_code == 200:
                return response.text
            else:
                time.sleep(2)  # Wait before retrying
        raise Exception(f"Failed to fetch data from {self.base_url} after {retries} attempts")

    def parse_front_page(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        file_data = []
        file_info_pattern = re.compile(r'(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}:\d{2} [APM]{2})\s+([\d,]+) (.+)')

        for line in soup.get_text().split('\n'):
            match = file_info_pattern.search(line)
            if match:
                data = {
                    'update_date': match.group(1),
                    'update_time': match.group(2),
                    'size': match.group(3),
                    'data': match.group(4),
                    'data_link': os.path.join(self.base_url, match.group(4))
                }
                file_data.append(data)

        return file_data