import os
from typing import List

import requests
from bs4 import BeautifulSoup

urls = []
pdf_links = []
filters = ['kiid', 'kluczowe', 'inwestycja', 'inwestycyjne', 'inwestor', 'inwestorów', 'dokument']


def check(url: str) -> bool:
    """
    Checks if given url is valid
    """
    if url.find('.pl') != -1:
        if url.find('.pl/') == -1:
            return False
    return True


def extract_kiid_files_from_url(base_url: str, url: str) -> None:
    """
    Extracts only KIID pdf files from given url
    :param base_url: base url of webpage
    :param url: some subpage of base_url
    """
    if not check(url):
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
        if any(filter in str_link for filter in filters):
            href = link['href'] if link["href"].startswith('/') else str('/' + link['href'])
            pdf_links.append(base_url + href)
            print(base_url + href)


def download_pdf(url: str, name: str) -> None:
    """
    Download pdf from given url
    :param url: url
    :param name: name of the file
    """
    response = requests.get(url, stream=True)
    if not response.ok:
        return
    with open(os.getcwd() + f'pdf_documents/pdf_{name}.pdf', 'wb') as f:
        f.write(response.content)


def create_url(website: str) -> str:
    """
    Create valid url from given website
    """
    return f"http://{website}/"


def generate_subpages(base_url: str, url: str, depth: int) -> None:
    """
    Generate subpage from given url
    :param base_url: global base url
    :param url: subpage of base_url
    :param depth: how much depth we need (recursive)
    """
    if depth == 0:
        return
    if check(url):
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
        if link['href'].__contains__('http'):
            temp = link['href']
        else:
            temp = url + link['href']
        if not temp in urls and temp.find(base_url) != -1:
            urls.append(correct_url(temp))
            print(correct_url(temp))
        generate_subpages(base_url, temp, depth - 1)


def stripp(raw: List[str]) -> List[str]:
    """
    Assures that given list is valid
    """
    return list(map(lambda url: url[:-1] if url[-1] == '/' else url, raw))


def extract_all(sites: List[str], depth: int = 1) -> None:
    sites = stripp(sites)
    for site in sites:
        urls.clear()
        generate_subpages(site, site, depth)
        for url in urls:
            extract_kiid_files_from_url(site, url)
    # print(pdf_links)


def download_all_pdfs() -> None:
    i = 0
    for pdf in list(set(pdf_links)):
        download_pdf(pdf, i)
        i += 1


def read_websites_from_file(filepath: str) -> List[str]:
    """
    Reads websites from file
    :param filepath:
    :return:
    """
    with open(filepath, 'r') as f:
        websites = [line[:-1] for line in f.readlines()]
    return websites


if __name__ == '__main__':
    sites = ['https://www.caspar.com.pl/']  ### example
    extract_all(sites, 1)
    download_all_pdfs()
