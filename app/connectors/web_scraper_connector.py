"""Web scraper knowledge connector for ingesting content from URLs."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse

from app.connectors.base_connector import KnowledgeConnector
from app.document.document import Document


@dataclass
class WebScraperConfig:
    """
    Configuration for the WebScraperConnector.

    Attributes:
        urls: Seed URLs to fetch
        follow_links: Whether to crawl linked pages on the same domain
        max_depth: Maximum crawl depth when follow_links is True (default 1)
        max_pages: Safety cap on total pages crawled (default 50)
        request_timeout_seconds: Per-request HTTP timeout (default 10)
        user_agent: HTTP User-Agent header
        headers: Additional HTTP headers to send with every request
    """

    urls: list[str]
    follow_links: bool = False
    max_depth: int = 1
    max_pages: int = 50
    request_timeout_seconds: int = 10
    user_agent: str = "EnterpriseAI-WebScraper/1.0"
    headers: dict[str, str] = field(default_factory=dict)


class WebScraperConnector(KnowledgeConnector):
    """
    Fetches web pages and extracts their text content as Documents.

    Supports:
    - Single URL fetching
    - Multi-page crawling within the same origin (follow_links=True)
    - Depth-limited crawling to avoid runaway scraping

    Usage:
        config = WebScraperConfig(
            urls=["https://docs.example.com"],
            follow_links=True,
            max_depth=2,
        )
        async with WebScraperConnector(config) as connector:
            documents = await connector.fetch()
    """

    CONNECTOR_ID = "web_scraper"

    def __init__(self, config: WebScraperConfig):
        self._config = config
        self._session = None

    @property
    def connector_id(self) -> str:
        return self.CONNECTOR_ID

    async def connect(self) -> None:
        """Create the async HTTP session."""
        try:
            import aiohttp
        except ImportError:
            raise RuntimeError(
                "aiohttp is required for WebScraperConnector. "
                "Install it with: pip install aiohttp"
            )

        import aiohttp

        headers = {
            "User-Agent": self._config.user_agent,
            **self._config.headers,
        }
        timeout = aiohttp.ClientTimeout(
            total=self._config.request_timeout_seconds,
        )
        self._session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout,
        )

    async def disconnect(self) -> None:
        """Close the async HTTP session."""
        if self._session is not None:
            await self._session.close()
            self._session = None

    async def fetch(self) -> list[Document]:
        """
        Fetch all configured URLs and optionally crawl linked pages.

        Returns:
            List of Document objects extracted from fetched pages
        """
        if self._session is None:
            raise RuntimeError(
                "WebScraperConnector is not connected. "
                "Use 'async with' or call connect() first."
            )

        visited: set[str] = set()
        documents: list[Document] = []

        # Queue entries: (url, depth)
        queue: list[tuple[str, int]] = [
            (url, 0) for url in self._config.urls
        ]

        while queue and len(visited) < self._config.max_pages:
            url, depth = queue.pop(0)

            normalized = self._normalize_url(url)
            if normalized in visited:
                continue
            visited.add(normalized)

            page_content = await self._fetch_page(normalized)
            if page_content is None:
                continue

            html, status_code = page_content
            text = self._extract_text(html)

            if text.strip():
                documents.append(
                    Document(
                        id=self._make_document_id(normalized),
                        name=self._extract_title(html) or normalized,
                        text=text.strip(),
                        metadata={
                            "source": "web_scraper",
                            "url": normalized,
                            "status_code": str(status_code),
                            "depth": str(depth),
                        },
                    )
                )

            # Crawl linked pages if enabled and within depth
            if (
                self._config.follow_links
                and depth < self._config.max_depth
                and len(visited) < self._config.max_pages
            ):
                linked_urls = self._extract_links(html, normalized)
                for linked_url in linked_urls:
                    if linked_url not in visited:
                        queue.append((linked_url, depth + 1))

        return documents

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    async def _fetch_page(
        self,
        url: str,
    ) -> tuple[str, int] | None:
        """
        Fetch a single page and return (html, status_code), or None on failure.
        """
        try:
            async with self._session.get(url) as response:
                if response.status >= 400:
                    return None
                html = await response.text(errors="replace")
                return html, response.status
        except Exception:
            return None

    def _extract_links(self, html: str, base_url: str) -> list[str]:
        """
        Extract same-origin links from HTML.

        Only follows links within the same scheme + netloc to avoid
        crawling off to external sites.
        """
        base_parsed = urlparse(base_url)
        base_origin = f"{base_parsed.scheme}://{base_parsed.netloc}"

        # Simple href extraction without a full HTML parser dependency
        raw_links = re.findall(
            r'href=["\']([^"\']+)["\']',
            html,
            flags=re.IGNORECASE,
        )

        same_origin_links: list[str] = []
        for raw in raw_links:
            # Skip anchors, javascript, mailto
            if raw.startswith(("#", "javascript:", "mailto:")):
                continue

            absolute = urljoin(base_url, raw)
            parsed = urlparse(absolute)

            # Strip fragment
            clean = absolute.split("#")[0]

            if f"{parsed.scheme}://{parsed.netloc}" == base_origin:
                same_origin_links.append(clean)

        return same_origin_links

    @staticmethod
    def _extract_text(html: str) -> str:
        """
        Extract readable text from HTML.

        Tries BeautifulSoup if available, falls back to regex strip.
        """
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html, "html.parser")

            # Remove non-content tags
            for tag in soup(["script", "style", "nav", "footer", "head"]):
                tag.decompose()

            return soup.get_text(separator="\n", strip=True)
        except ImportError:
            # Fallback: strip content of non-readable tags, then strip all HTML tags
            cleaned = re.sub(
                r"<(script|style|nav|footer|head)[^>]*>.*?</\1>",
                " ",
                html,
                flags=re.IGNORECASE | re.DOTALL,
            )
            no_tags = re.sub(r"<[^>]+>", " ", cleaned)
            return re.sub(r"\s{2,}", "\n", no_tags).strip()

    @staticmethod
    def _extract_title(html: str) -> str | None:
        """Extract <title> from HTML if present."""
        match = re.search(
            r"<title[^>]*>([^<]+)</title>",
            html,
            flags=re.IGNORECASE,
        )
        return match.group(1).strip() if match else None

    @staticmethod
    def _normalize_url(url: str) -> str:
        """Normalize URL by stripping trailing slashes and fragments."""
        return url.rstrip("/").split("#")[0]

    @staticmethod
    def _make_document_id(url: str) -> str:
        """Create a stable document ID from the URL."""
        return hashlib.sha256(url.encode()).hexdigest()[:16]
