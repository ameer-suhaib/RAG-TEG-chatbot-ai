import json
from pathlib import Path
import logging
from .models import CrawledPage

logger = logging.getLogger(__name__)

class CrawlStorage:
    def __init__(self):
        self.output = Path("./app/storage/raw_html")
        self.output.mkdir(parents=True, exist_ok=True)

    #save
    def save(self, page: CrawledPage):
        filename = page.url.host + "_" + page.url.path.replace("/", "_")
        filename = filename.strip("_")
        filepath = self.output / f"{filename}.json"

        with open(filepath, "w",encoding="utf8") as f:
            json.dump(
                page.model_dump(mode="json"),   
                f,
                indent=4,
                ensure_ascii=False,
            )

    def load_all(self) -> list[CrawledPage]:
        """
        Load all previously crawled pages from storage.
        """

        pages: list[CrawledPage] = []

        for file in self.output.glob("*.json"):

            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            pages.append(CrawledPage.model_validate(data))

        logger.info("Loaded %d crawled pages from storage.", len(pages))

        return pages