#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Optional

from news_scrapers.usp.exceptions import SitemapException
from news_scrapers.usp.fetch_parse import SitemapFetcher
from news_scrapers.usp.helpers import is_http_url, strip_url_to_homepage
from news_scrapers.usp.log import create_logger
from news_scrapers.usp.objects.sitemap import (AbstractSitemap, InvalidSitemap,
                                               IndexWebsiteSitemap, IndexRobotsTxtSitemap)
from news_scrapers.usp.web_client.abstract_client import AbstractWebClient

log = create_logger(__name__)

_UNPUBLISHED_SITEMAP_PATHS = {
    'sitemap.xml',
    'sitemap.xml.gz',
    'sitemap_index.xml',
    'sitemap-index.xml',
    'sitemap_index.xml.gz',
    'sitemap-index.xml.gz',
    '.sitemap.xml',
    'sitemap',
    'admin/config/search/xmlsitemap',
    'sitemap/sitemap-index.xml',
    # 'sitemap-main.xml',
    # 'sitemap-main-index.xml',
    # 'main-sitemap.xml',
    # 'sitemap1.xml',
    # 'sitemap2.xml',
    # 'sitemapindex.xml',
    # 'sitemaps/sitemap.xml',
    # 'sitemaps/main-sitemap.xml',
    # 'sitemaps/sitemap_index.xml',
    # 'sitemaps/sitemap-index.xml',
    # 'sitemaps/main-sitemap-index.xml',
}
"""Paths which are not exposed in robots.txt but might still contain a sitemap."""


def sitemap_tree_for_homepage(homepage_url: str, web_client: Optional[AbstractWebClient] = None) -> AbstractSitemap:
    """
    Using a homepage URL, fetch the tree of sitemaps and pages listed in them.

    :param homepage_url: Homepage URL of a website to fetch the sitemap tree for, e.g. "http://www.example.com/".
    :param web_client: Web client implementation to use for fetching sitemaps.
    :return: Root sitemap object of the fetched sitemap tree.
    """

    if not is_http_url(homepage_url):
        raise SitemapException("URL {} is not a HTTP(s) URL.".format(homepage_url))

    stripped_homepage_url = strip_url_to_homepage(url=homepage_url)
    if homepage_url != stripped_homepage_url:
        log.warning("Assuming that the homepage of {} is {}".format(homepage_url, stripped_homepage_url))
        homepage_url = stripped_homepage_url

    if not homepage_url.endswith('/'):
        homepage_url += '/'
    robots_txt_url = homepage_url + 'robots.txt'

    sitemaps = []

    robots_txt_fetcher = SitemapFetcher(url=robots_txt_url, web_client=web_client, recursion_level=0)
    robots_txt_sitemap = robots_txt_fetcher.sitemap(parent_url=homepage_url)
    sitemaps.append(robots_txt_sitemap)

    sitemap_urls_found_in_robots_txt = set()
    if isinstance(robots_txt_sitemap, IndexRobotsTxtSitemap):
        for sub_sitemap in robots_txt_sitemap.sub_sitemaps:
            sitemap_urls_found_in_robots_txt.add(sub_sitemap.url)

    for unpublished_sitemap_path in _UNPUBLISHED_SITEMAP_PATHS:
        unpublished_sitemap_url = homepage_url + unpublished_sitemap_path

        # Don't refetch URLs already found in robots.txt
        if unpublished_sitemap_url not in sitemap_urls_found_in_robots_txt:

            unpublished_sitemap_fetcher = SitemapFetcher(
                url=unpublished_sitemap_url,
                web_client=web_client,
                recursion_level=0,
            )
            unpublished_sitemap = unpublished_sitemap_fetcher.sitemap()

            # Skip the ones that weren't found
            if not isinstance(unpublished_sitemap, InvalidSitemap):
                sitemaps.append(unpublished_sitemap)

    index_sitemap = IndexWebsiteSitemap(url=homepage_url, sub_sitemaps=sitemaps)

    return index_sitemap
