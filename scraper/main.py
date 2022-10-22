from pathlib import Path
from typing import List
from fuzzywuzzy import fuzz
import requests
from bs4 import BeautifulSoup

import utils.utils as utils

data_path = Path(__file__).resolve().parents[0].joinpath('data', 'websites.txt')
urls = []
filter = 'kluczowe informacje dla inwestorow'
words = ['kiid', 'kluczowe informacje']
iterator = 0


def increment():
    global iterator
    iterator = iterator + 1


def extract_kiid_files_from_url(base_url: str, url: str) -> None:
    """
    Extracts & downloads only KIID related pdf files from given url
    :param base_url: base url of webpage
    :param url: some subpage of base_url
    """
    if not utils.check(url):
        return
    try:
        read = requests.get(url)
    except requests.exceptions:
        return
    if not read.ok:
        return
    html_content = read.content
    soup = BeautifulSoup(html_content, "html.parser")

    for link in soup.select("a[href$='.pdf']"):
        str_link = str(link).lower()
        str_link = str_link if str_link.endswith('/') else '/' + str_link
        if any(word in str_link for word in words) or fuzz.ratio(link.text, filter) > 75:
            href = link['href']
            print(href)
            utils.download_pdf(href, str(iterator))
            increment()


def generate_subpages(base_url: str, url: str, depth: int) -> None:
    """
    Generate subpage from given url
    :param base_url: global base url
    :param url: subpage of base_url
    :param depth: how much depth we need (recursive)
    """
    if depth == 0:
        return
    if utils.check(url):
        return
    try:
        response = requests.get(url)
    except requests.exceptions.InvalidURL:
        return
    if not response.ok:
        return
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):
        if link.get('href') is None:
            continue
        if 'http' in link['href']:
            temp = link['href']
        else:
            temp = url + link['href']
        if not temp in urls and temp.find(base_url) != -1:
            urls.append(temp)
            # print(temp)
        generate_subpages(base_url, temp, depth - 1)


def extract_all(sites: List[str], depth: int = 1) -> None:
    sites = utils.stripp(sites)
    for site in sites:
        urls.clear()
        generate_subpages(site, site, depth)
        for url in urls:
            extract_kiid_files_from_url(site, url)


if __name__ == '__main__':
    # sites = ['https://www.caspar.com.pl/']  ### example
    webpages = utils.read_websites_from_file(data_path)
    webpages = [utils.create_url(page) for page in webpages]
    extract_all(webpages, 1)
