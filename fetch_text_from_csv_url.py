import requests
import os
from urllib.parse import urlparse
from resiliparse.parse.html import *
from resiliparse.extract.html2text import extract_plain_text
# import jsonlines
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 启动Chrome浏览器
service = Service('/Applications/chromedriver/chromedriver')  # change to your chromedriver path
driver = webdriver.Chrome(executable_path=service.path, options=chrome_options)

def fetch_page_content(url):
    driver.get(url)
    # 等待页面加载完成
    driver.implicitly_wait(5)
    content = driver.page_source
    print(f"finished load page{url}")
    return content



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
    html_content = fetch_page_content(url)
    if html_content:
        plain_text = extract_plain_text(html_content, main_content=False, noscript=True)
        return plain_text
    else:
        return None


def fetch_text_from_csv(input_csv, output_csv):
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
    input_csv = "diverse-pos.csv"
    output_csv = "diverse-pos.csv"

    fetch_text_from_csv(input_csv, output_csv)

