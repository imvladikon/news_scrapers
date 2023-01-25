#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from newspaper import Article as NewspaperArticle

from news_scrapers.news_fetcher.article import Article
from news_scrapers.news_fetcher.base_article_fetcher import BaseArticleFetcher
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')


class NewspaperArticleFetcher(BaseArticleFetcher):
    def __init__(self, n_threads: int = 0, **kwargs):
        super().__init__(n_threads, **kwargs)
        self._fetcher = NewspaperArticle

    def parse(self, html: str, url: Optional[str] = None) -> Article:
        if not html:
            return Article.get_empty()
        source_article = self._fetcher(url)
        source_article.download(input_html=html)
        source_article.parse()
        source_article.nlp()
        published = (
            source_article.publish_date.strftime("%Y-%m-%d")
            if source_article.publish_date
            else ''
        )
        text = source_article.text
        if not text:
            text = self.make_readable(html)
        return Article(
            url=url or source_article.url,
            title=source_article.title,
            text=text,
            published=published,
            meta_language=source_article.meta_lang,
            authors=source_article.authors,
            domain=None,
            description=source_article.meta_description,
            meta_description=source_article.meta_description,
            meta_keywords=source_article.keywords,
            meta_encoding=None,
            tags=None,
        )


if __name__ == '__main__':

    article = NewspaperArticleFetcher().fetch(
        'https://www.theguardian.com/commentisfree/2022/may/01/republican-midterm-candidates-falling-into-line-trump'
    )
    print(article)
