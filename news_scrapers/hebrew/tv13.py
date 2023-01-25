#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class Tv13Scraper(BaseScraper):
    def __init__(
        self,
        url_pattern="https://13tv.co.il/item/news/economics/nir-barkat-903403129/?pid=62&cid=902992383",
        first_page=974455,
        last_page=974458,
        page_iterator=None,
        **kwargs
    ):
        super().__init__(
            url_pattern=url_pattern,
            first_page=first_page,
            last_page=last_page,
            page_iterator=page_iterator,
            language="hebrew",
            site_name="tv13",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return html is None or (
            "404" in html and "error" in html and "העמוד המבוקש לא נמצא" in html
        )


if __name__ == '__main__':
    scraper = Tv13Scraper()
    for url, article in scraper:
        print(article.description)
        print(article.text)
        break
