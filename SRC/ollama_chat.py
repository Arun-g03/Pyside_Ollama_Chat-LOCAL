import os
import re
import json
import requests
import subprocess
from datetime import datetime
from threading import Thread
#==PySide6 Core==
from PySide6.QtCore import Qt, QThread, Signal, QObject, QTimer
#==PySide6 Widgets==
from PySide6.QtWidgets import (QMainWindow, QTabWidget, 
                                QWidget, QVBoxLayout, 
                                QHBoxLayout, QLabel, 
                                QComboBox, QTextEdit, 
                                QPushButton, QLineEdit, 
                                QListWidget, QStatusBar, 
                                QFileDialog, QMessageBox, 
                                QSizePolicy, QFormLayout,
                                QSplitter, QDialog,
                                QDialogButtonBox, QListWidgetItem,
                                QCheckBox, QMenu, QFrame,
                                QGroupBox)

from PySide6.QtGui import QTextCharFormat, QColor, QFont, QTextCursor, QTextFormat, QAction
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from worker import Worker
from html import escape
from personality_widget import PersonalityWidget
from config_manager import ConfigManager
from settings_dialog import SettingsDialog
from complexity_widget import ComplexityWidget

# Spellchecker imports
try:
    import enchant
    SPELLCHECK_AVAILABLE = True
except ImportError:
    SPELLCHECK_AVAILABLE = False
    print("Spellchecker not available. Install pyenchant: pip install pyenchant")

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
                print("✅ Spellchecker initialized with en_US dictionary")
                # Create a single timer for spell checking
                self.spellcheck_timer = QTimer()
                self.spellcheck_timer.setSingleShot(True)
                self.spellcheck_timer.timeout.connect(self.highlight_misspelled_words)
            except Exception as e:
                print(f"Could not initialize spellchecker: {e}")
                self.spellchecker = None
        else:
            print("❌ Spellchecker not available - install pyenchant: pip install pyenchant")
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
                action.triggered.connect(lambda checked, s=suggestion, c=cursor: self.replace_word(c, s))
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
                print(f"Could not add '{word}' to dictionary: {e}")
    
    def ignore_word(self, word):
        """Ignore the word (add to personal dictionary)"""
        self.add_to_dictionary(word)
    
    def highlight_misspelled_words(self):
        """Highlight misspelled words in the text"""
        if not self.spellchecker:
            return
            
        # Store current cursor position
        current_cursor = self.textCursor()
        current_pos = current_cursor.position()
        
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
        
        # Restore cursor position
        current_cursor.setPosition(current_pos)
        self.setTextCursor(current_cursor)
    
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

class OllamaChat(QMainWindow):
    status_update_signal = Signal(str)
    model_op_finished_signal = Signal()

    def __init__(self):
        super().__init__()
        
        # Initialize configuration
        self.config_manager = ConfigManager()
        
        # Initialize variables
        self.conversation = []
        self.model = self.config_manager.get_default_model()
        # Initialize request state
        self.request_in_progress = False
        self.cancellation_requested = False
        self.follow_up_in_progress = False
        
        # Model change protection
        self.model_change_in_progress = False
        
        # Initialization protection
        self.initialization_complete = False
        self.init_retry_count = 0
        self.max_init_retries = 3
        
        # Timer instances to prevent handle leaks
        self.model_update_timer = None
        
        # Set up the main window
        self.setWindowTitle("Ollama Chat")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize configuration manager
        self.config_manager = ConfigManager()
        
        # Initialize session variables state
        self.session_variables = {
            'history': self.config_manager.is_history_enabled(),
            'wordwrap': self.config_manager.is_wordwrap_enabled(),
            'json_format': self.config_manager.is_json_format_enabled(),
            'verbose': self.config_manager.is_verbose_enabled(),
            'think': self.config_manager.is_think_enabled()
        }
        
        # Set up the base URL for Ollama
        self.base_url = self.config_manager.get_ollama_url()
        
        # Initialize conversation and metadata
        self.conversation = []
        self.current_conversation_file = None
        self.conversation_metadata = {
            "created": None,
            "last_modified": None,
            "model": None,
            "personality": None,
            "message_count": 0
        }
        
        # Auto-save settings
        self.auto_save_enabled = self.config_manager.is_auto_save_enabled()
        self.history_dir = self.config_manager.get_history_directory()
        
        # Create history directory if it doesn't exist
        os.makedirs(self.history_dir, exist_ok=True)
        
        # Initialize model and temperature
        self.model = self.config_manager.get_default_model()
        self.temperature = self.config_manager.get_default_temperature()
        
        # Initialize system prompt
        self.system_prompt = "You are a helpful AI assistant."
        
        # Initialize complexity analysis widget
        self.complexity_widget = ComplexityWidget(self)
        
        self.complexity_widget.model_recommendation_signal.connect(self.on_model_recommendation)
        # Set up the UI
        self.setup_ui()
        
        # Initialize personality system
        self.initialize_personality_system()
        
        
        
        # Initial model refresh (without triggering model change)
        self.refresh_models()
        
        # Mark initialization as complete
        self.initialization_complete = True
        
        # Don't initialize session variables here - wait for window to be shown
        # Session variables will be updated when model is selected

        # Apply dark theme with improved styles
        self.apply_dark_theme()

        # Initialize timers
        from PySide6.QtCore import QTimer
        self.model_update_timer = QTimer()
        self.model_update_timer.setSingleShot(True)
        self.model_update_timer.timeout.connect(self._delayed_model_update)

        # Set up the worker thread and connect signals
        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)

        # Connect the signal from the worker to a slot that updates the UI
        self.worker.update_message_signal.connect(lambda response: self.append_to_chat(self.chat_display, "Assistant", response))
        self.status_update_signal.connect(self.append_to_status)
        self.model_op_finished_signal.connect(self.on_model_op_finished)
        self.worker.stream_chunk_signal.connect(self.handle_stream_chunk)
    
        # Start the worker thread
        self.append_to_chat(self.chat_display, "System", "Starting worker thread...")
        self.worker_thread.start()
    
    def setup_ui(self):
        # Setup the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create main layout for central widget
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        self.chat_tab = QWidget()
        self.model_tab = QWidget()
        self.personality_tab = QWidget()  # New personality tab

        self.tabs.addTab(self.chat_tab, "Chat")
        self.tabs.addTab(self.model_tab, "Model Manager")
        self.tabs.addTab(self.personality_tab, "Personalities")  # New tab
    
        # Setup tabs
        self.setup_chat_tab()
        self.setup_model_tab()
        self.setup_personality_tab()  # New method
    
        # Status bar - moved before personality initialization
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_var = "Ready"
        self.status_bar.showMessage(self.status_var)
    
    def setup_chat_tab(self):
        layout = QVBoxLayout(self.chat_tab)
    
        # Model selection and settings
        top_layout = QHBoxLayout()
        self.model_combo = QComboBox(self)
        self.model_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Expand horizontally
        top_layout.addWidget(QLabel("Model:"))
        top_layout.addWidget(self.model_combo)
        self.model_combo.currentTextChanged.connect(self.on_model_changed)

        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Fixed size
        self.refresh_button.clicked.connect(self.refresh_models)
        top_layout.addWidget(self.refresh_button)

        # Personality selector for quick access
        self.personality_combo = QComboBox(self)
        self.personality_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.personality_combo.currentTextChanged.connect(self.on_personality_combo_changed)
        top_layout.addWidget(QLabel("Personality:"))
        top_layout.addWidget(self.personality_combo)

        self.temp_combo = QComboBox(self)
        self.temp_combo.addItems([str(x / 10) for x in range(1, 11)])
        default_temp = str(self.config_manager.get_default_temperature())
        self.temp_combo.setCurrentText(default_temp)
        self.temp_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Expand horizontally
        self.temp_combo.currentTextChanged.connect(self.set_temperature)
        top_layout.addWidget(QLabel("Temperature:"))
        top_layout.addWidget(self.temp_combo)

        # Spellchecker toggle
        self.spellcheck_toggle = QCheckBox("Spell Check")
        self.spellcheck_toggle.setChecked(self.config_manager.is_spellcheck_enabled())
        self.spellcheck_toggle.setToolTip("Enable/disable spell checking in the input box")
        self.spellcheck_toggle.toggled.connect(self.toggle_spellcheck)
        top_layout.addWidget(self.spellcheck_toggle)

        # Enhancement toggle
        self.enhancement_toggle = QCheckBox("Auto Enhance")
        self.enhancement_toggle.setChecked(self.config_manager.is_enhancement_enabled())
        self.enhancement_toggle.setToolTip("Enable/disable automatic response enhancement")
        self.enhancement_toggle.toggled.connect(self.toggle_enhancement)
        top_layout.addWidget(self.enhancement_toggle)

        # Complexity analysis toggle
        self.complexity_toggle = QCheckBox("Complexity Analysis")
        self.complexity_toggle.setChecked(False)  # Initially hidden
        self.complexity_toggle.setToolTip("Show/hide request complexity analysis")
        self.complexity_toggle.toggled.connect(self.toggle_complexity_analysis)
        top_layout.addWidget(self.complexity_toggle)

        layout.addLayout(top_layout)

        # Follow-up status indicator
        self.follow_up_status = QLabel("")
        self.follow_up_status.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-weight: bold;
                padding: 5px;
                border: 1px solid #4CAF50;
                border-radius: 5px;
                background-color: rgba(76, 175, 80, 0.1);
            }
        """)
        self.follow_up_status.setVisible(False)
        layout.addWidget(self.follow_up_status)

        # Create the QSplitter to allow resizing
        splitter = QSplitter(Qt.Vertical)
        splitter.setHandleWidth(10)  # Make the splitter handle wider and more visible
        splitter.setChildrenCollapsible(False)  # Prevent widgets from being fully collapsed

        # Create chat display and input area
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
        self.chat_input = SpellCheckerTextEdit(self)
        self.chat_input.setReadOnly(False)
        self.chat_input.setPlaceholderText("Type your message here... (Right-click misspelled words for suggestions)")
        self.chat_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow vertical expansion
        self.chat_input.setMinimumHeight(60)  # Set minimum height instead of fixed

        # Add both widgets to the splitter
        splitter.addWidget(self.chat_display)
        splitter.addWidget(self.chat_input)

        # Set initial sizes for the splitter
        splitter.setSizes([400, 100])  # Adjust these values as needed

        # Add the splitter to the layout
        layout.addWidget(splitter)

        # Add complexity analysis widget (initially hidden)
        self.complexity_widget.setMaximumHeight(300)
        layout.addWidget(self.complexity_widget)

        # Connect the keyPressEvent for handling Enter key
        self.chat_input.keyPressEvent = self.handle_keypress
        
        # Connect text changes to complexity analysis
        self.chat_input.textChanged.connect(self.on_text_changed_for_complexity)

        # Buttons for sending, clearing, and saving chat
        button_layout = QHBoxLayout()
        
        # Send and Cancel buttons
        send_cancel_layout = QHBoxLayout()
        
        self.send_button = QPushButton("Send", self)
        self.send_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.send_button.clicked.connect(self.send_message)
        send_cancel_layout.addWidget(self.send_button)
        
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.cancel_button.setStyleSheet("QPushButton { background-color: #d32f2f; color: white; }")
        self.cancel_button.clicked.connect(self.cancel_request)
        self.cancel_button.setEnabled(False)  # Initially disabled
        send_cancel_layout.addWidget(self.cancel_button)
        
        button_layout.addLayout(send_cancel_layout)

        clear_button = QPushButton("Clear Chat", self)
        clear_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        clear_button.clicked.connect(self.clear_chat)
        button_layout.addWidget(clear_button)

        save_button = QPushButton("Save Chat", self)
        save_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        save_button.clicked.connect(self.save_history)
        button_layout.addWidget(save_button)

        clear_memory_button = QPushButton("Clear Memory", self)
        clear_memory_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        clear_memory_button.clicked.connect(self.clear_memory)
        button_layout.addWidget(clear_memory_button)

        # Test follow-up button (for demonstration)
        test_followup_button = QPushButton("Test Auto Follow-up", self)
        test_followup_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        test_followup_button.setToolTip("Test the automatic follow-up response system")
        test_followup_button.clicked.connect(self.test_follow_up_system)
        button_layout.addWidget(test_followup_button)

        layout.addLayout(button_layout)

        # New conversation management buttons
        conv_button_layout = QHBoxLayout()
        
        new_conv_button = QPushButton("New Conversation", self)
        new_conv_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        new_conv_button.clicked.connect(self.start_new_conversation)
        conv_button_layout.addWidget(new_conv_button)
        
        load_button = QPushButton("Load Chat", self)
        load_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        load_button.clicked.connect(self.load_conversation)
        conv_button_layout.addWidget(load_button)
        
        manage_button = QPushButton("Conversation Manager", self)
        manage_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        manage_button.clicked.connect(self.list_conversations)
        conv_button_layout.addWidget(manage_button)
        
        settings_button = QPushButton("Settings", self)
        settings_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        settings_button.clicked.connect(self.show_settings)
        conv_button_layout.addWidget(settings_button)
        
        layout.addLayout(conv_button_layout)

    def setup_model_tab(self):
        model_layout = QVBoxLayout(self.model_tab)
        
        # Available models
        model_list_layout = QVBoxLayout()
        self.model_list = QListWidget(self)
        #add a link to the ollama models page
        link_label = QLabel('<a href="https://ollama.com/models">Get more models from https://ollama.com/models</a>')
        link_label.setOpenExternalLinks(True)
        model_list_layout.addWidget(link_label)
        model_list_layout.addWidget(QLabel("Available Models"))
        model_list_layout.addWidget(self.model_list)
        
        refresh_model_button = QPushButton("Refresh Models", self)
        refresh_model_button.clicked.connect(self.refresh_models)
        model_list_layout.addWidget(refresh_model_button)
        
        model_layout.addLayout(model_list_layout)

        # Pull model section
        pull_model_layout = QFormLayout()
        self.model_entry = QLineEdit(self)
        self.model_entry.setText("llama2")
        pull_model_layout.addRow("Model Name:", self.model_entry)
        
        self.pull_model_button = QPushButton("Pull Model", self)
        self.pull_model_button.clicked.connect(self.pull_model)
        pull_model_layout.addRow(self.pull_model_button)

        model_layout.addLayout(pull_model_layout)

        # Remove model button
        self.remove_button = QPushButton("Remove Selected Model", self)
        self.remove_button.clicked.connect(self.remove_model)
        model_layout.addWidget(self.remove_button)

        # Update model button
        self.update_button = QPushButton("Update Selected Model", self)
        self.update_button.clicked.connect(self.update_model)
        model_layout.addWidget(self.update_button)

        # Status display
        self.model_status = QTextEdit(self)
        self.model_status.setReadOnly(True)
        model_layout.addWidget(self.model_status)

        # Clear button for status display
        clear_status_button = QPushButton("Clear Output", self)
        clear_status_button.clicked.connect(self.clear_model_status)
        model_layout.addWidget(clear_status_button)

    def on_model_op_finished(self):
        """
        Handles post-operation tasks for model management.
        """
        self.pull_model_button.setEnabled(True)
        self.model_entry.setEnabled(True)
        self.remove_button.setEnabled(True)
        self.update_button.setEnabled(True)
        self.refresh_models()
        self.append_to_status("\nOperation finished.")

    def refresh_models(self):
        """Refresh the list of available models from Ollama"""
        try:
            print(f"🔧 DEBUG: Attempting to connect to Ollama at: {self.base_url}/tags")
            response = requests.get(f"{self.base_url}/tags")
            print(f"🔧 DEBUG: Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"🔧 DEBUG: Response data: {data}")
                model_names = [model['name'] for model in data.get('models', [])]
                
                # Clear and repopulate the model combo box
                self.model_combo.clear()
                
                # Add "Auto" option at the beginning
                self.model_combo.addItem("Auto")
                self.model_combo.addItems(model_names)
                
                # Set the current model if it exists in the list
                if self.model in model_names:
                    # Only trigger model change if initialization is complete
                    if self.initialization_complete:
                        self.model_combo.setCurrentText(self.model)
                    else:
                        # Set without triggering the change event
                        index = self.model_combo.findText(self.model)
                        if index >= 0:
                            self.model_combo.setCurrentIndex(index)
                elif model_names:
                    # Set first model if current model not found
                    if self.initialization_complete:
                        self.model_combo.setCurrentIndex(1)  # Skip "Auto", select first real model
                    else:
                        # Set without triggering the change event
                        self.model_combo.setCurrentIndex(1)  # Skip "Auto"
                        self.model = model_names[0]
                
                # Update model list (without "Auto" for the list widget)
                self.model_list.clear()
                self.model_list.addItems(model_names)
                
                self.status_var = f"Found {len(model_names)} models + Auto mode"
                self.status_bar.showMessage(self.status_var)
            else:
                print(f"🔧 DEBUG: Error response: {response.text}")
                self.append_to_status("Error fetching models. Is Ollama running?")
                self.status_var = "Error: Cannot connect to Ollama"
                self.status_bar.showMessage(self.status_var)
        except requests.exceptions.ConnectionError as e:
            print(f"🔧 DEBUG: Connection error: {e}")
            self.append_to_status("Cannot connect to Ollama. Make sure it's running on localhost:11434")
            self.status_var = "Error: Cannot connect to Ollama"
            self.status_bar.showMessage(self.status_var)
        except Exception as e:
            print(f"🔧 DEBUG: Unexpected error: {e}")
            self.append_to_status(f"Unexpected error: {e}")
            self.status_var = "Error: Cannot connect to Ollama"
            self.status_bar.showMessage(self.status_var)

    def set_temperature(self, text):
        try:
            self.temperature = float(text)
        except ValueError:
            self.temperature = 0.7

    def update_model(self):
        """Update the selected model"""
        self.model = self.model_combo.currentText()
        self.update_session_variables_for_model()
        print(f"Model changed to: {self.model}")

    def update_session_variables_for_model(self):
        """Update session variable checkboxes based on current model capabilities"""
        try:
            print(f"🔧 SESSION: Updating session variables for model '{self.model}'")
            
            # Update session variables from config (no UI toggles in main window)
            self.session_variables = {
                'history': self.config_manager.is_history_enabled(),
                'wordwrap': self.config_manager.is_wordwrap_enabled(),
                'json_format': self.config_manager.is_json_format_enabled(),
                'verbose': self.config_manager.is_verbose_enabled(),
                'think': self.config_manager.is_think_enabled()
            }
            
            print(f"🔧 SESSION: Session variables updated: {self.session_variables}")
            
        except Exception as e:
            print(f"🔧 SESSION: Error updating session variables: {e}")
            # Set default values if all else fails
            self.session_variables = {
                'history': True,
                'wordwrap': True,
                'json_format': False,
                'verbose': False,
                'think': False
            }

    def pull_model(self):
        model_name = self.model_entry.text().strip()
        if not model_name:
            QMessageBox.warning(self, "Warning", "Please enter a model name")
            return
        
        self.pull_model_button.setEnabled(False)
        self.model_entry.setEnabled(False)
        self.remove_button.setEnabled(False)
        self.update_button.setEnabled(False)
        self.model_status.clear()
        self.append_to_status(f"Pulling model: {model_name}...\n")

        thread = Thread(target=self._pull_model_thread, args=(model_name,), daemon=True)
        thread.start()

    def _pull_model_thread(self, model_name):
        try:
            command = ["ollama", "pull", model_name]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                       universal_newlines=True, encoding='utf-8', errors='replace', bufsize=1)

            for line in iter(process.stdout.readline, ''):
                self.status_update_signal.emit(line.strip())
            
            process.stdout.close()
            return_code = process.wait()
            if return_code:
                self.status_update_signal.emit(f"\nError pulling model (exit code: {return_code}).")

        except FileNotFoundError:
            self.status_update_signal.emit("Ollama command not found. Is it installed and in your PATH?")
        except Exception as e:
            self.status_update_signal.emit(f"An error occurred: {str(e)}")
        finally:
            self.model_op_finished_signal.emit()

    def remove_model(self):
        selection = self.model_list.selectedIndexes()
        if not selection:
            QMessageBox.warning(self, "Warning", "Please select a model to remove")
            return
        
        model_to_remove = self.model_list.itemFromIndex(selection[0]).text()
        confirm = QMessageBox.question(self, "Confirm Removal", 
                                     f"Are you sure you want to remove {model_to_remove}?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            self.pull_model_button.setEnabled(False)
            self.model_entry.setEnabled(False)
            self.remove_button.setEnabled(False)
            self.update_button.setEnabled(False)
            self.model_status.clear()
            self.append_to_status(f"Removing model: {model_to_remove}...")
            
            thread = Thread(target=self._remove_model_thread, args=(model_to_remove,), daemon=True)
            thread.start()
            
    def _remove_model_thread(self, model_name):
        try:
            result = subprocess.run(["ollama", "rm", model_name], 
                                  capture_output=True, text=True, encoding='utf-8', errors='replace')
            
            if result.stdout:
                self.status_update_signal.emit(result.stdout.strip())
            if result.stderr:
                self.status_update_signal.emit(result.stderr.strip())

            if result.returncode == 0:
                self.status_update_signal.emit(f"\nSuccessfully removed model: {model_name}")
            else:
                self.status_update_signal.emit(f"\nError removing model: {model_name}")
        except FileNotFoundError:
            self.status_update_signal.emit("Ollama command not found. Is it installed and in your PATH?")
        except Exception as e:
            self.status_update_signal.emit(f"An error occurred: {str(e)}")
        finally:
            self.model_op_finished_signal.emit()

    def detect_code_in_message(self, message):
        """
        Detect if a message contains code blocks or inline code.
        Returns True if code is detected, False otherwise.
        """
        # Check for block code (triple backticks)
        if re.search(r'```.*?```', message, re.DOTALL):
            return True
        
        # Check for inline code (single backticks)
        if re.search(r'`[^`]+`', message):
            return True
        
        # Check for common code patterns
        code_patterns = [
            r'\b(def|class|function|import|from|if|else|elif|for|while|try|except|finally|with|as)\b',
            r'[{}();=<>+\-*/]',  # Common code symbols
            r'\b(print|return|break|continue|pass|raise)\b',
            r'\b(var|let|const|function|if|else|for|while|try|catch|finally)\b',  # JavaScript
            r'\b(public|private|protected|static|final|abstract|interface|extends|implements)\b',  # Java
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, message):
                return True
        
        return False

    def send_message(self):
        message = self.chat_input.toPlainText().strip()
        if not message:
            return
        # Check if a request is already in progress
        if self.request_in_progress:
            self.append_to_chat(self.chat_display, "System", "Please wait for the current request to complete or cancel it.")
            return
        # Get the selected model from the model combo box
        selected_model = self.model_combo.currentText()
        # Check if a model is selected
        if not selected_model:
            self.append_to_chat(self.chat_display, "System", "No model selected!")
            return
        # Handle Auto mode - automatically select the best model based on complexity
        if selected_model == "Auto":
            if hasattr(self, 'complexity_widget') and self.complexity_widget.get_current_metrics():
                # Get the recommended model from complexity analysis
                available_models = [self.model_combo.itemText(i) for i in range(1, self.model_combo.count())]  # Skip "Auto"
                recommended_model = self.complexity_widget.analyzer.get_model_recommendation(
                    self.complexity_widget.get_current_metrics(), 
                    available_models
                )
                # Temporarily switch to the recommended model
                self.model = recommended_model
                self.append_to_chat(self.chat_display, "System", f"Auto mode: Using {recommended_model} for this request")
                print(f"🔧 AUTO: Selected {recommended_model} for request")
            else:
                # Fallback to first available model if no complexity analysis
                available_models = [self.model_combo.itemText(i) for i in range(1, self.model_combo.count())]
                if available_models:
                    self.model = available_models[0]
                    self.append_to_chat(self.chat_display, "System", f"Auto mode: Using {self.model} (fallback)")
                else:
                    self.append_to_chat(self.chat_display, "System", "Auto mode: No models available!")
                    return
        else:
            # Regular model selection
            self.model = selected_model
        # Set request state
        self.request_in_progress = True
        self.cancellation_requested = False
        # Update UI state
        self.send_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.chat_input.setEnabled(False)
        # --- Tag each new user request with a unique message ID ---
        self.message_id_counter = getattr(self, 'message_id_counter', 0) + 1
        user_message_id = self.message_id_counter
        print(f"[DEBUG] New user message: message_id={user_message_id}")
        self.append_to_chat(self.chat_display, "You", message)
        self.chat_input.clear()  # Clear the input field
        # Add user message to conversation history
        self.conversation.append({"role": "user", "content": message, "message_id": user_message_id})
        # --- Streaming state for updating last assistant message ---
        self.streaming_buffer = ""
        self.streaming_thoughts_buffer = ""
        self.streaming_answer_buffer = ""
        self.streaming_active = True
        self.streaming_in_thoughts = False
        self.streaming_in_answer = False
        self.current_thoughts_id = None
        self.current_answer_id = None
        self.streaming_blocks = getattr(self, 'streaming_blocks', {})
        try:
            # Send the message to Ollama for processing with context and handle follow-ups
            raw_response = self.process_ai_response(self.send_to_ollama())
            # Check if cancellation was requested during processing
            if self.cancellation_requested:
                return
            # Process for <think> tags
            thinking_text = None
            main_response = raw_response.strip()
            # Regex to find <think> or <thinking> tags and the content after
            match = re.search(r"<think(?:ing)?>([\s\S]*?)<\/think(?:ing)?>([\s\S]*)", main_response, re.IGNORECASE)
            if match:
                thinking_text = match.group(1).strip()
                main_response = match.group(2).strip()
            # Finalize the assistant's thoughts in the chat display
            if thinking_text:
                self._update_streaming_message(thinking_text, sender="Assistant's Thoughts", message_id=self.current_thoughts_id)
            # Finalize the assistant's main response in the chat display
            is_code_response = self.detect_code_in_message(main_response)
            self._update_streaming_message(main_response, sender="Assistant", message_id=self.current_answer_id, is_code=is_code_response)
            # Store ONLY the main assistant's response in conversation history
            self.message_id_counter += 1
            ai_message_id = self.message_id_counter
            print(f"[DEBUG] New AI response: message_id={ai_message_id}")
            self.conversation.append({"role": "assistant", "content": main_response, "message_id": ai_message_id})
            # Auto-save conversation and update metadata
            self.update_conversation_metadata()
            self.auto_save_conversation()
            # Update status with conversation info
            self.update_conversation_status()
        except Exception as e:
            if not self.cancellation_requested:
                self.append_to_chat(self.chat_display, "System", f"Error: {str(e)}")
        finally:
            # Reset request state
            self.request_in_progress = False
            self.cancellation_requested = False
            self.streaming_active = False
            self.streaming_in_thoughts = False
            self.streaming_in_answer = False
            # Update UI state
            self.send_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
            self.chat_input.setEnabled(True)
            self.chat_input.setFocus()

    def _insert_streaming_placeholder(self, sender):
        """Insert a placeholder for the streaming message and store its block number."""
        self.message_id_counter = getattr(self, 'message_id_counter', 0) + 1
        message_id = self.message_id_counter
        self.chat_display.moveCursor(QTextCursor.End)
        self.chat_display.insertHtml(f'<div id="streaming-{message_id}"><b style="color: #ffffff;">{sender}:</b> </div>')
        self.chat_display.append("")
        block_number = self.chat_display.document().lastBlock().blockNumber()
        self.streaming_blocks[message_id] = block_number
        print(f"[DEBUG] Inserted streaming placeholder: sender={sender}, message_id={message_id}, block_number={block_number}")
        return message_id

    def _update_streaming_message(self, content, sender, message_id, is_code=False):
        if message_id is None:
            print(f"[DEBUG] WARNING: Tried to update streaming message with None message_id for sender={sender}")
            return
        """Update the streaming message in the chat display with new content using the tracked block."""
        doc = self.chat_display.document()
        block_number = self.streaming_blocks.get(message_id, doc.blockCount() - 1)
        block = doc.findBlockByNumber(block_number)
        cursor = QTextCursor(block)
        cursor.select(QTextCursor.BlockUnderCursor)
        cursor.removeSelectedText()
        cleaned_message = self.cleanup_message(sender, content, is_code)
        formatted_message = f'<div style="background-color: #2e2e2e; padding: 10px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #444;"><b style="color: #ffffff;">{sender}:</b> {cleaned_message}</div>'
        cursor.insertHtml(formatted_message)
        print(f"[DEBUG] Updated streaming message: sender={sender}, message_id={message_id}, block_number={block_number}, content_len={len(content)}")

    def handle_stream_chunk(self, chunk):
        """Update the streaming message(s) in real time as streaming progresses, handling <think> blocks and main answer."""
        if not getattr(self, 'streaming_active', False):
            return
        # Initialize IDs if needed
        if self.current_thoughts_id is None and "<think>" in chunk:
            self.current_thoughts_id = self._insert_streaming_placeholder("Assistant's Thoughts")
        if self.current_answer_id is None and ("</think>" in chunk or "<think>" not in chunk):
            self.current_answer_id = self._insert_streaming_placeholder("Assistant")
        print(f"[DEBUG] handle_stream_chunk: chunk_len={len(chunk)}, in_thoughts={self.streaming_in_thoughts}, in_answer={self.streaming_in_answer}")
        # Handle <think> streaming
        if not self.streaming_in_answer:
            if "<think>" in chunk:
                self.streaming_in_thoughts = True
                chunk = chunk.split("<think>", 1)[1]
            if "</think>" in chunk:
                before, after = chunk.split("</think>", 1)
                self.streaming_thoughts_buffer += before
                self._update_streaming_message(self.streaming_thoughts_buffer, sender="Assistant's Thoughts", message_id=self.current_thoughts_id)
                self.streaming_in_thoughts = False
                self.streaming_in_answer = True
                self.streaming_answer_buffer += after
                self._update_streaming_message(self.streaming_answer_buffer, sender="Assistant", message_id=self.current_answer_id)
            else:
                if self.streaming_in_thoughts:
                    self.streaming_thoughts_buffer += chunk
                    self._update_streaming_message(self.streaming_thoughts_buffer, sender="Assistant's Thoughts", message_id=self.current_thoughts_id)
                else:
                    self.streaming_in_answer = True
                    self.streaming_answer_buffer += chunk
                    self._update_streaming_message(self.streaming_answer_buffer, sender="Assistant", message_id=self.current_answer_id)
        else:
            self.streaming_answer_buffer += chunk
            self._update_streaming_message(self.streaming_answer_buffer, sender="Assistant", message_id=self.current_answer_id)

    def detect_code_type(self, message):
        """
        Detects the programming language of a code block using Pygments.
        """
        try:
            lexer = guess_lexer(message)  # Automatically detect the lexer based on code content
            return lexer
        except Exception as e:
            print(f"Error detecting code type: {e}")
            return None

    def syntax_highlight_code(self, message, language=None):
        """
        Highlight the code using Pygments and return formatted HTML.
        """
        try:
            if language:
                # Try to get lexer by name first
                try:
                    lexer = get_lexer_by_name(language)
                except:
                    # Fallback to guessing
                    lexer = self.detect_code_type(message)
            else:
                lexer = self.detect_code_type(message)
                
            if lexer is None:
                # Fallback to text lexer if no language detected
                lexer = get_lexer_by_name('text')
            
            # Use Pygments to apply syntax highlighting with better styling
            formatter = HtmlFormatter(
                style="monokai", 
                full=True, 
                noclasses=True,
                nobackground=True,  # Don't add background to individual tokens
                prestyles="margin: 0; padding: 0; font-family: 'Consolas', 'Monaco', 'Courier New', monospace; font-size: 13px; line-height: 1.4;"
            )
            highlighted_code = highlight(message, lexer, formatter)
            
            return highlighted_code
            
        except Exception as e:
            print(f"Error highlighting code: {e}")
            # Return escaped code as fallback
            return escape(message)

    def detect_and_format_code(self, message):
        """
        Detects code and applies formatting. Highlights syntax using Pygments.
        It handles inline and block code wrapped in backticks (```) and applies syntax highlighting.
        """
        # Format block code (triple backticks) with optional language identifier
        # This regex captures: ```language\ncode``` or ```\ncode```
        block_code_pattern = re.compile(r'```(\w+)?\n?(.*?)```', re.DOTALL)
        formatted_message = message

        def format_block_code(match):
            language = match.group(1)  # Language identifier (may be None)
            code_content = match.group(2).strip()  # Get the content inside the block
            
            # Apply syntax highlighting
            highlighted_code = self.syntax_highlight_code(code_content, language)
            
            # Create language label if specified
            language_label = ""
            if language:
                language_label = f'<div style="background-color: #1e1e1e; color: #dcdcdc; padding: 5px 10px; border-bottom: 1px solid #444; font-family: monospace; font-size: 11px; text-transform: uppercase;">{language}</div>'
            
            # Return formatted code block with language label
            return f'<div style="background-color: #2d2d2d; border-radius: 5px; overflow: hidden; margin: 10px 0; border: 1px solid #444;">{language_label}<div style="padding: 10px; color: #dcdcdc; font-family: \'Consolas\', \'Monaco\', \'Courier New\', monospace; font-size: 13px; line-height: 1.4; overflow-x: auto;">{highlighted_code}</div></div>'

        # Replace block code with formatted HTML
        formatted_message = re.sub(block_code_pattern, format_block_code, formatted_message)

        # Format inline code (single backticks) - but avoid formatting if it's inside a code block
        # Use a simpler approach to avoid double-formatting
        inline_code_pattern = re.compile(r'`([^`]+)`')
        formatted_message = re.sub(inline_code_pattern, r'<code style="background-color: #2d2d2d; color: #dcdcaa; padding: 2px 4px; border-radius: 3px; font-family: \'Consolas\', \'Monaco\', \'Courier New\', monospace; font-size: 12px;">\1</code>', formatted_message)

        return formatted_message

    def handle_html_tags(self, message):
        """
        Properly handle HTML tags in messages - escape them for display when they're part of discussions
        but preserve actual formatting tags and code blocks.
        """
        # First, identify and protect code blocks (they may contain HTML tags that should be displayed, not interpreted)
        code_blocks = []
        
        def protect_code_blocks(match):
            code_blocks.append(match.group(0))
            return f"__CODE_BLOCK_{len(code_blocks)-1}__"
        
        # Temporarily replace code blocks with placeholders
        # Protect both inline and block code
        protected_message = re.sub(r'<code[^>]*>.*?</code>', protect_code_blocks, message, flags=re.DOTALL)
        protected_message = re.sub(r'<pre[^>]*>.*?</pre>', protect_code_blocks, protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<div[^>]*style="background-color: #2d2d2d[^>]*>.*?</div>', protect_code_blocks, protected_message, flags=re.DOTALL)
        
        # Handle formatting tags we want to preserve with better styling
        protected_message = re.sub(r'<ul>(.*?)</ul>', r'<ul style="list-style-type: disc; padding-left: 20px; margin: 10px 0;">\1</ul>', protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<ol>(.*?)</ol>', r'<ol style="padding-left: 20px; margin: 10px 0;">\1</ol>', protected_message, flags=re.DOTALL)
        protected_message = re.sub(r'<li>(.*?)</li>', r'<li style="margin: 5px 0;">\1</li>', protected_message)
        protected_message = re.sub(r'<b>(.*?)</b>', r'<b style="font-weight: bold; color: #ffffff;">\1</b>', protected_message)
        protected_message = re.sub(r'<i>(.*?)</i>', r'<i style="font-style: italic; color: #cccccc;">\1</i>', protected_message)
        protected_message = re.sub(r'<h1>(.*?)</h1>', r'<h1 style="font-size: 24px; font-weight: bold; color: #ffffff; margin: 15px 0 10px 0; border-bottom: 2px solid #555; padding-bottom: 5px;">\1</h1>', protected_message)
        protected_message = re.sub(r'<h2>(.*?)</h2>', r'<h2 style="font-size: 20px; font-weight: bold; color: #ffffff; margin: 12px 0 8px 0;">\1</h2>', protected_message)
        protected_message = re.sub(r'<h3>(.*?)</h3>', r'<h3 style="font-size: 16px; font-weight: bold; color: #ffffff; margin: 10px 0 6px 0;">\1</h3>', protected_message)
        protected_message = re.sub(r'<p>(.*?)</p>', r'<p style="margin: 8px 0;">\1</p>', protected_message)
        
        # Escape HTML tags outside of code blocks
        escaped_message = escape(protected_message)

        # Restore code blocks
        for i, code_block in enumerate(code_blocks):
            escaped_message = escaped_message.replace(f"__CODE_BLOCK_{i}__", code_block)

        return escaped_message

    def build_comprehensive_system_prompt(self):
        """Build a comprehensive system prompt that includes all personality components."""
        if not hasattr(self, 'personality_widget') or not self.personality_widget:
            return self.system_prompt
        
        # Use the personality widget's comprehensive system prompt method
        comprehensive_prompt = self.personality_widget.get_comprehensive_system_prompt()
        
        # Fallback to basic system prompt if comprehensive method fails
        if not comprehensive_prompt:
            return self.system_prompt
        
        return comprehensive_prompt

    def send_to_ollama(self):
        """Sends the conversation to Ollama using the /api/chat endpoint."""
        
        # Check for cancellation before starting
        if self.cancellation_requested:
            return "Request cancelled."
        
        # Build comprehensive system prompt that includes all personality components
        comprehensive_system_prompt = self.build_comprehensive_system_prompt()
        
        # Get personality-specific configuration
        personality_config = self.personality_widget.personality_model.get_personality_config()
        
        # Use personality config if available, otherwise use default settings
        temperature = personality_config.temperature if personality_config else self.temperature
        max_tokens = personality_config.max_tokens if personality_config else 2048
        top_p = personality_config.top_p if personality_config else 0.9
        
        # Always include the comprehensive system prompt at the beginning of the conversation
        messages = [{"role": "system", "content": comprehensive_system_prompt}] + self.conversation

        data = {
            "model": self.model,
            "messages": messages, # Use the 'messages' format for /api/chat
            "temperature": temperature,
            "top_p": top_p,
            "stream": True,  # Enable streaming
        }
        
        # Add session variables using proper Ollama /set commands
        # These will be sent as system messages before the actual conversation
        
        session_commands = []
        
        if not self.session_variables['history']:
            session_commands.append("/set nohistory")
        else:
            session_commands.append("/set history")
            
        if not self.session_variables['wordwrap']:
            session_commands.append("/set nowordwrap")
        else:
            session_commands.append("/set wordwrap")
            
        if self.session_variables['json_format']:
            session_commands.append("/set format json")
        else:
            session_commands.append("/set noformat")
            
        if self.session_variables['verbose']:
            session_commands.append("/set verbose")
        else:
            session_commands.append("/set quiet")
            
        if self.session_variables['think']:
            session_commands.append("/set think")
        else:
            session_commands.append("/set nothink")
        
        # Add session commands as system messages if any are set
        if session_commands:
            session_system_message = "\n".join(session_commands)
            # Insert session commands before the main system prompt
            data["messages"].insert(0, {"role": "system", "content": session_system_message})
            print(f"🔧 SESSION: Sending session commands: {session_commands}")
        
        # Add max_tokens if specified (use num_predict for Ollama)
        if max_tokens and max_tokens != 2048:
            data["num_predict"] = max_tokens
        
        # Debug: Show which session variables are being applied
        print(f"🔧 SESSION: Applying session variables: {self.session_variables}")
        if "options" in data:
            print(f"🔧 SESSION: Ollama options: {data['options']}")
        if "format" in data:
            print(f"🔧 SESSION: Response format: {data['format']}")
        
        try:
            # Check for cancellation before making the request
            if self.cancellation_requested:
                return "Request cancelled."
                
            print("====================SENDING TO OLLAMA====================")
            print(json.dumps(data, indent=2))
            print("=========================================================")

            url = f"{self.base_url}/chat" # Use the /api/chat endpoint
            try:
                with requests.post(url, json=data, stream=True) as response:
                    response.raise_for_status()
                    buffer = ""
                    for line in response.iter_lines(decode_unicode=True):
                        if line:
                            # Each line is a JSON object with a 'content' field
                            chunk = json.loads(line)
                            content = chunk.get("message", {}).get("content", "")
                            buffer += content
                            # Update the UI with the new content
                            self.append_to_chat(self.chat_display, "Assistant", buffer, is_code=False)
                    return buffer
            except Exception as e:
                return f"Error: {e}"

        except requests.exceptions.ConnectionError:
            return "Cannot connect to Ollama. Make sure it's running."
        except Exception as e:
            if not self.cancellation_requested:
                print(f"Error in send_to_ollama: {e}")
            return "An error occurred while processing your request."

    def detect_follow_up_question(self, response):
        """Detect if the AI response contains a follow-up question that needs user input."""
        # Patterns that indicate the AI needs more information
        follow_up_patterns = [
            r'\b(?:could you|can you|would you|please)\s+(?:provide|give|share|tell|specify|clarify|explain|describe|elaborate|detail)',
            r'\b(?:what|which|where|when|how|why)\s+(?:is|are|do|does|did|would|could|should)',
            r'\b(?:i need|i require|i would like|i want)\s+(?:to know|more information|additional details|clarification)',
            r'\b(?:to better|to properly|to accurately|to effectively)\s+(?:help|assist|answer|respond)',
            r'\b(?:more details|more information|additional context|further clarification)\s+(?:would|could|will)\s+(?:help|be useful|be needed)',
            r'\b(?:before i can|in order to|so that i can)\s+(?:help|assist|provide|give)',
            r'\b(?:could you clarify|can you specify|would you mind|please tell me)',
            r'\b(?:i\'m not sure|i don\'t know|i need to know|i would need)\s+(?:what|which|where|when|how|why)',
            r'\b(?:it would help|it would be useful|it would be better)\s+(?:if|to know|to have)',
            r'\b(?:what kind of|what type of|what specific|which specific)\s+(?:information|details|context|requirements)'
        ]
        
        # Check if response contains follow-up patterns
        response_lower = response.lower()
        for pattern in follow_up_patterns:
            if re.search(pattern, response_lower):
                return True
                
        # Check for question marks followed by requests for information
        if '?' in response:
            # Look for question marks followed by requests for more info
            question_sections = re.split(r'\?', response)
            for section in question_sections:
                if any(keyword in section.lower() for keyword in ['please', 'could you', 'can you', 'would you', 'need', 'require', 'specify', 'clarify']):
                    return True
                    
        return False

    def should_enhance_response(self, response):
        """Determine if the response should be enhanced with additional depth and detail."""
        # Don't enhance very simple greetings or casual responses
        simple_greetings = [
            r'^hi\b', r'^hello\b', r'^hey\b', r'^howdy\b',
            r'^good\s+(morning|afternoon|evening)\b',
            r'^how\s+are\s+you\?*$',
            r'^what\'s\s+up\?*$',
            r'^how\'s\s+it\s+going\?*$',
            r'^hey\s+\w+$',  # "hey baby", "hey there", etc.
            r'^hi\s+\w+$',   # "hi there", "hi friend", etc.
            r'^hello\s+\w+$' # "hello there", etc.
        ]
        
        response_lower = response.lower().strip()
        for pattern in simple_greetings:
            if re.match(pattern, response_lower):
                print(f"🔍 ENHANCEMENT: Skipping enhancement for simple greeting: '{response}'")
                return False
        
        # Check if response is relatively short and could benefit from more detail
        if len(response.strip()) < 150:  # Reduced from 200 to be more conservative
            print(f"🔍 ENHANCEMENT: Response too short ({len(response.strip())} chars), considering enhancement")
            return True
            
        # Check if response lacks specific examples or detailed explanations
        lacks_detail_patterns = [
            r'\b(?:here|this|that)\s+(?:is|are)\s+(?:a|an|the)\s+(?:good|basic|simple)\s+(?:example|way|approach)',
            r'\b(?:you\s+can|you\s+should|try|consider)\s+(?:this|that|the\s+following)',
            r'\b(?:for\s+example|e\.g\.|such\s+as)\s*[.!?]',
            r'\b(?:more\s+details|additional\s+information|further\s+explanation)\s+(?:would\s+be|are)\s+(?:helpful|useful)',
            r'\b(?:in\s+summary|basically|essentially|simply\s+put)',
            r'\b(?:this\s+is\s+(?:how|what|why|when|where))\s*[.!?]',
            r'\b(?:hope\s+this\s+helps|let\s+me\s+know|feel\s+free\s+to\s+ask)',
        ]
        
        response_lower = response.lower()
        for pattern in lacks_detail_patterns:
            if re.search(pattern, response_lower):
                print(f"🔍 ENHANCEMENT: Response lacks detail, considering enhancement")
                return True
                
        # Check if response ends abruptly or seems incomplete
        incomplete_patterns = [
            r'\b(?:and\s+so\s+on|etc\.|\.\.\.)\s*$',
            r'\b(?:that\'s\s+it|that\'s\s+all|end\s+of\s+story)\s*$',
            r'\b(?:hope\s+this\s+helps|let\s+me\s+know|feel\s+free\s+to\s+ask)\s*$',
            r'\b(?:any\s+questions|need\s+anything\s+else|anything\s+else)\s*\?$',
        ]
        
        for pattern in incomplete_patterns:
            if re.search(pattern, response_lower):
                print(f"🔍 ENHANCEMENT: Response seems incomplete, considering enhancement")
                return True
                
        # Check if response lacks structure or organization
        if not re.search(r'\b(?:first|second|third|finally|in\s+addition|moreover|furthermore|however|on\s+the\s+other\s+hand)\b', response_lower):
            # If it's a longer response without clear structure, it might benefit from enhancement
            if len(response.strip()) > 400:  # Increased from 300 to be more conservative
                print(f"🔍 ENHANCEMENT: Long response without structure, considering enhancement")
                return True
        
        print(f"🔍 ENHANCEMENT: Response doesn't need enhancement")
        return False

    def generate_follow_up_response(self, original_response, conversation_context):
        """Generate an enhanced version of the original response with additional depth and detail."""
        # Create a prompt that asks the AI to enhance its own response
        enhancement_prompt = f"""
You just provided this response to the user:

{original_response}

Now, please enhance this response by:
1. Adding more depth and detail to your explanations (but don't make assumptions about the user's situation)
2. Providing specific examples where relevant (only if the topic warrants examples)
3. Including additional context or background information (only if it adds value)
4. Offering practical tips or actionable advice (only if the user's message suggests they need help)
5. Making the response more comprehensive and thorough (but keep it natural and conversational)

IMPORTANT RULES:
- DO NOT make assumptions about the user's emotional state, problems, or situation
- DO NOT respond to questions that weren't asked
- DO NOT add emotional support unless the user's message clearly indicates they need it
- DO NOT ask follow-up questions unless the user's message suggests they want to continue the conversation
- Keep the enhanced response natural and conversational
- Only enhance what's already there - don't add completely new topics

The user's original question was in this context:
{conversation_context}

Please provide an enhanced version of your original response that is more detailed and comprehensive, 
but stays true to the original intent and doesn't add assumptions or respond to unasked questions.
"""
        
        # Send to AI for enhanced response
        try:
            # Check for cancellation before making API call
            if self.cancellation_requested:
                return original_response
                
            # Build comprehensive system prompt
            comprehensive_system_prompt = self.build_comprehensive_system_prompt()
            
            # Get personality-specific configuration
            personality_config = self.personality_widget.personality_model.get_personality_config()
            temperature = personality_config.temperature if personality_config else self.temperature
            max_tokens = personality_config.max_tokens if personality_config else 2048
            top_p = personality_config.top_p if personality_config else 0.9
            
            # Create a temporary conversation that doesn't include the original response
            # This prevents the AI from thinking it's responding to its own message
            temp_conversation = []
            if len(self.conversation) > 0:
                # Get the conversation up to but not including the assistant's response
                for msg in self.conversation:
                    if msg['role'] != 'assistant':  # Only include user messages
                        temp_conversation.append(msg)
            
            # Add the enhancement prompt
            temp_conversation.append({"role": "user", "content": enhancement_prompt})
            
            # Prepare messages for enhancement
            messages = [{"role": "system", "content": comprehensive_system_prompt}] + temp_conversation
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "top_p": top_p,
                "stream": True,  # Enable streaming
            }
            
            if max_tokens and max_tokens != 2048:
                data["num_predict"] = max_tokens
            
            # Check for cancellation before making the request
            if self.cancellation_requested:
                return original_response
                
            url = f"{self.base_url}/chat"
            try:
                with requests.post(url, json=data, stream=True) as response:
                    response.raise_for_status()
                    buffer = ""
                    for line in response.iter_lines(decode_unicode=True):
                        if line:
                            # Each line is a JSON object with a 'content' field
                            chunk = json.loads(line)
                            content = chunk.get("message", {}).get("content", "")
                            buffer += content
                            # Update the UI with the new content
                            self.append_to_chat(self.chat_display, "Assistant", buffer, is_code=False)
                    return buffer
            except Exception as e:
                return f"Error: {e}"

        except Exception as e:
            if not self.cancellation_requested:
                print(f"Error generating enhanced response: {e}")
            return "I apologize, but I'm having trouble enhancing the response at the moment."

    def process_ai_response(self, response):
        """Process AI response and enhance it with additional depth when needed."""
        print(f"🔍 ENHANCEMENT: Processing response: '{response[:100]}...'")
        
        # Check if enhancement is enabled
        if not self.config_manager.is_enhancement_enabled():
            print(f"🔍 ENHANCEMENT: Enhancement disabled, returning original response")
            return response
        
        # Check if response could benefit from enhancement
        if self.should_enhance_response(response):
            # Check for cancellation before starting enhancement
            if self.cancellation_requested:
                return response
                
            # Show enhancement status
            self.show_follow_up_status("Enhancing response with additional details...")
            
            # Generate conversation context for the enhancement
            conversation_context = ""
            if len(self.conversation) > 0:
                # Get the last few messages for context
                recent_messages = self.conversation[-3:]  # Last 3 messages
                conversation_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in recent_messages])
            
            print(f"🔍 ENHANCEMENT: Conversation context for enhancement:")
            print(f"   {conversation_context}")
            
            # Generate enhanced response
            enhanced_response = self.generate_follow_up_response(response, conversation_context)
            
            # Check for cancellation after enhancement
            if self.cancellation_requested:
                self.hide_follow_up_status()
                return response
            
            # Hide enhancement status
            self.hide_follow_up_status()
            
            print(f"🔍 ENHANCEMENT: Original response: '{response[:100]}...'")
            print(f"🔍 ENHANCEMENT: Enhanced response: '{enhanced_response[:100]}...'")
            
            # Return the enhanced response (replace the original)
            return enhanced_response
        else:
            # No enhancement needed, return response as is
            print(f"🔍 ENHANCEMENT: No enhancement needed, returning original response")
            return response

    def show_follow_up_status(self, message):
        """Show the enhancement status indicator."""
        if hasattr(self, 'follow_up_status'):
            self.follow_up_status.setText(f"✨ {message}")
            self.follow_up_status.setVisible(True)

    def hide_follow_up_status(self):
        """Hide the enhancement status indicator."""
        if hasattr(self, 'follow_up_status'):
            self.follow_up_status.setVisible(False)

    def append_to_status(self, message):
        self.model_status.append(f"{message}\n")
        self.model_status.verticalScrollBar().setValue(self.model_status.verticalScrollBar().maximum())

    def apply_dark_theme(self):
        from styles import dark_stylesheet
        self.setStyleSheet(dark_stylesheet)

    def handle_keypress(self, event):
        # Check if Shift + Enter is pressed to insert a new line
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:
            # Allow the new line to be inserted in the chat input
            QTextEdit.keyPressEvent(self.chat_input, event)
        elif event.key() == Qt.Key_Return:  # If just Enter is pressed, send the message
            self.send_message()
        else:
            # Call the original QTextEdit keyPressEvent method for other keys
            QTextEdit.keyPressEvent(self.chat_input, event)

    def reset_follow_up_state(self):
        """Reset all follow-up conversation state."""
        self.follow_up_mode = False
        self.pending_follow_up_question = None
        self.follow_up_context = None
        self.hide_follow_up_status()

    def clear_chat(self):
        confirm = QMessageBox.question(self, "Confirm Clear", "Are you sure you want to clear the chat?", 
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.chat_display.clear()
            self.conversation = []
            # Reset follow-up state
            self.reset_follow_up_state()
            # Refresh the current personality's system prompt
            self.system_prompt = self.personality_widget.get_system_prompt()
            self.append_to_chat(self.chat_display, "System", f"Chat cleared. Using {self.personality_widget.get_current_personality()} personality.")
            self.update_conversation_status()

    def clear_memory(self):
        self.conversation = []
        self.current_conversation_file = None
        self.conversation_metadata = {
            "created": None,
            "last_modified": None,
            "model": None,
            "personality": None,
            "message_count": 0
        }
        # Reset follow-up state
        self.reset_follow_up_state()
        self.append_to_chat(self.chat_display, "System", "Conversation cleared. Start a new chat.")
        self.update_conversation_status()

    def save_history(self):
        if not self.conversation:
            QMessageBox.information(self, "Info", "No conversation to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"{self.model}_{timestamp}.json"
        
        filename, _ = QFileDialog.getSaveFileName(self, "Save Chat", os.path.join(self.history_dir, default_filename), 
                                                  "JSON files (*.json);;All files (*.*)")

        if not filename:
            return
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.conversation, f, indent=2)
            
            QMessageBox.information(self, "Success", f"Chat history saved to {filename}")
            self.status_var = f"Chat saved to {os.path.basename(filename)}"
            self.status_bar.showMessage(self.status_var)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save chat: {str(e)}")
            self.status_var = "Error saving chat"
            self.status_bar.showMessage(self.status_var)

    def auto_save_conversation(self):
        """Auto-save the current conversation with metadata."""
        if not self.conversation or not self.auto_save_enabled:
            return
        
        # Update metadata
        self.conversation_metadata.update({
            "last_modified": datetime.now().isoformat(),
            "model": self.model,
            "personality": self.personality_widget.get_current_personality(),
            "message_count": len(self.conversation)
        })
        
        # Create filename if not exists
        if not self.current_conversation_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.current_conversation_file = os.path.join(self.history_dir, f"conversation_{timestamp}.json")
            self.conversation_metadata["created"] = datetime.now().isoformat()
        
        # Save conversation with metadata
        try:
            save_data = {
                "metadata": self.conversation_metadata,
                "conversation": self.conversation
            }
            with open(self.current_conversation_file, 'w') as f:
                json.dump(save_data, f, indent=2)
        except Exception as e:
            print(f"Auto-save failed: {e}")

    def load_conversation(self, filename=None):
        """Load a conversation from file."""
        if filename is None:
            filename, _ = QFileDialog.getOpenFileName(self, "Load Chat", self.history_dir, 
                                                     "JSON files (*.json);;All files (*.*)")
            if not filename:
                return
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Handle both old format (just conversation) and new format (with metadata)
            if isinstance(data, list):
                # Old format - just conversation array
                conversation = data
                metadata = {}
            else:
                # New format - with metadata
                conversation = data.get("conversation", [])
                metadata = data.get("metadata", {})
            
            # Clear current conversation
            self.conversation = conversation
            self.current_conversation_file = filename
            self.conversation_metadata = metadata
            
            # Update UI
            self.chat_display.clear()
            
            # Display loaded conversation
            for message in conversation:
                role = message.get("role", "unknown")
                content = message.get("content", "")
                
                if role == "user":
                    self.append_to_chat(self.chat_display, "You", content)
                elif role == "assistant":
                    self.append_to_chat(self.chat_display, "Assistant", content)
            
            # Show metadata if available
            if metadata:
                created = metadata.get("created", "Unknown")
                model = metadata.get("model", "Unknown")
                personality = metadata.get("personality", "Unknown")
                message_count = metadata.get("message_count", 0)
                
                info_msg = f"Conversation loaded: {message_count} messages, Model: {model}, Personality: {personality}"
                self.append_to_chat(self.chat_display, "System", info_msg)
            
            # Update status
            self.update_conversation_status()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load conversation: {str(e)}")

    def list_conversations(self):
        """Show a dialog to list and manage saved conversations."""
        dialog = ConversationManagerDialog(self.history_dir, self)
        if dialog.exec() == QDialog.Accepted and dialog.selected_file:
            self.load_conversation(dialog.selected_file)

    def start_new_conversation(self):
        """Start a new conversation."""
        if self.conversation:
            reply = QMessageBox.question(self, "New Conversation", 
                                       "Start a new conversation? Current conversation will be saved.",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
            # Auto-save current conversation
            self.auto_save_conversation()
        # Clear everything
        self.conversation = []
        self.current_conversation_file = None
        self.conversation_metadata = {
            "created": None,
            "last_modified": None,
            "model": None,
            "personality": None,
            "message_count": 0
        }
        self.chat_display.clear()
        # Reset follow-up state
        self.reset_follow_up_state()
        # Refresh the current personality's system prompt
        self.system_prompt = self.personality_widget.get_system_prompt()
        self.append_to_chat(self.chat_display, "System", f"Chat cleared. Using {self.personality_widget.get_current_personality()} personality.")
        self.update_conversation_status()
        # --- Reset streaming and message ID state ---
        self.message_id_counter = 0
        self.streaming_blocks = {}
        self.current_thoughts_id = None
        self.current_answer_id = None
        self.streaming_thoughts_buffer = ""
        self.streaming_answer_buffer = ""
        self.streaming_active = False
        self.streaming_in_thoughts = False
        self.streaming_in_answer = False

    def update_conversation_metadata(self):
        """Update conversation metadata with current state."""
        if not self.conversation_metadata["created"]:
            self.conversation_metadata["created"] = datetime.now().isoformat()
        
        self.conversation_metadata.update({
            "last_modified": datetime.now().isoformat(),
            "model": self.model,
            "personality": self.personality_widget.get_current_personality(),
            "message_count": len(self.conversation)
        })

    def append_to_chat(self, chat_display, sender, message, is_code=False):
        """Append a message to the chat display."""
        # Clean the message before appending it
        cleaned_message = self.cleanup_message(sender, message, is_code)
        
        # Apply different styles for different message types
        if sender == "System":
            formatted_message = f"""
                <div style="background-color: #1e1e1e; padding: 8px 10px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid #666;">
                    <b style="color: #888;">{sender}:</b> {cleaned_message}
                </div>
            """
        elif sender == "Assistant's Thoughts":
            formatted_message = f"""
                <div style="background-color: #1a1a1a; padding: 8px 10px; border-radius: 5px; margin-bottom: 10px; border-left: 3px solid #555;">
                    <b style="color: #aaa;">{sender}:</b> {cleaned_message}
                </div>
            """
        elif is_code:
            # For code messages, use a distinct dark background and a monospace font for better readability
            formatted_message = f"""
                <div style="background-color: #2d2d2d; padding: 10px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #444;">
                    <b style="color: #ffffff; margin-bottom: 5px; display: block;">{sender}:</b>
                    {cleaned_message}
                </div>
            """
        else:
            # For regular messages, apply a lighter background with soft contrast
            formatted_message = f"""
                <div style="background-color: #2e2e2e; padding: 10px; border-radius: 5px; margin-bottom: 10px; border: 1px solid #444;">
                    <b style="color: #ffffff;">{sender}:</b> {cleaned_message}
                </div>
            """

        chat_display.insertHtml(formatted_message)
        chat_display.append("")  # Add a new line after each message

        # Move the cursor to the end to show the latest message
        cursor = chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        chat_display.setTextCursor(cursor)

    def cleanup_message(self, sender, message, is_code=False):
        """Prepares a message for display by adding sender and formatting."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format based on sender
        if sender == "You":
            # Auto-detect and format code in the message
            message = self.detect_and_format_code(message)
        elif sender == "System":
            message = f"<i style='color: #aaa;'>{message}</i>"
        elif sender == "Assistant's Thoughts":
            # The message is already formatted HTML, so we don't process it further.
            pass
        else:  # Assistant
            if is_code:
                # For explicit code messages, apply syntax highlighting
                message = self.syntax_highlight_code(message)
                # Wrap in code block styling
                message = f'<div style="background-color: #2d2d2d; border-radius: 5px; overflow: hidden; margin: 10px 0; border: 1px solid #444;"><div style="padding: 10px; color: #dcdcdc; font-family: \'Consolas\', \'Monaco\', \'Courier New\', monospace; font-size: 13px; line-height: 1.4; overflow-x: auto;">{message}</div></div>'
            else:
                # For regular assistant messages, detect and format code blocks first
                message = self.detect_and_format_code(message)
                # Then handle any remaining HTML tags
                message = self.handle_html_tags(message)

        # Don't prepend sender here since it's handled in append_to_chat
        return message

    def closeEvent(self, event):
        """Handle application close event"""
        try:
            # Clean up timers to prevent handle leaks
            if hasattr(self, 'model_update_timer') and self.model_update_timer:
                self.model_update_timer.stop()
                self.model_update_timer.deleteLater()
            
            # Clean up spellchecker timer if it exists
            if hasattr(self, 'chat_input') and hasattr(self.chat_input, 'spellcheck_timer'):
                if self.chat_input.spellcheck_timer:
                    self.chat_input.spellcheck_timer.stop()
                    self.chat_input.spellcheck_timer.deleteLater()
            
            # Save conversation if auto-save is enabled
            if self.auto_save_enabled and self.conversation:
                self.auto_save_conversation()
            
            # Stop worker thread
            if hasattr(self, 'worker_thread'):
                self.worker_thread.quit()
                self.worker_thread.wait()
            
            print("Application closing gracefully...")
            event.accept()
            
        except Exception as e:
            print(f"Error during application close: {e}")
            event.accept()

    def clear_model_status(self):
        self.model_status.clear()

    def setup_personality_tab(self):
        """Setup the personality management tab"""
        layout = QVBoxLayout(self.personality_tab)
        
        # Add personality widget
        self.personality_widget = PersonalityWidget()
        self.personality_widget.personality_changed.connect(self.on_personality_changed)
        layout.addWidget(self.personality_widget)
        
        # Initialize personality system after widget is created
        self.initialize_personality_system()
    
    def initialize_personality_system(self):
        """Initialize the personality system after the widget is created"""
        if hasattr(self, 'personality_widget') and self.personality_widget:
            current_personality = self.personality_widget.get_current_personality()
            self.system_prompt = self.personality_widget.get_system_prompt()
            if current_personality:
                self.on_personality_changed(current_personality)
            
            # Populate personality combo box
            self.populate_personality_combo()
        else:
            # Fallback if personality widget is not available
            self.system_prompt = ""
            print("Warning: Personality widget not available during initialization")

    def on_personality_changed(self, personality_name: str):
        """Handle personality change and update system prompt."""
        self.append_to_chat(self.chat_display, "System", f"Switched to {personality_name} personality")
        self.system_prompt = self.personality_widget.get_system_prompt()
        self.clear_memory() # Clear conversation history when personality changes
        
        # Update the personality combo box to stay in sync
        if hasattr(self, 'personality_combo'):
            self.personality_combo.setCurrentText(personality_name)

    def update_conversation_status(self):
        """Update status bar with current conversation information."""
        if not hasattr(self, 'status_bar'):
            return  # Status bar not initialized yet
            
        if self.conversation:
            message_count = len(self.conversation)
            user_messages = sum(1 for msg in self.conversation if msg.get("role") == "user")
            assistant_messages = sum(1 for msg in self.conversation if msg.get("role") == "assistant")
            
            status_text = f"Messages: {message_count} (You: {user_messages}, Assistant: {assistant_messages})"
            if self.current_conversation_file:
                status_text += f" | Saved: {os.path.basename(self.current_conversation_file)}"
            
            self.status_var = status_text
            self.status_bar.showMessage(status_text)
        else:
            self.status_var = "No conversation"
            self.status_bar.showMessage("No conversation")

    def populate_personality_combo(self):
        """Populate the personality combo box with available personalities."""
        personalities = self.personality_widget.get_available_personalities()
        self.personality_combo.clear()
        self.personality_combo.addItems(personalities)
        if personalities:
            self.personality_combo.setCurrentIndex(0)

    def on_personality_combo_changed(self, personality_name: str):
        """Handle personality change from the combo box."""
        if personality_name and hasattr(self, 'personality_widget'):
            # Update the personality widget to match the combo box selection
            self.personality_widget.set_personality(personality_name)
            # Update system prompt and trigger personality change
            self.system_prompt = self.personality_widget.get_system_prompt()
            self.on_personality_changed(personality_name)

    def toggle_spellcheck(self, checked):
        """Toggle spellcheck functionality"""
        self.config_manager.set_spellcheck_enabled(checked)
        
        if checked:
            # Enable spellcheck
            self.chat_input.setup_spellchecker()
            self.chat_input.highlight_misspelled_words()
        else:
            # Disable spellcheck by clearing highlights
            self.chat_input.clear()
            # Re-add the text without spellcheck
            cursor = self.chat_input.textCursor()
            cursor.select(QTextCursor.Document)
            cursor.removeSelectedText()
            cursor.insertText(self.chat_input.toPlainText())

    def toggle_enhancement(self, checked):
        """Toggle response enhancement functionality"""
        self.config_manager.set_enhancement_enabled(checked)
        if checked:
            print("🔍 ENHANCEMENT: Auto-enhancement enabled")
        else:
            print("🔍 ENHANCEMENT: Auto-enhancement disabled")

    def toggle_wordwrap(self, checked):
        """Toggle wordwrap session variable"""
        try:
            if hasattr(self, 'wordwrap_toggle') and self.wordwrap_toggle:
                self.session_variables['wordwrap'] = checked
                self.config_manager.set_wordwrap_enabled(checked)
                print(f"🔧 SESSION: Word wrap {'enabled' if checked else 'disabled'}")
        except Exception as e:
            print(f"🔧 TOGGLE: Error toggling wordwrap: {e}")

    def toggle_json_format(self, checked):
        """Toggle JSON format session variable"""
        try:
            if hasattr(self, 'json_format_toggle') and self.json_format_toggle:
                self.session_variables['json_format'] = checked
                self.config_manager.set_json_format_enabled(checked)
                print(f"🔧 SESSION: JSON format {'enabled' if checked else 'disabled'}")
        except Exception as e:
            print(f"🔧 TOGGLE: Error toggling JSON format: {e}")

    def toggle_verbose(self, checked):
        """Toggle verbose session variable"""
        try:
            if hasattr(self, 'verbose_toggle') and self.verbose_toggle:
                self.session_variables['verbose'] = checked
                self.config_manager.set_verbose_enabled(checked)
                print(f"🔧 SESSION: Verbose {'enabled' if checked else 'disabled'}")
        except Exception as e:
            print(f"🔧 TOGGLE: Error toggling verbose: {e}")

    def toggle_think(self, checked):
        """Toggle think mode"""
        self.session_variables['think'] = checked
        self.config_manager.set_think_enabled(checked)
        print(f"🔧 SESSION: Think mode {'enabled' if checked else 'disabled'}")

    def toggle_complexity_analysis(self, checked):
        """Toggle complexity analysis widget visibility"""
        if hasattr(self, 'complexity_widget'):
            if checked:
                self.complexity_widget.show()
                # Analyze current input if there's text
                current_text = self.chat_input.toPlainText().strip()
                if current_text:
                    self.complexity_widget.analyze_request(
                        current_text, 
                        self.conversation,
                        [self.model_combo.itemText(i) for i in range(self.model_combo.count())]
                    )
            else:
                self.complexity_widget.hide()
                self.complexity_widget.clear_analysis()

    def on_model_recommendation(self, recommended_model: str):
        """Handle model recommendation from complexity analysis"""
        try:
            # Find the recommended model in the combo box
            index = self.model_combo.findText(recommended_model)
            if index >= 0:
                self.model_combo.setCurrentIndex(index)
                self.append_to_status(f"Switched to recommended model: {recommended_model}")
            else:
                self.append_to_status(f"Recommended model '{recommended_model}' not found in available models")
        except Exception as e:
            print(f"Error switching to recommended model: {e}")

    def on_text_changed_for_complexity(self):
        """Handle text changes for complexity analysis"""
        if hasattr(self, 'complexity_widget') and self.complexity_toggle.isChecked():
            current_text = self.chat_input.toPlainText().strip()
            if current_text:
                # Get available models for recommendation
                available_models = [self.model_combo.itemText(i) for i in range(self.model_combo.count())]
                self.complexity_widget.analyze_request(current_text, self.conversation, available_models)
            else:
                self.complexity_widget.clear_analysis()

    def set_current_model_as_default(self):
        """Set the currently selected model as the default"""
        current_model = self.model_combo.currentText()
        if current_model:
            success = self.config_manager.set_default_model(current_model)
            if success:
                QMessageBox.information(self, "Success", f"'{current_model}' set as default model")
            else:
                QMessageBox.warning(self, "Error", "Failed to save default model")
        else:
            QMessageBox.warning(self, "Warning", "No model selected")

    def set_current_temperature_as_default(self):
        """Set the current temperature as the default"""
        current_temp = self.temp_combo.currentText()
        if current_temp:
            try:
                temp_value = float(current_temp)
                success = self.config_manager.set_default_temperature(temp_value)
                if success:
                    QMessageBox.information(self, "Success", f"Temperature {temp_value} set as default")
                else:
                    QMessageBox.warning(self, "Error", "Failed to save default temperature")
            except ValueError:
                QMessageBox.warning(self, "Error", "Invalid temperature value")

    def set_current_personality_as_default(self):
        """Set the current personality as the default"""
        if hasattr(self, 'personality_widget'):
            current_personality = self.personality_widget.get_current_personality()
            if current_personality:
                success = self.config_manager.set_default_personality(current_personality)
                if success:
                    QMessageBox.information(self, "Success", f"'{current_personality}' set as default personality")
                else:
                    QMessageBox.warning(self, "Error", "Failed to save default personality")
            else:
                QMessageBox.warning(self, "Warning", "No personality selected")

    def show_settings(self):
        """Show the settings dialog"""
        # Get available models and personalities
        available_models = [self.model_combo.itemText(i) for i in range(self.model_combo.count())]
        available_personalities = []
        if hasattr(self, 'personality_widget'):
            available_personalities = self.personality_widget.get_available_personalities()
        
        dialog = SettingsDialog(self.config_manager, available_models, available_personalities, self)
        if dialog.exec() == QDialog.Accepted:
            # Refresh the UI with new settings
            self.refresh_models()
            if hasattr(self, 'personality_widget'):
                self.initialize_personality_system()
            # Refresh session variables from updated config
            self.refresh_session_variables_from_config()

    def refresh_session_variables_from_config(self):
        """Refresh session variables from config after settings changes"""
        try:
            print(f"🔧 REFRESH: Refreshing session variables from config")
            
            # Update session variables from config
            self.session_variables = {
                'history': self.config_manager.is_history_enabled(),
                'wordwrap': self.config_manager.is_wordwrap_enabled(),
                'json_format': self.config_manager.is_json_format_enabled(),
                'verbose': self.config_manager.is_verbose_enabled(),
                'think': self.config_manager.is_think_enabled()
            }
            
            print(f"🔧 REFRESH: Session variables updated: {self.session_variables}")
            
        except Exception as e:
            print(f"🔧 REFRESH: Error refreshing session variables: {e}")
            # Set default values if all else fails
            self.session_variables = {
                'history': True,
                'wordwrap': True,
                'json_format': False,
                'verbose': False,
                'think': False
            }

    def test_follow_up_system(self):
        """Test the response enhancement system with a sample response."""
        # Simulate an AI response that would benefit from enhancement
        test_response = """You can use Python for web development. There are several frameworks available like Django and Flask. Django is more comprehensive while Flask is lightweight. Both are good choices depending on your needs."""
        
        # Process this response through the enhancement system
        processed_response = self.process_ai_response(test_response)
        
        # Display the result in the chat
        self.append_to_chat(self.chat_display, "Assistant", processed_response, is_code=False)
        self.conversation.append({"role": "assistant", "content": processed_response})

    def cancel_request(self):
        """Handle cancellation of ongoing request."""
        if not self.request_in_progress:
            return
            
        # Set cancellation flag
        self.cancellation_requested = True
        
        # Hide any status indicators
        self.hide_follow_up_status()
        
        # Reset request state
        self.request_in_progress = False
        
        # Update UI state
        self.send_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.chat_input.setEnabled(True)
        self.chat_input.setFocus()
        
        # Notify user
        self.append_to_chat(self.chat_display, "System", "Request cancelled by user.")

    def on_model_changed(self, text):
        """Handle model change and update session variables."""
        if not text:  # Skip if no model selected
            return
            
        # Prevent model changes during initialization
        if not self.initialization_complete:
            print(f"🔧 MODEL: Skipping model change during initialization: {text}")
            return
            
        # Prevent multiple rapid model changes
        if self.model_change_in_progress:
            print(f"🔧 MODEL: Model change already in progress, skipping: {text}")
            return
            
        self.model_change_in_progress = True
        
        # Handle "Auto" mode
        if text == "Auto":
            print("🔧 MODEL: Auto mode selected - enabling complexity analysis")
            self.model = "Auto"
            # Enable complexity analysis automatically
            self.complexity_toggle.setChecked(True)
            # Show complexity widget
            if hasattr(self, 'complexity_widget'):
                self.complexity_widget.show()
            # Analyze current input if there's text
            current_text = self.chat_input.toPlainText().strip()
            if current_text:
                available_models = [self.model_combo.itemText(i) for i in range(1, self.model_combo.count())]  # Skip "Auto"
                self.complexity_widget.analyze_request(current_text, self.conversation, available_models)
        else:
            # Regular model selection
            self.model = text
            # Disable complexity analysis for manual model selection
            self.complexity_toggle.setChecked(False)
            if hasattr(self, 'complexity_widget'):
                self.complexity_widget.hide()
        
        # Use the single timer instance to delay the update
        if self.model_update_timer:
            self.model_update_timer.start(150)
        print(f"Model changed to: {self.model}")
    
    def _delayed_model_update(self):
        """Delayed model update to ensure UI is ready."""
        try:
            self.update_session_variables_for_model()
        finally:
            self.model_change_in_progress = False

    def _initialize_session_variables(self):
        """Initialize session variables after UI is fully ready"""
        try:
            print(f"🔧 INIT: Initializing session variables from config for model '{self.model}'")
            
            # Initialize session variables directly from config (no UI toggles in main window)
            self.session_variables = {
                'history': self.config_manager.is_history_enabled(),
                'wordwrap': self.config_manager.is_wordwrap_enabled(),
                'json_format': self.config_manager.is_json_format_enabled(),
                'verbose': self.config_manager.is_verbose_enabled(),
                'think': self.config_manager.is_think_enabled()
            }
            
            print(f"🔧 INIT: Session variables initialized: {self.session_variables}")
            
        except Exception as e:
            print(f"🔧 INIT: Error initializing session variables: {e}")
            # Set default values if all else fails
            self.session_variables = {
                'history': True,
                'wordwrap': True,
                'json_format': False,
                'verbose': False,
                'think': False
            }

    def showEvent(self, event):
        """Handle window show event"""
        super().showEvent(event)
        # Session variables are already initialized in _initialize_session_variables
        # No need for additional timer here

class ConversationManagerDialog(QDialog):
    """Dialog for managing saved conversations."""
    
    def __init__(self, history_dir, parent=None):
        super().__init__(parent)
        self.history_dir = history_dir
        self.selected_file = None
        self.setup_ui()
        self.load_conversations()
    
    def setup_ui(self):
        self.setWindowTitle("Conversation Manager")
        self.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Saved Conversations")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Conversation list
        self.conversation_list = QListWidget()
        self.conversation_list.itemDoubleClicked.connect(self.load_selected)
        layout.addWidget(self.conversation_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        load_button = QPushButton("Load")
        load_button.clicked.connect(self.load_selected)
        button_layout.addWidget(load_button)
        
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_selected)
        button_layout.addWidget(delete_button)
        
        delete_all_button = QPushButton("Delete All")
        delete_all_button.clicked.connect(self.delete_all_conversations)
        delete_all_button.setStyleSheet("QPushButton { background-color: #d32f2f; color: white; }")
        button_layout.addWidget(delete_all_button)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_conversations)
        button_layout.addWidget(refresh_button)
        
        button_layout.addStretch()
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
    
    def load_conversations(self):
        """Load and display all saved conversations."""
        self.conversation_list.clear()
        
        if not os.path.exists(self.history_dir):
            return
        
        for filename in os.listdir(self.history_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.history_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    # Handle both old and new formats
                    if isinstance(data, list):
                        # Old format
                        message_count = len(data)
                        metadata = {}
                    else:
                        # New format
                        conversation = data.get("conversation", [])
                        metadata = data.get("metadata", {})
                        message_count = len(conversation)
                    
                    # Create display text
                    created = metadata.get("created", "Unknown")
                    model = metadata.get("model", "Unknown")
                    personality = metadata.get("personality", "Unknown")
                    
                    if created != "Unknown":
                        try:
                            created_dt = datetime.fromisoformat(created)
                            created_str = created_dt.strftime("%Y-%m-%d %H:%M")
                        except:
                            created_str = created
                    else:
                        created_str = "Unknown"
                    
                    display_text = f"{filename}\n  Messages: {message_count} | Model: {model} | Personality: {personality} | Created: {created_str}"
                    
                    item = QListWidgetItem(display_text)
                    item.setData(Qt.UserRole, filepath)
                    self.conversation_list.addItem(item)
                    
                except Exception as e:
                    # Add file even if metadata is corrupted
                    item = QListWidgetItem(f"{filename} (Error reading metadata)")
                    item.setData(Qt.UserRole, filepath)
                    self.conversation_list.addItem(item)
    
    def load_selected(self):
        """Load the selected conversation."""
        current_item = self.conversation_list.currentItem()
        if current_item:
            self.selected_file = current_item.data(Qt.UserRole)
            self.accept()
    
    def delete_selected(self):
        """Delete the selected conversation."""
        current_item = self.conversation_list.currentItem()
        if not current_item:
            return
        
        filepath = current_item.data(Qt.UserRole)
        filename = os.path.basename(filepath)
        
        reply = QMessageBox.question(self, "Delete Conversation", 
                                   f"Are you sure you want to delete '{filename}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                os.remove(filepath)
                self.load_conversations()  # Refresh the list
                QMessageBox.information(self, "Success", f"Deleted {filename}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete {filename}: {str(e)}")

    def delete_all_conversations(self):
        """Delete all saved conversations."""
        # Count how many conversations exist
        conversation_count = 0
        if os.path.exists(self.history_dir):
            conversation_count = len([f for f in os.listdir(self.history_dir) if f.endswith('.json')])
        
        if conversation_count == 0:
            QMessageBox.information(self, "Info", "No conversations to delete")
            return
        
        reply = QMessageBox.question(self, "Delete All Conversations", 
                                   f"Are you sure you want to delete all {conversation_count} conversations?\n\nThis action cannot be undone!",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                deleted_count = 0
                for filename in os.listdir(self.history_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(self.history_dir, filename)
                        os.remove(filepath)
                        deleted_count += 1
                
                self.load_conversations()  # Refresh the list
                QMessageBox.information(self, "Success", f"Successfully deleted {deleted_count} conversations")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to delete conversations: {str(e)}")




