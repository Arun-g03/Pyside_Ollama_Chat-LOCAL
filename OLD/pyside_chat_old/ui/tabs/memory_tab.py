"""
Memory Management Tab - UI for managing LLM memory across conversations
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                               QLabel, QSlider, QSpinBox, QCheckBox, QPushButton,
                               QTextEdit, QListWidget, QListWidgetItem, QGroupBox,
                               QProgressBar, QComboBox, QLineEdit, QSplitter,
                               QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QColor
from datetime import datetime
import hashlib
from pyside_chat.services.memory_service import MemoryService, MemoryEntry
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger
from typing import Dict

logger = CustomLogger.get_logger(__name__)

class MemoryTab(QWidget):
    """Memory management tab for LLM memory settings and overview"""
    
    def __init__(self, memory_service: MemoryService):
        super().__init__()
        self.memory_service = memory_service
        self.setup_ui()
        self.setup_connections()
        self.refresh_data()
    
    def setup_ui(self):
        """Setup the memory tab UI"""
        layout = QVBoxLayout()
        
        # Create tab widget for different memory sections
        self.tab_widget = QTabWidget()
        
        # Settings tab
        self.settings_tab = self.create_settings_tab()
        self.tab_widget.addTab(self.settings_tab, "Settings")
        
        # Overview tab
        self.overview_tab = self.create_overview_tab()
        self.tab_widget.addTab(self.overview_tab, "Overview")
        
        # Memories tab
        self.memories_tab = self.create_memories_tab()
        self.tab_widget.addTab(self.memories_tab, "Memories")
        
        # Summaries tab
        self.summaries_tab = self.create_summaries_tab()
        self.tab_widget.addTab(self.summaries_tab, "Summaries")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def create_settings_tab(self):
        """Create the memory settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Context Window Settings
        context_group = QGroupBox("Context Window Settings")
        context_layout = QVBoxLayout()
        
        # Max context messages slider
        context_layout.addWidget(QLabel("Maximum Context Messages:"))
        context_hbox = QHBoxLayout()
        self.context_slider = QSlider(Qt.Horizontal)
        self.context_slider.setRange(5, 100)
        self.context_slider.setValue(self.memory_service.max_context_messages)
        self.context_spinbox = QSpinBox()
        self.context_spinbox.setRange(5, 100)
        self.context_spinbox.setValue(self.memory_service.max_context_messages)
        
        context_hbox.addWidget(self.context_slider)
        context_hbox.addWidget(self.context_spinbox)
        context_layout.addLayout(context_hbox)
        
        # Memory retrieval settings
        context_layout.addWidget(QLabel("Memory Retrieval:"))
        self.include_memories_checkbox = QCheckBox("Include relevant memories in context")
        self.include_memories_checkbox.setChecked(True)
        context_layout.addWidget(self.include_memories_checkbox)
        
        self.auto_summarize_checkbox = QCheckBox("Auto-summarize long conversations")
        self.auto_summarize_checkbox.setChecked(True)
        context_layout.addWidget(self.auto_summarize_checkbox)
        
        context_group.setLayout(context_layout)
        layout.addWidget(context_group)
        
        # Memory Actions
        actions_group = QGroupBox("Memory Actions")
        actions_layout = QVBoxLayout()
        
        # Buttons
        self.summarize_btn = QPushButton("Summarize Current Conversation")
        self.clear_memory_btn = QPushButton("Clear All Memories")
        self.cleanup_memory_btn = QPushButton("Cleanup Memory Entries")
        self.export_memory_btn = QPushButton("Export Memories")
        self.import_memory_btn = QPushButton("Import Memories")
        
        actions_layout.addWidget(self.summarize_btn)
        actions_layout.addWidget(self.clear_memory_btn)
        actions_layout.addWidget(self.cleanup_memory_btn)
        actions_layout.addWidget(self.export_memory_btn)
        actions_layout.addWidget(self.import_memory_btn)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_overview_tab(self):
        """Create the memory overview tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        self.overview_layout = layout  # Store reference for semantic search labels
        
        # Statistics
        stats_group = QGroupBox("Memory Statistics")
        stats_layout = QVBoxLayout()
        
        self.total_memories_label = QLabel("Total Memories: 0")
        self.total_summaries_label = QLabel("Total Summaries: 0")
        self.avg_importance_label = QLabel("Average Importance: 0.0")
        self.context_messages_label = QLabel("Max Context Messages: 20")
        
        stats_layout.addWidget(self.total_memories_label)
        stats_layout.addWidget(self.total_summaries_label)
        stats_layout.addWidget(self.avg_importance_label)
        stats_layout.addWidget(self.context_messages_label)
        
        # Semantic search info (will be populated in refresh_overview)
        self.semantic_status_label = QLabel("Model Status: Loading...")
        self.semantic_model_label = QLabel("Model: Unknown")
        self.semantic_count_label = QLabel("Vectorized Memories: 0")
        
        stats_layout.addWidget(QLabel(""))  # Spacer
        stats_layout.addWidget(QLabel("Semantic Search:"))
        stats_layout.addWidget(self.semantic_status_label)
        stats_layout.addWidget(self.semantic_model_label)
        stats_layout.addWidget(self.semantic_count_label)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Memory Types Breakdown
        types_group = QGroupBox("Memory Types")
        types_layout = QVBoxLayout()
        
        self.memory_types_table = QTableWidget()
        self.memory_types_table.setColumnCount(2)
        self.memory_types_table.setHorizontalHeaderLabels(["Type", "Count"])
        self.memory_types_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        types_layout.addWidget(self.memory_types_table)
        types_group.setLayout(types_layout)
        layout.addWidget(types_group)
        
        # Recent Activity
        activity_group = QGroupBox("Recent Activity")
        activity_layout = QVBoxLayout()
        
        self.recent_activity_list = QListWidget()
        activity_layout.addWidget(self.recent_activity_list)
        
        activity_group.setLayout(activity_layout)
        layout.addWidget(activity_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_memories_tab(self):
        """Create the memories management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Filter dropdown for STM/LTM
        filter_layout = QHBoxLayout()
        self.memory_scope_filter = QComboBox()
        self.memory_scope_filter.addItems(["Short-Term Memory", "Long-Term Memory"])
        self.memory_scope_filter.currentIndexChanged.connect(self.refresh_memories)
        filter_layout.addWidget(QLabel("Show:"))
        filter_layout.addWidget(self.memory_scope_filter)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Search and filter
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search memories...")
        self.memory_type_filter = QComboBox()
        self.memory_type_filter.addItems(["All Types", "conversation", "summary", "fact", "preference", "skill", "relationship"])
        self.search_btn = QPushButton("Search")
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.memory_type_filter)
        search_layout.addWidget(self.search_btn)
        
        layout.addLayout(search_layout)
        
        # Memories table
        self.memories_table = QTableWidget()
        self.memories_table.setColumnCount(7)
        self.memories_table.setHorizontalHeaderLabels([
            "ID", "Content", "Type", "Importance", "Tags", "Access Count", "Date"
        ])
        self.memories_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.memories_table)
        
        # Memory details
        details_group = QGroupBox("Memory Details")
        details_layout = QVBoxLayout()
        
        self.memory_details_text = QTextEdit()
        self.memory_details_text.setMaximumHeight(150)
        self.memory_details_text.setReadOnly(True)
        
        details_layout.addWidget(self.memory_details_text)
        
        # Action buttons
        details_buttons = QHBoxLayout()
        self.delete_memory_btn = QPushButton("Delete Selected")
        self.edit_memory_btn = QPushButton("Edit Memory")
        
        details_buttons.addWidget(self.delete_memory_btn)
        details_buttons.addWidget(self.edit_memory_btn)
        details_buttons.addStretch()
        
        details_layout.addLayout(details_buttons)
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_summaries_tab(self):
        """Create the summaries management tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summaries list
        self.summaries_list = QListWidget()
        layout.addWidget(self.summaries_list)
        
        # Summary details
        details_group = QGroupBox("Summary Details")
        details_layout = QVBoxLayout()
        
        self.summary_details_text = QTextEdit()
        self.summary_details_text.setReadOnly(True)
        
        details_layout.addWidget(self.summary_details_text)
        
        # Key points
        self.key_points_list = QListWidget()
        self.key_points_list.setMaximumHeight(100)
        details_layout.addWidget(QLabel("Key Points:"))
        details_layout.addWidget(self.key_points_list)
        
        details_group.setLayout(details_layout)
        layout.addWidget(details_group)
        
        widget.setLayout(layout)
        return widget
    
    def setup_connections(self):
        """Setup signal connections"""
        # Settings connections
        self.context_slider.valueChanged.connect(self.context_spinbox.setValue)
        self.context_spinbox.valueChanged.connect(self.context_slider.setValue)
        self.context_spinbox.valueChanged.connect(self.update_context_messages)
        
        # Memory service connections
        self.memory_service.memory_updated.connect(self.refresh_memories)
        self.memory_service.summary_updated.connect(self.refresh_summaries)
        
        # Button connections
        self.summarize_btn.clicked.connect(self.summarize_current_conversation)
        self.clear_memory_btn.clicked.connect(self.clear_all_memories)
        self.cleanup_memory_btn.clicked.connect(self.cleanup_memory_entries)
        self.search_btn.clicked.connect(self.search_memories)
        
        # Table connections
        self.memories_table.itemSelectionChanged.connect(self.show_memory_details)
        self.summaries_list.itemSelectionChanged.connect(self.show_summary_details)
        
        # Delete button
        self.delete_memory_btn.clicked.connect(self.delete_selected_memory)
    
    def update_context_messages(self, value):
        """Update the maximum context messages"""
        self.memory_service.set_max_context_messages(value)
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh all data displays"""
        self.refresh_overview()
        self.refresh_memories()
        self.refresh_summaries()
    
    def refresh_overview(self):
        """Refresh the overview tab data"""
        stats = self.memory_service.get_memory_stats()
        
        self.total_memories_label.setText(f"Total Memories: {stats['total_memories']}")
        self.total_summaries_label.setText(f"Total Summaries: {stats['total_summaries']}")
        self.avg_importance_label.setText(f"Average Importance: {stats['average_importance']:.2f}")
        self.context_messages_label.setText(f"Max Context Messages: {stats['max_context_messages']}")
        
        # Add semantic search information
        semantic_stats = stats.get('semantic_search', {})
        if semantic_stats:
            model_status = "Loaded" if semantic_stats.get('model_loaded', False) else "Not Loaded"
            model_name = semantic_stats.get('model_name', 'Unknown')
            vectorized_count = semantic_stats.get('total_memories', 0)
            
            self.semantic_status_label.setText(f"Model Status: {model_status}")
            self.semantic_model_label.setText(f"Model: {model_name}")
            self.semantic_count_label.setText(f"Vectorized Memories: {vectorized_count}")
        
        # Update memory types table
        self.memory_types_table.setRowCount(len(stats['memory_types']))
        for i, (memory_type, count) in enumerate(stats['memory_types'].items()):
            self.memory_types_table.setItem(i, 0, QTableWidgetItem(memory_type))
            self.memory_types_table.setItem(i, 1, QTableWidgetItem(str(count)))
        
        # Update recent activity
        self.recent_activity_list.clear()
        
        # Combine memories and LTM entries for recent activity
        all_entries = []
        
        # Add old memories (legacy support - these would be from the old memory structure)
        # The new structure uses stm_service and ltm_service instead of a direct memories list
        # For now, we'll skip the old memories since they're not accessible in the new structure
        pass
        
        # Add LTM entries
        for entry in self.memory_service.ltm_service.entries:
            content = entry.summary if entry.type == 'summary' else entry.value
            if content:
                all_entries.append({
                    'timestamp': entry.timestamp,
                    'type': entry.type,
                    'content': content
                })
        
        # Sort by timestamp and show recent entries
        recent_entries = sorted(all_entries, key=lambda x: x['timestamp'], reverse=True)[:10]
        
        for entry in recent_entries:
            date = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M")
            item_text = f"{date} - {entry['type']}: {entry['content'][:50]}..."
            item = QListWidgetItem(item_text)
            self.recent_activity_list.addItem(item)
    
    def refresh_memories(self):
        """Refresh the memories table based on STM/LTM filter"""
        scope = self.memory_scope_filter.currentText() if hasattr(self, 'memory_scope_filter') else "Short-Term Memory"
        if scope == "Short-Term Memory":
            memories = self.memory_service.stm_service.get_messages()
            self.memories_table.setRowCount(len(memories))
            # Only fill columns that make sense for STM
            for i, memory in enumerate(memories):
                self.memories_table.setItem(i, 0, QTableWidgetItem(str(i+1)))
                self.memories_table.setItem(i, 1, QTableWidgetItem(memory.get("content", "")))
                self.memories_table.setItem(i, 2, QTableWidgetItem(memory.get("role", "")))
                self.memories_table.setItem(i, 3, QTableWidgetItem("-"))
                self.memories_table.setItem(i, 4, QTableWidgetItem("-"))
                self.memories_table.setItem(i, 5, QTableWidgetItem("-"))
                self.memories_table.setItem(i, 6, QTableWidgetItem("-"))
        else:
            # LTM: fill all columns
            ltm_entries = self.memory_service.ltm_service.get_entries()
            self.memories_table.setRowCount(len(ltm_entries))
            for i, entry in enumerate(ltm_entries):
                self.memories_table.setItem(i, 0, QTableWidgetItem(str(i+1)))
                content = entry.summary if entry.type == "summary" else entry.value
                self.memories_table.setItem(i, 1, QTableWidgetItem(content or ""))
                self.memories_table.setItem(i, 2, QTableWidgetItem(entry.type))
                self.memories_table.setItem(i, 3, QTableWidgetItem(str(entry.importance)))
                # Handle potential None tags
                tags = entry.tags if entry.tags is not None else []
                self.memories_table.setItem(i, 4, QTableWidgetItem(", ".join(tags)))
                self.memories_table.setItem(i, 5, QTableWidgetItem(str(entry.access_count)))
                self.memories_table.setItem(i, 6, QTableWidgetItem(entry.timestamp))
    
    def refresh_summaries(self):
        """Refresh the summaries list"""
        self.summaries_list.clear()
        
        summaries = self.memory_service.ltm_service.get_entries('summary')
        for summary in summaries:
            date = datetime.fromisoformat(summary.timestamp).strftime("%Y-%m-%d %H:%M")
            summary_text = summary.summary or ""
            item_text = f"{date} - {summary_text[:50]}..."
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, summary.timestamp)  # Use timestamp as identifier
            self.summaries_list.addItem(item)
    
    def search_memories(self):
        """Search memories based on input"""
        query = self.search_input.text()
        memory_type = self.memory_type_filter.currentText()
        
        if memory_type == "All Types":
            memory_type = None
        
        results = self.memory_service.search_memories(query, memory_type)
        
        self.memories_table.setRowCount(len(results))
        for i, memory in enumerate(results):
            date = datetime.fromisoformat(memory.timestamp).strftime("%Y-%m-%d %H:%M")
            
            self.memories_table.setItem(i, 0, QTableWidgetItem(memory.id))
            self.memories_table.setItem(i, 1, QTableWidgetItem(memory.content[:50] + "..."))
            self.memories_table.setItem(i, 2, QTableWidgetItem(memory.memory_type))
            self.memories_table.setItem(i, 3, QTableWidgetItem(f"{memory.importance:.2f}"))
            self.memories_table.setItem(i, 4, QTableWidgetItem(", ".join(memory.tags)))
            self.memories_table.setItem(i, 5, QTableWidgetItem("-"))  # Access count not available for old memories
            self.memories_table.setItem(i, 6, QTableWidgetItem(date))
    
    def show_memory_details(self):
        """Show details for selected memory"""
        current_row = self.memories_table.currentRow()
        if current_row >= 0:
            try:
                # Get the memory ID from the table
                memory_id = self.memories_table.item(current_row, 0).text()
                
                # Try to find the memory in LTM entries first
                ltm_entries = self.memory_service.ltm_service.get_entries()
                memory = None
                
                for entry in ltm_entries:
                    entry_id = hashlib.md5(f"{entry.type}{entry.key}{entry.value}".encode()).hexdigest()
                    if entry_id == memory_id:
                        memory = entry
                        break
                
                if memory:
                    details = f"ID: {memory_id}\n"
                    content = memory.summary if memory.type == "summary" else memory.value
                    details += f"Content: {content or 'N/A'}\n"
                    details += f"Type: {memory.type}\n"
                    details += f"Importance: {memory.importance}\n"
                    details += f"Tags: {', '.join(memory.tags) if memory.tags else 'None'}\n"
                    details += f"Date: {datetime.fromisoformat(memory.timestamp).strftime('%Y-%m-%d %H:%M:%S')}\n"
                    details += f"Access Count: {memory.access_count}\n"
                    
                    self.memory_details_text.setText(details)
                else:
                    self.memory_details_text.setText("Memory not found or no longer available.")
            except Exception as e:
                self.memory_details_text.setText(f"Error loading memory details: {str(e)}")
    
    def show_summary_details(self):
        """Show details for selected summary"""
        current_item = self.summaries_list.currentItem()
        if current_item:
            summary_timestamp = current_item.data(Qt.UserRole)
            summaries = self.memory_service.ltm_service.get_entries('summary')
            summary = next((s for s in summaries if s.timestamp == summary_timestamp), None)
            
            if summary:
                self.summary_details_text.setText(summary.summary or "")
                
                self.key_points_list.clear()
                if summary.tags:
                    for tag in summary.tags:
                        self.key_points_list.addItem(tag)
    
    def summarize_current_conversation(self):
        """Summarize the current conversation"""
        # This method will be connected to the main conversation service
        # For now, show a message that it's connected
        QMessageBox.information(self, "Info", "Summarize functionality is connected to the conversation service.")
    
    def set_conversation_service(self, conversation_service):
        """Set the conversation service for summarization"""
        self.conversation_service = conversation_service
        # Reconnect the summarize button to use the actual service
        self.summarize_btn.clicked.disconnect()
        self.summarize_btn.clicked.connect(self._summarize_with_service)
    
    def _summarize_with_service(self):
        """Summarize the current conversation using the conversation service"""
        if hasattr(self, 'conversation_service') and self.conversation_service:
            messages = self.conversation_service.get_messages()
            if len(messages) >= 10:
                summary = self.memory_service.summarize_conversation(
                    messages, 
                    self.conversation_service.current_conversation_id or "current"
                )
                if summary:
                    QMessageBox.information(self, "Summary Created", 
                                          f"Conversation summarized successfully!\n\nSummary: {summary[:200]}...")
                else:
                    QMessageBox.information(self, "Summary", 
                                          "Conversation is too short to summarize (minimum 10 messages).")
            else:
                QMessageBox.information(self, "Summary", 
                                      "Conversation is too short to summarize (minimum 10 messages).")
        else:
            QMessageBox.warning(self, "Error", "Conversation service not connected.")
    
    def clear_all_memories(self):
        """Clear all memories"""
        reply = QMessageBox.question(
            self, "Confirm Clear", 
            "Are you sure you want to clear all memories? This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.memory_service.clear_memory()
            self.refresh_data()
            QMessageBox.information(self, "Success", "All memories cleared successfully!")
    
    def cleanup_memory_entries(self):
        """Clean up duplicate and conflicting memory entries"""
        reply = QMessageBox.question(
            self, "Confirm Cleanup", 
            "This will remove duplicate and conflicting memory entries. Continue?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.memory_service.cleanup_memory_entries()
                self.refresh_data()
                QMessageBox.information(self, "Success", "Memory entries cleaned up successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to cleanup memory entries: {str(e)}")
    
    def delete_selected_memory(self):
        """Delete the selected memory"""
        current_row = self.memories_table.currentRow()
        if current_row >= 0:
            memory_id = self.memories_table.item(current_row, 0).text()
            
            reply = QMessageBox.question(self, "Confirm Delete", 
                                       f"Are you sure you want to delete memory {memory_id}?",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.memory_service.delete_memory(memory_id)
                self.refresh_data() 