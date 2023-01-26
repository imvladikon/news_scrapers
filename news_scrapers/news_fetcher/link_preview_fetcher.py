#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from news_scrapers.linkpreview import link_preview
from news_scrapers.news_fetcher.article import Article
from news_scrapers.news_fetcher.base_article_fetcher import BaseArticleFetcher


class LinkPreviewFetcher(BaseArticleFetcher):
    def __init__(self, n_threads: int = 0, **kwargs):
        super().__init__(n_threads, **kwargs)

    def parse(self, html: str, url: Optional[str] = None) -> Article:
        if not html:
            return Article.get_empty()

        preview = link_preview(url, html)

        return Article(
            url=url or preview.link,
            title=preview.title,
            text=preview.jsonld.article_body or "",
            published=preview.opengraph.published_time,
            meta_language=None,
            authors=preview.opengraph.author,
            domain=None,
            description=preview.description,
            meta_description=preview.description,
            meta_keywords=None,
            meta_encoding=None,
            tags=None,
        )

