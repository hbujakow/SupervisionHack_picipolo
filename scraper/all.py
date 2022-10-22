from typing import List

import requests
from bs4 import BeautifulSoup

urls = []
pdf_links = []
filters = ['kiid', 'kluczowe', 'inwestycja', 'inwestycyjne', 'inwestor', 'inwestorów', 'dokument']


def get_base_url(url: str) -> str:
    start = 'h'
    http = '://'
    base_url = url[url.find(start):url.find('/', url.find(http) + len(http), len(url))]
    return base_url


def extract_kiid_files_from_url(base_url: str, url: str) -> None:
    try:
        read = requests.get(url)
    except Exception:
        return

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
                print(base_url + href)
                break


def generate_subpages(base_url, url, depth):
    if depth == 0:
        return
    response = requests.get(url)
    if not response.ok:
        return
    soup = BeautifulSoup(response.text, "html.parser")

    # for link in soup.select("a[href$='.html']"):
    for link in soup.find_all("a"):
        if link.get('href') is None:
            continue
        if link['href'].__contains__('http'):
            temp = link['href']
        else:
            temp = url + link['href']
        if not temp in urls and temp.find(base_url) != -1:
            urls.append(temp)
            # print(temp)
        # urls.append(temp)
        generate_subpages(base_url, temp, depth - 1)


def stripp(raw):
    return list(map(lambda url: url[:-1] if url[-1] == '/' else url, raw))

def extract_all(sites, depth=1):
    sites = stripp(sites)
    for site in sites:
        urls.clear()
        generate_subpages(site, site, depth)
        print(urls)
        for url in urls:
            extract_kiid_files_from_url(get_base_url(url), url)


if __name__ == '__main__':
    sites = ['http://www.caspartfi.pl/']
    extract_all(sites, 2)
