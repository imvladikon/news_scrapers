#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import List

from news_fetcher import ALL_FETCHERS
from news_fetcher.article import Article
from news_fetcher.html_fetcher import HtmlFetcher

PROJECT_DIR = Path(__file__).resolve().parent

logger = logging.getLogger(__name__)


@dataclass
class NewsArticle:
    url: str
    title: str
    text: str
    published: str
    language: str
    meta_language: str
    authors: List[str]
    classification_1: str
    Entities: List[str]
    facts: List[str]



def fetch_article(url, backend):
    html = HtmlFetcher(backend=backend).fetch(url)
    articles = [fetcher().parse(html=html, url=url) for fetcher in ALL_FETCHERS]
    article = Article.combine_all(articles)
    return (url, article)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '--screening_test_file',
        type=str,
        required=True,
        help='Screening test file path',
    )
    parser.add_argument(
        '--output_file',
        type=str,
        required=True,
        help='Output file path for mock data',
    )
    parser.add_argument(
        '--n_threads', type=int, required=False, default=4, help='Number of threads to use'
    )
    args = parser.parse_args()
