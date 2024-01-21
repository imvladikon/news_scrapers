#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class N12Scraper(BaseScraper):
    _site_url = "https://www.n12.co.il/"
    _language = "hebrew"
    _site_name = "n12"
    _url_pattern = "https://www.mako.co.il/news-military/2023_q1/Article-fc4e43361d9d581026.htm?sCh=31750a2610f26110&pId=173113802"
    _first_page = 1
    _last_page = 1000000

    def _is_error_page(self, html: str) -> bool:
        return "העמוד המבוקש לא נמצא" in html
