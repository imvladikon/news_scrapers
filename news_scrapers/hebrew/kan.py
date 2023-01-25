#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from news_scrapers.news_fetcher.html_fetcher import HtmlFetcher
from news_scrapers.base_scraper import BaseScraper


class KanScraper(BaseScraper):
    def __init__(self, first_page=1, last_page=143831, page_iterator=None, **kwargs):

        url_pattern = "https://www.kan.org.il/item/?itemId={}"
        super().__init__(
            url_pattern=url_pattern,
            first_page=first_page,
            last_page=last_page,
            page_iterator=page_iterator,
            language="hebrew",
            site_name="kan",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return "404" in html and "error" in html and "הדף שחיפשת כבר לא כאן" in html

    def default_page_iterator(self):
        for url in self._read_sitemap():
            html = HtmlFetcher().fetch(url)
            yield html, url

    def _read_sitemap(self):
        url = "https://www.kan.org.il/sitemap1.xml"
        html = HtmlFetcher().fetch(url)
        soup = BeautifulSoup(html, "html.parser")
        urls = (n.text for n in soup.select("loc") if "item" in n.text)
        yield from urls


if __name__ == '__main__':
    scraper = KanScraper(n_threads=4)
    for article, url in scraper:
        print(article)
        break
