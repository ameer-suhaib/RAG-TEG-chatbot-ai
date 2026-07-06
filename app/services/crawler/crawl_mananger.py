from crawl4ai import (CrawlerRunConfig, BrowserConfig, PruningContentFilter, DefaultMarkdownGenerator, CacheMode)

# factory-based design
##responsible for creating crawler configuration objects.


def get_browser_config() -> BrowserConfig:
    """
    stable rendering , consistenct page layout,
    custom crawler identity, easy debugging.
    """
    return BrowserConfig(
    browser_type="chromium",
    headless=True,
    verbose=False,
    user_agent=(
        "TEG-RAG-Crawler/1.0 "
        "(Academic Research Project)"       
    ),
    viewport_width=1920,
    viewport_height=1080,
)

def get_content_filtering() -> PruningContentFilter:
    """
    removes navigation, sidebar, cookie banners,
    empty divs, repeated bolcks
    """
    return PruningContentFilter(
    threshold=0.45,
    threshold_type="dynamic",
    min_word_threshold=25
)

def get_markdown_generator() -> DefaultMarkdownGenerator:
    """
    Markdown generator used by Crawl4AI.
    """
    return DefaultMarkdownGenerator(
    content_filter=get_content_filtering() 
)


def get_crawler_run_config() -> CrawlerRunConfig:
    """
    Runtime configuration for crawling.
    """
    return CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        markdown_generator=get_markdown_generator(),
        word_count_threshold=10,
        exclude_external_links=True,
        exclude_social_media_links=True,
        remove_overlay_elements=True,
        process_iframes=False,
        scan_full_page=True,
        wait_until="networkidle",
        page_timeout=30000,
    )