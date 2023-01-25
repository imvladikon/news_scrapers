#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scrapers.base_scraper import BaseScraper


class MakanScraper(BaseScraper):
    def __init__(
        self,
        url_pattern="https://www.makan.org.il/Item/?itemId={}",
        first_page=1,
        last_page=1000000,
        page_iterator=None,
    ):
        super().__init__(
            url_pattern=url_pattern,
            first_page=first_page,
            last_page=last_page,
            page_iterator=page_iterator,
            language="arabic",
            site_name="makan",
        )

    def _is_error_page(self, html: str) -> bool:
        return (
            "404" in html
            and "error" in html
            and "الصفحة التي تبحث عنها غير موجودة هنا" in html
        )

    def __iter__(self):
        # TODO: get list news from twitter
        for page in range(self._first_page, self._last_page + 1):
            url = f"https://www.makan.org.il/Item/?itemId={page}"
            html = self.get_one_page(url)
            if html:
                article = self.parse_article(html)
                if article:
                    yield url, article


def main():
    scraper = MakanScraper()
    for url, article in scraper:
        print(article)


if __name__ == '__main__':
    main()
