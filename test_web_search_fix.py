#!/usr/bin/env python3
"""
Test the fixed web search functionality
"""

import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from SRC.services import WebSearchService
    print("✓ WebSearchService imported successfully")

    # Create web search service
    search_service = WebSearchService(max_results=3)
    print("✓ WebSearchService instantiated")

    # Test search with UK news query
    query = "UK news today"
    print(f"\n🔍 Testing web search for: '{query}'")

    try:
        results = search_service.search_sync(query)
        print(f"✓ Search completed, found {len(results)} results")

        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            href = result.get('href', 'No URL')
            print(f"\n{i}. {title}")
            print(f"   URL: {href}")

            # Check if result is in English (not Dutch)
            body = result.get('body', '')
            if 'WIA' in title or 'uitkering' in body:
                print("   ⚠️  WARNING: Still getting Dutch results!")
            else:
                print("   ✓ English result detected")

        # Test the concise formatting
        concise_context = f"\n\nWeb Search Context ({len(results)} results found):\n"
        for i, result in enumerate(results[:3], 1):
            title = result.get('title', 'Untitled')[:80]
            body = result.get('body', '')[:150]
            concise_context += f"{i}. {title}: {body}\n"

        print(f"\n📝 Concise context length: {len(concise_context)} characters")
        print("Sample context:")
        print(concise_context[:300] + "...")

    except Exception as e:
        print(f"✗ Search failed: {e}")
        import traceback
        traceback.print_exc()

except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("Make sure duckduckgo-search is installed: pip install duckduckgo-search>=5.0.0")
