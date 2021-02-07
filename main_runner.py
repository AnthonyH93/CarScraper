# Function: Script to perform the entire scraping process
# Author: Anthony Hopkins
# Year: 2021

from scripts.car_scraping import CarScraper

car_scraper = CarScraper('Ferrari')

car_scraper.setup_scraping()
car_scraper.perform_scraping()