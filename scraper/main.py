import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

import pdf_reader

raw = ['https://www.aliortfi.com/', 'https://www.amundi.pl/Inwestorzy_indywidualni']


def strip(raw):
    return list(map(lambda url: url[:-1] if url[-1] == '/' else url, raw))


def generate_subpages(url, depth=1):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    return list(set([link['href'] if link['href'].__contains__('http') else url + link['href'] for link in
                     soup.select("a[href$='.html']")]))


def main():
    # urls = strip(raw)
    url = 'http://www.millenniumtfi.pl'

    # print(generate_subpages(url))

    print(pdf_reader.list_all_pdfs(url, url))
    # pdf_reader.download_single_pdf('http://www.millenniumtfi.pl/dl/5796/attachment/70ec21/Komentarz_18.10.2022.pdf')


if __name__ == '__main__':
    main()
