#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from news_scrapers.base_scraper import BaseScraper


class WallaScraper(BaseScraper):
    _site_url = "https://news.walla.co.il/"
    _language = "hebrew"
    _site_name = "walla"
    _url_pattern = "https://news.walla.co.il/item/{}"
    _first_page = 1
    _last_page = 1000000

    def _is_error_page(self, html: str) -> bool:
        return "דף האינטרנט שביקשת לא נמצא" in html

    def parse_article(self, html: str, url: str):
        article = super().parse_article(html, url)
        soup = BeautifulSoup(html, "html.parser")
        article_content = soup.select_one(".article-content")
        if article_content:
            nodes = article_content.select(".article_speakable")
            if nodes:
                paragraphs = [self.make_readable(node.text) for node in nodes]
                article.text = "\n".join(paragraphs)
        return article
