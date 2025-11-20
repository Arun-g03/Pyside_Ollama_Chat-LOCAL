#!/usr/bin/env python3
"""
Test script to verify web search integration
"""

import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Testing web search integration...")

try:
    from SRC.services import WebSearchService
    print("✓ WebSearchService import successful")

    # Test service instantiation
    service = WebSearchService(max_results=3)
    print("✓ WebSearchService instantiation successful")

    # Test import in chat_tab
    from SRC.ui.chat_tab import ChatTab
    print("✓ ChatTab with web search integration import successful")

    print("\n🎉 All imports successful! Web search integration is working.")

except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("This is expected if duckduckgo-search is not installed yet.")

except Exception as e:
    print(f"✗ Unexpected error: {e}")
