#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class DavarScraper(BaseScraper):
    _site_url = "https://davar1.co.il/"
    _language = "hebrew"
    _site_name = "davar"

    def __init__(self, page_iterator=None, **kwargs):
        super().__init__(page_iterator=page_iterator, **kwargs)


if __name__ == "__main__":
    scraper = DavarScraper()
    for url, article in scraper:
        print(article)
