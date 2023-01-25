#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from news_scrapers.base_scraper import BaseScraper


class GeektimeScraper(BaseScraper):
    def __init__(
        self,
        url_pattern="https://www.geektime.co.il/isaac-itzik-sigron-koch-disruptive-technologies/",
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
            site_name="geektime",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return html is None or (
            "404" in html and "error" in html and "העמוד המבוקש לא נמצא" in html
        )

    def fix_page(self, html, url):
        html = super().fix_page(html, url)
        if self._is_error_page(html):
            return None
        soup = BeautifulSoup(html, 'html.parser')
        # canonical_url = soup.find("link", {"rel": "canonical"}).attrs["href"]
        # if canonical_url != url:
        #     return None
        stop_words = [
            "הפרק המלא מחכה לכם כאן:",
            "כבר הצבעת",
            "לקריאת התקנון",
            "היי, יש לנו עוד הרבה פרקים מעניינים של עוד פודקאסט לסטארטאפים",
        ]
        for stop_word in stop_words:
            for p in soup.find_all("p"):
                if stop_word in p.get_text():
                    p.decompose()
            for h in soup.find_all("h3"):
                if stop_word in h.get_text():
                    h.decompose()
        html = str(soup)
        return html


if __name__ == '__main__':
    scraper = GeektimeScraper()
    for url, article in scraper:
        print(article.description)
        print(article.text)
        break
