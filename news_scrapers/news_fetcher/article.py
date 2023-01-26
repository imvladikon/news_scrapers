#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass
from typing import Dict, List, Optional
from functools import reduce


@dataclass
class Article:
    url: str
    title: str
    text: str
    published: Optional[str]
    meta_language: Optional[str]
    authors: Optional[List[str]]
    domain: Optional[str]
    description: Optional[str]
    meta_description: Optional[str]
    meta_keywords: Optional[List[str]]
    meta_encoding: Optional[str]
    tags: Optional[List[str]]
    toc: Optional[List[str]] = None
    site_name: Optional[str] = None
    language: Optional[str] = None
    canonical_link: Optional[str] = None

    def is_empty(self):
        return self.url == '' and self.title == '' and self.text == ''

    @staticmethod
    def get_empty():
        return Article(
            url='',
            title='',
            text='',
            published='',
            meta_language='',
            authors=[],
            domain='',
            description='',
            meta_description='',
            meta_keywords=[],
            meta_encoding='',
            tags=[],
        )

    @staticmethod
    def choose_best_text(texts: List[str]):
        texts = [text.strip() if text else "" for text in texts]
        return sorted(texts, key=len, reverse=True)[0]

    def combine_with(self, other: 'Article'):
        return Article(
            url=self.url or other.url,
            title=Article.choose_best_text([self.title, other.title]),
            text=Article.choose_best_text([self.text, other.text]),
            published=self.published or other.published,
            meta_language=self.meta_language or other.meta_language,
            authors=self.authors or other.authors,
            domain=self.domain or other.domain,
            description=Article.choose_best_text([self.description, other.description]),
            meta_description=Article.choose_best_text(
                [self.meta_description, other.meta_description]
            ),
            meta_keywords=self.meta_keywords or other.meta_keywords,
            meta_encoding=self.meta_encoding or other.meta_encoding,
            tags=self.tags or other.tags,
        )

    @staticmethod
    def combine_all(articles: List['Article']) -> 'Article':
        return reduce(lambda x, y: x.combine_with(y), articles, Article.get_empty())

    def to_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False)
