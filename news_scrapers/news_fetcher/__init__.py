#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .goose_article_fetcher import GooseArticleFetcher
from .newsplease_article_fetcher import NewspleaseArticleFetcher
from .newspaper_article_fetcher import NewspaperArticleFetcher


ALL_FETCHERS = [GooseArticleFetcher, NewspleaseArticleFetcher, NewspaperArticleFetcher]
