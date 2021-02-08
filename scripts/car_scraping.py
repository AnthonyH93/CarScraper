# Function: Scrape Wikipedia for information about a specific car
# Author: Anthony Hopkins
# Year: 2021

import requests
from bs4 import BeautifulSoup
from .models.car import Car
from random import randrange
import time
import re

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

# Class to describe the car scraper
class CarScraper:
    def __init__(self, manufacturer):
        self.base_url = 'https://en.wikipedia.org'
        self.manufacturer = manufacturer
        self.start_url = ''
    
    def setup_scraping(self):
        self.start_url = self.base_url + '/wiki/' + self.manufacturer
        # Some manufacturers need to add _Cars
        if (self.manufacturer == 'Jaguar' or self.manufacturer == 'Lotus'):
            self.start_url = self.start_url + '_Cars'
        print(self.start_url)

    def perform_scraping(self):
        # Get the first data from the start url
        start_page = requests.get(self.start_url, headers)
        if (start_page.status_code > 299 or start_page.status_code < 200):
            print('Invalid request for ' + self.start_url + ' status code was ' + start_page.status_code)
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
        
        # Decide next URL to scrape
        next_url = ''
        if len(links_to_lists) == 0:
            # Need to find a different link to follow
            next_url = self.start_url
        elif len(links_to_lists) > 1:
            # Need to pick one of the links to follow
            print(len(links_to_lists))
            random_selection = randrange(len(links_to_lists))
            next_url = self.base_url + links_to_lists[random_selection]
        else:
            # Should have a link to a list of vehicles by the given manufacturer
            print(1)
            print(links_to_lists[0])
            next_url = self.base_url + links_to_lists[0]
        
        print(next_url)
        next_page = requests.get(next_url, headers)
        if (next_page.status_code > 299 or next_page.status_code < 200):
            print('Invalid request for ' + next_url + ' status code was ' + next_page.status_code)
            exit
        
        soup = BeautifulSoup(next_page.content, 'html.parser')
        # Get all links which have a title
        all_valid_links = soup.find_all(lambda tag:tag.name == 'a' and 'title' in tag.attrs)

        # Discard all links without the car manufacturer in the title
        possible_car_links = []
        for link in all_valid_links:
            if (self.manufacturer not in link.get('title')):
                continue
            else:
                found_link = link.get('href')
                # Ensure links found build on base url
                if found_link.startswith('/'):
                    possible_car_links.append(self.base_url + found_link)

        print(len(possible_car_links))
        # Explore each potential car link and extract information if a car is found
        link_counter = 0
        cars_found = []
        regex = re.compile('[@_,+!#$%^&*()<>?/|}{~:]')
        for link in possible_car_links:
            # Delay to avoid overloading the server
            time.sleep(0.1)
            print(possible_car_links[link_counter])
            current_page = requests.get(possible_car_links[link_counter], headers)
            link_counter += 1

            # Skip invalid pages (if any exist)
            if (next_page.status_code > 299 or next_page.status_code < 200):
                continue
            # Determine if page contains a car and act accordingly
            else:
                soup = BeautifulSoup(current_page.content, 'html.parser')
                all_tables = soup.find_all('table', class_='infobox hproduct')

                if len(all_tables) > 0:
                    print('Might have found a car')
                    # Look through tables for tables that resemble a car
                    for table in all_tables:
                        if table.find('th', class_='fn'):
                            table_title = table.find('th', class_='fn')
                            if (self.manufacturer not in table_title.text.strip()):
                                continue
                            else:
                                # Add this table to the cars found list if it matches the expected form
                                if regex.search(table_title.text.strip().replace(' ', '')) == None:
                                    cars_found.append(table)
                                    print("Found: " + table_title.text.strip())
                        else:
                            continue
                else:
                    continue

