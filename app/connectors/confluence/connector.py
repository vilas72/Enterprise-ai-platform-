from __future__ import annotations

from datetime import datetime
from typing import Any

from app.connectors.confluence.client import ConfluenceClient
from app.connectors.confluence.models import (
    ConfluencePage,
    ConfluenceSearchResponse,
    ConfluenceSearchResult,
    ConfluenceSpace,
)


class ConfluenceConnector:
    """
    Enterprise Confluence connector.

    Responsibilities
    ----------------

    • Space operations

    • Page operations

    • Enterprise search

    • Documentation retrieval

    • Knowledge discovery

    The connector exposes enterprise domain models rather than
    raw Confluence REST payloads.
    """

    def __init__(
        self,
        client: ConfluenceClient,
    ) -> None:

        self._client = client

    # ==========================================================
    # Space Operations
    # ==========================================================

    async def get_space(
        self,
        key: str,
    ) -> ConfluenceSpace:
        """
        Retrieve a Confluence space.
        """

        response = await self._client.get(
            f"/wiki/api/v2/spaces/{key}"
        )

        return self._to_space(response)

    async def list_spaces(
        self,
        *,
        limit: int = 100,
    ) -> list[ConfluenceSpace]:
        """
        List accessible spaces.
        """

        response = await self._client.get(
            "/wiki/api/v2/spaces",
            params={
                "limit": limit,
            },
        )

        results = response.get(
            "results",
            [],
        )

        return [
            self._to_space(item)
            for item in results
        ]

    async def space_exists(
        self,
        key: str,
    ) -> bool:
        """
        Returns True if the space exists.
        """

        try:

            await self.get_space(key)

            return True

        except Exception:

            return False

    # ==========================================================
    # Utilities
    # ==========================================================

    @staticmethod
    def _parse_datetime(
        value: str | None,
    ) -> datetime | None:
        """
        Parse Confluence ISO datetime.
        """

        if value is None:

            return None

        return datetime.fromisoformat(
            value.replace(
                "Z",
                "+00:00",
            )
        )
    
        # ==========================================================
    # Page Operations
    # ==========================================================

    async def get_page(
        self,
        page_id: str,
        *,
        include_body: bool = True,
    ) -> ConfluencePage:
        """
        Retrieve a Confluence page.
        """

        params: dict[str, Any] = {}

        if include_body:
            params["body-format"] = "storage"

        response = await self._client.get(
            f"/wiki/api/v2/pages/{page_id}",
            params=params,
        )

        return self._to_page(response)

    async def get_page_by_title(
        self,
        *,
        space_key: str,
        title: str,
    ) -> ConfluencePage | None:
        """
        Retrieve a page using its title within a space.
        """

        cql = (
            f'space="{space_key}" '
            f'AND title="{title}"'
        )

        response = await self.search_cql(
            cql,
            limit=1,
        )

        if response.total == 0:
            return None

        return response.results[0].page

    async def list_pages(
        self,
        *,
        space_key: str,
        limit: int = 100,
    ) -> list[ConfluencePage]:
        """
        List pages inside a space.
        """

        response = await self._client.get(
            "/wiki/api/v2/pages",
            params={
                "spaceKey": space_key,
                "limit": limit,
            },
        )

        return [
            self._to_page(item)
            for item in response.get(
                "results",
                [],
            )
        ]

    async def list_child_pages(
        self,
        page_id: str,
        *,
        limit: int = 100,
    ) -> list[ConfluencePage]:
        """
        List child pages.
        """

        response = await self._client.get(
            f"/wiki/api/v2/pages/{page_id}/children",
            params={
                "limit": limit,
            },
        )

        return [
            self._to_page(item)
            for item in response.get(
                "results",
                [],
            )
        ]

    async def page_exists(
        self,
        page_id: str,
    ) -> bool:
        """
        Returns True if the page exists.
        """

        try:

            await self.get_page(
                page_id,
                include_body=False,
            )

            return True

        except Exception:

            return False

    async def get_page_content(
        self,
        page_id: str,
    ) -> str:
        """
        Retrieve the storage body of a page.
        """

        page = await self.get_page(
            page_id,
            include_body=True,
        )

        return page.body or ""

    async def get_page_summary(
        self,
        page_id: str,
    ) -> ConfluencePage:
        """
        Retrieve page metadata without body expansion.
        """

        return await self.get_page(
            page_id,
            include_body=False,
        )
    
        # ==========================================================
    # Page Operations
    # ==========================================================

    async def get_page(
        self,
        page_id: str,
        *,
        include_body: bool = True,
    ) -> ConfluencePage:
        """
        Retrieve a Confluence page.
        """

        params: dict[str, Any] = {}

        if include_body:
            params["body-format"] = "storage"

        response = await self._client.get(
            f"/wiki/api/v2/pages/{page_id}",
            params=params,
        )

        return self._to_page(response)

    async def get_page_by_title(
        self,
        *,
        space_key: str,
        title: str,
    ) -> ConfluencePage | None:
        """
        Retrieve a page using its title within a space.
        """

        cql = (
            f'space="{space_key}" '
            f'AND title="{title}"'
        )

        response = await self.search_cql(
            cql,
            limit=1,
        )

        if response.total == 0:
            return None

        return response.results[0].page

    async def list_pages(
        self,
        *,
        space_key: str,
        limit: int = 100,
    ) -> list[ConfluencePage]:
        """
        List pages inside a space.
        """

        response = await self._client.get(
            "/wiki/api/v2/pages",
            params={
                "spaceKey": space_key,
                "limit": limit,
            },
        )

        return [
            self._to_page(item)
            for item in response.get(
                "results",
                [],
            )
        ]

    async def list_child_pages(
        self,
        page_id: str,
        *,
        limit: int = 100,
    ) -> list[ConfluencePage]:
        """
        List child pages.
        """

        response = await self._client.get(
            f"/wiki/api/v2/pages/{page_id}/children",
            params={
                "limit": limit,
            },
        )

        return [
            self._to_page(item)
            for item in response.get(
                "results",
                [],
            )
        ]

    async def page_exists(
        self,
        page_id: str,
    ) -> bool:
        """
        Returns True if the page exists.
        """

        try:

            await self.get_page(
                page_id,
                include_body=False,
            )

            return True

        except Exception:

            return False

    async def get_page_content(
        self,
        page_id: str,
    ) -> str:
        """
        Retrieve the storage body of a page.
        """

        page = await self.get_page(
            page_id,
            include_body=True,
        )

        return page.body or ""

    async def get_page_summary(
        self,
        page_id: str,
    ) -> ConfluencePage:
        """
        Retrieve page metadata without body expansion.
        """

        return await self.get_page(
            page_id,
            include_body=False,
        )
        
        # ==========================================================
    # Mapping
    # ==========================================================

    @staticmethod
    def _to_space(
        payload: dict[str, Any],
    ) -> ConfluenceSpace:
        """
        Convert a Confluence REST payload into a
        ConfluenceSpace domain model.
        """

        homepage = payload.get("homepage") or {}

        links = payload.get("_links") or {}

        description = payload.get("description") or {}

        return ConfluenceSpace(
            id=str(payload.get("id", "")),
            key=payload.get("key", ""),
            name=payload.get("name", ""),
            type=payload.get("type"),
            description=description.get(
                "plain",
                {}).get(
                    "value",
                    None,
                )
                if isinstance(description, dict)
                else None,
            homepage_id=homepage.get("id"),
            web_url=links.get("webui"),
            metadata=payload.copy(),
        )

    def _to_page(
        self,
        payload: dict[str, Any],
    ) -> ConfluencePage:
        """
        Convert a Confluence REST payload into a
        ConfluencePage domain model.
        """

        space = payload.get("space") or {}

        version = payload.get("version")

        links = payload.get("_links") or {}

        body = payload.get("body") or {}

        storage = body.get("storage") or {}

        parent_id = None

        ancestors = payload.get("ancestors") or []

        if ancestors:
            parent_id = str(
                ancestors[-1].get("id")
            )

        return ConfluencePage(
            id=str(payload.get("id", "")),
            title=payload.get("title", ""),
            type=payload.get(
                "type",
                "page",
            ),
            status=payload.get(
                "status",
                "current",
            ),
            space_key=space.get(
                "key",
                "",
            ),
            space_name=space.get(
                "name",
            ),
            parent_id=parent_id,
            version=(
                self._to_version(version)
                if version
                else None
            ),
            body=storage.get(
                "value",
            ),
            web_url=links.get(
                "webui",
            ),
            created_at=self._parse_datetime(
                payload.get(
                    "createdAt",
                )
            ),
            updated_at=self._parse_datetime(
                payload.get(
                    "updatedAt",
                )
            ),
            metadata=payload.copy(),
        )

    def _to_version(
        self,
        payload: dict[str, Any],
    ) -> ConfluenceVersion:
        """
        Convert version payload.
        """

        author = payload.get("author") or {}

        return ConfluenceVersion(
            number=payload.get(
                "number",
                1,
            ),
            author=author.get(
                "displayName",
            ),
            created_at=self._parse_datetime(
                payload.get(
                    "createdAt",
                )
            ),
            message=payload.get(
                "message",
            ),
        )

    @staticmethod
    def _to_label(
        payload: dict[str, Any],
    ) -> ConfluenceLabel:
        """
        Convert label payload.
        """

        return ConfluenceLabel(
            id=str(
                payload.get(
                    "id",
                    "",
                )
            ),
            name=payload.get(
                "name",
                "",
            ),
            prefix=payload.get(
                "prefix",
            ),
        )

    @staticmethod
    def _to_attachment(
        payload: dict[str, Any],
    ) -> ConfluenceAttachment:
        """
        Convert attachment payload.
        """

        metadata = payload.get(
            "metadata",
            {},
        )

        extensions = metadata.get(
            "extensions",
            {},
        )

        links = payload.get(
            "_links",
            {},
        )

        return ConfluenceAttachment(
            id=str(payload.get("id", "")),
            title=payload.get(
                "title",
                "",
            ),
            media_type=metadata.get(
                "mediaType",
            ),
            file_size=extensions.get(
                "fileSize",
            ),
            download_url=links.get(
                "download",
            ),
            metadata=payload.copy(),
        )
        
        # ==========================================================
    # Utilities
    # ==========================================================

    async def get_page_tree(
        self,
        page_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve a lightweight page hierarchy.

        Returns the requested page and its immediate children.
        """

        page = await self.get_page(
            page_id,
            include_body=False,
        )

        children = await self.list_child_pages(
            page_id,
        )

        return {
            "page": page,
            "children": children,
        }

    async def documentation_statistics(
        self,
        *,
        space_key: str,
    ) -> dict[str, Any]:
        """
        Generate documentation statistics for a space.
        """

        pages = await self.list_pages(
            space_key=space_key,
        )

        return {
            "space": space_key,
            "total_pages": len(pages),
            "pages_with_content": len(
                [
                    page
                    for page in pages
                    if page.body
                ]
            ),
            "pages_without_content": len(
                [
                    page
                    for page in pages
                    if not page.body
                ]
            ),
        }

    async def connector_health(
        self,
    ) -> dict[str, Any]:
        """
        Perform a lightweight connector health check.
        """

        try:

            spaces = await self.list_spaces(
                limit=1,
            )

            return {
                "healthy": True,
                "spaces_accessible": len(spaces),
            }

        except Exception as exc:

            return {
                "healthy": False,
                "error": str(exc),
            }

    # ==========================================================
    # Lifecycle
    # ==========================================================

    async def close(
        self,
    ) -> None:
        """
        Release HTTP resources.
        """

        await self._client.close()
        
    