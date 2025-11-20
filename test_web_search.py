#!/usr/bin/env python3
"""
Test web search functionality with UK/English settings
"""

import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from SRC.services import WebSearchService
    print("✓ WebSearchService imported successfully")

    # Create and test web search
    search_service = WebSearchService(max_results=3)
    print("✓ WebSearchService instantiated")

    # Test search
    query = "current news in UK"
    print(f"\n🔍 Testing web search for: '{query}'")

    try:
        results = search_service.search_sync(query)
        print(f"✓ Search completed, found {len(results)} results")

        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   {result['body'][:100]}...")
            print(f"   Source: {result['href']}")

        # Test formatting
        formatted = search_service.format_results_for_chat(query, results)
        print(f"\n📝 Formatted results length: {len(formatted)} characters")

    except Exception as e:
        print(f"✗ Search failed: {e}")
        import traceback
        traceback.print_exc()

except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("Make sure duckduckgo-search is installed: pip install duckduckgo-search>=5.0.0")
