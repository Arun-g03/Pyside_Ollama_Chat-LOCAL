from pyside_chat.core.shared_imports.pyside_imports import *
"""
SpellChecker Widget - Extracted from ollama_chat.py
Handles spell checking functionality for text input widgets.
"""

import re

logger = CustomLogger.get_logger(__name__)

# Spellchecker imports
try:
    import enchant
    SPELLCHECK_AVAILABLE = True
except ImportError:
    SPELLCHECK_AVAILABLE = False
    logger.debug(
        "Spellchecker not available. Install pyenchant: pip install pyenchant", print_to_terminal=True)


class SpellCheckerTextEdit(QTextEdit):
    """Custom QTextEdit with spell checking functionality"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.spellchecker = None
        self.spellcheck_timer = None
        self.setup_spellchecker()
        self.setup_context_menu()

        # Connect text changed signal for better spell checking
        self.textChanged.connect(self.on_text_changed)

    def setup_spellchecker(self):
        """Initialize the spellchecker"""
        if SPELLCHECK_AVAILABLE:
            try:
                self.spellchecker = enchant.Dict("en_US")
                logger.debug(
                    "✅Spellchecker initialized with en_US dictionary", print_to_terminal=True)
                # Create a single timer for spell checking
                self.spellcheck_timer = QTimer()
                self.spellcheck_timer.setSingleShot(True)
                self.spellcheck_timer.timeout.connect(
                    self.highlight_misspelled_words)
            except Exception as e:
                logger.debug(
                    f"Could not initialize spellchecker: {e}", print_to_terminal=True)
                self.spellchecker = None
        else:
            logger.debug(
                "❌ Spellchecker not available - install pyenchant: pip install pyenchant", print_to_terminal=True)
            self.spellchecker = None

    def setup_context_menu(self):
        """Setup context menu for spell checking"""
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        """Show context menu with spell check suggestions"""
        if not self.spellchecker:
            return

        cursor = self.cursorForPosition(position)
        cursor.select(QTextCursor.WordUnderCursor)
        word = cursor.selectedText().strip()

        if not word or not word.isalpha():
            return

        # Check if word is misspelled
        if self.spellchecker.check(word):
            return

        # Get suggestions
        suggestions = self.spellchecker.suggest(word)

        # Create context menu
        menu = QMenu(self)

        # Add suggestions
        if suggestions:
            for suggestion in suggestions[:5]:  # Limit to 5 suggestions
                action = QAction(suggestion, self)
                # Fix lambda closure issue by creating a proper closure
                action.triggered.connect(
                    lambda checked, s=suggestion, c=cursor: self.replace_word(c, s))
                menu.addAction(action)

            menu.addSeparator()

        # Add "Add to dictionary" option
        add_action = QAction("Add to dictionary", self)
        add_action.triggered.connect(lambda: self.add_to_dictionary(word))
        menu.addAction(add_action)

        # Add "Ignore" option
        ignore_action = QAction("Ignore", self)
        ignore_action.triggered.connect(lambda: self.ignore_word(word))
        menu.addAction(ignore_action)

        menu.exec_(self.mapToGlobal(position))

    def replace_word(self, cursor, new_word):
        """Replace the misspelled word with the suggestion"""
        # Store cursor position
        pos = cursor.position()
        cursor.insertText(new_word)

        # Re-highlight after replacement using single timer
        if self.spellcheck_timer:
            self.spellcheck_timer.start(50)

    def add_to_dictionary(self, word):
        """Add word to personal dictionary"""
        if self.spellchecker:
            try:
                self.spellchecker.add_to_pwl(word)
                # Re-highlight after adding to dictionary using single timer
                if self.spellcheck_timer:
                    self.spellcheck_timer.start(50)
            except Exception as e:
                logger.debug(
                    f"Could not add '{word}' to dictionary: {e}", print_to_terminal=True)

    def ignore_word(self, word):
        """Ignore the word (add to personal dictionary)"""
        self.add_to_dictionary(word)

    def highlight_misspelled_words(self):
        """Highlight misspelled words in the text"""
        if not self.spellchecker:
            return

        # Store current cursor position and selection
        current_cursor = self.textCursor()
        anchor = current_cursor.anchor()
        position = current_cursor.position()

        # Clear previous highlighting
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())

        # Find and highlight misspelled words
        text = self.toPlainText()
        words = re.findall(r'\b[a-zA-Z]+\b', text)

        for word in words:
            if not self.spellchecker.check(word):
                # Find all occurrences of this word
                cursor = self.textCursor()
                cursor.movePosition(QTextCursor.Start)

                while not cursor.isNull() and not cursor.atEnd():
                    cursor = self.document().find(word, cursor)
                    if not cursor.isNull():
                        # Apply red underline format
                        format = QTextCharFormat()
                        format.setUnderlineColor(QColor(255, 0, 0))
                        format.setUnderlineStyle(QTextCharFormat.WaveUnderline)
                        cursor.mergeCharFormat(format)
                    else:
                        break

        # Only restore selection if the user hasn't changed it
        after_cursor = self.textCursor()
        if after_cursor.anchor() == anchor and after_cursor.position() == position:
            new_cursor = self.textCursor()
            new_cursor.setPosition(anchor)
            new_cursor.setPosition(position, QTextCursor.KeepAnchor)
            self.setTextCursor(new_cursor)
        # Otherwise, do not override the user's new selection

    def keyPressEvent(self, event):
        """Override key press event to check spelling on space/enter"""
        super().keyPressEvent(event)

        # Check spelling after certain key presses (only if spellchecker is enabled)
        if self.spellchecker and event.key() in [Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter]:
            # Use the single timer to delay the spell check slightly
            if self.spellcheck_timer:
                self.spellcheck_timer.start(200)

    def on_text_changed(self):
        """Handle text changes for spell checking"""
        if self.spellchecker:
            # Delay spell checking to avoid performance issues using single timer
            if self.spellcheck_timer:
                self.spellcheck_timer.start(500)

    def enable_spellcheck(self):
        """Enable spell checking"""
        if not self.spellchecker:
            self.setup_spellchecker()
        if self.spellchecker:
            self.highlight_misspelled_words()

    def disable_spellcheck(self):
        """Disable spell checking by clearing highlights"""
        # Clear all formatting
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())

        # Restore plain text
        current_text = self.toPlainText()
        self.clear()
        self.setPlainText(current_text)

    def cleanup(self):
        """Clean up resources"""
        if self.spellcheck_timer:
            self.spellcheck_timer.stop()
            self.spellcheck_timer.deleteLater()
            self.spellcheck_timer = None
