#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Optional

from bs4 import BeautifulSoup

from news_scrapers.news_fetcher.article import Article
from news_scrapers.news_fetcher.html_fetcher import HtmlFetcher
import readability


class BaseArticleFetcher(ABC):
    def __init__(self, n_threads: int = 0, **kwargs):
        self.n_threads = n_threads

    def parse(self, html: str, url: Optional[str] = None) -> Optional[Article]:
        raise NotImplementedError()

    def make_readable(self, html: str) -> str:
        doc = readability.Document(html)
        html = doc.summary()
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text().strip()

    def fetch(self, url: str) -> Optional[Article]:
        html = HtmlFetcher().fetch(url)
        if html:
            return self.parse(html, url)

    def fetch_all(self, urls: Iterable[str], n_threads: int = 0) -> Iterable[Article]:
        results = []
        if self.n_threads == 0:
            for url in urls:
                results.append(self.fetch(url))
        else:
            with ThreadPoolExecutor(max_workers=n_threads) as executor:
                for result in executor.map(self.fetch, urls):
                    if result:
                        results.append(result)
        return results
