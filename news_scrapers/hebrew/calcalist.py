#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from readability import readability

from news_scrapers.base_scraper import BaseScraper
from news_scrapers.news_fetcher import ALL_FETCHERS
from news_scrapers.news_fetcher.article import Article
from news_scrapers.news_fetcher.html_fetcher import HtmlFetcher


class CalcalistScraper(BaseScraper):
    def __init__(
        self,
        url_pattern="https://www.calcalist.co.il/world_news/article/{}",
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
            site_name="calcalist",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return "404" in html and "error" in html and "העמוד המבוקש לא נמצא" in html


if __name__ == '__main__':
    scraper = CalcalistScraper()
    for url, article in scraper:
        print(article.description)
        print(article.text)
        break
