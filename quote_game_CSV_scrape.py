# This program grabs data on every quote from the website http://quotes.toscrape.com/ and creates a guessing game.
# The player has four guesses to determine who said the quote.
# After every incorrect guess, the player receives a hint about the author.

import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter

#all_quotes = []
base_url = "Http://quotes.toscrape.com"


def scrape_quotes():
    all_quotes = []
    url = "/page/1"
    while url: 
        res = requests.get(f"{base_url}{url}")
        print(f"Now scraping {base_url}{url}...")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            all_quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "bio-link": quote.find("a")["href"]
            })
        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
        sleep(1)
    return all_quotes
# print(quote.find(class_="text").get_text())


# Write quotes to CSV file.
def write_quotes(quotes):
    with open("quotes.csv", "w") as file:
        headers = ["text", "author", "bio-link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)

quotes = scrape_quotes()
write_quotes(quotes)