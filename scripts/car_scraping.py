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
        # Some manufacturers need to add _Cars or other prefixes
        if (self.manufacturer == 'Jaguar' or self.manufacturer == 'Lotus'):
            self.start_url = self.start_url + '_Cars'
        if (self.manufacturer == 'Lincoln' or self.manufacturer == 'Pontiac'):
            self.start_url = self.start_url + '_Motor_Company'
        if (self.manufacturer == 'Mercury'):
            self.start_url = self.start_url + '_(automobile)'
        if (self.manufacturer == 'Pagani'):
            self.start_url = self.start_url + '_(company)'
        if (self.manufacturer == 'McLaren'):
            self.start_url = self.start_url + '_Automotive'
        print(self.start_url)

    def perform_scraping(self):
        # Get the first data from the start url
        start_page = requests.get(self.start_url, headers)
        if (start_page.status_code > 299 or start_page.status_code < 200):
            print('Invalid request for ' + self.start_url + ' status code was ' + start_page.status_code)
            exit
        
        soup = BeautifulSoup(start_page.content, 'html.parser')

        all_links = soup.find_all(lambda tag:tag.name == 'a' and 'title' in tag.attrs)

        # Use a dictionary to ensure links are not repeated
        simple_hash_table = {}
        hash_table_counter = 0

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
                    link_to_add = link.get('href')
                    links_to_lists.append(link_to_add)
        
        # Decide next URL to scrape
        next_url = ''
        if len(links_to_lists) == 0:
            # Need to find a different link to follow
            next_url = self.start_url
        elif len(links_to_lists) > 1:
            # Need to pick one of the links to follow
            random_selection = randrange(len(links_to_lists))
            next_url = self.base_url + links_to_lists[random_selection]
        else:
            # Should have a link to a list of vehicles by the given manufacturer
            next_url = self.base_url + links_to_lists[0]
        
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
                url_to_add = self.base_url + found_link
                # Ensure links are not duplicated
                is_new_link = simple_hash_table.get(url_to_add, -1)
                # Ensure links found build on base url
                if is_new_link == -1:
                    simple_hash_table.update({found_link: hash_table_counter})
                    hash_table_counter += 1
                    if found_link.startswith('/'):
                        possible_car_links.append(url_to_add)
                else:
                    continue
                
        # Explore each potential car link and extract information if a car is found
        link_counter = 0
        cars_found = []
        regex = re.compile('[@_,+!#$%^&*()<>?/|}{~:]')
        for link in possible_car_links:
            # Keep a link limit to avoid long execution time
            if link_counter > 25:
                break
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
        
        # Ready to iterate through the rows of the tables to gather car information
        full_cars_found = []
        for car_table in cars_found:
            # First, get the model of the car
            car_table_title = car_table.find('th', class_='fn').text.strip()

            car_manufacturer = self.manufacturer
            car_model = car_table_title.replace(self.manufacturer, '').replace(' ', '')
            car_assembly_location = ''
            car_years_produced = ''
            car_engine = ''
            car_transmission = ''
            car_weight = ''

            values_found = 2

            # Next, get all the rows and iterate through them
            car_table_rows = car_table.find_all('tr')
            for car_row in car_table_rows:
                if car_row.find('th') and car_row.find('td'):
                    car_row_title = car_row.find('th').text.strip()
                    car_row_data = car_row.find('td').text.strip()

                    # Check the row titles for the data needed to create a new car
                    if 'assembly' in car_row_title.lower():
                        car_assembly_location = car_row_data
                        values_found += 1
                    elif 'production' in car_row_title.lower():
                        car_years_produced = car_row_data
                        values_found += 1
                    elif 'engine' in car_row_title.lower():
                        car_engine = car_row_data
                        values_found += 1
                    elif 'transmission' in car_row_title.lower():
                        car_transmission = car_row_data
                        values_found += 1
                    elif 'weight' in car_row_title.lower():
                        car_weight = car_row_data
                        values_found += 1
                    else:
                        continue
                else:
                    continue

            if values_found == 7:
                print('Fully found a car')
                
                # Clean up the data before creating the car object
                car_assembly_location_final = ''
                car_years_produced_final = ''
                car_engine_final = ''
                car_transmission_final = ''
                car_weight_final = ''
                
                years = car_years_produced.split('[')
                if len(years) > 0:
                    car_years_produced_final = years[0]
                else:
                    car_years_produced_final = car_years_produced
                
                weights = car_weight.split('[')
                if len(weights) > 0:
                    car_weight_final = weights[0]
                else:
                    car_weight_final = car_weight
                
                engines = car_engine.split('[')
                if len(engines) > 0:
                    car_engine_final = engines[0]
                else:
                    car_engine_final = car_engine

                transmissions = car_transmission.split('[')
                if len(transmissions) > 0:
                    car_transmission_final = transmissions[0]
                else:
                    car_transmission_final = car_transmission
                
                locations = car_assembly_location.split('[')
                if len(locations) > 0:
                    car_assembly_location_final = locations[0]
                else:
                    car_assembly_location_final = car_assembly_location

                car_source = self.start_url

                new_car = Car(car_manufacturer, car_model, car_assembly_location_final, car_years_produced_final, car_engine_final, car_transmission_final, car_weight_final, car_source)  
                # Want unique entries in the full_cars_found list
                if full_cars_found.count(new_car) == 0:
                    full_cars_found.append(new_car)
        
        # Done scraping
        return full_cars_found
