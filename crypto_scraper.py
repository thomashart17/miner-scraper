# Crypto Terminal: Crypto Scraper
# Author: Thomas Hart

import bs4
import json
import requests

def get_cryptos():
    site = requests.get("https://www.coingecko.com/?page=1")
    soup = bs4.BeautifulSoup(site.text, "html.parser")
    max_page = 1
    for a in soup.find_all("a", class_="page-link"):
        val = bs4.BeautifulSoup.get_text(a)
        try:
            max_page = max(max_page, int(val))
        except:
            pass
    cryptos = {}
    print("Getting Currencies")
    for i in range(max_page):
        print(f"Loading Page {i+1}/{max_page}")
        site = requests.get(f"https://www.coingecko.com/?page={i+1}")
        soup = bs4.BeautifulSoup(site.text, "html.parser")
        crypto_tags = soup.find_all("a", class_="tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between")
        for crypto in crypto_tags:
            if bs4.BeautifulSoup.get_text(crypto).strip().lower() not in cryptos:
                cryptos[bs4.BeautifulSoup.get_text(crypto).strip().lower()] = crypto["href"].replace("/en/coins/", "")
    return cryptos

def get_symbols():
    site = requests.get("https://www.coingecko.com/?page=1")
    soup = bs4.BeautifulSoup(site.text, "html.parser")
    max_page = 1
    for a in soup.find_all("a", class_="page-link"):
        val = bs4.BeautifulSoup.get_text(a)
        try:
            max_page = max(max_page, int(val))
        except:
            pass
    symbols = {}
    urls = {}
    print("Getting Symbols")
    for i in range(max_page):
        print(f"Loading Page {i+1}/{max_page}")
        site = requests.get(f"https://www.coingecko.com/?page={i+1}")
        soup = bs4.BeautifulSoup(site.text, "html.parser")
        crypto_tags = soup.find_all("a", class_="d-lg-none font-bold tw-w-12")
        for crypto in crypto_tags:
            if bs4.BeautifulSoup.get_text(crypto).strip().replace("$", "") not in symbols:
                symbols[bs4.BeautifulSoup.get_text(crypto).strip().replace("$", "")] = crypto["href"].replace("/en/coins/", "")
                urls[crypto["href"].replace("/en/coins/", "")] = bs4.BeautifulSoup.get_text(crypto).strip().replace("$", "")
    return symbols, urls
    
def update_json():
    with open("data.json", "r") as f:
        data = json.load(f)
    data["cryptos"] = get_cryptos()
    data["symbols"], data["urls"] = get_symbols()
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)