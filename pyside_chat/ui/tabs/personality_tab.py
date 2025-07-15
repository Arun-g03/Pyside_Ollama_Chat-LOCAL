from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.features.personality.models.personality_model import PersonalityModel

"""
Personality Tab - Extracted from ollama_chat.py
Handles personality selection and management.
"""

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
        self.personality_combo.currentTextChanged.connect(
            self.on_personality_changed)
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
        refresh_button.setToolTip(
            "Refresh personalities from disk (useful for nested folders)")
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

        # Create scroll area for better organization
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #777;
            }
        """)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

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
        self.name_edit.setPlaceholderText("Enter personality name")

        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(60)
        self.description_edit.setPlaceholderText(
            "Enter personality description")

        self.tone_edit = QLineEdit()
        self.tone_edit.setPlaceholderText(
            "e.g., friendly, professional, humorous")

        self.style_edit = QLineEdit()
        self.style_edit.setPlaceholderText("e.g., casual, formal, creative")

        basic_layout.addRow("Name:", self.name_edit)
        basic_layout.addRow("Description:", self.description_edit)
        basic_layout.addRow("Tone:", self.tone_edit)
        basic_layout.addRow("Style:", self.style_edit)

        scroll_layout.addWidget(basic_group)

        # Traits configuration
        traits_group = QGroupBox("Traits Configuration")
        traits_layout = QFormLayout(traits_group)
        traits_layout.setLabelAlignment(Qt.AlignRight)

        self.expertise_edit = QTextEdit()
        self.expertise_edit.setMaximumHeight(60)
        self.expertise_edit.setPlaceholderText(
            "Enter expertise areas (one per line)")

        self.conversation_style_combo = QComboBox()
        self.conversation_style_combo.addItems(["conversational", "professional", "casual",
                                               "formal", "friendly", "mentoring", "entertaining", "inspirational", "exploratory"])

        self.response_length_combo = QComboBox()
        self.response_length_combo.addItems(
            ["brief", "detailed", "comprehensive"])

        self.formality_level_combo = QComboBox()
        self.formality_level_combo.addItems(
            ["casual", "semi-formal", "formal"])

        self.humor_level_combo = QComboBox()
        self.humor_level_combo.addItems(["none", "subtle", "moderate", "high"])

        self.emoji_usage_check = QCheckBox("Use emojis")
        self.emoji_usage_check.setChecked(True)

        self.code_formatting_check = QCheckBox("Enable code formatting")
        self.code_formatting_check.setChecked(False)

        self.examples_usage_check = QCheckBox("Include examples")
        self.examples_usage_check.setChecked(True)

        self.questions_usage_check = QCheckBox("Ask questions")
        self.questions_usage_check.setChecked(True)

        traits_layout.addRow("Expertise:", self.expertise_edit)
        traits_layout.addRow("Conversation Style:",
                             self.conversation_style_combo)
        traits_layout.addRow("Response Length:", self.response_length_combo)
        traits_layout.addRow("Formality Level:", self.formality_level_combo)
        traits_layout.addRow("Humor Level:", self.humor_level_combo)
        traits_layout.addRow("", self.emoji_usage_check)
        traits_layout.addRow("", self.code_formatting_check)
        traits_layout.addRow("", self.examples_usage_check)
        traits_layout.addRow("", self.questions_usage_check)

        scroll_layout.addWidget(traits_group)

        # Prompt configuration
        prompt_group = QGroupBox("Prompt Configuration")
        prompt_layout = QVBoxLayout(prompt_group)

        # System prompt
        system_prompt_label = QLabel("System Prompt:")
        self.system_prompt_edit = QTextEdit()
        self.system_prompt_edit.setMaximumHeight(100)
        self.system_prompt_edit.setPlaceholderText(
            "Enter the system prompt for this personality")

        # Conversation style template
        conversation_style_label = QLabel("Conversation Style Template:")
        conversation_style_layout = QHBoxLayout()

        self.conversation_style_template_combo = QComboBox()
        self.conversation_style_template_combo.addItems([
            "Simple: User: {user_input}\nAssistant:",
            "Formal: {user_title} {user_name}: {user_input}\nAssistant:",
            "Casual: Hey! {user_input}\nAssistant:",
            "Professional: Client: {user_input}\nConsultant:",
            "Character-based: Human: {user_input}\n{character_name}:",
            "Custom..."
        ])
        self.conversation_style_template_combo.currentTextChanged.connect(
            self.on_conversation_style_changed)

        conversation_style_layout.addWidget(
            self.conversation_style_template_combo)

        # Custom conversation template
        self.custom_conversation_edit = QLineEdit()
        self.custom_conversation_edit.setPlaceholderText(
            "Or enter custom template with keywords like {user_input}, {user_name}, etc.")
        self.custom_conversation_edit.setVisible(False)
        conversation_style_layout.addWidget(self.custom_conversation_edit)

        # Context template
        context_template_label = QLabel("Context Template:")
        context_template_layout = QHBoxLayout()

        self.context_template_combo = QComboBox()
        self.context_template_combo.addItems([
            "Simple: Previous conversation:\n{context}\n\nUser: {user_input}",
            "Detailed: Our conversation history:\n{context}\n\nCurrent question: {user_input}",
            "Formal: Previous consultation:\n{context}\n\nCurrent inquiry: {user_input}",
            "Character: Our story so far:\n{context}\n\nHuman: {user_input}",
            "Custom..."
        ])
        self.context_template_combo.currentTextChanged.connect(
            self.on_context_template_changed)

        context_template_layout.addWidget(self.context_template_combo)

        # Custom context template
        self.custom_context_edit = QTextEdit()
        self.custom_context_edit.setMaximumHeight(60)
        self.custom_context_edit.setPlaceholderText(
            "Or enter custom context template")
        self.custom_context_edit.setVisible(False)
        context_template_layout.addWidget(self.custom_context_edit)

        # Available keywords help
        keywords_label = QLabel("Available Keywords:")
        keywords_label.setStyleSheet("color: #888; font-size: 12px;")
        keywords_text = QLabel(
            "{user_input} - User's message\n{user_name} - User's name\n{user_title} - User's title\n{context} - Previous conversation\n{character_name} - Personality name")
        keywords_text.setStyleSheet(
            "color: #888; font-size: 11px; background-color: #1a1a1a; padding: 8px; border-radius: 4px;")
        keywords_text.setWordWrap(True)

        # Examples
        examples_label = QLabel("Example Responses:")
        self.examples_edit = QTextEdit()
        self.examples_edit.setMaximumHeight(80)
        self.examples_edit.setPlaceholderText(
            "Enter example responses (one per line)")

        # Constraints
        constraints_label = QLabel("Constraints:")
        self.constraints_edit = QTextEdit()
        self.constraints_edit.setMaximumHeight(80)
        self.constraints_edit.setPlaceholderText(
            "Enter constraints (one per line)")

        prompt_layout.addWidget(system_prompt_label)
        prompt_layout.addWidget(self.system_prompt_edit)
        prompt_layout.addWidget(conversation_style_label)
        prompt_layout.addLayout(conversation_style_layout)
        prompt_layout.addWidget(context_template_label)
        prompt_layout.addLayout(context_template_layout)
        prompt_layout.addWidget(keywords_label)
        prompt_layout.addWidget(keywords_text)
        prompt_layout.addWidget(examples_label)
        prompt_layout.addWidget(self.examples_edit)
        prompt_layout.addWidget(constraints_label)
        prompt_layout.addWidget(self.constraints_edit)

        scroll_layout.addWidget(prompt_group)

        # Configuration
        config_group = QGroupBox("Model Configuration")
        config_layout = QFormLayout(config_group)
        config_layout.setLabelAlignment(Qt.AlignRight)

        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 2.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(0.7)
        self.temperature_spin.setDecimals(1)

        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(512, 8192)
        self.max_tokens_spin.setSingleStep(512)
        self.max_tokens_spin.setValue(2048)

        self.top_p_spin = QDoubleSpinBox()
        self.top_p_spin.setRange(0.0, 1.0)
        self.top_p_spin.setSingleStep(0.1)
        self.top_p_spin.setValue(0.9)
        self.top_p_spin.setDecimals(1)

        self.frequency_penalty_spin = QDoubleSpinBox()
        self.frequency_penalty_spin.setRange(-2.0, 2.0)
        self.frequency_penalty_spin.setSingleStep(0.1)
        self.frequency_penalty_spin.setValue(0.0)
        self.frequency_penalty_spin.setDecimals(1)

        self.presence_penalty_spin = QDoubleSpinBox()
        self.presence_penalty_spin.setRange(-2.0, 2.0)
        self.presence_penalty_spin.setSingleStep(0.1)
        self.presence_penalty_spin.setValue(0.0)
        self.presence_penalty_spin.setDecimals(1)

        self.use_prompt_templates_check = QCheckBox("Use prompt templates")
        self.use_prompt_templates_check.setChecked(True)

        config_layout.addRow("Temperature:", self.temperature_spin)
        config_layout.addRow("Max Tokens:", self.max_tokens_spin)
        config_layout.addRow("Top P:", self.top_p_spin)
        config_layout.addRow("Frequency Penalty:", self.frequency_penalty_spin)
        config_layout.addRow("Presence Penalty:", self.presence_penalty_spin)
        config_layout.addRow("", self.use_prompt_templates_check)

        scroll_layout.addWidget(config_group)

        # Metadata
        metadata_group = QGroupBox("Metadata")
        metadata_layout = QFormLayout(metadata_group)
        metadata_layout.setLabelAlignment(Qt.AlignRight)

        self.category_combo = QComboBox()
        self.category_combo.addItems(
            ["custom", "professions", "family", "historic", "specialists"])

        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Enter tags separated by commas")

        metadata_layout.addRow("Category:", self.category_combo)
        metadata_layout.addRow("Tags:", self.tags_edit)

        scroll_layout.addWidget(metadata_group)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

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
        self.system_personalities_list.itemClicked.connect(
            self.on_system_personality_selected)
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
        self.custom_personalities_list.itemClicked.connect(
            self.on_custom_personality_selected)
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
        sorted_personalities = sorted(
            personalities, key=lambda x: (x.count('.'), x))

        # Add personalities with folder structure display
        for personality in sorted_personalities:
            if '.' in personality:
                # Show folder structure in display
                parts = personality.split('.')
                display_name = f"{' → '.join(parts[:-1])} → {parts[-1]}"
                # Store original name as data
                self.personality_combo.addItem(display_name, personality)
            else:
                # Simple personality name
                self.personality_combo.addItem(personality, personality)

        # Update system and custom personalities lists
        self.update_system_personalities_list()
        self.update_custom_personalities_list()

        # Set default personality
        if personalities:
            # Try to set Specialists.assistant personality first, then assistant, otherwise use first available
            if "Specialists.assistant" in personalities:
                self.personality_combo.setCurrentText(
                    "Specialists → assistant")
                self.personality_model.set_current_personality(
                    "Specialists.assistant")
                self.update_personality_info("Specialists.assistant")
            elif "assistant" in personalities:
                self.personality_combo.setCurrentText("assistant")
                self.personality_model.set_current_personality("assistant")
                self.update_personality_info("assistant")
            else:
                first_personality = sorted_personalities[0]
                self.personality_combo.setCurrentText(first_personality)
                self.personality_model.set_current_personality(
                    first_personality)
                self.update_personality_info(first_personality)

    def update_system_personalities_list(self):
        """Update the system personalities list"""
        try:
            system_personalities = self.personality_model.service.get_system_personalities()
            self.system_personalities_list.clear()

            for personality in system_personalities:
                self.system_personalities_list.addItem(personality)
        except Exception as e:
            logger.debug(
                f"[ID:0097] Failed to update system personalities list: {e}", print_to_terminal=True)
            logger.debug(traceback.format_exc(), print_to_terminal=True)

    def update_custom_personalities_list(self):
        """Update the custom personalities list"""
        try:
            custom_personalities = self.personality_model.service.get_custom_personalities()
            self.custom_personalities_list.clear()

            for personality in custom_personalities:
                self.custom_personalities_list.addItem(personality)
        except Exception as e:
            logger.debug(
                f"[ID:0096] Failed to update custom personalities list: {e}", print_to_terminal=True)

    def on_system_personality_selected(self, item):
        """Handle system personality selection"""
        if item:
            personality_name = item.text()
            self.update_system_personality_info(personality_name)

    def update_system_personality_info(self, personality_name: str):
        """Update the system personality info display"""
        try:
            personality_data = self.personality_model.get_personality(
                personality_name)
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
            self.system_personality_info.setText(
                f"Error loading personality info: {e}")

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
            personality_data = self.personality_model.get_personality(
                personality_name)
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
                self.personality_info.setPlainText(
                    "No information available for this personality.")
        except Exception as e:
            self.personality_info.setPlainText(
                f"Error loading personality info: {str(e)}")

    def create_personality(self):
        """Create a new personality"""
        try:
            # Get basic form data
            name = self.name_edit.text().strip()
            description = self.description_edit.toPlainText().strip()
            tone = self.tone_edit.text().strip()
            style = self.style_edit.text().strip()

            # Get traits data
            expertise_text = self.expertise_edit.toPlainText().strip()
            expertise = [line.strip()
                         for line in expertise_text.split('\n') if line.strip()]
            conversation_style = self.conversation_style_combo.currentText()
            response_length = self.response_length_combo.currentText()
            formality_level = self.formality_level_combo.currentText()
            humor_level = self.humor_level_combo.currentText()
            emoji_usage = self.emoji_usage_check.isChecked()
            code_formatting = self.code_formatting_check.isChecked()
            examples_usage = self.examples_usage_check.isChecked()
            questions_usage = self.questions_usage_check.isChecked()

            # Get prompt data
            system_prompt = self.system_prompt_edit.toPlainText().strip()
            user_prompt_template = self.get_user_prompt_template()
            context_prompt = self.get_context_prompt()
            examples_text = self.examples_edit.toPlainText().strip()
            examples = [line.strip()
                        for line in examples_text.split('\n') if line.strip()]
            constraints_text = self.constraints_edit.toPlainText().strip()
            constraints = [line.strip()
                           for line in constraints_text.split('\n') if line.strip()]

            # Get config data
            temperature = self.temperature_spin.value()
            max_tokens = self.max_tokens_spin.value()
            top_p = self.top_p_spin.value()
            frequency_penalty = self.frequency_penalty_spin.value()
            presence_penalty = self.presence_penalty_spin.value()
            use_prompt_templates = self.use_prompt_templates_check.isChecked()

            # Get metadata
            category = self.category_combo.currentText()
            tags_text = self.tags_edit.text().strip()
            tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]

            # Validate required fields
            if not name:
                QMessageBox.warning(
                    self, "Warning", "Please enter a personality name")
                return

            if not system_prompt:
                QMessageBox.warning(
                    self, "Warning", "Please enter a system prompt")
                return

            # Create personality objects
            from pyside_chat.features.personality.models.personality_model import PersonalityTraits, PersonalityPrompt, PersonalityConfig, PersonalityMetadata

            traits = PersonalityTraits(
                name=name,
                description=description,
                tone=tone,
                style=style,
                expertise=expertise,
                conversation_style=conversation_style,
                response_length=response_length,
                formality_level=formality_level,
                humor_level=humor_level,
                emoji_usage=emoji_usage,
                code_formatting=code_formatting,
                examples_usage=examples_usage,
                questions_usage=questions_usage
            )

            prompt = PersonalityPrompt(
                system_prompt=system_prompt,
                user_prompt_template=user_prompt_template,
                context_prompt=context_prompt,
                examples=examples,
                constraints=constraints
            )

            config = PersonalityConfig(
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                use_prompt_templates=use_prompt_templates
            )

            metadata = PersonalityMetadata(
                category=category,
                tags=tags,
                created_date=datetime.now().isoformat(),
                last_modified=datetime.now().isoformat()
            )

            # Create personality
            success = self.personality_model.create_custom_personality(
                name, traits, prompt, config, metadata)

            if success:
                # Refresh lists
                self.load_personalities()

                # Clear form
                self.clear_creation_form()

                QMessageBox.information(
                    self, "Success", f"Personality '{name}' created successfully!")
            else:
                QMessageBox.warning(
                    self, "Warning", f"Failed to create personality '{name}'. It may already exist.")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to create personality: {str(e)}")
            logger.error(f"Error creating personality: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")

    def clear_creation_form(self):
        """Clear the personality creation form"""
        # Basic information
        self.name_edit.clear()
        self.description_edit.clear()
        self.tone_edit.clear()
        self.style_edit.clear()

        # Traits configuration
        self.expertise_edit.clear()
        self.conversation_style_combo.setCurrentIndex(0)
        self.response_length_combo.setCurrentIndex(0)
        self.formality_level_combo.setCurrentIndex(0)
        self.humor_level_combo.setCurrentIndex(0)
        self.emoji_usage_check.setChecked(True)
        self.code_formatting_check.setChecked(False)
        self.examples_usage_check.setChecked(True)
        self.questions_usage_check.setChecked(True)

        # Prompt configuration
        self.system_prompt_edit.clear()
        self.conversation_style_template_combo.setCurrentIndex(0)
        self.custom_conversation_edit.clear()
        self.custom_conversation_edit.setVisible(False)
        self.context_template_combo.setCurrentIndex(0)
        self.custom_context_edit.clear()
        self.custom_context_edit.setVisible(False)
        self.examples_edit.clear()
        self.constraints_edit.clear()

        # Configuration
        self.temperature_spin.setValue(0.7)
        self.max_tokens_spin.setValue(2048)
        self.top_p_spin.setValue(0.9)
        self.frequency_penalty_spin.setValue(0.0)
        self.presence_penalty_spin.setValue(0.0)
        self.use_prompt_templates_check.setChecked(True)

        # Metadata
        self.category_combo.setCurrentIndex(0)
        self.tags_edit.clear()

    def delete_custom_personality(self):
        """Delete the selected custom personality"""
        current_item = self.custom_personalities_list.currentItem()
        if not current_item:
            QMessageBox.warning(
                self, "Warning", "Cannot delete system personality")
            return

        personality_name = current_item.text()

        # Check if it's actually a custom personality
        if not self.personality_model.service.is_custom_personality(personality_name):
            QMessageBox.warning(
                self, "Warning", f"Cannot delete system personality '{personality_name}'")
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
                success = self.personality_model.delete_custom_personality(
                    personality_name)
                if success:
                    self.load_personalities()
                    QMessageBox.information(
                        self, "Success", f"Personality '{personality_name}' deleted successfully!")
                else:
                    QMessageBox.warning(
                        self, "Warning", f"Failed to delete personality '{personality_name}'")
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Error deleting personality: {str(e)}")

    def export_personality(self):
        """Export the selected personality to a file"""
        current_item = self.custom_personalities_list.currentItem()
        if not current_item:
            QMessageBox.warning(
                self, "Warning", "Please select a personality to export")
            return

        personality_name = current_item.text()

        try:
            personality_data = self.personality_model.get_personality(
                personality_name)
            if not personality_data:
                QMessageBox.warning(
                    self, "Warning", f"Could not load personality '{personality_name}'")
                return

            # TODO: Implement export functionality
            QMessageBox.information(
                self, "Info", f"Export functionality for '{personality_name}' will be implemented soon!")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error exporting personality: {str(e)}")

    def refresh_personalities(self):
        """Refresh personalities from disk"""
        try:
            self.personality_model.refresh_personalities()
            self.load_personalities()
            QMessageBox.information(
                self, "Success", "Personalities refreshed successfully!")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to refresh personalities: {str(e)}")

    def get_current_personality(self) -> str:
        """Get the currently selected personality name"""
        return self.personality_model.get_selected_model()

    def get_system_prompt(self) -> str:
        """Get the system prompt for the current personality"""
        current_personality = self.get_current_personality()
        if current_personality:
            try:
                personality_data = self.personality_model.get_personality(
                    current_personality)
                return personality_data.get('system_prompt', '') if personality_data else ''
            except:
                return ''
        return ''

    def get_available_personalities(self) -> list:
        """Get list of available personality names"""
        try:
            return self.personality_model.get_available_personalities()
        except Exception as e:
            logger.debug(
                f"[ID:0095] Error getting available personalities: {e}", print_to_terminal=True)
            return []

    def on_conversation_style_changed(self, text):
        """Handle conversation style template selection"""
        if text == "Custom...":
            self.custom_conversation_edit.setVisible(True)
            self.custom_conversation_edit.setFocus()
        else:
            self.custom_conversation_edit.setVisible(False)

    def on_context_template_changed(self, text):
        """Handle context template selection"""
        if text == "Custom...":
            self.custom_context_edit.setVisible(True)
            self.custom_context_edit.setFocus()
        else:
            self.custom_context_edit.setVisible(False)

    def get_user_prompt_template(self):
        """Get the user prompt template from the form"""
        if self.conversation_style_template_combo.currentText() == "Custom...":
            return self.custom_conversation_edit.text().strip()
        else:
            # Extract template from dropdown text
            text = self.conversation_style_template_combo.currentText()
            if ":" in text:
                return text.split(":", 1)[1].strip()
            return text

    def get_context_prompt(self):
        """Get the context prompt from the form"""
        if self.context_template_combo.currentText() == "Custom...":
            return self.custom_context_edit.toPlainText().strip()
        else:
            # Extract template from dropdown text
            text = self.context_template_combo.currentText()
            if ":" in text:
                return text.split(":", 1)[1].strip()
            return text
