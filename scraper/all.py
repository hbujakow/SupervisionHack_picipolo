from typing import List

import requests
from bs4 import BeautifulSoup
from re import search

urls = []
pdf_links = []
filters = ['kiid', 'kluczowe', 'inwestycja', 'inwestycyjne', 'inwestor', 'inwestorów', 'dokument']


def get_base_url(url: str) -> str:
    start = 'h'
    http = '://'
    end = '/'
    base_url = url[url.find(start):url.find('/', url.find(http) + len(http), len(url))]
    return base_url


def extract_kiid_files_from_url(pdf_links: List[str], base_url: str, url: str) -> None:
    read = requests.get(url)
    html_content = read.content
    soup = BeautifulSoup(html_content, "html.parser")
    links = [a for a in soup.select("a[href$='.pdf']")]

    for link in links:
        str_link = str(link).lower()
        str_link = str_link if str_link.endswith('/') else '/' + str_link
        for f in filters:
            if f in str_link:
                href = link['href'] if link["href"].startswith('/') else str('/' + link['href'])
                pdf_links.append(base_url + href)
                break


def generate_subpages(base_url, url, limit):
    if limit == 0:
        return
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # for link in soup.select("a[href$='.html']"):
    for link in soup.find_all("a"):
        if link.get('href') is None:
            continue
        if link['href'].__contains__('http'):
            temp = link['href']
        else:
            temp = url + link['href']
        if not temp in urls and temp.find(base_url)!=-1:
            urls.append(temp)
            # print(temp)
        urls.append(temp)
        generate_subpages(base_url, temp, limit - 1)


def stripp(raw):
    return list(map(lambda url: url[:-1] if url[-1] == '/' else url, raw))


if __name__ == '__main__':
    site = 'http://www.noblefunds.pl'
    generate_subpages(site, site, 1)
    for url in urls:
        base_url = get_base_url(url)
        extract_kiid_files_from_url(pdf_links, base_url, url)
    print(pdf_links)
    print(len(pdf_links))
