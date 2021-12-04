import requests
from bs4 import BeautifulSoup

FETCH_PAGE_TIMEOUT = 5.0
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"


def get_page(link: str) -> str:
    return requests.get(
        link, timeout=FETCH_PAGE_TIMEOUT, headers={"User-Agent": UA}
    ).content


def get_page_tree(content: str) -> BeautifulSoup:
    soup = BeautifulSoup(content, "html.parser")
    return soup


def prepare_content(txt: str) -> str:
    return txt.strip("\n").strip()


def find_content(tree: BeautifulSoup) -> str:
    content = tree.find("div", {"class": "resultsearch_text"})
    return prepare_content(content.text).split(":")[-1].split()[0]


def find_status(tree: BeautifulSoup, column: str) -> str:
    for element in tree.find_all("div", {"class": "row_card"}):
        left = element.find("div", {"class": "left"}).text
        if prepare_content(left) == column:
            return prepare_content(element.find("div", {"class": "right"}).text)


def get_info_by_link(link: str) -> str:
    page = get_page(link)
    tree = get_page_tree(page)
    return find_content(tree)


def get_status_by_link(link: str, column: str) -> str:
    page = get_page(link)
    tree = get_page_tree(page)
    return find_status(tree, column)

