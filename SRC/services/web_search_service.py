"""
Web Search Service - DuckDuckGo Web Search Integration
Provides web search capabilities for the chat system.
"""

import asyncio
from typing import List, Dict, Optional, Any
from duckduckgo_search import DDGS
from PySide6.QtCore import QObject, Signal
from SRC.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)
logger.info("WebSearchService logger initialized")


class WebSearchService(QObject):
    """Service for handling web search operations using DuckDuckGo"""

    # Signals for async operations
    search_started = Signal(str)  # Emits search query
    search_completed = Signal(list)  # Emits list of search results
    search_error = Signal(str)  # Emits error message

    def __init__(self, max_results: int = 5, region: str = 'uk-en'):
        super().__init__()
        self.max_results = max_results
        self.region = region  # uk-en for UK English results
        self.ddgs = None

    def _initialize_ddgs(self):
        """Initialize DuckDuckGo search instance if not already done"""
        if self.ddgs is None:
            try:
                # Configure DDGS for English/UK results
                self.ddgs = DDGS()
                logger.info("DuckDuckGo search initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize DuckDuckGo search: {e}")
                raise

    def search_sync(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Perform synchronous web search

        Args:
            query: Search query string
            max_results: Maximum number of results to return (overrides instance default)

        Returns:
            List of search result dictionaries with keys: title, href, body
        """
        try:
            self.search_started.emit(query)
            logger.info(f"Starting web search for: '{query}'")

            self._initialize_ddgs()

            results_limit = max_results or self.max_results

            # Perform the search with UK region and safesearch off for better results
            results = list(self.ddgs.text(query, max_results=results_limit, region='uk-en', safesearch='off'))

            logger.info(f"Web search completed. Found {len(results)} results")

            # Format results
            formatted_results = []
            for result in results:
                formatted_result = {
                    'title': result.get('title', ''),
                    'href': result.get('href', ''),
                    'body': result.get('body', ''),
                    'source': 'DuckDuckGo'
                }
                formatted_results.append(formatted_result)

            self.search_completed.emit(formatted_results)
            return formatted_results

        except Exception as e:
            error_msg = f"Web search failed: {str(e)}"
            logger.error(error_msg)
            self.search_error.emit(error_msg)
            return []

    async def search_async(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Perform asynchronous web search

        Args:
            query: Search query string
            max_results: Maximum number of results to return (overrides instance default)

        Returns:
            List of search result dictionaries
        """
        try:
            self.search_started.emit(query)
            logger.info(f"Starting async web search for: '{query}'")

            self._initialize_ddgs()

            results_limit = max_results or self.max_results

            # Perform async search with UK region and safesearch off
            results = []
            async for result in self.ddgs.atext(query, max_results=results_limit, region='uk-en', safesearch='off'):
                results.append(result)

            logger.info(f"Async web search completed. Found {len(results)} results")

            # Format results
            formatted_results = []
            for result in results:
                formatted_result = {
                    'title': result.get('title', ''),
                    'href': result.get('href', ''),
                    'body': result.get('body', ''),
                    'source': 'DuckDuckGo'
                }
                formatted_results.append(formatted_result)

            self.search_completed.emit(formatted_results)
            return formatted_results

        except Exception as e:
            error_msg = f"Async web search failed: {str(e)}"
            logger.error(error_msg)
            self.search_error.emit(error_msg)
            return []

    def extract_search_summary(self, results: List[Dict[str, Any]]) -> str:
        """
        Extract a summary from search results for use in chat context

        Args:
            results: List of search result dictionaries

        Returns:
            Formatted summary string
        """
        if not results:
            return "No search results found."

        summary_parts = []
        summary_parts.append(f"Web search results ({len(results)} found):")

        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            body = result.get('body', '')[:200] + '...' if len(result.get('body', '')) > 200 else result.get('body', '')
            href = result.get('href', '')

            summary_parts.append(f"{i}. {title}")
            if body:
                summary_parts.append(f"   {body}")
            if href:
                summary_parts.append(f"   Source: {href}")
            summary_parts.append("")  # Empty line between results

        return "\n".join(summary_parts)

    def format_results_for_chat(self, query: str, results: List[Dict[str, Any]]) -> str:
        """
        Format search results in a chat-friendly format

        Args:
            query: Original search query
            results: List of search result dictionaries

        Returns:
            Formatted string suitable for chat context
        """
        if not results:
            return f"I searched for '{query}' but found no results."

        formatted = f"Here are the top {len(results)} web search results for '{query}':\n\n"

        for i, result in enumerate(results, 1):
            title = result.get('title', 'Untitled')
            body = result.get('body', 'No description available')
            href = result.get('href', '')

            formatted += f"**{i}. {title}**\n"
            formatted += f"{body}\n"
            if href:
                formatted += f"🔗 {href}\n"
            formatted += "\n"

        return formatted
