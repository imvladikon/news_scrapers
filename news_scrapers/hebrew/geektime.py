#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from news_scrapers.base_scraper import BaseScraper


class GeektimeScraper(BaseScraper):
    _site_url = "https://www.geektime.co.il/"
    _language = "hebrew"
    _site_name = "geektime"

    def __init__(self, page_iterator=None, **kwargs):
        super().__init__(page_iterator=page_iterator, **kwargs)

    def fix_page(self, html, url):
        html = super().fix_page(html, url)
        if self._is_error_page(html):
            return None
        soup = BeautifulSoup(html, "html.parser")
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


if __name__ == "__main__":
    scraper = GeektimeScraper()
    for url, article in scraper:
        print(article.description)
        print(article.text)
        break
