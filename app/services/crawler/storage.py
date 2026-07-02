import json
from pathlib import Path

from .models import CrawledPage

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