#!/usr/bin/env python3
"""
Test script to verify list formatting fixes
"""

import re

def test_list_formatting():
    """Test the list formatting with the problematic message"""
    
    # Test message with concatenated list items
    test_message = """Here is a well-organized list of natural items, categorized for clarity:

1. **Fruits** - Apples - Pears - Grapes2. **Vegetables** - Broccoli - Carrots - Spinach3. **Nuts and Seeds** - Almonds - Walnuts4. **Fish** - Salmon - Tuna - Sardines

This list encompasses a variety of natural items, providing both plant-based and animal-based examples that are commonly found in nature and used daily."""

    print("=== ORIGINAL MESSAGE ===")
    print(test_message)
    print("\n" + "="*80 + "\n")
    
    # Test the list formatting logic
    def _format_lists(message: str) -> str:
        """Format both ordered and unordered lists properly."""
        # First, handle concatenated list items (items without proper line breaks)
        # Split on numbered list patterns to separate items
        message = re.sub(r'(\d+)\.\s+', r'\n\1. ', message)
        
        # Also handle cases where items are concatenated without spaces
        # e.g., "1.**Fruits**-Apples-Pears" should become "1. **Fruits** - Apples - Pears"
        message = re.sub(r'(\d+)\.\*\*', r'\1. **', message)
        message = re.sub(r'\*\*([^*]+)\*\*([A-Za-z])', r'**\1** - \2', message)
        
        print("=== AFTER INITIAL CLEANUP ===")
        print(message)
        print("\n" + "="*80 + "\n")
        
        lines = message.split('\n')
        formatted_lines = []
        in_ordered_list = False
        in_unordered_list = False
        ordered_items = []
        unordered_items = []

        for line in lines:
            stripped_line = line.strip()
            
            # Check for ordered list items (1. 2. 3. etc.)
            ordered_match = re.match(r'^(\d+)\.\s+(.+)$', stripped_line)
            # Check for unordered list items (- * •)
            unordered_match = re.match(r'^[-*•]\s+(.+)$', stripped_line)
            
            if ordered_match:
                # Start or continue ordered list
                if not in_ordered_list:
                    # Close any existing unordered list
                    if in_unordered_list and unordered_items:
                        formatted_lines.append(
                            f'<ul style="list-style-type: none; padding-left: 20px; margin: 15px 0; border-left: 2px solid #444;">')
                        formatted_lines.extend(unordered_items)
                        formatted_lines.append('</ul>')
                        unordered_items = []
                        in_unordered_list = False
                    
                    in_ordered_list = True
                    ordered_items = []
                
                content = ordered_match.group(2)
                ordered_items.append(f'<li style="margin: 8px 0; padding-left: 5px; color: #e2e8f0;">{content}</li>')
                
            elif unordered_match:
                # Start or continue unordered list
                if not in_unordered_list:
                    # Close any existing ordered list
                    if in_ordered_list and ordered_items:
                        formatted_lines.append(
                            f'<ol style="padding-left: 20px; margin: 15px 0; border-left: 2px solid #444;">')
                        formatted_lines.extend(ordered_items)
                        formatted_lines.append('</ol>')
                        ordered_items = []
                        in_ordered_list = False
                    
                    in_unordered_list = True
                    unordered_items = []
                
                content = unordered_match.group(1)
                unordered_items.append(f'<li style="margin: 8px 0; padding-left: 5px; color: #e2e8f0;">{content}</li>')
                
            else:
                # Not a list item, close any existing lists
                if in_ordered_list and ordered_items:
                    formatted_lines.append(
                        f'<ol style="padding-left: 20px; margin: 15px 0; border-left: 2px solid #444;">')
                    formatted_lines.extend(ordered_items)
                    formatted_lines.append('</ol>')
                    ordered_items = []
                    in_ordered_list = False
                
                if in_unordered_list and unordered_items:
                    formatted_lines.append(
                        f'<ul style="list-style-type: none; padding-left: 20px; margin: 15px 0; border-left: 2px solid #444;">')
                    formatted_lines.extend(unordered_items)
                    formatted_lines.append('</ul>')
                    unordered_items = []
                    in_unordered_list = False
                
                formatted_lines.append(line)

        # Handle any remaining list items
        if in_ordered_list and ordered_items:
            formatted_lines.append(
                f'<ol style="padding-left: 20px; margin: 15px 0; border-left: 2px solid #444;">')
            formatted_lines.extend(ordered_items)
            formatted_lines.append('</ol>')
        
        if in_unordered_list and unordered_items:
            formatted_lines.append(
                f'<ul style="list-style-type: none; padding-left: 20px; margin: 15px 0; border-left: 2px solid #444;">')
            formatted_lines.extend(unordered_items)
            formatted_lines.append('</ul>')

        return '\n'.join(formatted_lines)
    
    # Test the formatting
    result = _format_lists(test_message)
    
    print("=== AFTER LIST FORMATTING ===")
    print(result)

if __name__ == "__main__":
    test_list_formatting() 