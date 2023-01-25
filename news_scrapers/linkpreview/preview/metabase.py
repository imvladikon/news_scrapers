from news_scrapers.linkpreview.preview.base import PreviewBase


class MetaPreviewBase(PreviewBase):
    """
    Base class for OpenGraph, TwitterCard
    """

    __target_attr__ = None

    def _get_property(self, name):
        meta = self._soup.find("meta", attrs={self.__target_attr__: name})
        if meta and meta["content"]:
            return meta["content"]
