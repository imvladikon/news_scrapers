#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from news_scrapers.base_scraper import BaseScraper


class MakanScraper(BaseScraper):
    _url_pattern = "https://www.makan.org.il/Item/?itemId={}"
    _first_page = 417230
    _last_page = 417235
    _language = "arabic"
    _site_name = "makan"
    _site_url = "https://www.makan.org.il/"

    def __init__(self, page_iterator=None, **kwargs):
        super().__init__(page_iterator=page_iterator, **kwargs)

    def _is_error_page(self, html: str) -> bool:
        return "الصفحة التي تبحث عنها غير موجودة هنا" in html
