#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class AljazeeraScraper(BaseScraper):
    _site_url = "https://www.aljazeera.net/"
    _language = "arabic"
    _site_name = "aljazeera"

    def __init__(self, page_iterator=None, **kwargs):
        super().__init__(page_iterator=page_iterator, **kwargs)

    def _is_error_page(self, html: str) -> bool:
        return "الصفحة التي تبحث عنها غير موجودة هنا" in html


if __name__ == "__main__":
    from tqdm import tqdm

    scraper = AljazeeraScraper()

    for article, url in tqdm(scraper):
        json_str = article.to_json()
