"""
Message Formatter - Extracted from ollama_chat.py
Handles message formatting, code highlighting, and HTML processing.
"""

import re
from html import escape, unescape
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class MessageFormatter:
    """Utility class for formatting messages with code highlighting and HTML processing"""
    
    # Define colors locally to avoid circular import
    COLORS = {
        'user_bubble': '#1a3a5d',
        'ai_bubble': '#374151', 
        'system_bubble': '#1a1a1a',
        'thinking_bubble': '#23272e',
        'thought_bubble': '#1a1a1a',
        'user_text': '#ffffff',
        'ai_text': '#e2e8f0',
        'system_text': '#666666',
        'thinking_text': '#aaaaaa',
        'thought_text': '#ffffff',
        'cursor': '#888888',
        'border': '#444444',
        'border_light': '#555555',
        'border_dark': '#333333',
        'code_background': '#2d2d2d',
        'code_text': '#dcdcdc',
        'code_border': '#444444',
        'inline_code_bg': '#2d2d2d',
        'inline_code_text': '#dcdcaa',
        'header_primary': '#ffffff',
        'header_secondary': '#4a9eff',
        'bold_text': '#ffd700',
        'italic_text': '#cccccc',
        'link_color': '#4a9eff',
    }
    
    @staticmethod
    def detect_code_in_message(message: str) -> bool:
        """
        Detect if a message contains code blocks or inline code.
        Returns True if code is detected, False otherwise.
        """
        # Check for block code (triple backticks)
        if re.search(r'```.*?```', message, re.DOTALL):
            return True
        
        # Check for inline code (single backticks)
        if re.search(r'`[^`]+`', message):
            return True
        
        # Check for common code patterns
        code_patterns = [
            r'\b(def|class|function|import|from|if|else|elif|for|while|try|except|finally|with|as)\b',
            r'[{}();=<>+\-*/]',  # Common code symbols
            r'\b(print|return|break|continue|pass|raise)\b',
            r'\b(var|let|const|function|if|else|for|while|try|catch|finally)\b',  # JavaScript
            r'\b(public|private|protected|static|final|abstract|interface|extends|implements)\b',  # Java
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, message):
                return True
        
        return False
    
    @staticmethod
    def detect_code_type(message: str):
        """
        Detects the programming language of a code block using Pygments.
        """
        try:
            lexer = guess_lexer(message)  # Automatically detect the lexer based on code content
            return lexer
        except Exception as e:
            logger.debug(f"Error detecting code type: {e}",print_to_terminal=True)
            return None
    
    @staticmethod
    def syntax_highlight_code(message: str, language: str = None) -> str:
        """
        Highlight the code using Pygments and return formatted HTML.
        """
        try:
            if language:
                # Try to get lexer by name first
                try:
                    lexer = get_lexer_by_name(language)
                except:
                    # Fallback to guessing
                    lexer = MessageFormatter.detect_code_type(message)
            else:
                lexer = MessageFormatter.detect_code_type(message)
                
            if lexer is None:
                # Fallback to text lexer if no language detected
                lexer = get_lexer_by_name('text')
            
            # Use Pygments to apply syntax highlighting with better styling
            formatter = HtmlFormatter(
                style="monokai", 
                full=True, 
                noclasses=True,
                nobackground=True,  # Don't add background to individual tokens
                prestyles="margin: 0; padding: 0; font-family: 'Consolas', 'Monaco', 'Courier New', monospace; font-size: 13px; line-height: 1.4;"
            )
            highlighted_code = highlight(message, lexer, formatter)
            
            return highlighted_code
            
        except Exception as e:
            logger.debug(f"Error highlighting code: {e}",print_to_terminal=True)
            # Return escaped code as fallback
            return escape(message)
    
    @staticmethod
    def detect_and_format_code(message: str) -> str:
        """
        Detects code and applies formatting. Highlights syntax using Pygments.
        It handles inline and block code wrapped in backticks (```) and applies syntax highlighting.
        """
        # Format block code (triple backticks) with optional language identifier
        # This regex captures: ```language\ncode``` or ```\ncode```
        block_code_pattern = re.compile(r'```(\w+)?\n?(.*?)```', re.DOTALL)
        formatted_message = message

        def format_block_code(match):
            language = match.group(1)  # Language identifier (may be None)
            code_content = match.group(2).strip()  # Get the content inside the block
            
            # Apply syntax highlighting
            highlighted_code = MessageFormatter.syntax_highlight_code(code_content, language)
            
            # Create code block HTML directly
            language_label = ""
            if language:
                language_label = f'<div style="background-color: #1e1e1e; color: #dcdcdc; padding: 5px 10px; border-bottom: 1px solid #444; font-family: monospace; font-size: 11px; text-transform: uppercase;">{language}</div>'
            
            return (
                f'<div style="background-color: #2d2d2d; border-radius: 5px; overflow: hidden; margin: 10px 0; border: 1px solid #444;">'
                f'{language_label}'
                f'<div style="padding: 10px; color: #dcdcdc; font-family: \'Consolas\', \'Monaco\', \'Courier New\', monospace; font-size: 13px; line-height: 1.4; overflow-x: auto;">{highlighted_code}</div>'
                '</div>'
            )

        # Replace block code with formatted HTML
        formatted_message = re.sub(block_code_pattern, format_block_code, formatted_message)

        # Format inline code (single backticks) - but avoid formatting if it's inside a code block
        # Use a simpler approach to avoid double-formatting
        inline_code_pattern = re.compile(r'`([^`]+)`')
        formatted_message = re.sub(inline_code_pattern, lambda m: f'<code style="background-color: #2d2d2d; color: #dcdcaa; padding: 2px 4px; border-radius: 3px; font-family: \'Consolas\', \'Monaco\', \'Courier New\', monospace; font-size: 12px;">{m.group(1)}</code>', formatted_message)

        return formatted_message
    
    @staticmethod
    def _protect_code_blocks(message: str):
        """Helper function to protect code blocks from processing"""
        code_blocks = []
        
        def protect_code_blocks(match):
            code_blocks.append(match.group(0))
            return f"__CODE_BLOCK_{len(code_blocks)-1}__"
        
        # Protect code blocks
        protected_message = re.sub(r'<code[^>]*>.*?</code>', protect_code_blocks, message, flags=re.DOTALL)
        protected_message = re.sub(r'<pre[^>]*>.*?</pre>', protect_code_blocks, protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<div[^>]*style="background-color: #2d2d2d[^>]*>.*?</div>', protect_code_blocks, protected_message, flags=re.DOTALL)
        
        return protected_message, code_blocks

    @staticmethod
    def format_markdown(message: str) -> str:
        """
        Enhanced markdown formatting for better AI output presentation.
        Handles headers, lists, emphasis, and other markdown elements.
        """
        # First, identify and protect code blocks
        protected_message, code_blocks = MessageFormatter._protect_code_blocks(message)
        
        # Clean up excessive horizontal rules and separators
        protected_message = re.sub(r'---\s*---\s*---', '---', protected_message)
        protected_message = re.sub(r'---\s*###', '###', protected_message)
        
        # Format headers with consistent styling using local colors
        protected_message = re.sub(r'^###\s+(.+)$', f'<h3 style="font-size: 18px; font-weight: bold; color: {MessageFormatter.COLORS["header_secondary"]}; margin: 20px 0 10px 0; padding: 8px 0; border-bottom: 1px solid {MessageFormatter.COLORS["border"]};">\\1</h3>', protected_message, flags=re.MULTILINE)
        protected_message = re.sub(r'^##\s+(.+)$', f'<h2 style="font-size: 20px; font-weight: bold; color: {MessageFormatter.COLORS["header_primary"]}; margin: 25px 0 15px 0; padding: 10px 0; border-bottom: 2px solid {MessageFormatter.COLORS["border_light"]};">\\1</h2>', protected_message, flags=re.MULTILINE)
        protected_message = re.sub(r'^#\s+(.+)$', f'<h1 style="font-size: 24px; font-weight: bold; color: {MessageFormatter.COLORS["header_primary"]}; margin: 30px 0 20px 0; padding: 12px 0; border-bottom: 3px solid {MessageFormatter.COLORS["border_dark"]};">\\1</h1>', protected_message, flags=re.MULTILINE)
        
        # Format horizontal rules
        protected_message = re.sub(r'^---$', f'<hr style="border: none; border-top: 1px solid {MessageFormatter.COLORS["border"]}; margin: 20px 0;">', protected_message, flags=re.MULTILINE)
        
        # Format unordered lists with better styling
        protected_message = re.sub(r'^\s*[-*•]\s+(.+)$', f'<li style="margin: 8px 0; padding-left: 5px; color: {MessageFormatter.COLORS["ai_text"]};">\\1</li>', protected_message, flags=re.MULTILINE)
        
        # Group consecutive list items into proper lists
        lines = protected_message.split('\n')
        formatted_lines = []
        in_list = False
        list_items = []
        
        for line in lines:
            if line.strip().startswith('<li'):
                if not in_list:
                    in_list = True
                    list_items = []
                list_items.append(line)
            else:
                if in_list and list_items:
                    # Close the previous list
                    formatted_lines.append(f'<ul style="list-style-type: none; padding-left: 20px; margin: 15px 0; border-left: 2px solid {MessageFormatter.COLORS["border"]};">')
                    formatted_lines.extend(list_items)
                    formatted_lines.append('</ul>')
                    list_items = []
                    in_list = False
                formatted_lines.append(line)
        
        # Handle any remaining list items
        if in_list and list_items:
            formatted_lines.append(f'<ul style="list-style-type: none; padding-left: 20px; margin: 15px 0; border-left: 2px solid {MessageFormatter.COLORS["border"]};">')
            formatted_lines.extend(list_items)
            formatted_lines.append('</ul>')
        
        protected_message = '\n'.join(formatted_lines)
        
        # Format bold text (reduce excessive bold usage)
        protected_message = re.sub(r'\*\*(.+?)\*\*', f'<strong style="color: {MessageFormatter.COLORS["bold_text"]}; font-weight: 600;">\\1</strong>', protected_message)
        
        # Format italic text
        protected_message = re.sub(r'\*(.+?)\*', f'<em style="color: {MessageFormatter.COLORS["italic_text"]}; font-style: italic;">\\1</em>', protected_message)
        
        # Format inline code using local styling
        protected_message = re.sub(r'`([^`]+)`', lambda m: f'<code style="background-color: {MessageFormatter.COLORS["inline_code_bg"]}; color: {MessageFormatter.COLORS["inline_code_text"]}; padding: 2px 4px; border-radius: 3px; font-family: \'Consolas\', \'Monaco\', \'Courier New\', monospace; font-size: 12px;">{m.group(1)}</code>', protected_message)
        
        # Add paragraph spacing for better readability
        protected_message = re.sub(r'\n\n+', '</p><p style="margin: 12px 0; line-height: 1.6;">', protected_message)
        protected_message = '<p style="margin: 12px 0; line-height: 1.6;">' + protected_message + '</p>'
        
        # Clean up empty paragraphs
        protected_message = re.sub(r'<p[^>]*>\s*</p>', '', protected_message)
        
        return protected_message
    
    @staticmethod
    def handle_html_tags(message: str) -> str:
        """
        Properly handle HTML tags in messages - escape them for display when they're part of discussions
        but preserve actual formatting tags and code blocks.
        """
        # First, identify and protect code blocks (they may contain HTML tags that should be displayed, not interpreted)
        protected_message, code_blocks = MessageFormatter._protect_code_blocks(message)
        
        # Handle formatting tags we want to preserve with better styling using local colors
        protected_message = re.sub(r'<ul>(.*?)</ul>', f'<ul style="list-style-type: disc; padding-left: 20px; margin: 10px 0;">\\1</ul>', protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<ol>(.*?)</ol>', f'<ol style="padding-left: 20px; margin: 10px 0;">\\1</ol>', protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<li>(.*?)</li>', f'<li style="margin: 5px 0;">\\1</li>', protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<b>(.*?)</b>', f'<b style="font-weight: bold; color: {MessageFormatter.COLORS["header_primary"]};">\\1</b>', protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<i>(.*?)</i>', f'<i style="font-style: italic; color: {MessageFormatter.COLORS["italic_text"]};">\\1</i>', protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<h1>(.*?)</h1>', f'<h1 style="font-size: 24px; font-weight: bold; color: {MessageFormatter.COLORS["header_primary"]}; margin: 15px 0 10px 0; border-bottom: 2px solid {MessageFormatter.COLORS["border_light"]}; padding-bottom: 5px;">\\1</h1>', protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<h2>(.*?)</h2>', f'<h2 style="font-size: 20px; font-weight: bold; color: {MessageFormatter.COLORS["header_primary"]}; margin: 12px 0 8px 0;">\\1</h2>', protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<h3>(.*?)</h3>', f'<h3 style="font-size: 16px; font-weight: bold; color: {MessageFormatter.COLORS["header_primary"]}; margin: 10px 0 6px 0;">\\1</h3>', protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<p>(.*?)</p>', f'<p style="margin: 8px 0;">\\1</p>', protected_message, flags=re.DOTALL)
        
        # Escape HTML tags outside of code blocks
        escaped_message = escape(protected_message)

        # Restore code blocks
        for i, code_block in enumerate(code_blocks):
            escaped_message = escaped_message.replace(f"__CODE_BLOCK_{i}__", code_block)

        return escaped_message
    
    @staticmethod
    def cleanup_message(sender: str, message: str, is_code: bool = False) -> str:
        """Prepares a message for display by adding sender and formatting."""
        # Format based on sender
        if sender == "You":
            # Auto-detect and format code in the message
            message = MessageFormatter.detect_and_format_code(message)
        elif sender == "System":
            message = f"<i style='color: {MessageFormatter.COLORS['system_text']};'>{message}</i>"
        elif sender == "Assistant's Thoughts":
            # The message is already formatted HTML, so we don't process it further.
            pass
        else:  # AI Assistant (dynamic name from personality)
            if is_code:
                # For explicit code messages, apply syntax highlighting
                message = MessageFormatter.syntax_highlight_code(message)
                # Wrap in code block styling
                message = f'<div style="background-color: #2d2d2d; border-radius: 5px; overflow: hidden; margin: 10px 0; border: 1px solid #444;"><div style="padding: 10px; color: #dcdcdc; font-family: \'Consolas\', \'Monaco\', \'Courier New\', monospace; font-size: 13px; line-height: 1.4; overflow-x: auto;">{message}</div></div>'
            else:
                # For regular assistant messages, apply enhanced markdown formatting first
                message = MessageFormatter.format_markdown(message)
                # Then detect and format code blocks
                message = MessageFormatter.detect_and_format_code(message)
                # Don't escape HTML tags for AI messages - we want to render them
                # The HTML we create should be preserved, not escaped

        return message
    
    @staticmethod
    def format_chat_message(sender: str, message: str, is_code: bool = False) -> str:
        """Format a complete chat message with styling based on sender type."""
        # Clean the message before formatting
        cleaned_message = MessageFormatter.cleanup_message(sender, message, is_code)
        
        # Apply different styles for different message types using local colors
        if sender == "System":
            formatted_message = f"""
                <div style="background-color: {MessageFormatter.COLORS['system_bubble']}; padding: 8px 10px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid {MessageFormatter.COLORS['border_dark']};">
                    <b style="color: {MessageFormatter.COLORS['system_text']};">{sender}:</b> {cleaned_message}
                </div>
            """
        elif sender == "Assistant's Thoughts":
            formatted_message = f"""
                <div style="background-color: {MessageFormatter.COLORS['thought_bubble']}; padding: 8px 10px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid {MessageFormatter.COLORS['border']};">
                    <b style="color: {MessageFormatter.COLORS['thought_text']};">{sender}:</b> {cleaned_message}
                </div>
            """
        elif is_code:
            # For code messages, use a distinct dark background and a monospace font for better readability
            formatted_message = f"""
                <div style="background-color: {MessageFormatter.COLORS['code_background']}; padding: 10px; border-radius: 5px; margin-bottom: 10px; border: 1px solid {MessageFormatter.COLORS['code_border']};">
                    <b style="color: {MessageFormatter.COLORS['header_primary']}; margin-bottom: 5px; display: block;">{sender}:</b>
                    {cleaned_message}
                </div>
            """
        else:
            # For regular messages, apply a lighter background with soft contrast
            formatted_message = f"""
                <div style="background-color: {MessageFormatter.COLORS['ai_bubble']}; padding: 10px; border-radius: 5px; margin-bottom: 10px; border: 1px solid {MessageFormatter.COLORS['border']};">
                    <b style="color: {MessageFormatter.COLORS['header_primary']};">{sender}:</b> {cleaned_message}
                </div>
            """

        return formatted_message
    
    @staticmethod
    def split_thoughts_and_answer(message: str):
        """
        Splits a message into (thoughts, main_answer) if <think>...</think> is present.
        If <think> is detected but </think> is missing, treat everything after <think> as thoughts.
        Returns a tuple (thoughts, main_answer). If no <think>, thoughts is None.
        """
        import re
        # Try to find a complete <think>...</think> block
        match = re.search(r'<think>(.*?)</think>', message, re.DOTALL | re.IGNORECASE)
        if match:
            thoughts = match.group(1).strip()
            # Remove the <think>...</think> part from the message
            main_answer = re.sub(r'<think>.*?</think>', '', message, flags=re.DOTALL | re.IGNORECASE).strip()
            return thoughts, main_answer
        # If <think> is present but </think> is missing, treat everything after <think> as thoughts
        start_idx = message.lower().find('<think>')
        if start_idx != -1:
            thoughts = message[start_idx+7:].strip()
            main_answer = message[:start_idx].strip()
            return thoughts, main_answer
        # No thoughts block found
        return None, message
    
    @staticmethod
    def to_plain_text(message: str) -> str:
        """
        Convert a message with markdown, code, and HTML to plain text for TTS.
        Removes formatting, code blocks, and HTML tags.
        """
        import re
        # Remove code blocks (```...```)
        message = re.sub(r'```[\s\S]*?```', '', message)
        # Remove inline code (`...`)
        message = re.sub(r'`[^`]+`', '', message)
        # Remove markdown bold/italic/strikethrough
        message = re.sub(r'\*\*([^*]+)\*\*', r'\1', message)
        message = re.sub(r'\*([^*]+)\*', r'\1', message)
        message = re.sub(r'__([^_]+)__', r'\1', message)
        message = re.sub(r'_([^_]+)_', r'\1', message)
        message = re.sub(r'~~([^~]+)~~', r'\1', message)
        # Remove markdown headers, lists, blockquotes
        message = re.sub(r'^#+\s*', '', message, flags=re.MULTILINE)
        message = re.sub(r'^\s*[-*•]\s+', '', message, flags=re.MULTILINE)
        message = re.sub(r'^>\s*', '', message, flags=re.MULTILINE)
        # Remove horizontal rules
        message = re.sub(r'^---$', '', message, flags=re.MULTILINE)
        # Remove HTML tags
        message = re.sub(r'<[^>]+>', '', message)
        # Unescape HTML entities
        message = unescape(message)
        # Collapse multiple newlines and strip
        message = re.sub(r'\n+', '\n', message)
        return message.strip() 