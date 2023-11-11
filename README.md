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
    def __init__(
        self,
        url_pattern=<url_pattern>,
        first_page=1,
        last_page=<last_page>,
        page_iterator=None,
        **kwargs
    ):
```
where need to pass or range of pages (which will be used in `url_pattern`) or `page_iterator`.
possible to pass `page_iterator` as a function which will read the page from folder or from web:

```python
def page_iterator(self):
    for _ in range(1, 10):
        url = self.url_pattern.format(_)
        html = requests.get(url).text
        yield html, url
```


And usage:

```python
scraper = CustomScraper()
for record in scraper:
    print(record)
```

where record is a dictionary with `text`, `description`, `title`, `url`, `date`, `author`, etc.


