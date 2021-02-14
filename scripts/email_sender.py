# Function: Send emails about cars found from a certain manufacturer
# Author: Anthony Hopkins
# Year: 2021

import smtplib, ssl
from .models.car import Car
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randrange

class EmailSender:
    def __init__(self, cars_list):
        self.email_to_use = ''
        self.email_password = ''
        self.cars_list = cars_list
        self.emails_list = []
    
    def get_email_login_details(self):
        email_login_file = open('resources/email_setup.txt', 'r')
        email_login_lines = email_login_file.readlines()

        self.email_to_use = email_login_lines[0]
        self.email_password = email_login_lines[1]

    def get_emails(self):
        email_file = open('resources/emails_list.txt', 'r')
        email_file_lines = email_file.readlines()

        for line in email_file_lines:
            self.emails_list.append(line.strip())
    
    def get_email_content(self, car, email_to_send_to):
        email_message = MIMEMultipart("alternative")
        email_message["Subject"] = "Car of the Day from Car Scraper"
        email_message["from"] = self.email_to_use
        email_message["to"] = email_to_send_to

        # Create plain text version and HTML version of message
        text_message = """\
        Hello,

        The car of the day is the {manufacturer} {model}.

        This car was produced from {production}.

        It was built in the following locations:
        {location}

        Key Stats:

        Engine: {engine}
        Transmission: {transmission}
        Curb Weight: {weight}

        Information scraped from: {source}

        From,

        Car Scraper
        """.format(
            manufacturer=car.manufacturer,
            model=car.model,
            production=car.years_produced,
            location=car.assembly_location,
            engine=car.engine,
            transmission=car.transmission,
            weight=car.weight,
            source=car.source
        )

        email_message_text = MIMEText(text_message, "plain")

        email_message.attach(email_message_text)

        return email_message

    def send_emails(self):
        port = 465
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(self.email_to_use, self.email_password)

            # Logged into dev email now, can send emails
            for email in self.emails_list:
                # Pick a random car from the list
                rand_index = randrange(len(self.cars_list))

                email_content = self.get_email_content(self.cars_list[rand_index], email)
                server.sendmail(
                    self.email_to_use, email, email_content.as_string()
                )
    
    def perform_complete_emailing_function(self):
        self.get_emails()
        self.get_email_login_details()
        self.send_emails()