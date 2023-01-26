#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from news_scrapers.news_fetcher.html_fetcher import HtmlFetcher
from news_scrapers.base_scraper import BaseScraper


class KanScraper(BaseScraper):

    def __init__(self, first_page=1, last_page=143831, page_iterator=None, **kwargs):

        super().__init__(
            url_pattern="https://www.kan.org.il/item/?itemId={}",
            first_page=first_page,
            last_page=last_page,
            page_iterator=page_iterator,
            language="hebrew",
            site_name="kan",
            **kwargs
        )

    def _is_error_page(self, html: str) -> bool:
        return "404" in html and "error" in html and "הדף שחיפשת כבר לא כאן" in html

    def default_page_iterator(self):
        for url in self._read_sitemap():
            html = HtmlFetcher().fetch(url)
            yield html, url

    def _read_sitemap(self):
        url = "https://www.kan.org.il/sitemap1.xml"
        html = HtmlFetcher().fetch(url)
        soup = BeautifulSoup(html, "html.parser")
        urls = (n.text for n in soup.select("loc") if "item" in n.text)
        yield from urls


if __name__ == '__main__':
    from tqdm import tqdm
    import requests
    from news_scrapers.writers import JsonWriter
    from news_scrapers.news_fetcher import LinkPreviewFetcher



    scraper = KanScraper.from_path(path="/media/robert/BC7CA8E37CA899A2/datasets/kan")
    url = "https://www.kan.org.il/item/?itemId=60959"
    html = requests.get(url).text

    article = scraper.parse_article(html, url)
    print(article.to_json())
    # with JsonWriter("kan.jsonl") as writer:
    #     for article, url in tqdm(scraper):
    #         writer.write(article.to_json())

