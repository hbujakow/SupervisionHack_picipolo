import os
import requests
from pathlib import Path
from bs4 import BeautifulSoup

folder_location = os.getcwd()


def list_all_pdfs(base_url, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return list(set(list(base_url + link['href'] for link in soup.select("a[href$='.pdf']"))))


def download_single_pdf(link):
    filename = Path('test.pdf')
    response = requests.get(link)
    filename.write_bytes(response.content)
    # response = requests.get(link, stream=True)
    # print(response.text)
    # filename = os.path.join(folder_location, 'test.pdf')
    # with open(filename, 'wb') as f:
    #     f.write(response)


def main():
    base_url = 'https://www.millenniumtfi.pl'
    some_subpage = 'https://www.millenniumtfi.pl/dokumenty.html'

    print(list_all_pdfs(base_url, some_subpage))


if __name__ == '__main__':
    main()
