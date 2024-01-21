#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class KanScraper(BaseScraper):
    _site_url = "https://www.kan.org.il/"
    _language = "hebrew"
    _site_name = "kan"
    _url_pattern = "https://www.kan.org.il/item/?itemId={}"
    _first_page = 1
    _last_page = 143831

    def __init__(self, page_iterator=None, **kwargs):
        super().__init__(page_iterator=page_iterator, **kwargs)

    def _is_error_page(self, html: str) -> bool:
        return "הדף שחיפשת כבר לא כאן" in html
