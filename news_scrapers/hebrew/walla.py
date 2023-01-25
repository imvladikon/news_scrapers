#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from news_scrapers.base_scraper import BaseScraper


class WallaScraper(BaseScraper):
    def __init__(
        self,
        url_pattern="https://news.walla.co.il/item/{page}",
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
            site_name="walla",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return html is None or (
            "404" in html and "error" in html and "דף האינטרנט שביקשת לא נמצא" in html
        )

    def parse_article(self, html: str, url: str):
        article = super().parse_article(html, url)
        soup = BeautifulSoup(html, 'html.parser')
        article_content = soup.select_one(".article-content")
        if article_content:
            nodes = article_content.select(".article_speakable")
            if nodes:
                paragraphs = [self.make_readable(node.text) for node in nodes]
                article.text = "\n".join(paragraphs)
        return article


if __name__ == '__main__':
    scraper = WallaScraper()
    for url, article in scraper:
        print(url)
        print(article.text)
        break
