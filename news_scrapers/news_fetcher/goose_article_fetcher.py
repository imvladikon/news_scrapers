#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from goose3 import Goose

from news_scrapers.news_fetcher.article import Article
from news_scrapers.news_fetcher.base_article_fetcher import BaseArticleFetcher
from news_scrapers.news_fetcher.random_user_agent_service import RandomUserAgentService


class GooseArticleFetcher(BaseArticleFetcher):
    def __init__(self, n_threads: int = 0, **kwargs):
        super().__init__(n_threads, **kwargs)
        self._fetcher = Goose(
            {
                'browser_user_agent': RandomUserAgentService().get(),
            }
        )

    def parse(self, html: str, url: Optional[str] = None) -> Article:
        if not html:
            return Article.get_empty()
        source_article = self._fetcher.extract(raw_html=html)
        published = (
            source_article.publish_datetime_utc.strftime("%Y-%m-%d")
            if source_article.publish_datetime_utc
            else ''
        )
        if not published:
            published = source_article.infos.get("opengraph", {}).get(
                "article:published_time"
            )
        description = source_article.meta_description
        if not description:
            description = source_article.infos.get("meta", {}).get("description")
        if not description:
            description = source_article.infos.get("opengraph", {}).get("description")
        authors = source_article.authors
        if not authors:
            authors = [source_article.infos.get("opengraph", {}).get("article:author")]
        tags = source_article.tags
        if not tags:
            tags = source_article.infos.get("opengraph", {}).get("article:tag")

        title = source_article.title
        if not title:
            title = source_article.infos.get("title", "")

        text = source_article.cleaned_text
        if not text:
            text = self.make_readable(html)

        return Article(
            url=url or source_article.final_url,
            title=title,
            text=text,
            published=published,
            meta_language=source_article.meta_lang,
            authors=authors,
            domain=source_article.domain,
            description=description,
            meta_description=source_article.meta_description,
            meta_keywords=source_article.meta_keywords,
            meta_encoding=source_article.meta_encoding,
            tags=tags,
        )


if __name__ == '__main__':

    article = GooseArticleFetcher().fetch(
        'https://www.theguardian.com/commentisfree/2022/may/01/republican-midterm-candidates-falling-into-line-trump'
    )
    print(article)
