from typing import List
from pathlib import Path

import requests


def download_pdf(url: str, name: str) -> None:
    """
    Download pdf from given url
    :param url: url
    :param name: name of the file
    """
    response = requests.get(url, stream=True)
    if not response.ok:
        return
    with open(Path(__file__).resolve().parents[1].joinpath('data', 'documents', f'pdf{name}.pdf'), 'wb') as f:
        f.write(response.content)


def create_url(website: str) -> str:
    """
    Create valid url from given website
    """
    return f"http://{website}/"


def stripp(raw: List[str]) -> List[str]:
    """
    Assures that given list is valid
    """
    return list(map(lambda url: url[:-1] if url[-1] == '/' else url, raw))


def read_websites_from_file(filepath: str) -> List[str]:
    """
    Reads websites from file
    :param filepath:
    :return:
    """
    with open(filepath, 'r') as f:
        websites = [line[:-1] for line in f.readlines()]
    return websites


def check(url: str) -> bool:
    """
    Checks if given url is valid
    """
    if url.find('.pl') != -1:
        if url.find('.pl/') == -1:
            return False
    return True
