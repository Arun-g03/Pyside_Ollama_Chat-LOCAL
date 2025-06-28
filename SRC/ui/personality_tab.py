"""
Personality Tab - Extracted from ollama_chat.py
Handles personality selection and management.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QTextEdit, QLineEdit,
                               QFormLayout, QGroupBox, QCheckBox, QSpinBox,
                               QMessageBox, QListWidget, QSplitter, QTabWidget)
from PySide6.QtCore import Signal, Qt
from SRC.Personalities.personality_model_refactored import PersonalityModel, PersonalityTraits, PersonalityPrompt, PersonalityConfig, PersonalityMetadata


class PersonalityTab(QWidget):
    """Personality management tab"""
    
    # Signals
    personality_changed = Signal(str)  # Emitted when personality changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.personality_model = PersonalityModel()
        self.setup_ui()
        self.load_personalities()
        
    def setup_ui(self):
        """Setup the personality management UI"""
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Personality selection tab
        self.setup_selection_tab()
        
        # Personality creation tab
        self.setup_creation_tab()
        
        # Personality management tab
        self.setup_management_tab()
        
    def setup_selection_tab(self):
        """Setup the personality selection tab"""
        selection_widget = QWidget()
        layout = QVBoxLayout(selection_widget)
        
        # Current personality group
        current_group = QGroupBox("Current Personality")
        current_layout = QVBoxLayout(current_group)
        
        # Personality selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Select Personality:"))
        self.personality_combo = QComboBox()
        self.personality_combo.currentTextChanged.connect(self.on_personality_changed)
        self.personality_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #ffffff;
            }
        """)
        selector_layout.addWidget(self.personality_combo)
        
        # Add refresh button
        refresh_button = QPushButton("Refresh")
        refresh_button.setToolTip("Refresh personalities from disk (useful for nested folders)")
        refresh_button.clicked.connect(self.refresh_personalities)
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
        selector_layout.addWidget(refresh_button)
        
        current_layout.addLayout(selector_layout)
        
        # Personality info display
        self.personality_info = QTextEdit()
        self.personality_info.setReadOnly(True)
        self.personality_info.setMaximumHeight(200)
        self.personality_info.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        current_layout.addWidget(self.personality_info)
        
        layout.addWidget(current_group)
        layout.addStretch()
        
        self.tabs.addTab(selection_widget, "Select Personality")
        
    def setup_creation_tab(self):
        """Setup the personality creation tab"""
        creation_widget = QWidget()
        layout = QVBoxLayout(creation_widget)
        
        # Basic information
        basic_group = QGroupBox("Basic Information")
        basic_layout = QFormLayout(basic_group)
        
        self.name_edit = QLineEdit()
        self.name_edit.setStyleSheet("""
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
        
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(60)
        self.description_edit.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        
        self.tone_edit = QLineEdit()
        self.tone_edit.setStyleSheet("""
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
        
        self.style_edit = QLineEdit()
        self.style_edit.setStyleSheet("""
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
        
        basic_layout.addRow("Name:", self.name_edit)
        basic_layout.addRow("Description:", self.description_edit)
        basic_layout.addRow("Tone:", self.tone_edit)
        basic_layout.addRow("Style:", self.style_edit)
        
        layout.addWidget(basic_group)
        
        # System prompt
        prompt_group = QGroupBox("System Prompt")
        prompt_layout = QVBoxLayout(prompt_group)
        
        self.system_prompt_edit = QTextEdit()
        self.system_prompt_edit.setMaximumHeight(100)
        self.system_prompt_edit.setPlaceholderText("Enter the system prompt for this personality")
        self.system_prompt_edit.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        prompt_layout.addWidget(self.system_prompt_edit)
        
        layout.addWidget(prompt_group)
        
        # Create button
        create_button = QPushButton("Create Personality")
        create_button.clicked.connect(self.create_personality)
        create_button.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0e6e0e;
            }
            QPushButton:pressed {
                background-color: #0c5c0c;
            }
        """)
        layout.addWidget(create_button)
        
        layout.addStretch()
        
        self.tabs.addTab(creation_widget, "Create Personality")
        
    def setup_management_tab(self):
        """Setup the personality management tab"""
        management_widget = QWidget()
        layout = QVBoxLayout(management_widget)
        
        # Custom personalities list
        custom_group = QGroupBox("Custom Personalities")
        custom_layout = QVBoxLayout(custom_group)
        
        self.custom_personalities_list = QListWidget()
        self.custom_personalities_list.setStyleSheet("""
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
        self.custom_personalities_list.itemClicked.connect(self.on_custom_personality_selected)
        custom_layout.addWidget(self.custom_personalities_list)
        
        # Management buttons
        buttons_layout = QHBoxLayout()
        
        delete_button = QPushButton("Delete Selected")
        delete_button.clicked.connect(self.delete_custom_personality)
        delete_button.setStyleSheet("""
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
        """)
        buttons_layout.addWidget(delete_button)
        
        export_button = QPushButton("Export Selected")
        export_button.clicked.connect(self.export_personality)
        export_button.setStyleSheet("""
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
        buttons_layout.addWidget(export_button)
        
        custom_layout.addLayout(buttons_layout)
        layout.addWidget(custom_group)
        
        layout.addStretch()
        
        self.tabs.addTab(management_widget, "Manage Personalities")
        
    def load_personalities(self):
        """Load available personalities"""
        try:
            personalities = self.personality_model.get_available_personalities()
            
            # Clear existing items
            self.personality_combo.clear()
            
            # Add personalities to combo box
            for personality in personalities:
                self.personality_combo.addItem(personality)
                
            # Update custom personalities list
            self.update_custom_personalities_list()
            
            # Select first personality if available
            if personalities:
                self.personality_combo.setCurrentIndex(0)
                self.update_personality_info(personalities[0])
                
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Failed to load personalities: {str(e)}")
            
    def update_custom_personalities_list(self):
        """Update the custom personalities list"""
        try:
            custom_personalities = self.personality_model.get_custom_personalities()
            self.custom_personalities_list.clear()
            
            for personality in custom_personalities:
                self.custom_personalities_list.addItem(personality)
                
        except Exception as e:
            print(f"Failed to update custom personalities list: {e}")
            
    def on_personality_changed(self, personality_name: str):
        """Handle personality selection change"""
        if personality_name:
            self.update_personality_info(personality_name)
            self.personality_changed.emit(personality_name)
            
    def update_personality_info(self, personality_name: str):
        """Update the personality info display"""
        try:
            personality_data = self.personality_model.get_personality(personality_name)
            if personality_data:
                info_text = f"""
<b>Name:</b> {personality_data.get('name', 'N/A')}<br>
<b>Description:</b> {personality_data.get('description', 'N/A')}<br>
<b>Tone:</b> {personality_data.get('tone', 'N/A')}<br>
<b>Style:</b> {personality_data.get('style', 'N/A')}<br>
<br>
<b>System Prompt:</b><br>
{personality_data.get('system_prompt', 'N/A')}
                """
                self.personality_info.setHtml(info_text)
            else:
                self.personality_info.setPlainText("No information available for this personality.")
        except Exception as e:
            self.personality_info.setPlainText(f"Error loading personality info: {str(e)}")
            
    def create_personality(self):
        """Create a new personality"""
        try:
            # Get form data
            name = self.name_edit.text().strip()
            description = self.description_edit.toPlainText().strip()
            tone = self.tone_edit.text().strip()
            style = self.style_edit.text().strip()
            system_prompt = self.system_prompt_edit.toPlainText().strip()
            
            # Validate required fields
            if not name:
                QMessageBox.warning(self, "Warning", "Please enter a personality name")
                return
                
            if not system_prompt:
                QMessageBox.warning(self, "Warning", "Please enter a system prompt")
                return
                
            # Create personality data
            personality_data = {
                'name': name,
                'description': description,
                'tone': tone,
                'style': style,
                'system_prompt': system_prompt
            }
            
            # Save personality
            self.personality_model.save_custom_personality(name, personality_data)
            
            # Refresh lists
            self.load_personalities()
            
            # Clear form
            self.clear_creation_form()
            
            QMessageBox.information(self, "Success", f"Personality '{name}' created successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create personality: {str(e)}")
            
    def clear_creation_form(self):
        """Clear the personality creation form"""
        self.name_edit.clear()
        self.description_edit.clear()
        self.tone_edit.clear()
        self.style_edit.clear()
        self.system_prompt_edit.clear()
        
    def on_custom_personality_selected(self, item):
        """Handle custom personality selection"""
        personality_name = item.text()
        self.update_personality_info(personality_name)
        
    def delete_custom_personality(self):
        """Delete the selected custom personality"""
        current_item = self.custom_personalities_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a personality to delete")
            return
            
        personality_name = current_item.text()
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion", 
            f"Are you sure you want to delete the personality '{personality_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.personality_model.delete_custom_personality(personality_name)
                self.load_personalities()
                QMessageBox.information(self, "Success", f"Personality '{personality_name}' deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete personality: {str(e)}")
                
    def export_personality(self):
        """Export the selected personality"""
        current_item = self.custom_personalities_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a personality to export")
            return
            
        personality_name = current_item.text()
        
        try:
            # Get personality data
            personality_data = self.personality_model.get_personality(personality_name)
            if personality_data:
                # For now, just show the data in a message box
                # In a real implementation, you'd save to a file
                import json
                json_data = json.dumps(personality_data, indent=2)
                QMessageBox.information(self, "Personality Data", f"Personality '{personality_name}' data:\n\n{json_data}")
            else:
                QMessageBox.warning(self, "Warning", "No data found for this personality")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export personality: {str(e)}")
            
    def refresh_personalities(self):
        """Refresh personalities from disk"""
        try:
            self.personality_model.refresh_personalities()
            self.load_personalities()
            QMessageBox.information(self, "Success", "Personalities refreshed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh personalities: {str(e)}")
            
    def get_current_personality(self) -> str:
        """Get the currently selected personality"""
        return self.personality_combo.currentText()
        
    def get_system_prompt(self) -> str:
        """Get the system prompt for the current personality"""
        current_personality = self.get_current_personality()
        if current_personality:
            try:
                personality_data = self.personality_model.get_personality(current_personality)
                return personality_data.get('system_prompt', '') if personality_data else ''
            except:
                return ''
        return ''
    
    def get_available_personalities(self) -> list:
        """Get list of available personality names"""
        try:
            return self.personality_model.get_available_personalities()
        except Exception as e:
            print(f"Error getting available personalities: {e}")
            return [] 