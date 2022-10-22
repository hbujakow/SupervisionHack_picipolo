import requests
from bs4 import BeautifulSoup

urls = []


def generate_subpages(url, limit):
    if limit == 0:
        return
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.select("a[href$='.html']"):
        if link['href'].__contains__('http'):
            temp = link['href']
        else:
            temp = url + link['href']
        if not temp in urls:
            urls.append(temp)
        urls.append(temp)
        generate_subpages(temp, limit - 1)


if __name__ == '__main__':
    # site = 'http://www.millenniumtfi.pl' # example
    site = 'https://www.franklintempleton.pl' # cookie example
    generate_subpages(site, 1)
    print(len(urls))
    urls = []
    # generate_subpages(site, 2)
    # print(len(urls))
    # print(len(list(set(urls))))
