"""Unit tests for WebScraperConnector."""

import sys
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.connectors.web_scraper_connector import WebScraperConnector, WebScraperConfig


SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head><title>Enterprise AI Docs</title></head>
<body>
  <h1>Welcome to Enterprise AI</h1>
  <p>This platform provides scalable AI solutions.</p>
  <a href="/overview">Overview</a>
  <a href="/api/reference">API Reference</a>
  <a href="https://external.com/page">External Link</a>
</body>
</html>
"""

SAMPLE_HTML_2 = """
<html>
<head><title>Overview</title></head>
<body>
  <p>Overview content here.</p>
  <script>var x = 1;</script>
  <nav>Nav items</nav>
</body>
</html>
"""


def make_mock_response(html: str, status: int = 200):
    """Create a mock aiohttp response."""
    response = AsyncMock()
    response.status = status
    response.text = AsyncMock(return_value=html)
    response.__aenter__ = AsyncMock(return_value=response)
    response.__aexit__ = AsyncMock(return_value=None)
    return response


@pytest.fixture
def mock_session():
    """Create a mock aiohttp ClientSession."""
    session = MagicMock()
    session.close = AsyncMock()
    return session


class TestWebScraperConnectorConnect:
    """Test connector lifecycle."""

    @pytest.mark.asyncio
    async def test_connect_creates_session(self):
        config = WebScraperConfig(urls=["https://example.com"])
        connector = WebScraperConnector(config)

        mock_aiohttp = MagicMock()
        mock_aiohttp.ClientSession.return_value = MagicMock()
        mock_aiohttp.ClientTimeout.return_value = MagicMock()

        with patch.dict(sys.modules, {"aiohttp": mock_aiohttp}):
            await connector.connect()

        mock_aiohttp.ClientSession.assert_called_once()

    @pytest.mark.asyncio
    async def test_disconnect_closes_session(self, mock_session):
        config = WebScraperConfig(urls=["https://example.com"])
        connector = WebScraperConnector(config)
        connector._session = mock_session

        await connector.disconnect()

        mock_session.close.assert_awaited_once()
        assert connector._session is None

    @pytest.mark.asyncio
    async def test_fetch_without_connect_raises(self):
        config = WebScraperConfig(urls=["https://example.com"])
        connector = WebScraperConnector(config)

        with pytest.raises(RuntimeError, match="not connected"):
            await connector.fetch()

    def test_connector_id(self):
        config = WebScraperConfig(urls=["https://example.com"])
        connector = WebScraperConnector(config)
        assert connector.connector_id == "web_scraper"


class TestWebScraperConnectorFetch:
    """Test document fetching."""

    @pytest.mark.asyncio
    async def test_fetch_single_url(self, mock_session):
        config = WebScraperConfig(
            urls=["https://example.com"],
            follow_links=False,
        )
        connector = WebScraperConnector(config)
        connector._session = mock_session
        mock_session.get.return_value = make_mock_response(SAMPLE_HTML)

        documents = await connector.fetch()

        assert len(documents) == 1
        assert "Enterprise AI" in documents[0].text

    @pytest.mark.asyncio
    async def test_fetch_document_metadata(self, mock_session):
        config = WebScraperConfig(urls=["https://example.com"])
        connector = WebScraperConnector(config)
        connector._session = mock_session
        mock_session.get.return_value = make_mock_response(SAMPLE_HTML)

        documents = await connector.fetch()

        doc = documents[0]
        assert doc.metadata["source"] == "web_scraper"
        assert "https://example.com" in doc.metadata["url"]
        assert doc.metadata["status_code"] == "200"
        assert doc.metadata["depth"] == "0"

    @pytest.mark.asyncio
    async def test_fetch_uses_title_as_name(self, mock_session):
        config = WebScraperConfig(urls=["https://example.com"])
        connector = WebScraperConnector(config)
        connector._session = mock_session
        mock_session.get.return_value = make_mock_response(SAMPLE_HTML)

        documents = await connector.fetch()

        assert documents[0].name == "Enterprise AI Docs"

    @pytest.mark.asyncio
    async def test_fetch_skips_404_pages(self, mock_session):
        config = WebScraperConfig(urls=["https://example.com/missing"])
        connector = WebScraperConnector(config)
        connector._session = mock_session
        mock_session.get.return_value = make_mock_response("", status=404)

        documents = await connector.fetch()

        assert documents == []

    @pytest.mark.asyncio
    async def test_fetch_stable_document_ids(self, mock_session):
        """Same URL always produces the same document ID."""
        config = WebScraperConfig(urls=["https://example.com"])
        connector = WebScraperConnector(config)
        connector._session = mock_session
        mock_session.get.return_value = make_mock_response(SAMPLE_HTML)

        docs_first = await connector.fetch()
        mock_session.get.return_value = make_mock_response(SAMPLE_HTML)
        docs_second = await connector.fetch()

        assert docs_first[0].id == docs_second[0].id

    @pytest.mark.asyncio
    async def test_fetch_deduplicates_urls(self, mock_session):
        """Duplicate URLs in config are only fetched once."""
        config = WebScraperConfig(
            urls=["https://example.com", "https://example.com/"],
            follow_links=False,
        )
        connector = WebScraperConnector(config)
        connector._session = mock_session
        mock_session.get.return_value = make_mock_response(SAMPLE_HTML)

        documents = await connector.fetch()

        assert len(documents) == 1

    @pytest.mark.asyncio
    async def test_fetch_multiple_urls(self, mock_session):
        config = WebScraperConfig(
            urls=["https://example.com/page1", "https://example.com/page2"],
            follow_links=False,
        )
        connector = WebScraperConnector(config)
        connector._session = mock_session

        responses = [
            make_mock_response("<html><body><p>Page 1 content</p></body></html>"),
            make_mock_response("<html><body><p>Page 2 content</p></body></html>"),
        ]
        mock_session.get.side_effect = responses

        documents = await connector.fetch()

        assert len(documents) == 2


class TestWebScraperLinkExtraction:
    """Test internal link discovery."""

    def test_extract_same_origin_links(self):
        config = WebScraperConfig(urls=["https://example.com"])
        connector = WebScraperConnector(config)

        links = connector._extract_links(SAMPLE_HTML, "https://example.com")

        # Should include same-origin relative links
        assert "https://example.com/overview" in links
        assert "https://example.com/api/reference" in links

        # Should NOT include external links
        assert not any("external.com" in link for link in links)

    def test_skip_fragment_links(self):
        html = '<a href="#section">Jump</a>'
        config = WebScraperConfig(urls=["https://example.com"])
        connector = WebScraperConnector(config)

        links = connector._extract_links(html, "https://example.com")

        assert links == []

    def test_skip_javascript_links(self):
        html = '<a href="javascript:void(0)">Click</a>'
        config = WebScraperConfig(urls=["https://example.com"])
        connector = WebScraperConnector(config)

        links = connector._extract_links(html, "https://example.com")

        assert links == []


class TestWebScraperTextExtraction:
    """Test HTML-to-text extraction."""

    def test_extract_text_removes_script_tags(self):
        text = WebScraperConnector._extract_text(SAMPLE_HTML_2)
        assert "var x = 1" not in text
        assert "Overview content here" in text

    def test_extract_text_removes_nav_tags(self):
        text = WebScraperConnector._extract_text(SAMPLE_HTML_2)
        assert "Nav items" not in text

    def test_extract_title(self):
        title = WebScraperConnector._extract_title(SAMPLE_HTML)
        assert title == "Enterprise AI Docs"

    def test_extract_title_missing(self):
        title = WebScraperConnector._extract_title("<html><body>No title</body></html>")
        assert title is None
