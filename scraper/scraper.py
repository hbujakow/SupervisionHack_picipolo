import requests
from bs4 import BeautifulSoup
from typing import List


def get_base_url(url: str) -> str:
    start = 'h'
    http = '://'
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

def download_pdf(url: str, name: str) -> None:
    response = requests.get(url, stream=True)
    with open(f"pdf_{name}.pdf", 'wb') as f:
        f.write(response.content)
        f.close()


if __name__ == '__main__':
    # urls = ["https://www.tfi.bnpparibas.pl/dokumenty,kluczowe-informacje-dla-inwestorow.html", 
    #     "https://www.pkotfi.pl/dokumenty-do-pobrania/kiid/", 
    #     "https://www.superfund.pl/",
    #     "https://noblefunds.pl/dokumenty-kiid"]
    urls = ['https://noblefunds.pl/dokumenty-kiid']
    pdf_links = []
    filters = ['kiid', 'kluczowe', 'inwestycja', 'inwestycyjne', 'inwestor', 'inwestorów', 'dokument']
    for url in urls:
        base_url = get_base_url(url)
        extract_kiid_files_from_url(pdf_links, base_url, url)
    print(pdf_links)
    print(len(pdf_links))
