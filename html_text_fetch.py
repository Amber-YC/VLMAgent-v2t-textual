import requests
import os
from urllib.parse import urlparse
from resiliparse.parse.html import *
from resiliparse.extract.html2text import extract_plain_text
import jsonlines

# Function to fetch HTML content from a URL
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


def fetch_text(urls, output_dir, jsonl_file):
    text_data = []
    for url in urls:
        html_content = fetch_html(url)
        if html_content:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            path = parsed_url.path.strip("/").replace("/", "-")
            filename = f"{domain}_{path}.html"

            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            plain_text = extract_plain_text(html_content, main_content=False, links=False, skip_elements=['li'], noscript=True) # may ignore key text if main_content=True
            # plain_text = extract_plain_text(html_content, main_content=True)
            print(plain_text)
            text_data.append({
                'url': url,
                'html_filename': filename,
                'plain_text': plain_text
            })
            with jsonlines.open(jsonl_file, 'w') as writer:
                writer.write_all(text_data)
            # print(f"HTML content from {url} saved to {filepath}")
        else:
            print(f"Skipping {url} due to fetch error")


if __name__ == "__main__":
    pos_urls = ["https://support.apple.com/en-gb/guide/mac-help/mchl834d18c2/14.0/mac/14.0",
            "https://support.microsoft.com/en-gb/windows/find-and-open-file-explorer-ef370130-1cca-9dc5-e0df-2f7416fe1cb1"]
    # Directory to save HTML files
    pos_output_dir = "pos_html_files"
    os.makedirs(pos_output_dir, exist_ok=True)
    fetch_text(pos_urls, pos_output_dir, "pos_texts.jsonl")

    neg_urls = ["https://www.youtube.com"]
    # Directory to save HTML files
    neg_output_dir = "neg_html_files"
    os.makedirs(neg_output_dir, exist_ok=True)
    fetch_text(neg_urls, neg_output_dir, "neg_texts.jsonl")

    print("HTML fetching and text saving completed.")
