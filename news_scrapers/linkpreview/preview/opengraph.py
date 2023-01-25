from news_scrapers.linkpreview.preview.metabase import MetaPreviewBase


class OpenGraph(MetaPreviewBase):
    """
    Gets OpenGraph meta properties of a webpage.
    sample: <meta property="og:title" content="blabla">
    https://ogp.me/
    """

    __target_attr__ = "property"

    @property
    def site_name(self):
        return self._get_property("og:site_name")

    @property
    def title(self):
        return self._get_property("og:title")

    @property
    def description(self):
        return self._get_property("og:description")

    @property
    def image(self):
        return self._get_property("og:image")

    @property
    def published_time(self):
        return self._get_property("article:published_time")

    @property
    def modified_time(self):
        return self._get_property("article:modified_time")

    @property
    def expiration_time(self):
        return self._get_property("article:expiration_time")

    @property
    def author(self):
        return self._get_property("article:author")

    @property
    def section(self):
        return self._get_property("article:section")

    @property
    def tag(self):
        return self._get_property("article:tag")

    @property
    def url(self):
        return self._get_property("og:url")

