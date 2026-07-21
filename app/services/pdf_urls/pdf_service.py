
from app.services.crawler.models import CrawledPage
from pathlib import Path
import aiohttp
import tempfile
import fitz
import logging
from urllib.parse import urlparse
from datetime import datetime, timezone


logger = logging.getLogger(__name__)

class PdfService:
    
    async def load(self, url: str) -> CrawledPage:
        """
        Download a PDF, extract its text, and return it as a CrawledPage.
        """

        logger.info("Downloading PDF: %s", url)

        pdf_path = await self._download_pdf(url)

        try:
            text = self._extract_text(pdf_path)

            filename = Path(urlparse(url).path).name

            page = CrawledPage(
                url=url,
                title=filename,
                markdown=text,
                html=None,
                status_code=200,
                success=True,
                crawled_at=datetime.now(timezone.utc),
            )

            logger.info(
                "Successfully extracted PDF (%d chars): %s",
                len(text),
                filename,
            )

            return page

        finally:
            if pdf_path.exists():
                pdf_path.unlink(missing_ok=True)

    
    async def _download_pdf(self, url: str) -> Path:
        """
        Downloads the PDF to a temporary file.
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                response.raise_for_status()

                with tempfile.NamedTemporaryFile(
                    suffix=".pdf",
                    delete=False,
                ) as tmp:

                    tmp.write(await response.read())

                    return Path(tmp.name)

    
    
    def _extract_text(self, pdf_path: Path) -> str:

        doc = fitz.open(pdf_path)

        output = []

        for i, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()

            if text:
                output.append(
                    f"\n\n--- Page {i} ---\n\n{text}"
                )

        doc.close()
        return "".join(output)
