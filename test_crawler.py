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


cleaned_text = "Leis na fianáin sin is féidir linn cuairteanna agus foinsí tráchta a chomhaireamh ionas go mbeimid in ann feidhmíocht ár suímh a thomhas agus a fheabhsú. Cabhraíonn siad linn na leathanaigh is mó tóir agus is lú tóir a aithint, mar aon leis an gcaoi a mbogann cuairteoirí ar an suíomh. Déantar gach eolas a bhailítear leis na fianáin sin a comhiomlánú agus mar sin is eolas anaithnid é. Mura gceadaíonn tú na fianáin sin, ní bheidh a fhios againn cén uair ar thug tú cuairt ar ár suíomh. Tá na fianáin seo riachtanach don suíomh gréasáin agus ní féidir iad a chasadh as inár gcórais. Is iondúil nach socraítear iad ach amháin mar fhreagra ar ghníomhartha atá déanta agatsa, arb ionann iad agus iarratas ar sheirbhísí, cosúil le do roghanna príobháideachais a shocrú, logáil isteach nó foirmeacha a chomhlánú. Is féidir leat do bhrabhsálaí a shocrú chun an fianáin sin a bhlocáil, nó foláireamh a thabhairt duit ina dtaobh, ach d’fhéadfadh sé nach n-oibreoidh codanna den suíomh sa chás sin."


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