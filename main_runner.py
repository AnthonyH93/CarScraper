# Function: Script to perform the entire scraping process
# Author: Anthony Hopkins
# Year: 2021

from scripts.car_scraping import CarScraper
from random import randrange

# Choose a random car manufacturer from the list
car_manufacturers_file = open('resources/car_manufacturers.txt', 'r')
car_manufacturers_lines = car_manufacturers_file.readlines()

car_manufacturers = []

line_counter = 0
for line in car_manufacturers_lines:
    line_counter += 1
    car_manufacturers.append(line.strip())

random_number = randrange(line_counter)
random_manufacturer = car_manufacturers[random_number]

car_scraper = CarScraper(random_manufacturer)

car_scraper.setup_scraping()
car_scraper.perform_scraping()