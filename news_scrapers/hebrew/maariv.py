#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class MaarivScraper(BaseScraper):
    def __init__(
        self,
        url_pattern="https://www.maariv.co.il/news/law/Article-1",
        first_page=1,
        last_page=1000000,
        page_iterator=None,
        **kwargs
    ):

        super().__init__(
            url_pattern=url_pattern,
            first_page=first_page,
            last_page=last_page,
            page_iterator=page_iterator,
            language="hebrew",
            site_name="maariv",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return html is None or (
            "404" in html and "error" in html and "העמוד המבוקש לא נמצא" in html
        )


if __name__ == '__main__':
    scraper = MaarivScraper()
    for url, article in scraper:
        print(article.text)
        break
