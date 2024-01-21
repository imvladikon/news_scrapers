# News Scrapers [WIP]

## Description

This repository contains scripts for scraping news from different sources, 
tailored for research purposes such as NLP and summarization. 
The scripts enable the extraction of news content along with meta tags information, 
JSON+LD data, crawling sitemap files, and more, 
enhancing the capabilities for comprehensive data analysis and exploration    
Disclaimer: The scripts are provided as-is, and intended for customization and further development.

## Example

Examples check in the [hebrew](news_scrapers%2Fhebrew) and [arabic](news_scrapers%2Farabic) directories.

Custom scraper example:

```python
from news_scrapers.base_scraper import BaseScraper

class CustomScraper(BaseScraper):
    
    _site_url = <site_url>
    _site_name = <site_name>
    _language = <language>

```

And usage:

```python
scraper = CustomScraper()
for article, url in scraper:
    print(article)
```


By default, the scraper checks the `sitemap.xml` file and iterates over all pages.
Otherwise, it is possible to pass `page_iterator` which will be used to iterate over pages.

```python
def page_iterator(self):
    for _ in range(1, 10):
        url = self.url_pattern.format(_)
        yield url
```
```python
scraper = CustomScraper(page_iterator=page_iterator())
for article, url in scraper:
    print(article)
```

And `article` is a data class with `text`, `description`, `title`, `url`, `date`, `author`, etc.
If needed, it is possible to convert it to a dictionary using `article.to_dict()`, or to JSON using `article.to_json()`.






