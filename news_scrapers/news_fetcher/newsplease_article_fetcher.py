#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from newsplease import NewsPlease

from news_scrapers.news_fetcher.article import Article
from news_scrapers.news_fetcher.base_article_fetcher import BaseArticleFetcher


class NewspleaseArticleFetcher(BaseArticleFetcher):
    def __init__(self, n_threads: int = 0, **kwargs):
        super().__init__(n_threads, **kwargs)
        self._fetcher = NewsPlease

    def parse(self, html: str, url: Optional[str] = None) -> Article:
        if not html:
            return Article.get_empty()
        source_article = self._fetcher.from_html(html)
        text = source_article.maintext
        if not text:
            text = self.make_readable(html)
        return Article(
            url=url or source_article.url,
            title=source_article.title,
            text=text,
            published=None,
            meta_language=source_article.language,
            authors=source_article.authors,
            domain=source_article.source_domain,
            description=source_article.description,
            meta_description=None,
            meta_keywords=None,
            meta_encoding=None,
            tags=None,
        )


if __name__ == '__main__':

    article = NewspleaseArticleFetcher().fetch(
        'https://www.theguardian.com/commentisfree/2022/may/01/republican-midterm-candidates-falling-into-line-trump'
    )
    print(article)
