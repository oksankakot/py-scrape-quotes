import csv
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List


@dataclass
class Quote:
    text: str
    author: str
    tags: List[str]


def get_quotes(page_url: str) -> List[Quote]:
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    quote_elements = soup.select(".quote")
    quotes = []
    for quote_element in quote_elements:
        text = quote_element.select_one(".text").get_text(strip=True)
        author = quote_element.select_one(".author").get_text(strip=True)
        tag_elements = quote_element.select(".tag")
        tags = [tag_element.get_text(strip=True)
                for tag_element in tag_elements]
        quotes.append(Quote(text, author, tags))
    next_page = soup.select_one(".next > a")
    if next_page is not None:
        quotes.extend(
            get_quotes("https://quotes.toscrape.com" + next_page["href"])
        )
    return quotes


def main(output_csv_path: str) -> None:
    quotes = get_quotes("https://quotes.toscrape.com")
    with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["text", "author", "tags"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for quote in quotes:
            writer.writerow(quote.__dict__)


if __name__ == "__main__":
    main("quotes.csv")
