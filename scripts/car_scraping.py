# Function: Scrape Wikipedia for information about a specific car
# Author: Anthony Hopkins
# Year: 2021

import requests
from bs4 import BeautifulSoup

URL = 'https://en.wikipedia.org/wiki/Lamborghini_Jalpa'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')