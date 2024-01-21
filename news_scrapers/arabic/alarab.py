#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from string import punctuation

from bs4 import BeautifulSoup

from news_scrapers.base_scraper import BaseScraper


class AlarabScraper(BaseScraper):
    _site_url = "https://www.alarab.co.il/"
    _url_pattern = "https://www.alarab.co.il/Article/{}"
    _first_page = 1083681
    _last_page = 1083681
    _language = "arabic"
    _site_name = "alarab"

    def __init__(self, page_iterator=None, **kwargs):
        super().__init__(page_iterator=page_iterator, **kwargs)

    def _is_error_page(self, html: str) -> bool:
        return "الصفحة التي تبحث عنها غير موجودة هنا" in html

    def _public_date_from(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        node = soup.select_one("#main-content")
        if node is None:
            return None
        node = node.select_one(".crinfo small")
        if node is None:
            return None
        text = node.text.strip()
        # delete text
        for char in text:
            if char in "0123456789/:" + punctuation + " ":
                continue
            text = text.replace(char, "")
        return text.strip(punctuation + " ").strip()

    def parse_article(self, html, url):
        ret = super().parse_article(html, url)
        ret.public_date = self._public_date_from(html, url)
        return ret
