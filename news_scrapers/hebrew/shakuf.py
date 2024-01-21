#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class ShakufScraper(BaseScraper):
    _site_url = "https://shakuf.co.il/"
    _language = "hebrew"
    _site_name = "shakuf"


if __name__ == '__main__':
    scraper = ShakufScraper()
    for article, url in scraper:
        print(article)
