"""
Personality Widget - Extracted from ollama_chat.py
Handles personality selection and display.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QTextEdit, QLineEdit,
                               QFormLayout, QGroupBox, QCheckBox, QSpinBox,
                               QMessageBox, QListWidget, QSplitter, QTabWidget)
from PySide6.QtCore import Signal, Qt
from SRC.Personalities.personality_model_refactored import PersonalityModel, PersonalityTraits, PersonalityPrompt, PersonalityConfig, PersonalityMetadata
from typing import List, Dict

class PersonalityWidget(QWidget):
    """Widget for managing AI personalities"""
    
    personality_changed = Signal(str)  # Signal emitted when personality changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.personality_model = PersonalityModel()
        self.setup_ui()
        self.load_personalities()
    
    def setup_ui(self):
        """Setup the user interface"""
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
        
        # Apply sleek style to all QSplitters in this widget
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
        current_layout = QVBoxLayout(current_group)
        
        # Personality selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Select Personality:"))
        self.personality_combo = QComboBox()
        self.personality_combo.currentTextChanged.connect(self.on_personality_changed)
        selector_layout.addWidget(self.personality_combo)
        
        # Add refresh button
        refresh_button = QPushButton("Refresh")
        refresh_button.setToolTip("Refresh personalities from disk (useful for nested folders)")
        refresh_button.clicked.connect(self.refresh_personalities)
        selector_layout.addWidget(refresh_button)
        
        current_layout.addLayout(selector_layout)
        
        # Personality info display
        self.personality_info = QTextEdit()
        self.personality_info.setReadOnly(True)
        self.personality_info.setMaximumHeight(200)
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
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(60)
        self.tone_edit = QLineEdit()
        self.style_edit = QLineEdit()
        
        basic_layout.addRow("Name:", self.name_edit)
        basic_layout.addRow("Description:", self.description_edit)
        basic_layout.addRow("Tone:", self.tone_edit)
        basic_layout.addRow("Style:", self.style_edit)
        
        layout.addWidget(basic_group)
        
        # Personality traits
        traits_group = QGroupBox("Personality Traits")
        traits_layout = QFormLayout(traits_group)
        
        self.expertise_edit = QTextEdit()
        self.expertise_edit.setMaximumHeight(60)
        self.expertise_edit.setPlaceholderText("Enter expertise areas separated by commas")
        
        self.conversation_style_combo = QComboBox()
        self.conversation_style_combo.addItems(["conversational", "professional", "friendly", "mentoring", "inspirational"])
        
        self.response_length_combo = QComboBox()
        self.response_length_combo.addItems(["concise", "detailed", "verbose"])
        
        self.formality_combo = QComboBox()
        self.formality_combo.addItems(["casual", "semi-formal", "formal"])
        
        self.humor_combo = QComboBox()
        self.humor_combo.addItems(["none", "subtle", "moderate", "high"])
        
        traits_layout.addRow("Expertise:", self.expertise_edit)
        traits_layout.addRow("Conversation Style:", self.conversation_style_combo)
        traits_layout.addRow("Response Length:", self.response_length_combo)
        traits_layout.addRow("Formality Level:", self.formality_combo)
        traits_layout.addRow("Humor Level:", self.humor_combo)
        
        # Checkboxes for boolean traits
        self.emoji_checkbox = QCheckBox("Use Emojis")
        self.code_checkbox = QCheckBox("Format Code")
        self.examples_checkbox = QCheckBox("Provide Examples")
        self.questions_checkbox = QCheckBox("Ask Questions")
        
        traits_layout.addRow(self.emoji_checkbox)
        traits_layout.addRow(self.code_checkbox)
        traits_layout.addRow(self.examples_checkbox)
        traits_layout.addRow(self.questions_checkbox)
        
        layout.addWidget(traits_group)
        
        # Prompt configuration
        prompt_group = QGroupBox("Prompt Configuration")
        prompt_layout = QFormLayout(prompt_group)
        
        self.system_prompt_edit = QTextEdit()
        self.system_prompt_edit.setMaximumHeight(100)
        self.system_prompt_edit.setPlaceholderText("Enter the system prompt for this personality")
        
        self.user_prompt_edit = QTextEdit()
        self.user_prompt_edit.setMaximumHeight(60)
        self.user_prompt_edit.setPlaceholderText("Enter user prompt template (use {user_input} for placeholder)")
        
        self.context_prompt_edit = QTextEdit()
        self.context_prompt_edit.setMaximumHeight(60)
        self.context_prompt_edit.setPlaceholderText("Enter context prompt template (use {context} and {user_input} for placeholders)")
        
        prompt_layout.addRow("System Prompt:", self.system_prompt_edit)
        prompt_layout.addRow("User Prompt Template:", self.user_prompt_edit)
        prompt_layout.addRow("Context Prompt Template:", self.context_prompt_edit)
        
        layout.addWidget(prompt_group)
        
        # Examples and Constraints
        examples_constraints_group = QGroupBox("Examples and Constraints")
        examples_constraints_layout = QFormLayout(examples_constraints_group)
        
        self.examples_edit = QTextEdit()
        self.examples_edit.setMaximumHeight(100)
        self.examples_edit.setPlaceholderText("Enter example responses (one per line)")
        
        self.constraints_edit = QTextEdit()
        self.constraints_edit.setMaximumHeight(100)
        self.constraints_edit.setPlaceholderText("Enter constraints (one per line)")
        
        examples_constraints_layout.addRow("Example Responses:", self.examples_edit)
        examples_constraints_layout.addRow("Constraints:", self.constraints_edit)
        
        layout.addWidget(examples_constraints_group)
        
        # Configuration settings
        config_group = QGroupBox("Configuration Settings")
        config_layout = QFormLayout(config_group)
        
        self.temperature_spin = QSpinBox()
        self.temperature_spin.setRange(0, 20)
        self.temperature_spin.setValue(7)
        self.temperature_spin.setSuffix(" (×0.1)")
        self.temperature_spin.setToolTip("Temperature setting (0.0 to 2.0)")
        
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(100, 8192)
        self.max_tokens_spin.setValue(2048)
        self.max_tokens_spin.setSuffix(" tokens")
        
        self.top_p_spin = QSpinBox()
        self.top_p_spin.setRange(1, 100)
        self.top_p_spin.setValue(90)
        self.top_p_spin.setSuffix(" (×0.01)")
        self.top_p_spin.setToolTip("Top-p setting (0.0 to 1.0)")
        
        self.use_templates_checkbox = QCheckBox("Use Prompt Templates")
        self.use_templates_checkbox.setChecked(True)
        self.use_templates_checkbox.setToolTip("Whether to use user/context prompt templates")
        
        config_layout.addRow("Temperature:", self.temperature_spin)
        config_layout.addRow("Max Tokens:", self.max_tokens_spin)
        config_layout.addRow("Top-p:", self.top_p_spin)
        config_layout.addRow(self.use_templates_checkbox)
        
        layout.addWidget(config_group)
        
        # Metadata
        metadata_group = QGroupBox("Metadata")
        metadata_layout = QFormLayout(metadata_group)
        
        self.author_edit = QLineEdit()
        self.author_edit.setPlaceholderText("Enter author name")
        
        self.category_edit = QLineEdit()
        self.category_edit.setPlaceholderText("e.g., professional, creative, casual")
        
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Enter tags separated by commas")
        
        self.version_edit = QLineEdit()
        self.version_edit.setText("1.0")
        
        metadata_layout.addRow("Author:", self.author_edit)
        metadata_layout.addRow("Category:", self.category_edit)
        metadata_layout.addRow("Tags:", self.tags_edit)
        metadata_layout.addRow("Version:", self.version_edit)
        
        layout.addWidget(metadata_group)
        
        # Create button
        create_btn = QPushButton("Create Personality")
        create_btn.clicked.connect(self.create_personality)
        layout.addWidget(create_btn)
        
        layout.addStretch()
        
        self.tabs.addTab(creation_widget, "Create Personality")
        
        # Apply stylesheet
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
        """)
    
    def setup_management_tab(self):
        """Setup the personality management tab"""
        management_widget = QWidget()
        layout = QVBoxLayout(management_widget)
        
        # Custom personalities list
        list_group = QGroupBox("Custom Personalities")
        list_layout = QVBoxLayout(list_group)
        
        self.custom_list = QListWidget()
        self.custom_list.itemClicked.connect(self.on_custom_personality_selected)
        list_layout.addWidget(self.custom_list)
        
        # Management buttons
        btn_layout = QHBoxLayout()
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_custom_personality)
        self.export_btn = QPushButton("Export Selected")
        self.export_btn.clicked.connect(self.export_personality)
        
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.export_btn)
        list_layout.addLayout(btn_layout)
        
        layout.addWidget(list_group)
        
        # Personality details
        details_group = QGroupBox("Personality Details")
        details_layout = QVBoxLayout(details_group)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        details_layout.addWidget(self.details_text)
        
        layout.addWidget(details_group)
        
        self.tabs.addTab(management_widget, "Manage Personalities")
    
    def load_personalities(self):
        """Load available personalities into the combo box"""
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
        
        # Load custom personalities into list (all personalities are now in the same system)
        self.custom_list.clear()
        # For now, we'll consider all personalities as available for management
        # In the future, you might want to distinguish between built-in and custom
        self.custom_list.addItems(personalities)
        
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
    
    def on_personality_changed(self, personality_name: str):
        """Handle personality selection change"""
        if personality_name:
            # Get the actual personality name from combo box data
            current_index = self.personality_combo.currentIndex()
            actual_personality_name = self.personality_combo.itemData(current_index)
            
            if actual_personality_name:
                # Set the current personality in the model
                self.personality_model.set_current_personality(actual_personality_name)
                self.update_personality_info(actual_personality_name)
                self.personality_changed.emit(actual_personality_name)
    
    def set_personality(self, personality_name: str):
        """Set a specific personality"""
        # Find the personality in the combo box
        for i in range(self.personality_combo.count()):
            if self.personality_combo.itemData(i) == personality_name:
                self.personality_combo.setCurrentIndex(i)
                break
        # Ensure the personality model is updated
        self.personality_model.set_current_personality(personality_name)
    
    def update_personality_info(self, personality_name: str):
        """Update the personality info display"""
        info = self.personality_model.get_personality_info(personality_name)
        if info:
            # Get full personality data for examples, constraints, config, and metadata
            personality_data = self.personality_model.get_personality(personality_name)
            prompt_data = personality_data.get('prompt', {}) if personality_data else {}
            config_data = personality_data.get('config', {}) if personality_data else {}
            metadata_data = personality_data.get('metadata', {}) if personality_data else {}
            
            info_text = f"""Name: {info['name']}
Description: {info['description']}
Tone: {info['tone']}
Style: {info['style']}
Expertise: {', '.join(info['expertise'])}
Conversation Style: {info['conversation_style']}
Response Length: {info['response_length']}
Formality Level: {info['formality_level']}
Humor Level: {info['humor_level']}
Use Emojis: {'Yes' if info['emoji_usage'] else 'No'}
Format Code: {'Yes' if info['code_formatting'] else 'No'}
Provide Examples: {'Yes' if info['examples_usage'] else 'No'}
Ask Questions: {'Yes' if info['questions_usage'] else 'No'}"""
            
            # Add configuration information
            if config_data:
                info_text += "\n\nCONFIGURATION:"
                info_text += f"\n• Temperature: {config_data.get('temperature', 0.7)}"
                info_text += f"\n• Max Tokens: {config_data.get('max_tokens', 2048)}"
                info_text += f"\n• Top-p: {config_data.get('top_p', 0.9)}"
                info_text += f"\n• Use Prompt Templates: {'Yes' if config_data.get('use_prompt_templates', True) else 'No'}"
            
            # Add metadata information
            if metadata_data:
                info_text += "\n\nMETADATA:"
                if metadata_data.get('author'):
                    info_text += f"\n• Author: {metadata_data['author']}"
                if metadata_data.get('category'):
                    info_text += f"\n• Category: {metadata_data['category']}"
                if metadata_data.get('version'):
                    info_text += f"\n• Version: {metadata_data['version']}"
                if metadata_data.get('created_date'):
                    info_text += f"\n• Created: {metadata_data['created_date']}"
                if metadata_data.get('last_modified'):
                    info_text += f"\n• Last Modified: {metadata_data['last_modified']}"
                if metadata_data.get('tags'):
                    info_text += f"\n• Tags: {', '.join(metadata_data['tags'])}"
            
            # Add examples if available
            examples = prompt_data.get('examples', [])
            if examples:
                info_text += "\n\nEXAMPLE RESPONSES:"
                for i, example in enumerate(examples, 1):
                    info_text += f"\n{i}. {example}"
            
            # Add constraints if available
            constraints = prompt_data.get('constraints', [])
            if constraints:
                info_text += "\n\nCONSTRAINTS:"
                for constraint in constraints:
                    info_text += f"\n• {constraint}"
            
            self.personality_info.setText(info_text)
            
            # Also update the details text in management tab
            self.details_text.setText(info_text)
    
    def create_personality(self):
        """Create a new custom personality"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a personality name")
            return
        
        if name in self.personality_model.get_available_personalities():
            QMessageBox.warning(self, "Warning", "A personality with this name already exists")
            return
        
        try:
            # Create traits
            traits = PersonalityTraits(
                name=name,
                description=self.description_edit.toPlainText().strip(),
                tone=self.tone_edit.text().strip(),
                style=self.style_edit.text().strip(),
                expertise=[x.strip() for x in self.expertise_edit.toPlainText().split(',') if x.strip()],
                conversation_style=self.conversation_style_combo.currentText(),
                response_length=self.response_length_combo.currentText(),
                formality_level=self.formality_combo.currentText(),
                humor_level=self.humor_combo.currentText(),
                emoji_usage=self.emoji_checkbox.isChecked(),
                code_formatting=self.code_checkbox.isChecked(),
                examples_usage=self.examples_checkbox.isChecked(),
                questions_usage=self.questions_checkbox.isChecked()
            )
            
            # Create prompt
            prompt = PersonalityPrompt(
                system_prompt=self.system_prompt_edit.toPlainText().strip(),
                user_prompt_template=self.user_prompt_edit.toPlainText().strip(),
                context_prompt=self.context_prompt_edit.toPlainText().strip(),
                examples=[x.strip() for x in self.examples_edit.toPlainText().split('\n') if x.strip()],
                constraints=[x.strip() for x in self.constraints_edit.toPlainText().split('\n') if x.strip()]
            )
            
            # Create configuration
            config = PersonalityConfig(
                temperature=self.temperature_spin.value() / 10.0,
                max_tokens=self.max_tokens_spin.value(),
                top_p=self.top_p_spin.value() / 100.0,
                use_prompt_templates=self.use_templates_checkbox.isChecked()
            )
            
            # Create metadata
            metadata = PersonalityMetadata(
                author=self.author_edit.text().strip(),
                category=self.category_edit.text().strip(),
                tags=[x.strip() for x in self.tags_edit.text().split(',') if x.strip()],
                version=self.version_edit.text().strip()
            )
            
            # Create the personality
            success = self.personality_model.create_custom_personality(name, traits, prompt, config, metadata)
            
            if success:
                QMessageBox.information(self, "Success", f"Personality '{name}' created successfully!")
                self.load_personalities()
                self.clear_creation_form()
            else:
                QMessageBox.critical(self, "Error", "Failed to create personality")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error creating personality: {str(e)}")
    
    def clear_creation_form(self):
        """Clear the personality creation form"""
        self.name_edit.clear()
        self.description_edit.clear()
        self.tone_edit.clear()
        self.style_edit.clear()
        self.expertise_edit.clear()
        self.conversation_style_combo.setCurrentIndex(0)
        self.response_length_combo.setCurrentIndex(0)
        self.formality_combo.setCurrentIndex(0)
        self.humor_combo.setCurrentIndex(0)
        self.emoji_checkbox.setChecked(False)
        self.code_checkbox.setChecked(False)
        self.examples_checkbox.setChecked(False)
        self.questions_checkbox.setChecked(False)
        self.system_prompt_edit.clear()
        self.user_prompt_edit.clear()
        self.context_prompt_edit.clear()
        self.examples_edit.clear()
        self.constraints_edit.clear()
        
        # Clear new fields
        self.temperature_spin.setValue(7)
        self.max_tokens_spin.setValue(2048)
        self.top_p_spin.setValue(90)
        self.use_templates_checkbox.setChecked(True)
        self.author_edit.clear()
        self.category_edit.clear()
        self.tags_edit.clear()
        self.version_edit.setText("1.0")
    
    def on_custom_personality_selected(self, item):
        """Handle custom personality selection in management tab"""
        personality_name = item.text()
        info = self.personality_model.get_personality_info(personality_name)
        if info:
            self.update_personality_info(personality_name)
    
    def delete_custom_personality(self):
        """Delete the selected custom personality"""
        current_item = self.custom_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a personality to delete")
            return
        
        personality_name = current_item.text()
        confirm = QMessageBox.question(self, "Confirm Delete", 
                                     f"Are you sure you want to delete '{personality_name}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            success = self.personality_model.delete_custom_personality(personality_name)
            if success:
                QMessageBox.information(self, "Success", f"Personality '{personality_name}' deleted successfully!")
                self.load_personalities()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete personality")
    
    def export_personality(self):
        """Export the selected personality (placeholder for future implementation)"""
        current_item = self.custom_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a personality to export")
            return
        
        QMessageBox.information(self, "Info", "Export functionality will be implemented in a future version")
    
    def get_current_personality(self) -> str:
        """Get the currently selected personality name"""
        current_index = self.personality_combo.currentIndex()
        actual_personality_name = self.personality_combo.itemData(current_index)
        return actual_personality_name if actual_personality_name else ""
    
    def get_formatted_prompt(self, user_input: str, context: str = "") -> str:
        """Get a formatted prompt using the current personality"""
        return self.personality_model.format_prompt_with_personality(user_input, context)
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the current personality"""
        return self.personality_model.get_system_prompt()

    def get_available_personalities(self) -> list:
        """Get list of available personality names"""
        return self.personality_model.get_available_personalities()

    def get_comprehensive_system_prompt(self, memory_service=None, is_new_conversation=False) -> str:
        """Get a comprehensive system prompt that includes all personality components and user information from memory."""
        # Use the personality model's comprehensive system prompt method
        return self.personality_model.build_comprehensive_system_prompt(memory_service)

    def get_user_context_messages(self, memory_service=None, is_new_conversation=False) -> List[Dict]:
        """Get dynamic user context messages that should be added to conversation"""
        return self.personality_model.get_user_context_messages(memory_service, is_new_conversation)

    def refresh_personalities(self):
        """Refresh personalities from disk"""
        # Call the model's refresh method
        success = self.personality_model.refresh_personalities()
        if success:
            # Reload the UI with updated personalities
            self.load_personalities()
            # Update the current personality info
            current_personality = self.personality_model.get_current_personality()
            if current_personality:
                self.update_personality_info(self.personality_combo.currentText())
        else:
            QMessageBox.warning(self, "Warning", "Failed to refresh personalities from disk")

    def on_personality_changed(self, personality_name: str):
        """Handle personality selection change"""
        if personality_name:
            # Get the actual personality name from combo box data
            current_index = self.personality_combo.currentIndex()
            actual_personality_name = self.personality_combo.itemData(current_index)
            
            if actual_personality_name:
                # Set the current personality in the model
                self.personality_model.set_current_personality(actual_personality_name)
                self.update_personality_info(actual_personality_name)
                self.personality_changed.emit(actual_personality_name) 