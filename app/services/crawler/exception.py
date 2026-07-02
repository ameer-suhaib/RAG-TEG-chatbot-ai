class CrawlError(Exception):
    """Base crawl exception"""


class UrlDiscoveryError(CrawlError):
    """URL discovery failed"""


class CrawlFailedError(CrawlError):
    """Page crawl failed"""