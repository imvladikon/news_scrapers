#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class WeizmannScraper(BaseScraper):
    _site_url = "https://davidson.weizmann.ac.il/"
    _language = "hebrew"
    _site_name = "weizmann"


if __name__ == "__main__":
    scraper = WeizmannScraper()
    for article, url in scraper:
        print(article)
