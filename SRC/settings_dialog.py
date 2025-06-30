from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QCheckBox, QSpinBox,
                               QFormLayout, QGroupBox, QMessageBox, QTabWidget,
                               QWidget)
from PySide6.QtCore import Qt, QTimer
from SRC.config_manager import ConfigManager
from SRC.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class SettingsDialog(QDialog):
    """Dialog for configuring application settings"""
    
    def __init__(self, config_manager: ConfigManager, available_models: list, available_personalities: list, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.available_models = available_models
        self.available_personalities = available_personalities
        self.ui_ready = False
        self.setup_ui()
        
        # Delay loading settings until UI is fully ready
        QTimer.singleShot(50, self._delayed_load_settings)
    
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 500, 400)
        
        layout = QVBoxLayout(self)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # General settings tab
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "General")
        
        # Chat settings tab
        chat_tab = self.create_chat_tab()
        tabs.addTab(chat_tab, "Chat")
        
        # Session variables tab
        session_tab = self.create_session_tab()
        tabs.addTab(session_tab, "Session Variables")
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        reset_button = QPushButton("Reset to Defaults")
        reset_button.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(reset_button)
        
        layout.addLayout(button_layout)
    
    def create_general_tab(self):
        """Create the general settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Default model group
        model_group = QGroupBox("Default Model")
        model_layout = QFormLayout(model_group)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.available_models)
        model_layout.addRow("Default Model:", self.model_combo)
        
        layout.addWidget(model_group)
        
        # Default personality group
        personality_group = QGroupBox("Default Personality")
        personality_layout = QFormLayout(personality_group)
        
        self.personality_combo = QComboBox()
        self.personality_combo.addItems(self.available_personalities)
        personality_layout.addRow("Default Personality:", self.personality_combo)
        
        layout.addWidget(personality_group)
        
        # Default temperature group
        temp_group = QGroupBox("Default Temperature")
        temp_layout = QFormLayout(temp_group)
        
        self.temp_spin = QSpinBox()
        self.temp_spin.setRange(1, 20)
        self.temp_spin.setSuffix(" (×0.1)")
        self.temp_spin.setToolTip("Temperature setting (0.1 to 2.0)")
        temp_layout.addRow("Default Temperature:", self.temp_spin)
        
        layout.addWidget(temp_group)
        
        # Default theme group
        theme_group = QGroupBox("Theme")
        theme_layout = QFormLayout(theme_group)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        theme_layout.addRow("Theme:", self.theme_combo)
        layout.addWidget(theme_group)
        
        # Window settings group
        window_group = QGroupBox("Window Settings")
        window_layout = QFormLayout(window_group)
        
        self.width_spin = QSpinBox()
        self.width_spin.setRange(800, 2000)
        self.width_spin.setSuffix(" px")
        window_layout.addRow("Default Width:", self.width_spin)
        
        self.height_spin = QSpinBox()
        self.height_spin.setRange(600, 1500)
        self.height_spin.setSuffix(" px")
        window_layout.addRow("Default Height:", self.height_spin)
        
        layout.addWidget(window_group)
        
        layout.addStretch()
        return widget
    
    def create_chat_tab(self):
        """Create the chat settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # General chat options
        options_group = QGroupBox("Chat Options")
        options_layout = QVBoxLayout(options_group)
        
        self.auto_save_checkbox = QCheckBox("Enable Auto-Save")
        self.auto_save_checkbox.setToolTip("Automatically save conversations")
        options_layout.addWidget(self.auto_save_checkbox)
        
        self.spellcheck_checkbox = QCheckBox("Enable Spell Check")
        self.spellcheck_checkbox.setToolTip("Enable spell checking in chat input")
        options_layout.addWidget(self.spellcheck_checkbox)
        
        self.enhancement_checkbox = QCheckBox("Enable Response Enhancement")
        self.enhancement_checkbox.setToolTip("Automatically enhance AI responses with additional details")
        options_layout.addWidget(self.enhancement_checkbox)
        
        self.memory_checkbox = QCheckBox("Enable Memory Management")
        self.memory_checkbox.setToolTip("Enable or disable LLM memory management features")
        options_layout.addWidget(self.memory_checkbox)
        
        layout.addWidget(options_group)
        
        # Chat parameters group
        params_group = QGroupBox("Chat Parameters")
        params_layout = QFormLayout(params_group)
        
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(100, 8192)
        self.max_tokens_spin.setSuffix(" tokens")
        params_layout.addRow("Max Tokens:", self.max_tokens_spin)
        
        self.top_p_spin = QSpinBox()
        self.top_p_spin.setRange(1, 100)
        self.top_p_spin.setSuffix(" (×0.01)")
        self.top_p_spin.setToolTip("Top-p setting (0.01 to 1.0)")
        params_layout.addRow("Top-p:", self.top_p_spin)
        
        layout.addWidget(params_group)
        
        layout.addStretch()
        return widget
    
    def create_session_tab(self):
        """Create the session variables tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Session variables group
        session_group = QGroupBox("Model Session Variables")
        session_layout = QVBoxLayout(session_group)
        
        self.history_checkbox = QCheckBox("Enable History")
        self.history_checkbox.setToolTip("Enable conversation history (/set history)")
        session_layout.addWidget(self.history_checkbox)
        
        self.wordwrap_checkbox = QCheckBox("Enable Word Wrap")
        self.wordwrap_checkbox.setToolTip("Enable word wrapping (/set wordwrap)")
        session_layout.addWidget(self.wordwrap_checkbox)
        
        self.json_format_checkbox = QCheckBox("Enable JSON Mode")
        self.json_format_checkbox.setToolTip("Force responses in JSON format (/set format json)")
        session_layout.addWidget(self.json_format_checkbox)
        
        self.verbose_checkbox = QCheckBox("Enable Verbose")
        self.verbose_checkbox.setToolTip("Show detailed LLM statistics (/set verbose)")
        session_layout.addWidget(self.verbose_checkbox)
        
        self.think_checkbox = QCheckBox("Enable Think Mode")
        self.think_checkbox.setToolTip("Enable thinking mode (/set think)")
        session_layout.addWidget(self.think_checkbox)
        
        layout.addWidget(session_group)
        
        # Add description
        description = QLabel("These settings control Ollama session behavior using /set commands. Changes take effect immediately for new conversations.")
        description.setWordWrap(True)
        description.setStyleSheet("color: #888; font-style: italic;")
        layout.addWidget(description)
        
        layout.addStretch()
        return widget
    
    def _delayed_load_settings(self):
        """Load settings after UI is fully ready"""
        self.ui_ready = True
        self.load_current_settings()
    
    def load_current_settings(self):
        """Load current settings into the UI"""
        if not self.ui_ready:
            logger.debug(f" SETTINGS: UI not ready yet, skipping settings load",print_to_terminal=False)
            return
            
        try:
            # Load default model
            default_model = self.config_manager.get_default_model()
            if default_model in self.available_models:
                self.model_combo.setCurrentText(default_model)
            
            # Load default personality
            default_personality = self.config_manager.get_default_personality()
            if default_personality in self.available_personalities:
                self.personality_combo.setCurrentText(default_personality)
            
            # Load default temperature
            default_temp = self.config_manager.get_default_temperature()
            self.temp_spin.setValue(int(default_temp * 10))
            
            # Load theme
            theme = self.config_manager.get("theme", "Dark")
            self.theme_combo.setCurrentText(theme)
            
            # Load window size
            width, height = self.config_manager.get_window_size()
            self.width_spin.setValue(width)
            self.height_spin.setValue(height)
            
            # Load chat options
            self.auto_save_checkbox.setChecked(self.config_manager.is_auto_save_enabled())
            self.spellcheck_checkbox.setChecked(self.config_manager.is_spellcheck_enabled())
            self.enhancement_checkbox.setChecked(self.config_manager.is_enhancement_enabled())
            self.memory_checkbox.setChecked(self.config_manager.get("memory_enabled", True))
            
            # Load session variables with safety checks
            try:
                self.history_checkbox.setChecked(self.config_manager.is_history_enabled())
                self.wordwrap_checkbox.setChecked(self.config_manager.is_wordwrap_enabled())
                self.json_format_checkbox.setChecked(self.config_manager.is_json_format_enabled())
                self.verbose_checkbox.setChecked(self.config_manager.is_verbose_enabled())
                self.think_checkbox.setChecked(self.config_manager.is_think_enabled())
            except RuntimeError as e:
                logger.debug(f" SETTINGS: UI elements deleted during load: {e}",print_to_terminal=True)
                return
            
            # Load chat parameters
            chat_settings = self.config_manager.get_chat_settings()
            self.max_tokens_spin.setValue(chat_settings.get("max_tokens", 2048))
            self.top_p_spin.setValue(int(chat_settings.get("top_p", 0.9) * 100))
            
        except Exception as e:
            logger.debug(f" SETTINGS: Error loading settings: {e}",print_to_terminal=True)
            QMessageBox.warning(self, "Warning", f"Some settings could not be loaded: {str(e)}")
    
    def save_settings(self):
        """Save the current settings"""
        try:
            # Save default model
            self.config_manager.set_default_model(self.model_combo.currentText())
            
            # Save default personality
            self.config_manager.set_default_personality(self.personality_combo.currentText())
            
            # Save default temperature
            temp_value = self.temp_spin.value() / 10.0
            self.config_manager.set_default_temperature(temp_value)
            
            # Save theme
            self.config_manager.set("theme", self.theme_combo.currentText())
            
            # Save window size
            self.config_manager.set_window_size(self.width_spin.value(), self.height_spin.value())
            
            # Save chat options
            self.config_manager.set_auto_save_enabled(self.auto_save_checkbox.isChecked())
            self.config_manager.set_spellcheck_enabled(self.spellcheck_checkbox.isChecked())
            self.config_manager.set_enhancement_enabled(self.enhancement_checkbox.isChecked())
            self.config_manager.set("memory_enabled", self.memory_checkbox.isChecked())
            
            # Save session variables
            self.config_manager.set_history_enabled(self.history_checkbox.isChecked())
            self.config_manager.set_wordwrap_enabled(self.wordwrap_checkbox.isChecked())
            self.config_manager.set_json_format_enabled(self.json_format_checkbox.isChecked())
            self.config_manager.set_verbose_enabled(self.verbose_checkbox.isChecked())
            self.config_manager.set_think_enabled(self.think_checkbox.isChecked())
            
            # Save chat parameters
            chat_settings = {
                "max_tokens": self.max_tokens_spin.value(),
                "top_p": self.top_p_spin.value() / 100.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
            self.config_manager.set("chat_settings", chat_settings)
            
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
    
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(self, "Reset Settings", 
                                   "Are you sure you want to reset all settings to defaults?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Reset to default values
            self.model_combo.setCurrentText("llama2")
            self.personality_combo.setCurrentText("assistant")
            self.temp_spin.setValue(7)  # 0.7
            self.width_spin.setValue(1200)
            self.height_spin.setValue(800)
            self.auto_save_checkbox.setChecked(True)
            self.spellcheck_checkbox.setChecked(True)
            self.enhancement_checkbox.setChecked(True)
            self.memory_checkbox.setChecked(True)
            self.history_checkbox.setChecked(True)
            self.wordwrap_checkbox.setChecked(True)
            self.json_format_checkbox.setChecked(False)
            self.verbose_checkbox.setChecked(False)
            self.think_checkbox.setChecked(False)
            self.max_tokens_spin.setValue(2048)
            self.top_p_spin.setValue(90)  # 0.9
            self.theme_combo.setCurrentText("Dark")
            
            QMessageBox.information(self, "Reset Complete", "Settings have been reset to defaults.") 