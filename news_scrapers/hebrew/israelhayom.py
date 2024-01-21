#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from news_scrapers.base_scraper import BaseScraper


class IsraelhayomScraper(BaseScraper):
    _site_url = "https://www.israelhayom.co.il/"
    _language = "hebrew"
    _site_name = "israelhayom"
    _first_page = 1
    _last_page = 1000000
    _url_pattern = "https://www.israelhayom.co.il/news/{}"

    def __init__(self, page_iterator=None, **kwargs):

        if kwargs.get("fetcher_kwargs") is None:
            kwargs["fetcher_kwargs"] = {}
        if kwargs["fetcher_kwargs"].get("headers") is None:
            kwargs["fetcher_kwargs"]["headers"] = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "Accept": "application/html+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "host": "www.israelhayom.co.il",
                "Accept-Language": "en-US,en;q=0.5",
                "referer": "https://www.israelhayom.co.il/",
                "Referer-Policy": "strict-origin-when-cross-origin",
                "pragma": "no-cache",
                "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
            }

        super().__init__(page_iterator=page_iterator, **kwargs)

    def _is_error_page(self, html: str) -> bool:
        return "העמוד המבוקש לא נמצא" in html


if __name__ == "__main__":
    scraper = IsraelhayomScraper()
    for url, article in scraper:
        print(article.description)
        print(article.text)
        break
