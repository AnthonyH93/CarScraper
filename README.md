# CarScraper

A simple web scraper built with Python utilizing BeautifulSoup.

Scrapes Wikipedia starting from a random car manufacturers main page and following links to try to find unique cars. It gathers relevant information from possible cars that it encounters and selects a random car from this group and emails the details as a "Car of the Day" email.

Built primarily for learning purposes and exposure to Python's powerful web scraping techniques.

## Steps to Run

Python 3 is required to run this program.

### Prerequisites

* In the resources folder create two text files called email_list.txt and email_setup.txt
* Populate the emails_list.txt file with the email addresses which will be emailed by this program (each on a new line)
* Populate the email_setup.txt file wuth the email address and password of the account (each on a new line)
  * This email must be a gmail account and the "Allow less secure apps" setting must be ON (create/use a throwaway account for this)

### Commands

Once the prerequisites are met, simply run the program with the following command from the CarScraper directory:
* python main.py


## Functionality and Limitations

* The web scraper tries to find tables which correspond to a single car and extracts information such as engine, years produced and weight from this table
* If the scraper does not get all the required information from one of these tables, it does not consider a car to have been found
* Due to the nature of Wikipedia pages not being extremely consistent, it is difficult to format this found information in a robust manner
* It would be desireable to try to extract images of the cars and this is something I will revisit in the future
