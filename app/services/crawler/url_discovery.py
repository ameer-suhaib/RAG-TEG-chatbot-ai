import site
from bs4 import BeautifulSoup
import httpx

class URLDiscovery:
    def __init__(self):
        self.base_url = "https://www.teg.ie"

    async def discover(self) -> list[str]:
        sitemap = f"{self.base_url}/sitemap.xml"

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(sitemap)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "xml")
        urls = []

        for loc in soup.find_all("loc"):
            urls.append(loc.text.strip())
        return sorted(set(urls))