import pandas as pd
import requests
import os
import time
import matplotlib.pyplot as plt
import os.path
import json

class DataDownloader:
    def __init__(self, url, cache_timeout=600):
        self.url = url
        self.cache_timeout = cache_timeout
        self.cache_file = 'data.json'
    
    def is_cache_valid(self):
        if not os.path.exists(self.cache_file):
            return False
        cache_age = time.time() - os.stat(self.cache_file).st_mtime
        return cache_age < self.cache_timeout
    
    def download_data(self):
        response = requests.get(self.url)
        with open(self.cache_file, 'w') as f:
            f.write(response.text)
    
    def get_data(self):
        if not self.is_cache_valid():
            self.download_data()
        with open(self.cache_file, 'r') as f:
            data = f.read()
            return data

class DataAnalyzer:
    def __init__(self, data):
        self.df = pd.DataFrame(json.loads(data))
    
    def analyze_data(self):
        grouped = self.df.groupby('candidate_party').agg({'list_votes': ['sum', 'mean', 'median']})
        grouped.columns = ['total_votes', 'mean_votes', 'median_votes']
        return grouped
    
    def plot_data(self, grouped):
        ax = grouped.plot(kind="bar", y="total_votes", legend=False)
        ax.set_ylabel("Total Votes")
        ax.set_xlabel("Party")
        ax.set_title("Total Votes by Party")
        x_pos = [i for i, _ in enumerate(grouped.index)]
        plt.xticks(x_pos, grouped.index, rotation=45, ha="right")
        plt.tight_layout()
        plt.show()

downloader = DataDownloader('https://abstimmungen.gr.ch/election/grw-2022-1809/data-json')
analyzer = DataAnalyzer(downloader.get_data())
grouped_data = analyzer.analyze_data()
print(grouped_data)
analyzer.plot_data(grouped_data)