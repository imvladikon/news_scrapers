#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from multiprocessing.pool import ThreadPool
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from readability import readability

from news_scrapers.news_fetcher import ALL_FETCHERS, LinkPreviewFetcher
from news_scrapers.news_fetcher.article import Article
from news_scrapers.news_fetcher.html_fetcher import HtmlFetcher
import os
import glob


def get_files(folder, extensions):
    if isinstance(extensions, str):
        extensions = [extensions]
    for extension in extensions:
        for filename in glob.iglob('{}/**/*{}'.format(folder, extension), recursive=True):
            if os.path.isfile(filename):
                yield filename


class BaseScraper:

    def __init__(
        self,
        url_pattern,
        language,
        site_name,
        first_page=1,
        last_page=1,
        page_iterator=None,
        n_threads=1,
        fetcher_kwargs=None,
    ):
        self._first_page = first_page
        self._last_page = last_page
        self.url_pattern = url_pattern
        self.language = language
        self.site_name = site_name
        if page_iterator is None:
            self._page_iterator = self.default_page_iterator
        else:
            self._page_iterator = page_iterator
        self.n_threads = n_threads
        self.fetcher_kwargs = fetcher_kwargs or {}
    @property
    def fetcher(self):
        return HtmlFetcher(**self.fetcher_kwargs)

    def default_page_iterator(self):
        for page_idx in range(self._first_page, self._last_page + 1):
            url = self.url_pattern.format(page_idx)
            html = self.fetcher.fetch(url)
            yield html, url

    def make_readable(self, html: str) -> str:
        doc = readability.Document(html)
        html = doc.summary()
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text().strip()

    def get_page_iterator(self):
        return self._page_iterator(self)

    def _is_error_page(self, html: str) -> bool:
        return False

    def _process_page(self, html_and_url):
        html, url = html_and_url
        article = self.parse_article(html, url)
        if article:
            return article, url
        return None, url

    def __iter__(self):
        n_threads = self.n_threads
        if n_threads == 1:
            for html_and_url in self.get_page_iterator():
                article_and_url = self._process_page(html_and_url)
                if article_and_url[0]:
                    yield article_and_url
        else:
            pool = ThreadPool(n_threads)
            for article_and_url in pool.imap_unordered(
                self._process_page, self.get_page_iterator()
            ):
                if article_and_url[0]:
                    yield article_and_url

    def get_cookies(self, url, headers):
        with requests.Session() as s:
            s.get(url, headers=headers)
        return s.cookies

    @classmethod
    def from_path(cls, path, **kwargs):
        def _iterator(self):
            for file in get_files(path, ".html"):
                file = Path(file)
                html = file.read_text()
                url = self.url_pattern.format(file.stem)
                yield html, url

        return cls(
            page_iterator=_iterator,
            **kwargs
        )

    def fix_page(self, html, url):
        if self._is_error_page(html):
            return None
        soup = BeautifulSoup(html, 'html.parser')
        # canonical_url = soup.find("link", {"rel": "canonical"}).attrs["href"]
        # if canonical_url != url:
        #     return None
        newsletter = soup.select_one(".wrap-newsletter-article-module")
        if newsletter:
            newsletter.decompose()
        comments = soup.select_one(".comments")
        if comments:
            comments.decompose()
        for iframe in soup.find_all("iframe"):
            iframe.decompose()
        read_more = soup.select_one(".read-more")
        if read_more:
            read_more.decompose()
        share = soup.select_one(".share")
        if share:
            share.decompose()
        for img in soup.find_all("img"):
            img.decompose()
        not_for_print = soup.select_one(".not-for-print")
        if not_for_print:
            not_for_print.decompose()
        comments = soup.select_one("#single-post-comments")
        if comments:
            comments.decompose()
        blockquote = soup.select("blockquote")
        if blockquote:
            for block in blockquote:
                block.decompose()
        tweets = soup.select(".twitter-tweet")
        if tweets:
            for tweet in tweets:
                tweet.decompose()
        html = str(soup)
        return html, url

    def parse_article(self, html, url):
        html, url = self.fix_page(html, url)
        if html is None:
            return None

        soup = BeautifulSoup(html, 'html.parser')

        articles = [fetcher().parse(html=html, url=url) for fetcher in ALL_FETCHERS]
        article = Article.combine_all(articles)
        link = soup.find("link", {"rel": "canonical"})
        if link:
            article.canonical_link = link.attrs["href"]
        if not article.text:
            preview = LinkPreviewFetcher().parse(html, url)
            article.text = preview.text
            if not article.text:
                text = soup.select_one(".article-body")
                if text:
                    text = text.get_text()
                    text = "\n".join(s for s in text.split("\n") if s.strip())
                    article.text = text
        article.language = self.language
        article.site_name = self.site_name
        return article
