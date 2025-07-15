#!/usr/bin/env python3
"""
Script to fix chat display references in chat_tab.py
"""

import re

# Read the file
with open('pyside_chat/ui/tabs/chat_tab/chat_tab.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences of chat_display.chat_display with chat_display.scroll_area
content = re.sub(r'self\.chat_display\.chat_display', 'self.chat_display.scroll_area', content)

# Write the file back
with open('pyside_chat/ui/tabs/chat_tab/chat_tab.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed chat display references in chat_tab.py") 