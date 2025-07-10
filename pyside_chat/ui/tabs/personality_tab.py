"""
Personality Tab - Extracted from ollama_chat.py
Handles personality selection and management.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QTextEdit, QLineEdit,
                               QFormLayout, QGroupBox, QCheckBox, QSpinBox,
                               QMessageBox, QListWidget, QSplitter, QTabWidget)
from PySide6.QtCore import Signal, Qt
from pyside_chat.features.personality.models.personality_model import PersonalityModel
from pyside_chat.features.personality.models.personality_types import PersonalityTraits, PersonalityPrompt, PersonalityConfig, PersonalityMetadata
from datetime import datetime
from pyside_chat.core.logging.logger import CustomLogger
import traceback

logger = CustomLogger.get_logger(__name__)

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
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #444;
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #555;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 8px 16px;
                margin-right: 2px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background-color: #3d3d3d;
                color: #ffffff;
            }
        """)
        layout.addWidget(self.tabs)
        
        # Personality selection tab
        self.setup_selection_tab()
        
        # Personality creation tab
        self.setup_creation_tab()
        
        # Personality management tab
        self.setup_management_tab()
        
        # Apply sleek style to all QSplitters in this tab
        self.setStyleSheet("""
            QSplitter::handle {
                background: #232323;
                border: none;
                width: 3px;
                border-radius: 2px;
            }
            QSplitter::handle:hover {
                background: #444444;
            }
        """)
        
    def setup_selection_tab(self):
        """Setup the personality selection tab"""
        selection_widget = QWidget()
        layout = QVBoxLayout(selection_widget)
        
        # Current personality group
        current_group = QGroupBox("Current Personality")
        current_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #2d2d2d;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
        """)
        current_layout = QVBoxLayout(current_group)
        
        # Personality selector
        selector_layout = QHBoxLayout()
        personality_label = QLabel("Select Personality:")
        personality_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        selector_layout.addWidget(personality_label)
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
        creation_widget.setStyleSheet("""
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                color: #ffffff;
                background-color: #2d2d2d;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #0078d4;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #ffffff;
                selection-background-color: #0078d4;
            }
            QCheckBox, QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QGroupBox::title {
                color: #ffffff;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                font-weight: bold;
                font-size: 15px;
            }
        """)
        layout = QVBoxLayout(creation_widget)
        
        # Basic information
        basic_group = QGroupBox("Basic Information")
        basic_group.setStyleSheet(basic_group.styleSheet() + """
            QFormLayout QLabel {
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
        """)
        basic_layout = QFormLayout(basic_group)
        basic_layout.setLabelAlignment(Qt.AlignRight)
        
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
        prompt_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #2d2d2d;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
        """)
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
                color: #ffffff;
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
        
        # System personalities group (read-only)
        system_group = QGroupBox("System Personalities (Read-Only)")
        system_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #2d2d2d;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
        """)
        system_layout = QVBoxLayout(system_group)
        
        self.system_personalities_list = QListWidget()
        self.system_personalities_list.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
            }
            QListWidget::item:hover {
                background-color: #2d2d2d;
            }
        """)
        self.system_personalities_list.itemClicked.connect(self.on_system_personality_selected)
        system_layout.addWidget(self.system_personalities_list)
        
        # System personality info
        self.system_personality_info = QTextEdit()
        self.system_personality_info.setReadOnly(True)
        self.system_personality_info.setMaximumHeight(150)
        self.system_personality_info.setStyleSheet("""
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
        system_layout.addWidget(self.system_personality_info)
        
        layout.addWidget(system_group)
        
        # Custom personalities group (editable)
        custom_group = QGroupBox("Custom Personalities")
        custom_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #555;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
                background-color: #2d2d2d;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
        """)
        custom_layout = QVBoxLayout(custom_group)
        
        self.custom_personalities_list = QListWidget()
        self.custom_personalities_list.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
            }
            QListWidget::item:hover {
                background-color: #2d2d2d;
            }
        """)
        self.custom_personalities_list.itemClicked.connect(self.on_custom_personality_selected)
        custom_layout.addWidget(self.custom_personalities_list)
        
        # Custom personality buttons
        buttons_layout = QHBoxLayout()
        
        delete_button = QPushButton("Delete Selected")
        delete_button.setToolTip("Delete the selected custom personality")
        delete_button.clicked.connect(self.delete_custom_personality)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #d13438;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b02a2e;
            }
            QPushButton:pressed {
                background-color: #8e2226;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
        """)
        buttons_layout.addWidget(delete_button)
        
        export_button = QPushButton("Export Selected")
        export_button.setToolTip("Export the selected personality to a file")
        export_button.clicked.connect(self.export_personality)
        export_button.setStyleSheet("""
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
        """)
        buttons_layout.addWidget(export_button)
        
        buttons_layout.addStretch()
        custom_layout.addLayout(buttons_layout)
        
        layout.addWidget(custom_group)
        layout.addStretch()
        
        self.tabs.addTab(management_widget, "Manage Personalities")
        
    def load_personalities(self):
        """Load available personalities into the combo box and lists"""
        self.personality_combo.clear()
        personalities = self.personality_model.get_available_personalities()
        
        # Sort personalities to group by folder structure
        sorted_personalities = sorted(personalities, key=lambda x: (x.count('.'), x))
        
        # Add personalities with folder structure display
        for personality in sorted_personalities:
            if '.' in personality:
                # Show folder structure in display
                parts = personality.split('.')
                display_name = f"{' → '.join(parts[:-1])} → {parts[-1]}"
                self.personality_combo.addItem(display_name, personality)  # Store original name as data
            else:
                # Simple personality name
                self.personality_combo.addItem(personality, personality)
        
        # Update system and custom personalities lists
        self.update_system_personalities_list()
        self.update_custom_personalities_list()
        
        # Set default personality
        if personalities:
            # Try to set assistant personality first, otherwise use first available
            if "assistant" in personalities:
                self.personality_combo.setCurrentText("assistant")
                self.personality_model.set_current_personality("assistant")
                self.update_personality_info("assistant")
            else:
                first_personality = sorted_personalities[0]
                self.personality_combo.setCurrentText(first_personality)
                self.personality_model.set_current_personality(first_personality)
                self.update_personality_info(first_personality)
    
    def update_system_personalities_list(self):
        """Update the system personalities list"""
        try:
            system_personalities = self.personality_model.service.get_system_personalities()
            self.system_personalities_list.clear()
            
            for personality in system_personalities:
                self.system_personalities_list.addItem(personality)
        except Exception as e:
            logger.debug(f"[ID:0097] Failed to update system personalities list: {e}",print_to_terminal=True)
            logger.debug(traceback.format_exc(), print_to_terminal=True)
    
    def update_custom_personalities_list(self):
        """Update the custom personalities list"""
        try:
            custom_personalities = self.personality_model.service.get_custom_personalities()
            self.custom_personalities_list.clear()
            
            for personality in custom_personalities:
                self.custom_personalities_list.addItem(personality)
        except Exception as e:
            logger.debug(f"[ID:0096] Failed to update custom personalities list: {e}",print_to_terminal=True)
    
    def on_system_personality_selected(self, item):
        """Handle system personality selection"""
        if item:
            personality_name = item.text()
            self.update_system_personality_info(personality_name)
    
    def update_system_personality_info(self, personality_name: str):
        """Update the system personality info display"""
        try:
            personality_data = self.personality_model.get_personality(personality_name)
            if personality_data:
                traits = personality_data.get('traits', {})
                metadata = personality_data.get('metadata', {})
                
                info_text = f"Name: {personality_name}\n"
                info_text += f"Description: {traits.get('description', 'No description')}\n"
                info_text += f"Tone: {traits.get('tone', 'Not specified')}\n"
                info_text += f"Style: {traits.get('style', 'Not specified')}\n"
                info_text += f"Category: {metadata.get('category', 'Not specified')}\n"
                info_text += f"Created: {metadata.get('created_date', 'Unknown')}\n"
                info_text += f"Modified: {metadata.get('last_modified', 'Unknown')}\n\n"
                info_text += f"System Prompt:\n{personality_data.get('system_prompt', 'No system prompt')}"
                
                self.system_personality_info.setText(info_text)
        except Exception as e:
            self.system_personality_info.setText(f"Error loading personality info: {e}")
    
    def on_custom_personality_selected(self, item):
        """Handle custom personality selection"""
        if item:
            personality_name = item.text()
            self.update_personality_info(personality_name)
    
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
                traits = personality_data.get('traits', {})
                metadata = personality_data.get('metadata', {})
                
                info_text = f"Name: {personality_name}\n"
                info_text += f"Description: {traits.get('description', 'No description')}\n"
                info_text += f"Tone: {traits.get('tone', 'Not specified')}\n"
                info_text += f"Style: {traits.get('style', 'Not specified')}\n"
                info_text += f"Category: {metadata.get('category', 'Not specified')}\n"
                info_text += f"Created: {metadata.get('created_date', 'Unknown')}\n"
                info_text += f"Modified: {metadata.get('last_modified', 'Unknown')}\n\n"
                info_text += f"System Prompt:\n{personality_data.get('system_prompt', 'No system prompt')}"
                
                self.personality_info.setPlainText(info_text)
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
            
            # Create personality objects
            from pyside_chat.features.personality.models.personality_model import PersonalityTraits, PersonalityPrompt, PersonalityConfig, PersonalityMetadata
            
            traits = PersonalityTraits(
                description=description,
                tone=tone,
                style=style
            )
            
            prompt = PersonalityPrompt(
                system_prompt=system_prompt
            )
            
            config = PersonalityConfig()
            
            metadata = PersonalityMetadata(
                category="custom",
                created_date=datetime.now().isoformat(),
                last_modified=datetime.now().isoformat()
            )
            
            # Create personality
            success = self.personality_model.create_custom_personality(name, traits, prompt, config, metadata)
            
            if success:
                # Refresh lists
                self.load_personalities()
                
                # Clear form
                self.clear_creation_form()
                
                QMessageBox.information(self, "Success", f"Personality '{name}' created successfully!")
            else:
                QMessageBox.warning(self, "Warning", f"Failed to create personality '{name}'. It may already exist.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create personality: {str(e)}")
    
    def clear_creation_form(self):
        """Clear the personality creation form"""
        self.name_edit.clear()
        self.description_edit.clear()
        self.tone_edit.clear()
        self.style_edit.clear()
        self.system_prompt_edit.clear()
    
    def delete_custom_personality(self):
        """Delete the selected custom personality"""
        current_item = self.custom_personalities_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Cannot delete system personality")
            return
        
        personality_name = current_item.text()
        
        # Check if it's actually a custom personality
        if not self.personality_model.service.is_custom_personality(personality_name):
            QMessageBox.warning(self, "Warning", f"Cannot delete system personality '{personality_name}'")
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete the personality '{personality_name}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                success = self.personality_model.delete_custom_personality(personality_name)
                if success:
                    self.load_personalities()
                    QMessageBox.information(self, "Success", f"Personality '{personality_name}' deleted successfully!")
                else:
                    QMessageBox.warning(self, "Warning", f"Failed to delete personality '{personality_name}'")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error deleting personality: {str(e)}")
    
    def export_personality(self):
        """Export the selected personality to a file"""
        current_item = self.custom_personalities_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a personality to export")
            return
        
        personality_name = current_item.text()
        
        try:
            personality_data = self.personality_model.get_personality(personality_name)
            if not personality_data:
                QMessageBox.warning(self, "Warning", f"Could not load personality '{personality_name}'")
                return
            
            # TODO: Implement export functionality
            QMessageBox.information(self, "Info", f"Export functionality for '{personality_name}' will be implemented soon!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error exporting personality: {str(e)}")
    
    def refresh_personalities(self):
        """Refresh personalities from disk"""
        try:
            self.personality_model.refresh_personalities()
            self.load_personalities()
            QMessageBox.information(self, "Success", "Personalities refreshed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh personalities: {str(e)}")
    
    def get_current_personality(self) -> str:
        """Get the currently selected personality name"""
        return self.personality_model.get_selected_model()
    
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
            logger.debug(f"[ID:0095] Error getting available personalities: {e}",print_to_terminal=True)
            return [] 