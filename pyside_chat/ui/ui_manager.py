from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *


# Import UI components
from pyside_chat.ui.tabs.chat_tab.chat_tab import ChatTab
from pyside_chat.ui.tabs.model_tab import ModelTab
from pyside_chat.ui.tabs.personality_tab import PersonalityTab
from pyside_chat.ui.tabs.memory_tab import MemoryTab
from pyside_chat.ui.tabs.tab_styles import TabStyles
from pyside_chat.ui.themes.styles import light_stylesheet, dark_stylesheet
from pyside_chat.core.utils.prompts import PromptFormatter

# Import ConfigManager
from pyside_chat.config.config_manager import ConfigManager


"""
UI Manager - Handles UI setup, menu creation, and styling
"""

logger = CustomLogger.get_logger(__name__)


class UIManager:
    """Manages UI setup, menu creation, and styling"""

    def __init__(self, main_window: QMainWindow, config_manager: ConfigManager):
        self.main_window = main_window
        self.config_manager = config_manager
        self.tabs: Optional[QTabWidget] = None
        self.chat_tab: Optional[ChatTab] = None
        self.model_tab: Optional[ModelTab] = None
        self.personality_tab: Optional[PersonalityTab] = None
        self.memory_tab: Optional[MemoryTab] = None
        self.status_bar: Optional[QStatusBar] = None
        self.status_var: str = ""

        # Menu actions for external connections
        self.menu_actions = {}

    def setup_ui(self, conversation_manager, summarization_service, memory_enabled, memory_service=None):
        """Setup the main UI components"""
        try:
            # Set window properties
            self.main_window.setWindowTitle(
                "Ollama Chat - Local LLM Chat Application")
            self.main_window.setGeometry(100, 100, 1200, 800)

            # Create central widget
            central_widget = QWidget()
            self.main_window.setCentralWidget(central_widget)

            # Create main layout
            main_layout = QVBoxLayout(central_widget)

            # Create tab widget with external styling
            self.tabs = QTabWidget()
            self.tabs.setStyleSheet(TabStyles.get_tab_style())
            main_layout.addWidget(self.tabs)

            # Create and add tabs with reduced coupling
            self.chat_tab = ChatTab(
                # Pass main window as parent so chat tab can access chat controller
                parent=self.main_window,
                conversation_manager=conversation_manager,
                summarization_service=summarization_service,
                config_manager=self.config_manager
            )
            self.model_tab = ModelTab()
            self.personality_tab = PersonalityTab()

            self.tabs.addTab(self.chat_tab, "Chat")
            self.tabs.addTab(self.model_tab, "Model Manager")
            self.tabs.addTab(self.personality_tab, "Personalities")

            # Conditionally add memory tab
            if memory_enabled:
                self.memory_tab = MemoryTab(memory_service=memory_service)
                if hasattr(self.memory_tab, 'set_conversation_service'):
                    self.memory_tab.set_conversation_service(
                        conversation_manager)
                self.tabs.addTab(self.memory_tab, "Memory")
            else:
                self.memory_tab = None

            # Setup status bar
            self.status_bar = QStatusBar(self.main_window)
            self.main_window.setStatusBar(self.status_bar)
            self.status_var = PromptFormatter.format_status_message("ready")
            self.status_bar.showMessage(self.status_var)

            logger.info("[ID:0106] UI setup completed successfully")

        except Exception as e:
            logger.error(f"[ID:0105] Error setting up UI: {e}")
            raise

    def setup_menu_bar(self):
        """Setup the menu bar with all actions"""
        try:
            menubar = self.main_window.menuBar()

            # File menu
            file_menu = menubar.addMenu("&File")

            # New conversation action
            new_conversation_action = QAction(
                "&New Conversation", self.main_window)
            new_conversation_action.setShortcut("Ctrl+N")
            new_conversation_action.setStatusTip("Start a new conversation")
            file_menu.addAction(new_conversation_action)
            self.menu_actions['new_conversation'] = new_conversation_action

            # Clear chat action
            clear_chat_action = QAction("&Clear Chat", self.main_window)
            clear_chat_action.setShortcut("Ctrl+L")
            clear_chat_action.setStatusTip("Clear the current chat display")
            file_menu.addAction(clear_chat_action)
            self.menu_actions['clear_chat'] = clear_chat_action

            file_menu.addSeparator()

            # Save chat action
            save_chat_action = QAction("&Save Chat...", self.main_window)
            save_chat_action.setShortcut("Ctrl+S")
            save_chat_action.setStatusTip("Save current chat to file")
            file_menu.addAction(save_chat_action)
            self.menu_actions['save_chat'] = save_chat_action

            # Load chat action
            load_chat_action = QAction("&Load Chat...", self.main_window)
            load_chat_action.setShortcut("Ctrl+O")
            load_chat_action.setStatusTip("Load chat from file")
            file_menu.addAction(load_chat_action)
            self.menu_actions['load_chat'] = load_chat_action

            file_menu.addSeparator()

            # Exit action
            exit_action = QAction("E&xit", self.main_window)
            exit_action.setShortcut("Ctrl+Q")
            exit_action.setStatusTip("Exit the application")
            file_menu.addAction(exit_action)
            self.menu_actions['exit'] = exit_action

            # Edit menu
            edit_menu = menubar.addMenu("&Edit")

            # Settings action
            settings_action = QAction("&Settings...", self.main_window)
            settings_action.setShortcut("Ctrl+,")
            settings_action.setStatusTip("Open application settings")
            edit_menu.addAction(settings_action)
            self.menu_actions['settings'] = settings_action

            # Tools menu
            tools_menu = menubar.addMenu("&Tools")

            # Refresh models action
            refresh_models_action = QAction(
                "&Refresh Models", self.main_window)
            refresh_models_action.setStatusTip(
                "Refresh available models from Ollama")
            tools_menu.addAction(refresh_models_action)
            self.menu_actions['refresh_models'] = refresh_models_action

            # Help menu
            help_menu = menubar.addMenu("&Help")

            # About action
            about_action = QAction("&About", self.main_window)
            about_action.setStatusTip("About Ollama Chat")
            help_menu.addAction(about_action)
            self.menu_actions['about'] = about_action

            logger.info("[ID:0104] Menu bar setup completed successfully")

        except Exception as e:
            logger.error(f"[ID:0103] Error setting up menu bar: {e}")
            raise

    def apply_theme(self, theme: str = "Dark"):
        """Apply the specified theme"""
        try:
            if theme == "Light":
                self.main_window.setStyleSheet(light_stylesheet)
            else:
                self.main_window.setStyleSheet(dark_stylesheet)

            logger.info(f"[ID:0102] Theme applied: {theme}")

        except Exception as e:
            logger.error(f"[ID:0101] Error applying theme: {e}")

    def update_status(self, message: str):
        """Update status bar message"""
        try:
            self.status_var = message
            if self.status_bar:
                self.status_bar.showMessage(self.status_var)
        except Exception as e:
            logger.error(f"[ID:0100] Error updating status: {e}")

    def get_menu_action(self, action_name: str) -> Optional[QAction]:
        """Get a menu action by name"""
        return self.menu_actions.get(action_name)

    def get_main_window(self) -> Optional[QMainWindow]:
        """Get the main window"""
        return self.main_window

    def get_chat_tab(self) -> Optional[ChatTab]:
        """Get the chat tab"""
        return self.chat_tab

    def get_model_tab(self) -> Optional[ModelTab]:
        """Get the model tab"""
        return self.model_tab

    def get_personality_tab(self) -> Optional[PersonalityTab]:
        """Get the personality tab"""
        return self.personality_tab

    def get_memory_tab(self) -> Optional[MemoryTab]:
        """Get the memory tab"""
        return self.memory_tab

    def get_tabs(self) -> Optional[QTabWidget]:
        """Get the tab widget"""
        return self.tabs

    def show_about_dialog(self):
        """Show the about dialog"""
        try:
            about_text = PromptFormatter.get_menu_text("about_text")
            QMessageBox.about(self.main_window,
                              "About Ollama Chat", about_text)
        except Exception as e:
            logger.error(f"[ID:0099] Error showing about dialog: {e}")

    def show_clear_chat_dialog(self) -> bool:
        """Show clear chat confirmation dialog"""
        try:
            question_text = PromptFormatter.get_menu_text(
                "clear_chat_question")
            reply = QMessageBox.question(
                self.main_window, "Clear Chat", question_text,
                QMessageBox.Yes | QMessageBox.No
            )
            return reply == QMessageBox.Yes
        except Exception as e:
            logger.error(f"[ID:0098] Error showing clear chat dialog: {e}")
            return False
