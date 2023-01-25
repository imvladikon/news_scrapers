#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from typing import Dict, List, Optional, Tuple, Union

import requests
from playwright.sync_api import sync_playwright
from selenium import webdriver
from requests.adapters import HTTPAdapter, Retry

from news_scrapers.news_fetcher.random_user_agent_service import RandomUserAgentService


logger = logging.getLogger(__name__)


class HtmlFetcher:
    def __init__(
        self,
        backend: str = 'requests',
        use_wayback: bool = False,
        infer_encoding_from_content: bool = False,
        **requests_kwargs
    ):
        self.backoff_factor = requests_kwargs.get('backoff_factor', 0.3)
        self.retries = requests_kwargs.get('retries', 3)
        self.use_wayback = use_wayback
        self.wayback_api_url = 'https://archive.org/wayback/available?url={}'
        self.backend = backend
        self.session = None
        self.status_forcelist: Union[List, Tuple] = (
            400,
            401,
            403,
            500,
            502,
            503,
            504,
            505,
        )
        self.infer_encoding_from_content = infer_encoding_from_content

        assert self.backend in [
            'requests',
            'playwright',
            'selenium',
        ], 'backend must be one of requests, playwright, selenium'

    def requests_retry_session(self) -> requests.Session:
        """
        Retries the HTTP GET method in case of some specific HTTP errors.
        :param retries: Time of retries
        :param backoff_factor: The amount of delay after each retry
        :param status_forcelist: The error codes that the script should retry; Otherwise, it won't retry
        :param session: the requests session
        :return: the new session
        """
        session = self.session or requests.Session()
        retry = Retry(
            total=self.retries,
            read=self.retries,
            connect=self.retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=self.status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def get_response(self, url: str, headers: Dict = {}) -> Optional[requests.Response]:
        self.session = requests.Session()
        try:
            headers = {**{'User-agent': RandomUserAgentService().get()}, **headers}
            request = self.requests_retry_session().get(
                url=url, allow_redirects=True, headers=headers, verify=False
            )
            try:
                request.encoding = request.headers['content-type'].split('charset=')[-1]
            except:
                pass
            if self.infer_encoding_from_content:
                # infering using chardet
                request.encoding = request.apparent_encoding
            return request
        except Exception as e:
            logger.error('failed to get html from url: {}'.format(url))
        return None

    def get_html_wayback(self, url: str) -> Optional[str]:
        response = self.get_response(url=self.wayback_api_url.format(url))
        if response is not None:
            try:
                url = response.json()['archived_snapshots']['closest']['url']
                response = self.get_response(url=url)
                if response is not None:
                    return response.text
            except:
                pass
        return None

    def _fetch_requests(self, url: str, headers: Dict = {}) -> Optional[str]:
        response = self.get_response(url=url, headers=headers)
        if response is None and self.use_wayback:
            return self.get_html_wayback(url=url)
        return response.text

    def make_request(self, url: str, headers: Dict = {}) -> Optional[str]:
        response = self.get_response(url=url, headers=headers)
        return response

    def fetch(self, url: str, timeout: int = 2000, headers: Dict = {}) -> Optional[str]:
        if self.backend == 'requests':
            return self._fetch_requests(url=url, headers=headers)
        elif self.backend == 'playwright':
            return self._fetch_playwright(url=url, timeout=timeout)
        elif self.backend == 'selenium':
            return self._fetch_selenium(url=url, timeout=timeout)
        else:
            raise ValueError('unknown backend: {}'.format(self.backend))

    def _fetch_playwright(self, url, timeout):
        with sync_playwright() as p:
            session = p.chromium.launch(headless=True)
            page = session.new_page()
            page.goto(url)
            page.wait_for_timeout(timeout)
            content = page.content()
            session.close()
        return content

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.session is not None:
                self.session.close()
                self.session = None
        except:
            pass

    def _fetch_selenium(self, url, timeout):
        # headless chrome
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        options.add_argument('disable-gpu')
        options.add_argument('no-sandbox')
        options.add_argument('disable-dev-shm-usage')
        options.add_argument('user-agent={}'.format(RandomUserAgentService().get()))

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        page = driver.page_source
        driver.close()
        return page


if __name__ == '__main__':
    print(HtmlFetcher(backend="playwright").fetch('https://www.google.com'))
