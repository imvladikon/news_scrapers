#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class GlobesScraper(BaseScraper):
    _site_url = "https://www.globes.co.il/"
    _language = "hebrew"
    _site_name = "globes"
    _url_pattern = "https://www.globes.co.il/news/article.aspx?did={}"
    _first_page = 67967
    _last_page = 1001436107

    def __init__(self, page_iterator=None, **kwargs):
        super().__init__(page_iterator=page_iterator, **kwargs)

    def _is_error_page(self, html: str) -> bool:
        return "לא נמצא" in html


if __name__ == "__main__":
    scraper = GlobesScraper()
    for url, article in scraper:
        print(article.description)
        print(article.text)
        break
