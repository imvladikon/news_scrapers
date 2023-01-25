#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from preprocessing.scrapers.news_fetcher import ALL_FETCHERS
from preprocessing.scrapers.news_fetcher.article import Article

urls = ["https://ar.timesofisrael.com/wp-content/themes/rgb/ajax/topics_for_terms.php?taxonomy=category&post_tag=&numposts=3000&is_mobile=true&post_type="
"https://ar.timesofisrael.com/wp-content/themes/rgb/ajax/topics_for_terms.php?taxonomy=category&post_tag=&before_date=1627216812&numposts=3000&is_mobile=true&post_type="
"https://ar.timesofisrael.com/wp-content/themes/rgb/ajax/topics_for_terms.php?taxonomy=category&post_tag=&before_date=1595680863&numposts=3000&is_mobile=true&post_type="
"https://ar.timesofisrael.com/wp-content/themes/rgb/ajax/topics_for_terms.php?taxonomy=category&post_tag=&before_date=1564058463&numposts=3000&is_mobile=true&post_type="]


page_urls = {}
for url in urls:
    html = requests.get(url).text
    doc = BeautifulSoup(html, 'html.parser')
    for node in doc.select(".news .headline a"):
        page_urls[node.attrs["href"]] = 1
print(page_urls.keys())
with open("articles_ar_timesofisrael.jsonl", "w", encoding="utf-8") as f_out:
    for url in page_urls:
        html = requests.get(url).text
        doc = BeautifulSoup(html, 'html.parser')
        articles = [fetcher().parse(html=html, url=url) for fetcher in ALL_FETCHERS]
        article = Article.combine_all(articles)
        article.text = doc.select_one(".article-content").text
        f_out.write(article.to_json() + "\n")

