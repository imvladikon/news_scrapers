#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from news_scrapers.base_scraper import BaseScraper


class MakanScraper(BaseScraper):
    def __init__(
        self,
        url_pattern="https://www.makan.org.il/Item/?itemId={}",
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
            language="arabic",
            site_name="makan",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return (
            "404" in html
            and "error" in html
            and "الصفحة التي تبحث عنها غير موجودة هنا" in html
        )


def main():
    scraper = MakanScraper()
    for url, article in scraper:
        print(article)


if __name__ == '__main__':
    main()
