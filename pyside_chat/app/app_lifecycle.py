"""
Application Lifecycle Manager - Handles startup, shutdown, and error handling
"""

import subprocess
import time
import threading
from PySide6.QtWidgets import QMainWindow, QMessageBox, QProgressDialog
from PySide6.QtCore import Qt, QTimer
from typing import Optional
from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.core.logging.helpers import LoggingHelpers
from pyside_chat.core.utils.prompts import PromptFormatter

logger = CustomLogger.get_logger(__name__)

class AppLifecycleManager:
    """Manages application startup, shutdown, and error handling"""
    
    def __init__(self, main_window: QMainWindow, service_manager, ui_manager, event_handler):
        self.main_window = main_window
        self.service_manager = service_manager
        self.ui_manager = ui_manager
        self.event_handler = event_handler
        
        # State tracking
        self.initialization_complete = False
        self.ollama_error_shown = False
        self.ollama_process = None
        self.auto_start_ollama = True  # Configurable flag
        
        # Crash detection and restart
        self.ollama_crash_detection_timer = QTimer()
        self.ollama_crash_detection_timer.timeout.connect(self._check_ollama_crash)
        self.ollama_crash_detection_timer.start(5000)  # Check every 5 seconds
        self.ollama_restart_attempts = 0
        self.max_restart_attempts = 3
        
    def initialize_application(self):
        """Initialize the application"""
        try:
            logger.info("[ID:0231] Starting application initialization...")
            
            # Apply initial theme
            theme = self.service_manager.config_manager.get("theme", "Dark")
            self.ui_manager.apply_theme(theme)
            
            # Always ensure Ollama is running since it's required
            self._ensure_ollama_running()
            
            # Mark initialization as complete
            self.initialization_complete = True
            
            # Initial model refresh
            self.event_handler._on_refresh_models()
            
            logger.info("[ID:0230] Application initialization completed successfully")
            
        except Exception as e:
            logger.error(f"[ID:0229] Error during application initialization: {e}")
            self._show_initialization_error(str(e))
            raise
    
    def handle_show_event(self):
        """Handle application show event"""
        try:
            # Skip if initialization not complete
            if not self.initialization_complete:
                return
            
            # Update window size from config
            width, height = self.service_manager.config_manager.get_window_size()
            if width > 0 and height > 0:
                self.main_window.resize(width, height)
            
            # Apply theme
            theme = self.service_manager.config_manager.get("theme", "Dark")
            self.ui_manager.apply_theme(theme)
            
            logger.info("[ID:0228] Application show event handled successfully")
            
        except Exception as e:
            logger.error(f"[ID:0227] Error handling show event: {e}")
    
    def handle_close_event(self, event):
        """Handle application close event"""
        try:
            logger.info("[ID:0226] Handling application close event...")
            
            # Clean up Event Bus resources (worker threads, etc.)
            self.event_handler.cleanup_on_exit()
            
            # Save current conversation
            conversation_service = self.service_manager.get_conversation_service()
            if conversation_service.get_messages():
                conversation_manager = self.service_manager.get_conversation_manager()
                conversation_manager.auto_save_conversation(
                    conversation_service.get_messages()
                )
            
            # Clean up voice service audio files
            chat_tab = self.ui_manager.get_chat_tab()
            if chat_tab and hasattr(chat_tab, 'voice_service'):
                chat_tab.voice_service.cleanup_on_exit()
            
            # Stop crash detection timer
            if hasattr(self, 'ollama_crash_detection_timer'):
                self.ollama_crash_detection_timer.stop()
                logger.info("[ID:0248A] Stopped Ollama crash detection timer")
            
            # Stop Ollama process if we started it
            if self.ollama_process:
                logger.info("[ID:0248] Stopping Ollama process on application close")
                self._stop_ollama_process()
            
            # Save window state
            self.service_manager.config_manager.set_window_size(
                self.main_window.width(), 
                self.main_window.height()
            )
            
            # Clean up services
            self.service_manager.cleanup()
            
            event.accept()
            logger.info("[ID:0225] Application close event handled successfully")
            
        except Exception as e:
            error_msg = PromptFormatter.format_error_message("close_error", error=str(e))
            LoggingHelpers.log_error("close", e, )
            event.accept()
    
    def show_initialization_error(self, error_message: str):
        """Show initialization error dialog"""
        try:
            QMessageBox.critical(
                self.main_window,
                "Initialization Error",
                f"Failed to initialize application:\n\n{error_message}\n\nPlease check your configuration and try again."
            )
        except Exception as e:
            logger.error(f"[ID:0224] Error showing initialization error dialog: {e}")
    
    def show_ollama_connection_error(self, context="general", force_show=False):
        """Show a user-friendly error dialog when Ollama is not running"""
        if not force_show and self.ollama_error_shown:
            return
        if not force_show:
            self.ollama_error_shown = True
            
        download_link = "https://ollama.com/download"
        
        if context == "startup":
            title = "Ollama Not Running"
            message = (
                'Ollama is not running or not accessible.<br><br>'
                'To fix this:<br>'
                '1. Make sure Ollama is installed<br>'
                "2. Start Ollama by running 'ollama serve' in a terminal<br>"
                f'3. Or download from: <a href="{download_link}">{download_link}</a><br><br>'
                "The application will continue to work, but you won't be able to send messages until Ollama is running."
            )
        elif context == "crash":
            title = "Ollama Crashed"
            message = (
                'Ollama has crashed and could not be automatically restarted.<br><br>'
                'The application attempted to restart Ollama automatically but failed.<br><br>'
                'To fix this:<br>'
                "1. Close this application<br>"
                "2. Start Ollama manually by running 'ollama serve' in a terminal<br>"
                "3. Restart this application<br>"
                f'4. Or download Ollama from: <a href="{download_link}">{download_link}</a><br><br>'
                'This may be due to insufficient system resources or a model loading issue.'
            )
        else:
            title = "Connection Error"
            message = (
                'Cannot connect to Ollama.<br><br>'
                'Please make sure:<br>'
                "1. Ollama is running (run 'ollama serve' in a terminal)<br>"
                '2. Ollama is accessible at http://localhost:11434<br>'
                '3. No firewall is blocking the connection<br>'
                f'4. Download Ollama from: <a href="{download_link}">{download_link}</a><br><br>'
                'Try sending your message again once Ollama is running.'
            )
        
        msg_box = QMessageBox(self.main_window)
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setTextInteractionFlags(Qt.TextBrowserInteraction)
        msg_box.setText(message)
        
        # Add buttons for different actions
        if self._is_ollama_installed():
            msg_box.addButton("Start Ollama", QMessageBox.ActionRole)
            msg_box.addButton("Try Again", QMessageBox.ActionRole)
        
        msg_box.addButton("OK", QMessageBox.AcceptRole)
        
        # Show the dialog and handle button clicks
        result = msg_box.exec()
        
        if result == QMessageBox.ActionRole:  # "Start Ollama" button
            if self._is_ollama_installed():
                logger.info("[ID:0249] User requested to start Ollama from error dialog")
                self.start_ollama_manually()
        elif result == 1:  # "Try Again" button (second ActionRole)
            logger.info("[ID:0250] User requested to try connecting again")
            if self.check_ollama_connection():
                logger.info("[ID:0251] Connection successful on retry")
                self.ollama_error_shown = False  # Reset flag so user can see success
            else:
                logger.warning("[ID:0252] Connection still failed on retry")
    
    def show_ollama_startup_dialog(self):
        """Show a dialog asking if user wants to start Ollama automatically"""
        # This method is kept for backward compatibility but is no longer used
        # since Ollama is always started automatically
        logger.info("[ID:0253] Startup dialog called but Ollama is started automatically")
        return self.start_ollama_manually()
    
    def check_ollama_connection(self):
        """Check if Ollama is running and accessible"""
        ollama_service = self.service_manager.get_ollama_service()
        connection_ok = ollama_service.test_connection()
        
        # Reset restart attempts if connection is successful
        if connection_ok:
            self._reset_ollama_restart_attempts()
        
        return connection_ok
    
    def is_initialization_complete(self) -> bool:
        """Check if initialization is complete"""
        return self.initialization_complete
    
    def set_ollama_error_shown(self, shown: bool):
        """Set the Ollama error shown flag"""
        self.ollama_error_shown = shown
    
    def get_ollama_error_shown(self) -> bool:
        """Get the Ollama error shown flag"""
        return self.ollama_error_shown
    
    def _ensure_ollama_running(self):
        """Ensure Ollama is running, start it if needed"""
        try:
            logger.info("[ID:0232] Checking if Ollama is running...")
            
            # First check if Ollama is already running
            if self.check_ollama_connection():
                logger.info("[ID:0233] Ollama is already running")
                return True
            
            # Check if Ollama is installed
            if not self._is_ollama_installed():
                logger.warning("[ID:0234] Ollama is not installed")
                self.show_ollama_connection_error("startup", force_show=True)
                return False
            
            # Start Ollama automatically
            logger.info("[ID:0236] Ollama not running, starting automatically")
            return self._start_ollama_background()
            
        except Exception as e:
            logger.error(f"[ID:0237] Error ensuring Ollama is running: {e}")
            return False
    
    def _is_ollama_installed(self) -> bool:
        """Check if Ollama is installed and accessible"""
        try:
            result = subprocess.run(
                ["ollama", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            return False
    
    def _start_ollama_background(self) -> bool:
        """Start Ollama in the background with progress dialog"""
        try:
            # Create progress dialog
            progress = QProgressDialog("Starting Ollama...", "Cancel", 0, 100, self.main_window)
            progress.setWindowTitle("Starting Ollama")
            progress.setModal(True)
            progress.setAutoClose(False)
            progress.setValue(0)
            progress.show()
            
            # Start Ollama process
            self.ollama_process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            logger.info(f"[ID:0237] Started Ollama process with PID: {self.ollama_process.pid}")
            
            # Wait for Ollama to start in a separate thread
            def wait_for_ollama():
                max_wait_time = 30  # 30 seconds timeout
                check_interval = 1   # Check every second
                elapsed_time = 0
                
                while elapsed_time < max_wait_time:
                    if progress.wasCanceled():
                        logger.info("[ID:0238] User cancelled Ollama startup")
                        self._stop_ollama_process()
                        return False
                    
                    # Update progress
                    progress_value = min(int((elapsed_time / max_wait_time) * 100), 95)
                    progress.setValue(progress_value)
                    
                    # Check if Ollama is responding
                    if self.check_ollama_connection():
                        progress.setValue(100)
                        logger.info(f"[ID:0239] Ollama started successfully after {elapsed_time} seconds")
                        return True
                    
                    time.sleep(check_interval)
                    elapsed_time += check_interval
                
                # Timeout
                logger.warning("[ID:0240] Ollama startup timeout")
                self._stop_ollama_process()
                return False
            
            # Run the wait function in a separate thread
            wait_thread = threading.Thread(target=wait_for_ollama, daemon=True)
            wait_thread.start()
            
            # Wait for the thread to complete
            wait_thread.join(timeout=35)  # Slightly longer than max_wait_time
            
            if wait_thread.is_alive():
                # Thread is still running, which means timeout
                logger.warning("[ID:0241] Ollama startup thread timeout")
                self._stop_ollama_process()
                progress.close()
                return False
            
            progress.close()
            
            # Final check
            if self.check_ollama_connection():
                logger.info("[ID:0242] Ollama is now running and accessible")
                return True
            else:
                logger.warning("[ID:0243] Ollama process started but not responding")
                return False
                
        except Exception as e:
            logger.error(f"[ID:0244] Error starting Ollama: {e}")
            self._stop_ollama_process()
            return False
    
    def _stop_ollama_process(self):
        """Stop the Ollama process if running"""
        if self.ollama_process:
            try:
                self.ollama_process.terminate()
                self.ollama_process.wait(timeout=5)
                logger.info("[ID:0245] Ollama process terminated")
            except subprocess.TimeoutExpired:
                self.ollama_process.kill()
                logger.warning("[ID:0246] Force killed Ollama process")
            except Exception as e:
                logger.error(f"[ID:0247] Error stopping Ollama process: {e}")
            finally:
                self.ollama_process = None
    
    def start_ollama_manually(self) -> bool:
        """Manually start Ollama (called from UI)"""
        # Reset restart attempts when manually starting
        self.ollama_restart_attempts = 0
        return self._start_ollama_background()
    
    def stop_ollama_manually(self):
        """Manually stop Ollama (called from UI)"""
        self._stop_ollama_process()
    
    def is_ollama_running(self) -> bool:
        """Check if Ollama is currently running"""
        return self.check_ollama_connection()
    
    def get_ollama_process_info(self) -> Optional[dict]:
        """Get information about the Ollama process"""
        if self.ollama_process:
            try:
                return {
                    "pid": self.ollama_process.pid,
                    "returncode": self.ollama_process.returncode,
                    "alive": self.ollama_process.poll() is None
                }
            except Exception:
                return None
        return None
    
    def set_auto_start_ollama(self, enabled: bool):
        """Set whether to auto-start Ollama (deprecated - always enabled)"""
        logger.info("[ID:0256] Auto-start Ollama is always enabled")
        return True
    
    def get_auto_start_ollama(self) -> bool:
        """Get whether auto-start Ollama is enabled (always True)"""
        return True
    
    def _check_ollama_crash(self):
        """Check if Ollama has crashed and restart if needed"""
        try:
            # Only check if we started Ollama ourselves
            if not self.ollama_process:
                return
            
            # Check if the process is still alive
            if self.ollama_process.poll() is not None:
                logger.warning(f"[ID:0257] Ollama process crashed (PID: {self.ollama_process.pid})")
                
                # Check if we can still connect to Ollama
                if not self.check_ollama_connection():
                    logger.error("[ID:0258] Ollama connection lost, attempting restart")
                    
                    if self.ollama_restart_attempts < self.max_restart_attempts:
                        self.ollama_restart_attempts += 1
                        logger.info(f"[ID:0259] Attempting to restart Ollama (attempt {self.ollama_restart_attempts}/{self.max_restart_attempts})")
                        
                        # Stop the crashed process
                        self._stop_ollama_process()
                        
                        # Restart Ollama
                        if self._start_ollama_background():
                            logger.info("[ID:0260] Ollama restarted successfully after crash")
                            self.ollama_restart_attempts = 0  # Reset counter on success
                        else:
                            logger.error(f"[ID:0261] Failed to restart Ollama (attempt {self.ollama_restart_attempts})")
                    else:
                        logger.error(f"[ID:0262] Maximum restart attempts ({self.max_restart_attempts}) reached, stopping auto-restart")
                        self.show_ollama_connection_error("crash", force_show=True)
                        
        except Exception as e:
            logger.error(f"[ID:0263] Error in Ollama crash detection: {e}")
    
    def _reset_ollama_restart_attempts(self):
        """Reset the restart attempts counter (called on successful connection)"""
        self.ollama_restart_attempts = 0 