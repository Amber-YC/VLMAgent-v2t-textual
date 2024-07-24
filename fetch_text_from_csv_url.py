import requests
import os
from urllib.parse import urlparse
from resiliparse.parse.html import *
from resiliparse.extract.html2text import extract_plain_text
# import jsonlines
import pandas as pd
from bs4 import BeautifulSoup


def fetch_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def fetch_text_from_url(url):
    html_content = fetch_html(url)
    if html_content:
        plain_text = extract_plain_text(html_content, main_content=False, noscript=True)
        return plain_text
    else:
        return None


def fetch_text_from_csv(input_csv, output_csv, column_id=1):
    df = pd.read_csv(input_csv)
    texts = []
    for url in df['urls']:
        # print(url)
        text = fetch_text_from_url(url)
        texts.append(text if text else "")

    df['Text'] = texts
    df.to_csv(output_csv, index=False)
    print("finish extract text from urls.")


if __name__ == "__main__":
    input_csv = "pos.csv"
    output_csv = "pos.csv"

    fetch_text_from_csv(input_csv, output_csv)

