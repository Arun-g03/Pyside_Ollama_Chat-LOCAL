"""
Model Tab - Extracted from ollama_chat.py
Handles model management, pulling, removing, and updating models.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                               QPushButton, QLineEdit, QLabel, QTextEdit, 
                               QGroupBox, QProgressBar, QMessageBox, QSplitter)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QFont, QTextCursor

from SRC.services.ollama_service import OllamaService


class ModelTab(QWidget):
    """Model management tab"""
    
    # Signals
    model_pull_requested = Signal(str)  # Emitted when user requests to pull a model
    model_remove_requested = Signal(str)  # Emitted when user requests to remove a model
    model_update_requested = Signal(str)  # Emitted when user requests to update a model
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.setup_connections()
        
        # State variables
        self.models = []
        self.operation_in_progress = False
        
    def setup_ui(self):
        """Setup the model management UI"""
        layout = QVBoxLayout(self)
        
        # Create splitter for model list and operations
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Model list area
        self.setup_model_list(splitter)
        
        # Operations area
        self.setup_operations(splitter)
        
        # Set splitter proportions
        splitter.setSizes([300, 400])
        
    def setup_model_list(self, parent):
        """Setup the model list area"""
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        
        # Model list group
        models_group = QGroupBox("Available Models")
        models_layout = QVBoxLayout(models_group)
        
        # Model list
        self.model_list = QListWidget()
        self.model_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #444;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)
        models_layout.addWidget(self.model_list)
        
        # Refresh button
        refresh_button = QPushButton("Refresh Models")
        refresh_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        refresh_button.clicked.connect(self.refresh_models)
        models_layout.addWidget(refresh_button)
        
        list_layout.addWidget(models_group)
        parent.addWidget(list_widget)
        
    def setup_operations(self, parent):
        """Setup the operations area"""
        operations_widget = QWidget()
        operations_layout = QVBoxLayout(operations_widget)
        
        # Pull model group
        pull_group = QGroupBox("Pull New Model")
        pull_layout = QVBoxLayout(pull_group)
        
        # Model name input
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Model Name:"))
        self.model_name_input = QLineEdit()
        self.model_name_input.setPlaceholderText("e.g., llama2:7b")
        self.model_name_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
        """)
        input_layout.addWidget(self.model_name_input)
        
        # Pull button
        self.pull_button = QPushButton("Pull Model")
        self.pull_button.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0e6e0e;
            }
            QPushButton:pressed {
                background-color: #0c5c0c;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        input_layout.addWidget(self.pull_button)
        
        pull_layout.addLayout(input_layout)
        operations_layout.addWidget(pull_group)
        
        # Model operations group
        operations_group = QGroupBox("Model Operations")
        operations_layout_ops = QVBoxLayout(operations_group)
        
        # Operation buttons
        buttons_layout = QHBoxLayout()
        
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.setStyleSheet("""
            QPushButton {
                background-color: #d83b01;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b02e01;
            }
            QPushButton:pressed {
                background-color: #8a2301;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        buttons_layout.addWidget(self.remove_button)
        
        self.update_button = QPushButton("Update Selected")
        self.update_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        buttons_layout.addWidget(self.update_button)
        
        operations_layout_ops.addLayout(buttons_layout)
        operations_layout.addWidget(operations_group)
        
        # Status area
        status_group = QGroupBox("Operation Status")
        status_layout = QVBoxLayout(status_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 3px;
                text-align: center;
                background-color: #2d2d2d;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 2px;
            }
        """)
        status_layout.addWidget(self.progress_bar)
        
        # Status text
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(200)
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        status_layout.addWidget(self.status_text)
        
        operations_layout.addWidget(status_group)
        parent.addWidget(operations_widget)
        
    def setup_connections(self):
        """Setup signal connections"""
        # Connect buttons
        self.pull_button.clicked.connect(self.pull_model)
        self.remove_button.clicked.connect(self.remove_selected_model)
        self.update_button.clicked.connect(self.update_selected_model)
        
        # Connect model list selection
        self.model_list.itemSelectionChanged.connect(self.on_model_selection_changed)
        
    def refresh_models(self):
        """Refresh the list of available models"""
        if self.parent and hasattr(self.parent, 'ollama_service'):
            models = self.parent.ollama_service.get_models()
            self.update_model_list(models)
        else:
            self.append_status("No Ollama service available")
            
    def update_model_list(self, models: list):
        """Update the model list display"""
        self.models = models
        self.model_list.clear()
        
        for model in models:
            self.model_list.addItem(model)
            
        self.append_status(f"Found {len(models)} models")
        
    def pull_model(self):
        """Pull a new model"""
        model_name = self.model_name_input.text().strip()
        if not model_name:
            QMessageBox.warning(self, "Warning", "Please enter a model name")
            return
            
        # Confirm action
        reply = QMessageBox.question(
            self, "Confirm Pull", 
            f"Are you sure you want to pull the model '{model_name}'? This may take a while.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.start_operation()
            self.model_pull_requested.emit(model_name)
            
    def remove_selected_model(self):
        """Remove the selected model"""
        current_item = self.model_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a model to remove")
            return
            
        model_name = current_item.text()
        
        # Confirm action
        reply = QMessageBox.question(
            self, "Confirm Removal", 
            f"Are you sure you want to remove the model '{model_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.start_operation()
            self.model_remove_requested.emit(model_name)
            
    def update_selected_model(self):
        """Update the selected model"""
        current_item = self.model_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a model to update")
            return
            
        model_name = current_item.text()
        
        # Confirm action
        reply = QMessageBox.question(
            self, "Confirm Update", 
            f"Are you sure you want to update the model '{model_name}'? This may take a while.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.start_operation()
            self.model_update_requested.emit(model_name)
            
    def on_model_selection_changed(self):
        """Handle model selection change"""
        current_item = self.model_list.currentItem()
        if current_item:
            model_name = current_item.text()
            self.append_status(f"Selected model: {model_name}")
            
    def start_operation(self):
        """Start an operation (disable UI elements)"""
        self.operation_in_progress = True
        self.pull_button.setEnabled(False)
        self.remove_button.setEnabled(False)
        self.update_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
    def stop_operation(self):
        """Stop an operation (enable UI elements)"""
        self.operation_in_progress = False
        self.pull_button.setEnabled(True)
        self.remove_button.setEnabled(True)
        self.update_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
    def append_status(self, message: str):
        """Append a status message to the status text area"""
        self.status_text.append(f"[{self.get_current_time()}] {message}")
        
        # Scroll to bottom
        cursor = self.status_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.status_text.setTextCursor(cursor)
        
    def get_current_time(self) -> str:
        """Get current time as string"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
        
    def on_operation_progress(self, message: str):
        """Handle operation progress updates"""
        self.append_status(message)
        
    def on_operation_finished(self, operation: str):
        """Handle operation completion"""
        self.stop_operation()
        self.append_status(f"{operation.capitalize()} operation completed")
        
        # Refresh model list
        self.refresh_models()
        
    def on_operation_error(self, error: str):
        """Handle operation errors"""
        self.stop_operation()
        self.append_status(f"Error: {error}")
        QMessageBox.critical(self, "Error", f"Operation failed: {error}")
        
    def get_selected_model(self) -> str:
        """Get the currently selected model"""
        current_item = self.model_list.currentItem()
        return current_item.text() if current_item else ""
        
    def clear_status(self):
        """Clear the status text area"""
        self.status_text.clear() 