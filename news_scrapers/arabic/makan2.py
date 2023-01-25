#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from tqdm import tqdm

from preprocessing.scrapers.news_fetcher import ALL_FETCHERS
from preprocessing.scrapers.news_fetcher.article import Article
from preprocessing.scrapers.news_fetcher.html_fetcher import HtmlFetcher


CATEGORIES_PAGES = {
    "https://www.makan.org.il/program/?catid=1760&page={}": 90,
    "https://www.makan.org.il/program/?catid=1761&page={}": 220,
    "https://www.makan.org.il/program/?catid=1762&page={}": 201,
    "https://www.makan.org.il/program/?catid=1763&page={}": 160,
    "https://www.makan.org.il/program/?catid=1764&page={}": 35
}

@lru_cache(maxsize=10240)
def get_html(browser, url, timeout=1000):
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(timeout)
    content = page.content()
    page.close()
    return content


def main():
    fetcher = HtmlFetcher(backend="playwright")

    all_urls = {}


    with open("articles.jsonl", "w") as f_out:
        for category, pages in CATEGORIES_PAGES.items():
            with sync_playwright() as p:
                session = p.chromium.launch(headless=True)
                for page in tqdm(range(1, pages + 1), total=pages):
                    url = category.format(page)
                    html = get_html(session, url)
                    soup = BeautifulSoup(html, 'html.parser')
                    urls = []
                    for node in soup.select(".program_list_link"):
                        url = "https://www.makan.org.il" + node.attrs["href"]
                        urls.append(url)
                    urls = list(set(urls))

                    for url in urls:
                        if url in all_urls:
                            continue
                        try:
                            html = get_html(session, url)
                            articles = [fetcher().parse(html=html, url=url) for fetcher in ALL_FETCHERS]
                            article = Article.combine_all(articles)

                            soup = BeautifulSoup(html, 'html.parser')
                            main_content = []
                            for node in soup.select(".program_content_section"):
                                text = node.get_text().replace(" ", " ")
                                text = "\n".join(
                                s for s in text.split("\n") if s.strip())
                                main_content.append(text)
                            main_content = max(main_content, key=len)
                            article.text = main_content
                            f_out.write(article.to_json() + "\n")
                        except:
                            pass
                        all_urls[url] = True
                session.close()

if __name__ == '__main__':
    main()
