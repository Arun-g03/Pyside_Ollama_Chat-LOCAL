"""
Chat Navigation Widget
Displays a list of previous conversations for easy navigation.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                               QListWidgetItem, QPushButton, QLabel, QFrame,
                               QMenu, QMessageBox, QInputDialog)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QFont, QIcon, QCursor
import os
from datetime import datetime
from typing import List, Tuple, Optional

from SRC.models.conversation_metadata import ConversationManager, ConversationMetadata


class ChatNavigationWidget(QWidget):
    """Widget for navigating between previous conversations"""
    
    # Signals
    conversation_selected = Signal(str)  # Emitted when a conversation is selected (filepath)
    conversation_deleted = Signal(str)   # Emitted when a conversation is deleted
    conversation_renamed = Signal(str, str)  # Emitted when a conversation is renamed (old_path, new_path)
    new_conversation_requested = Signal() # Emitted when new conversation is requested
    
    def __init__(self, conversation_manager: ConversationManager, parent=None):
        super().__init__(parent)
        self.conversation_manager = conversation_manager
        self.current_conversation_file = None
        self.setup_ui()
        self.setup_connections()
        self.refresh_conversations()
        
    def setup_ui(self):
        """Setup the navigation UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Header
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Conversations")
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff; padding: 5px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # New conversation button
        self.new_btn = QPushButton("New Chat")
        self.new_btn.setMinimumWidth(90)
        self.new_btn.setMaximumHeight(30)
        self.new_btn.setToolTip("New Conversation")
        self.new_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
                padding-left: 12px;
                padding-right: 12px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        header_layout.addWidget(self.new_btn)
        
        # Clear all button
        self.clear_all_btn = QPushButton("Clear All")
        self.clear_all_btn.setMinimumWidth(80)
        self.clear_all_btn.setMaximumHeight(30)
        self.clear_all_btn.setToolTip("Delete all conversations")
        self.clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #d83b01;
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                font-size: 14px;
                padding-left: 10px;
                padding-right: 10px;
            }
            QPushButton:hover {
                background-color: #b02e01;
            }
            QPushButton:pressed {
                background-color: #8a2301;
            }
        """)
        header_layout.addWidget(self.clear_all_btn)
        
        layout.addLayout(header_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #444;")
        separator.setFixedHeight(1)
        layout.addWidget(separator)
        
        # Conversations list
        self.conversations_list = QListWidget()
        self.conversations_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 5px;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
                padding: 5px;
            }
            QListWidget::item {
                background-color: transparent;
                padding: 8px;
                border-radius: 3px;
                margin: 1px;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
            QListWidget::item:selected {
                background-color: #444444;
            }
            QListWidget::item:selected:active {
                background-color: #555555;
            }
        """)
        layout.addWidget(self.conversations_list)
        
        # Status label
        self.status_label = QLabel("No conversations found")
        self.status_label.setStyleSheet("color: #888; font-size: 11px; padding: 5px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Set context menu for the list
        self.conversations_list.setContextMenuPolicy(Qt.CustomContextMenu)
        
    def setup_connections(self):
        """Setup signal connections"""
        self.new_btn.clicked.connect(self.new_conversation_requested.emit)
        self.clear_all_btn.clicked.connect(self.clear_all_conversations)
        self.conversations_list.itemDoubleClicked.connect(self.on_conversation_double_clicked)
        self.conversations_list.customContextMenuRequested.connect(self.show_context_menu)
        
    def refresh_conversations(self):
        """Refresh the list of conversations"""
        self.conversations_list.clear()
        
        try:
            conversations = self.conversation_manager.list_conversations()
            
            if not conversations:
                self.status_label.setText("No conversations found")
                return
            
            # Sort conversations by last modified (newest first)
            conversations.sort(key=lambda x: x[1].last_modified or "", reverse=True)
            
            for filepath, metadata in conversations:
                item = self.create_conversation_item(filepath, metadata)
                self.conversations_list.addItem(item)
                
                # Mark current conversation
                if filepath == self.current_conversation_file:
                    item.setSelected(True)
            
            self.status_label.setText(f"{len(conversations)} conversation(s)")
            
        except Exception as e:
            self.status_label.setText(f"Error loading conversations: {str(e)}")
    
    def create_conversation_item(self, filepath: str, metadata: ConversationMetadata) -> QListWidgetItem:
        """Create a list item for a conversation"""
        # Create display text
        filename = os.path.basename(filepath)
        created_time = metadata.get_formatted_created_time()
        model = metadata.model or "Unknown"
        message_count = metadata.message_count
        
        display_text = f"{os.path.basename(filepath)}\n{created_time} | {model} ({message_count} messages)"
        
        item = QListWidgetItem(display_text)
        item.setData(Qt.UserRole, filepath)
        item.setToolTip(f"File: {filename}\nModel: {model}\nMessages: {message_count}\nCreated: {created_time}")
        
        return item
    
    def on_conversation_double_clicked(self, item: QListWidgetItem):
        """Handle double-click on conversation item"""
        filepath = item.data(Qt.UserRole)
        if filepath:
            self.conversation_selected.emit(filepath)
    
    def show_context_menu(self, position):
        """Show context menu for conversation items"""
        item = self.conversations_list.itemAt(position)
        if not item:
            return
        
        filepath = item.data(Qt.UserRole)
        if not filepath:
            return
        
        menu = QMenu(self)
        
        # Open action
        open_action = menu.addAction("Open")
        open_action.triggered.connect(lambda: self.conversation_selected.emit(filepath))
        
        # Rename action
        rename_action = menu.addAction("Rename")
        rename_action.triggered.connect(lambda: self.rename_conversation(filepath))
        
        menu.addSeparator()
        
        # Delete action
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.delete_conversation(filepath))
        
        menu.exec_(QCursor.pos())
    
    def rename_conversation(self, filepath: str):
        """Rename a conversation file"""
        try:
            old_filename = os.path.basename(filepath)
            new_filename, ok = QInputDialog.getText(
                self, "Rename Conversation", 
                "Enter new filename:", 
                text=old_filename
            )
            
            if ok and new_filename and new_filename != old_filename:
                # Ensure .json extension
                if not new_filename.endswith('.json'):
                    new_filename += '.json'
                
                new_filepath = os.path.join(os.path.dirname(filepath), new_filename)
                
                # Check if new filename already exists
                if os.path.exists(new_filepath):
                    QMessageBox.warning(self, "Error", "A file with that name already exists.")
                    return
                
                # Use conversation manager to rename the file
                if self.conversation_manager.rename_conversation(filepath, new_filepath):
                    # Update current conversation file reference if this was the current one
                    if self.current_conversation_file == filepath:
                        self.current_conversation_file = new_filepath
                    
                    # Refresh the list
                    self.refresh_conversations()
                    self.conversation_renamed.emit(filepath, new_filepath)
                else:
                    QMessageBox.warning(self, "Error", "Failed to rename conversation.")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to rename conversation: {str(e)}")
    
    def delete_conversation(self, filepath: str):
        """Delete a conversation"""
        try:
            filename = os.path.basename(filepath)
            reply = QMessageBox.question(
                self, "Delete Conversation",
                f"Are you sure you want to delete '{filename}'?\n\nThis action cannot be undone.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                if self.conversation_manager.delete_conversation(filepath):
                    self.conversation_deleted.emit(filepath)
                    self.refresh_conversations()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete conversation.")
                    
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to delete conversation: {str(e)}")
    
    def set_current_conversation(self, filepath: Optional[str]):
        """Set the currently active conversation"""
        self.current_conversation_file = filepath
        self.refresh_conversations()
    
    def get_selected_conversation(self) -> Optional[str]:
        """Get the currently selected conversation filepath"""
        current_item = self.conversations_list.currentItem()
        if current_item:
            return current_item.data(Qt.UserRole)
        return None
    
    def clear_all_conversations(self):
        """Delete all conversations after confirmation"""
        reply = QMessageBox.question(
            self, "Clear All Conversations",
            "Are you sure you want to delete ALL conversations?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                conversations = self.conversation_manager.list_conversations()
                for filepath, _ in conversations:
                    self.conversation_manager.delete_conversation(filepath)
                self.refresh_conversations()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to clear all conversations: {str(e)}") 