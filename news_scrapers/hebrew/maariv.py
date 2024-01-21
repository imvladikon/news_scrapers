#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class MaarivScraper(BaseScraper):
    _site_url = "https://www.maariv.co.il/"
    _language = "hebrew"
    _site_name = "maariv"
    _url_pattern = "https://www.maariv.co.il/news/law/Article-{}"
    _first_page = 1
    _last_page = 1000000

    def __init__(self, page_iterator=None, **kwargs):
        super().__init__(page_iterator=page_iterator, **kwargs)

    def _is_error_page(self, html: str) -> bool:
        return "העמוד המבוקש לא נמצא" in html
