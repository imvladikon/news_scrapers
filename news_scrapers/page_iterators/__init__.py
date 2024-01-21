#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.usp.tree import sitemap_tree_for_homepage


class BasePageIterator:

    def __init__(self, **kwargs):
        pass

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


class UrlsRangeIterator(BasePageIterator):

    def __init__(self, url_pattern, first_page, last_page, **kwargs):
        super().__init__(**kwargs)
        self.url_pattern = url_pattern
        self._first_page = first_page
        self._last_page = last_page

    def __iter__(self):
        return self

    def __next__(self):
        if self._first_page > self._last_page:
            raise StopIteration

        url = self.url_pattern.format(self._first_page)
        self._first_page += 1
        return url


class SitemapIterator(BasePageIterator):

    def __init__(self, site, sitemap_filters=None, **kwargs):
        super().__init__(**kwargs)
        self.site = site
        self._sitemap_tree = None
        self._sitemap_tree_generator = None
        if not sitemap_filters:
            self.sitemap_filters = lambda p: True
        elif isinstance(sitemap_filters, str):
            self.sitemap_filters = lambda p: p.parent_url.startswith(sitemap_filters) if p.parent_url else False
        else:
            self.sitemap_filters = sitemap_filters

    @property
    def sitemap_tree(self):
        if self._sitemap_tree is None:
            self._sitemap_tree = sitemap_tree_for_homepage(self.site)
        return self._sitemap_tree

    @property
    def sitemap_tree_generator(self):
        if self._sitemap_tree_generator is None:
            self._sitemap_tree_generator = (p for p in self.sitemap_tree.all_pages() if self.sitemap_filters(p))
        return self._sitemap_tree_generator

    def __iter__(self):
        return self

    def __next__(self):
        if not self.sitemap_tree or not self.sitemap_tree_generator:
            raise StopIteration

        sitemap_page = next(self.sitemap_tree_generator, None)
        if sitemap_page is None:
            raise StopIteration

        url = sitemap_page.url
        return url
