# import asyncio
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
# from lingua import Language, LanguageDetectorBuilder

# async def main():
#     browser_conf = BrowserConfig(headless=True)  # or False to see the browser
#     run_conf = CrawlerRunConfig(
#         cache_mode=CacheMode.BYPASS
#     )

#     async with AsyncWebCrawler(config=browser_conf) as crawler:
#         result = await crawler.arun(
#             url="https://www.teg.ie",
#             config=run_conf
#         )
#         print(result.markdown)

# if __name__ == "__main__":
#     asyncio.run(main())



# # https://www.teg.ie


cleaned_text = "explain about langgraph"


from lingua import Language, LanguageDetectorBuilder

detector = LanguageDetectorBuilder.from_languages(
    Language.ENGLISH,
    Language.IRISH
).build()

language = detector.detect_language_of(cleaned_text)
print(type(language))
print(language.name,"namee")
if language.name == 'IRISH':
    print("ga")
print(language,"---langg")