import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "http://quotes.toscrape.com"

def scrape_quotes():
    all_quotes = []

    page_number = 1
    while True:
        response = requests.get(f"{BASE_URL}/page/{page_number}/")
        soup = BeautifulSoup(response.text, "html.parser")

        quotes = soup.find_all("div", class_="quote")
        if not quotes:
            break

        for quote in quotes:
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]

            quote_data = {
                "tags": tags,
                "author": author,
                "quote": text
            }
            all_quotes.append(quote_data)

        page_number += 1

    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(all_quotes, f, ensure_ascii=False, indent=4)

def scrape_authors():
    authors = []

    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    for author in soup.find_all("div", class_="quote"):
        name = author.find("small", class_="author").text
        description = author.find("span", class_="text").text.split("—")[0].strip()

        author_data = {
            "fullname": name,
            "description": description
        }
        if author_data not in authors:
            authors.append(author_data)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrape_quotes()
    scrape_authors()
