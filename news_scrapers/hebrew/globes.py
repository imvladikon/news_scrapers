#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class GlobesScraper(BaseScraper):
    def __init__(
        self,
        url_pattern="https://www.globes.co.il/news/article.aspx?did={}",
        first_page=67967,
        last_page=1001436107,
        page_iterator=None,
        **kwargs
    ):
        super().__init__(
            url_pattern=url_pattern,
            first_page=first_page,
            last_page=last_page,
            page_iterator=page_iterator,
            language="hebrew",
            site_name="globes",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return html is None or ("404" in html and "לא נמצא" in html)


if __name__ == '__main__':
    scraper = GlobesScraper()
    for url, article in scraper:
        print(article.description)
        print(article.text)
        break
