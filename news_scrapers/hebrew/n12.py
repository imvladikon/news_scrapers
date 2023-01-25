#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from news_scrapers.base_scraper import BaseScraper


class N12Scraper(BaseScraper):
    def __init__(
            self,
            url_pattern="https://www.mako.co.il/news-military/2023_q1/Article-fc4e43361d9d581026.htm?sCh=31750a2610f26110&pId=173113802",
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
            site_name="mako",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return html is None or (
                    "404" in html and "error" in html and "העמוד המבוקש לא נמצא" in html)


if __name__ == '__main__':
    # url = f"https://www.mako.co.il/news-military/2023_q1/Article-fc4e43361d9d581026.htm?sCh=31750a2610f26110&pId=173113802"
    scraper = N12Scraper()
    for url, article in scraper:
        print(article.description)
        break
