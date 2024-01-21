#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class CalcalistScraper(BaseScraper):
    _site_url = "https://www.calcalist.co.il/"
    _language = "hebrew"
    _site_name = "calcalist"

    def __init__(self, page_iterator=None, **kwargs):
        super().__init__(page_iterator=page_iterator, **kwargs)

    def _is_error_page(self, html: str) -> bool:
        return "העמוד המבוקש לא נמצא" in html


if __name__ == "__main__":
    scraper = CalcalistScraper()
    for url, article in scraper:
        print(article.description)
        print(article.text)
        break
