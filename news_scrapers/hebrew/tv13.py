#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class Tv13Scraper(BaseScraper):
    _site_url = "https://13tv.co.il/"
    _language = "hebrew"
    _site_name = "tv13"
    _url_pattern = "https://13tv.co.il/item/news/economics/nir-barkat-903403129/?pid=62&cid=902992383"
    _first_page = 974455
    _last_page = 974458

    def _is_error_page(self, html: str) -> bool:
        return "העמוד המבוקש לא נמצא" in html
