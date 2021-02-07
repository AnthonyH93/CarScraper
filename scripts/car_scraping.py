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
        # Jaguar is a special case
        if (self.manufacturer == 'Jaguar'):
            self.start_url = self.start_url + '_Cars'
        print(self.start_url)

    def perform_scraping(self):
        # Get the first data from the start url
        start_page = requests.get(self.start_url)
        if (start_page.status_code > 299 or start_page.status_code < 200):
            print('Invalid request for ' +self.start_url + ' status code was ' + start_page.status_code)
            exit
        
        soup = BeautifulSoup(start_page.content, 'html.parser')

        all_links = soup.find_all(lambda tag:tag.name == 'a' and 'title' in tag.attrs)

        links_to_lists = []
        # Check if manufacturer has a list of automobiles
        for link in all_links:
            if 'List' not in link.get('title'):
                continue
            else:
                # Make sure it is a list of vehicles from the manufacturer
                if ((self.manufacturer not in link.get('title')) or (('vehicle' or 'car' or 'auto') not in link.get('title'))):
                    continue 
                else:
                    links_to_lists.append(link.get('href'))
        
        if len(links_to_lists) == 0:
            # Need to find a different link to follow
            print(0)
        elif len(links_to_lists) > 1:
            # Need to pick one of the links to follow
            print(len(links_to_lists))
            print(links_to_lists)
        else:
            # Should have a link to a list of vehicles by the given manufacturer
            print(1)
            print(links_to_lists[0])

