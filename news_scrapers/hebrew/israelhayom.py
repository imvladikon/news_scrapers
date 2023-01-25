#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from news_scrapers.base_scraper import BaseScraper


class IsraelhayomScraper(BaseScraper):
    def __init__(
        self,
        url_pattern="https://www.israelhayom.co.il/news/{}",
        first_page=1,
        last_page=1000000,
        page_iterator=None,
        **kwargs
    ):

        super().__init__(
            url_pattern=url_pattern,
            first_page=first_page,
            last_page=last_page,
            page_iterator=page_iterator,
            language="hebrew",
            site_name="israelhayom",
            **kwargs
        )
        self.headers = {
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

    def _read_sitemap(self):
        cookies = self.get_cookies(
            url="https://www.israelhayom.co.il/", headers=self.headers
        )
        for idx in range(1, 123):
            url = f"https://www.israelhayom.co.il/sitemaps/wp-sitemap-posts-post-{idx}.xml"
            text = requests.get(url, headers=self.headers, cookies=cookies).text
            for n in BeautifulSoup(text, "html.parser").select("loc"):
                yield n.text

    def _is_error_page(self, html: str) -> bool:
        return html is None or (
            "404" in html and "error" in html and "העמוד המבוקש לא נמצא" in html
        )

    def default_page_iterator(self):
        cookies = self.get_cookies(
            url="https://www.israelhayom.co.il/", headers=self.headers
        )
        for url in self._read_sitemap():
            with requests.Session() as s:
                html = s.get(url, headers=self.headers, cookies=cookies).text
            if self._is_error_page(html):
                continue
            yield html, url


if __name__ == '__main__':
    scraper = IsraelhayomScraper()
    for url, article in scraper:
        print(article.description)
        print(article.text)
        break
