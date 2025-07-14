from pyside_chat.core.shared_imports.pyside_imports import *
"""
Editable Message Widget
Provides an editable message interface with edit/save/cancel functionality.
"""

class EditableMessageWidget(QWidget):
    """Widget for displaying and editing user messages"""
    
    # Signal emitted when message is edited
    message_edited = Signal(str)  # new_content
    message_edit_cancelled = Signal()  # when edit is cancelled
    
    def __init__(self, content: str, message_id: str, parent=None):
        super().__init__(parent)
        self.original_content = content
        self.current_content = content
        self.message_id = message_id
        self.is_editing = False
        
        self.setup_ui()
        self.setup_styles()
        
    def setup_ui(self):
        """Setup the widget UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Main container
        self.container = QFrame()
        self.container.setFrameStyle(QFrame.StyledPanel)
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        
        # Message content area
        self.content_area = QWidget()
        content_layout = QHBoxLayout(self.content_area)
        content_layout.setContentsMargins(10, 8, 10, 8)
        
        # Message display (read-only)
        self.message_display = QLabel(self.current_content)
        self.message_display.setWordWrap(True)
        self.message_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        content_layout.addWidget(self.message_display)
        
        # Edit button
        self.edit_button = QPushButton("✏️")
        self.edit_button.setFixedSize(24, 24)
        self.edit_button.setToolTip("Edit message")
        self.edit_button.clicked.connect(self.start_editing)
        content_layout.addWidget(self.edit_button)
        
        container_layout.addWidget(self.content_area)
        
        # Edit area (initially hidden)
        self.edit_area = QWidget()
        self.edit_area.setVisible(False)
        edit_layout = QVBoxLayout(self.edit_area)
        edit_layout.setContentsMargins(10, 8, 10, 8)
        
        # Text editor
        self.text_editor = QTextEdit()
        self.text_editor.setMaximumHeight(100)
        self.text_editor.setPlaceholderText("Edit your message...")
        edit_layout.addWidget(self.text_editor)
        
        # Edit buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 5, 0, 0)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_edit)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_edit)
        button_layout.addWidget(self.cancel_button)
        
        button_layout.addStretch()
        edit_layout.addLayout(button_layout)
        
        container_layout.addWidget(self.edit_area)
        layout.addWidget(self.container)
        
    def setup_styles(self):
        """Setup widget styles"""
        self.setStyleSheet("""
            EditableMessageWidget {
                background-color: transparent;
            }
            EditableMessageWidget QFrame {
                background-color: #1a3a5d;
                border-radius: 8px;
                border: 1px solid #2d5a8a;
            }
            EditableMessageWidget QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                line-height: 1.4;
            }
            EditableMessageWidget QPushButton {
                background-color: transparent;
                border: none;
                color: #ffffff;
                font-size: 12px;
                padding: 2px;
                border-radius: 3px;
            }
            EditableMessageWidget QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
            EditableMessageWidget QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
            EditableMessageWidget QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        
        # Style for edit buttons
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #444;
            }
        """)
        
    def start_editing(self):
        """Start editing the message"""
        self.is_editing = True
        self.text_editor.setPlainText(self.current_content)
        self.content_area.setVisible(False)
        self.edit_area.setVisible(True)
        self.text_editor.setFocus()
        self.text_editor.selectAll()
        
    def save_edit(self):
        """Save the edited message"""
        new_content = self.text_editor.toPlainText().strip()
        if new_content and new_content != self.original_content:
            self.current_content = new_content
            self.message_display.setText(new_content)
            self.message_edited.emit(new_content)
        
        self.finish_editing()
        
    def cancel_edit(self):
        """Cancel editing and revert to original content"""
        self.finish_editing()
        self.message_edit_cancelled.emit()
        
    def finish_editing(self):
        """Finish editing mode"""
        self.is_editing = False
        self.content_area.setVisible(True)
        self.edit_area.setVisible(False)
        
    def get_content(self) -> str:
        """Get the current message content"""
        return self.current_content
        
    def set_content(self, content: str):
        """Set the message content"""
        self.current_content = content
        self.original_content = content
        self.message_display.setText(content) 