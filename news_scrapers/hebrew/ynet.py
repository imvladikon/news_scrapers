#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from news_scrapers.base_scraper import BaseScraper


class YnetScraper(BaseScraper):
    def __init__(
        self,
        url_pattern="https://www.ynet.co.il/news/article/ry3uldtij",
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
            site_name="ynet",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return html is None or (
            "404" in html and "error" in html and "הדף שחיפשת אינו קיים במערכת" in html
        )

    def parse_article(self, html: str, url: str):
        article = super().parse_article(html, url)
        soup = BeautifulSoup(html, 'html.parser')
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


if __name__ == '__main__':
    # f"https://www.ynet.co.il/news/article/ry3uldtij"
    scraper = YnetScraper()
    for url, article in scraper:
        print(article.text)
        print(article.toc)
        break
