#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from news_scrapers.base_scraper import BaseScraper


class YnetScraper(BaseScraper):
    _site_url = "https://www.ynet.co.il/"
    _language = "hebrew"
    _site_name = "ynet"

    def _is_error_page(self, html: str) -> bool:
        return "הדף שחיפשת אינו קיים במערכת" in html

    def parse_article(self, html: str, url: str):
        article = super().parse_article(html, url)
        soup = BeautifulSoup(html, "html.parser")
        article_body = soup.select_one("#ArticleBodyComponent")
        if article_body:
            nodes = list(soup.select(".pHeader"))
            if nodes:
                toc = []
                for idx in range(len(nodes)):
                    node = nodes[idx]
                    text = node.get_text().strip()
                    if text:
                        toc.append(self.make_readable(text))
                    node.decompose()
                article.toc = toc
            article.text = self.make_readable(str(article_body))
        return article
