#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from news_scrapers.base_scraper import BaseScraper


class SomeScraper(BaseScraper):
    _site_url = "https://edition.cnn.com/"
    _language = "english"
    _site_name = "cnn"


if __name__ == '__main__':
    from pprint import pprint

    for article, url in SomeScraper():
        pprint(article.to_dict())
        break
