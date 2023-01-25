#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class DavarScraper(BaseScraper):
    def __init__(
        self,
        url_pattern="https://davar1.co.il/{}/",
        first_page=417230,
        last_page=417235,
        page_iterator=None,
        **kwargs
    ):
        super().__init__(
            url_pattern=url_pattern,
            first_page=first_page,
            last_page=last_page,
            page_iterator=page_iterator,
            language="hebrew",
            site_name="davar",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return "404" in html and "error" in html


if __name__ == '__main__':
    scraper = DavarScraper()
    for url, article in scraper:
        print(article)
