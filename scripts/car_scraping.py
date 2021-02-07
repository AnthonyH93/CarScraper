# Function: Scrape Wikipedia for information about a specific car
# Author: Anthony Hopkins
# Year: 2021

import requests
from bs4 import BeautifulSoup
from .models.car import Car

# Class to describe the car scraper
class CarScraper:
    def __init__(self, manufacturer):
        self.base_url = 'https://en.wikipedia.org/wiki/'
        self.manufacturer = manufacturer
        self.start_url = ''
    
    def setup_scraping(self):
        self.start_url = self.base_url + self.manufacturer
        print(self.start_url)

    def perform_scraping(self):
        # Get the first data from the start url
        page = requests.get(self.start_url)
        if (page.status_code > 299 or page.status_code < 200):
            print('Invalid request for ' +self.start_url + ' status code was ' + page.status_code)
            exit
        
        soup = BeautifulSoup(page.content, 'html.parser')
