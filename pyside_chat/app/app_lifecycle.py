# Shared imports
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *



"""
Application Lifecycle Manager - Handles startup, shutdown, and error handling
"""

import subprocess
import threading
import requests
import json

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
        self.ollama_started_by_app = False  # Track if we started Ollama
        
        # Crash detection and restart
        self.ollama_crash_detection_timer = QTimer()
        self.ollama_crash_detection_timer.timeout.connect(self._check_ollama_crash)
        self.ollama_crash_detection_timer.start(5000)  # Check every 5 seconds
        logger.info("[ID:0256] Started Ollama crash detection timer (every 5 seconds)")
        self.ollama_restart_attempts = 0
        self.max_restart_attempts = 3
        
        # Start Ollama immediately when lifecycle manager is created
        logger.info("[ID:OLLAMA_IMMEDIATE] Starting immediate Ollama check and startup")
        
        
    def initialize_application(self):
        """Initialize the application"""
        try:
            logger.info("[ID:0231] Starting application initialization...")
            
            # Apply initial theme
            theme = self.service_manager.config_manager.get("theme", "Dark")
            self.ui_manager.apply_theme(theme)
            
            # Verify Ollama installation and connection before proceeding
            if not self._verify_ollama_installation():
                logger.warning("[ID:VERIFY_FAILED] Ollama verification failed - app will not proceed")
                return False
            
            # Mark initialization as complete
            self.initialization_complete = True
            
            # Initial model refresh
            self.event_handler._on_refresh_models()
            
            logger.info("[ID:0230] Application initialization completed successfully")
            return True
            
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
            logger.info("[ID:0226] Application closing, cleaning up...")
            
            # Stop Ollama crash detection
            if self.ollama_crash_detection_timer:
                self.ollama_crash_detection_timer.stop()
                logger.info("[ID:0226A] Stopped Ollama crash detection timer")
            
            # Check if we should close Ollama on app exit
            close_ollama_on_exit = self.service_manager.config_manager.get("close_ollama_on_exit", True)
            
            if close_ollama_on_exit and self.ollama_process and self.ollama_started_by_app:
                logger.info("[ID:0226B] Closing Ollama app.exe on application exit (config enabled, started by app)")
                self._stop_ollama_process()
            elif not close_ollama_on_exit and self.ollama_process and self.ollama_started_by_app:
                logger.info("[ID:0226C] Keeping Ollama app.exe running on application exit (config disabled, started by app)")
            elif self.ollama_process and not self.ollama_started_by_app:
                logger.info("[ID:0226D] Not closing Ollama app.exe (was not started by this app)")
            else:
                logger.info("[ID:0226E] No Ollama process to close")
            
            # Save window size
            size = self.main_window.size()
            self.service_manager.config_manager.set_window_size(size.width(), size.height())
            
            # Save configuration
            self.service_manager.config_manager.save_config()
            
            logger.info("[ID:0225] Application cleanup completed")
            
        except Exception as e:
            logger.error(f"[ID:0224] Error during application cleanup: {e}")
        
        # Accept the close event
        event.accept()
    
    def show_initialization_error(self, error_message: str):
        """Show initialization error dialog"""
        msg_box = QMessageBox(self.main_window)
        msg_box.setWindowTitle("Initialization Error")
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("Failed to initialize the application.")
        msg_box.setInformativeText(error_message)
        msg_box.exec()
    
    def show_ollama_connection_error(self, context="general", force_show=False):
        """Show a user-friendly error dialog when Ollama is not running"""
        logger.info(f"[ID:ERROR_DIALOG] Showing Ollama error dialog - context: {context}, force_show: {force_show}, error_shown: {self.ollama_error_shown}")
        
        if not force_show and self.ollama_error_shown:
            logger.info("[ID:ERROR_DIALOG] Skipping error dialog (already shown and not forced)")
            return
        if not force_show:
            self.ollama_error_shown = True
            
        download_link = "https://ollama.com/download"
        
        if context == "not_installed":
            title = "Ollama Not Found"
            message = (
                '<b>Ollama app.exe was not found in the expected locations.</b><br><br>'
                'Ollama is required for this application to work properly.<br><br>'
                '<b>Possible solutions:</b><br>'
                f'1. Install Ollama from: <a href="{download_link}">{download_link}</a><br>'
                '2. If Ollama is already installed, specify the custom path<br>'
                '3. Make sure Ollama app.exe is in your PATH<br><br>'
                '<b>Installation instructions:</b><br>'
                '<b>Windows:</b> Download the installer and run it<br>'
                '<b>macOS:</b> Download the .dmg file and drag to Applications<br>'
                '<b>Linux:</b> Run: curl -fsSL https://ollama.com/install.sh | sh<br><br>'
                'The application will continue to work, but you won\'t be able to send messages until Ollama is running.'
            )
        elif context == "startup":
            title = "Ollama Not Running"
            message = (
                'Ollama is not running or not accessible.<br><br>'
                'To fix this:<br>'
                '1. Make sure Ollama is installed<br>'
                "2. Start Ollama by running the Ollama app.exe application<br>"
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
                "2. Start Ollama manually by running the Ollama app.exe application<br>"
                "3. Restart this application<br>"
                f'4. Or download Ollama from: <a href="{download_link}">{download_link}</a><br><br>'
                'This may be due to insufficient system resources or a model loading issue.'
            )
        elif context == "startup_failed":
            title = "Ollama Startup Failed"
            message = (
                'Failed to start the Ollama app.exe application.<br><br>'
                'The application tried to start Ollama automatically but encountered an error.<br><br>'
                'To fix this:<br>'
                "1. Make sure Ollama is properly installed<br>"
                "2. Try starting Ollama manually by running the Ollama app.exe application<br>"
                "3. Check if Ollama is already running<br>"
                f'4. Download Ollama from: <a href="{download_link}">{download_link}</a><br><br>'
                'The application will continue to work, but you won\'t be able to send messages until Ollama is running.'
            )
        else:
            title = "Connection Error"
            message = (
                'Cannot connect to Ollama.<br><br>'
                'Please make sure:<br>'
                "1. Ollama is running (start the Ollama app.exe application)<br>"
                '2. Ollama is accessible at http://localhost:11434<br>'
                '3. No firewall is blocking the connection<br>'
                f'4. Download Ollama from: <a href="{download_link}">{download_link}</a><br><br>'
                'Try sending your message again once Ollama is running.'
            )
        
        logger.info(f"[ID:ERROR_DIALOG] Creating message box with title: {title}")
        msg_box = QMessageBox(self.main_window)
        msg_box.setWindowTitle(title)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setTextInteractionFlags(Qt.TextBrowserInteraction)
        msg_box.setText(message)
        logger.info("[ID:ERROR_DIALOG] Message box created successfully")
        
        # Add the four buttons as requested
        close_button = msg_box.addButton("Close", QMessageBox.RejectRole)
        recheck_button = msg_box.addButton("Recheck", QMessageBox.ActionRole)
        open_browser_button = msg_box.addButton("Open Browser", QMessageBox.ActionRole)
        custom_path_button = msg_box.addButton("Specify Custom Path", QMessageBox.ActionRole)
        
        # Show the dialog and handle button clicks
        logger.info("[ID:ERROR_DIALOG] About to show message box with four buttons")
        result = msg_box.exec()
        logger.info(f"[ID:ERROR_DIALOG] Message box closed with result: {result}")
        
        # Handle button clicks
        clicked_button = msg_box.clickedButton()
        logger.info(f"[ID:ERROR_DIALOG] Clicked button: {clicked_button}")
        
        if clicked_button == close_button:
            logger.info("[ID:CLOSE_APP] User clicked Close - shutting down app")
            # Close the application
            self.main_window.close()
            
        elif clicked_button == recheck_button:
            logger.info("[ID:RECHECK] User clicked Recheck - verifying Ollama installation")
            # Reset error flag to allow showing dialog again
            self.ollama_error_shown = False
            
            # Perform full verification
            if self._verify_ollama_installation():
                logger.info("[ID:RECHECK] Ollama verification successful - proceeding with app initialization")
                # Complete the initialization process
                self.initialization_complete = True
                # Initial model refresh
                self.event_handler._on_refresh_models()
                # Show the main window if it's not already visible
                if not self.main_window.isVisible():
                    logger.info("[ID:RECHECK] Showing main window after successful verification")
                    self.main_window.show()
                return  # Success, don't show error dialog again
            else:
                logger.warning("[ID:RECHECK] Ollama verification failed - showing error dialog again")
                # If verification failed, show error dialog again
                self.show_ollama_connection_error(context, force_show=True)
            
        elif clicked_button == open_browser_button:
            logger.info("[ID:OPEN_BROWSER] User clicked Open Browser")
            logger.info(f"[ID:OPEN_BROWSER] Download link: {download_link}")
            # Open the download link in default browser
            try:
                import webbrowser
                success = webbrowser.open(download_link)
                logger.info(f"[ID:OPEN_BROWSER] Browser open result: {success}")
                if not success:
                    logger.warning("[ID:OPEN_BROWSER] Failed to open browser, trying alternative method")
                    # Try alternative method
                    import subprocess
                    import platform
                    if platform.system() == "Windows":
                        subprocess.run(["start", download_link], shell=True)
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.run(["open", download_link])
                    else:  # Linux
                        subprocess.run(["xdg-open", download_link])
            except Exception as e:
                logger.error(f"[ID:OPEN_BROWSER] Error opening browser: {e}")
                # Show error message to user
                error_msg = QMessageBox(self.main_window)
                error_msg.setWindowTitle("Browser Error")
                error_msg.setIcon(QMessageBox.Warning)
                error_msg.setText("Failed to open browser automatically.")
                error_msg.setInformativeText(f"Please manually visit: {download_link}")
                error_msg.exec()
                
        elif clicked_button == custom_path_button:
            logger.info("[ID:CUSTOM_PATH] User clicked Specify Custom Path")
            self._show_custom_path_dialog(context)
            
        else:
            logger.warning(f"[ID:ERROR_DIALOG] Unexpected button result: {result}")
    
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
    
    def reset_ollama_error_shown(self):
        """Reset the Ollama error shown flag to allow showing error dialogs again"""
        self.ollama_error_shown = False
        logger.info("[ID:RESET_ERROR] Reset Ollama error shown flag")
    
    def force_show_ollama_error(self, context="not_installed"):
        """Force show the Ollama error dialog regardless of the shown flag"""
        logger.info(f"[ID:FORCE_ERROR] Force showing Ollama error dialog - context: {context}")
        self.show_ollama_connection_error(context, force_show=True)
    
    def test_error_dialog(self):
        """Test method to show the error dialog for testing purposes"""
        logger.info("[ID:TEST_ERROR] Testing error dialog display")
        self.reset_ollama_error_shown()  # Reset the flag
        self.show_ollama_connection_error("not_installed", force_show=True)
    
    def get_available_models(self) -> List[str]:
        """Get list of available models from Ollama"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                logger.info(f"[ID:MODEL_QUERY] Found {len(models)} available models")
                return models
            else:
                logger.warning(f"[ID:MODEL_QUERY] Error fetching models: HTTP {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"[ID:MODEL_QUERY] Error getting models: {e}")
            return []
    
    def send_test_message(self, model_name: str, message: str = "Hello, this is a test message. Please respond with a simple greeting.") -> tuple[bool, str]:
        """Send a test message to Ollama and get response"""
        try:
            logger.info(f"[ID:TEST_MSG] Sending test message to model: {model_name}")
            
            # Prepare the request payload
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            # Send the request
            response = requests.post(
                "http://localhost:11434/api/chat",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('message', {}).get('content', 'No response content')
                logger.info(f"[ID:TEST_MSG] Successfully received response from {model_name}")
                return True, ai_response
            else:
                logger.warning(f"[ID:TEST_MSG] Error sending message: HTTP {response.status_code}")
                logger.warning(f"[ID:TEST_MSG] Response: {response.text}")
                return False, None
                
        except Exception as e:
            logger.error(f"[ID:TEST_MSG] Error sending test message: {e}")
            return False, None
    
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
                logger.warning("[ID:0234] Ollama is not installed or not accessible")
                
                # Try to find where Ollama should be
                ollama_executable = self._find_ollama_executable()
                logger.info(f"[ID:0234A] Ollama executable path: {ollama_executable}")
                
                if ollama_executable == "ollama app.exe":
                    error_msg = "Ollama executable not found. Please install Ollama from https://ollama.com/download"
                else:
                    error_msg = f"Ollama executable not found at expected location. Please ensure Ollama is properly installed."
                
                logger.info("[ID:0234B] About to show error dialog for not_installed context")
                self.show_ollama_connection_error("not_installed", force_show=True)
                logger.info("[ID:0234C] Error dialog call completed")
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
            # First try to find the executable
            ollama_executable = self._find_ollama_executable()
            
            # For GUI executables, just check if the file exists and is executable
            if os.path.exists(ollama_executable) and os.access(ollama_executable, os.X_OK):
                logger.info(f"[ID:OLLAMA_VERSION] Ollama executable found: {ollama_executable}")
                return True
            
            # If it's not a full path, try to find it in PATH
            if not os.path.isabs(ollama_executable):
                import shutil
                full_path = shutil.which(ollama_executable)
                if full_path and os.path.exists(full_path) and os.access(full_path, os.X_OK):
                    logger.info(f"[ID:OLLAMA_VERSION] Ollama executable found in PATH: {full_path}")
                    return True
            
            logger.warning(f"[ID:OLLAMA_VERSION] Ollama executable not found: {ollama_executable}")
            return False
                
        except Exception as e:
            logger.error(f"[ID:OLLAMA_VERSION] Error checking Ollama installation: {e}")
            return False
    
    def _find_ollama_executable(self) -> str:
        """Find the Ollama app.exe executable path"""
        try:
            logger.info("[ID:OLLAMA_PATH_DEBUG] Starting Ollama app.exe executable search...")
            
            # First check for custom path from config
            custom_path = self.service_manager.config_manager.get("custom_ollama_path", "")
            if custom_path and os.path.exists(custom_path):
                logger.info(f"[ID:OLLAMA_PATH] Using custom Ollama path: {custom_path}")
                return custom_path
            
            # Then try to find ollama app.exe in PATH
            import shutil
            ollama_path = shutil.which("ollama app.exe")
            if ollama_path:
                logger.info(f"[ID:OLLAMA_PATH] Found Ollama app.exe in PATH: {ollama_path}")
                return ollama_path
            
            # Check common Windows install locations for ollama app.exe only
            possible_paths = [
                r"C:\Program Files\Ollama\ollama app.exe",
                r"C:\Program Files (x86)\Ollama\ollama app.exe",
                r"C:\Users\{}\AppData\Local\Programs\Ollama\ollama app.exe".format(os.getenv('USERNAME', '')),
                r"C:\Users\{}\AppData\Roaming\Ollama\ollama app.exe".format(os.getenv('USERNAME', '')),
                r"C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\ollama app.exe".format(os.getenv('USERNAME', '')),
            ]
            
            logger.info(f"[ID:OLLAMA_PATH_DEBUG] Checking {len(possible_paths)} possible paths for ollama app.exe...")
            for i, path in enumerate(possible_paths):
                exists = os.path.exists(path)
                logger.info(f"[ID:OLLAMA_PATH_DEBUG] Path {i+1}: {path} - Exists: {exists}")
                if exists:
                    logger.info(f"[ID:OLLAMA_PATH] Found Ollama app.exe at: {path}")
                    return path
            
            # If not found, return the expected name for PATH fallback
            logger.warning("[ID:OLLAMA_PATH] Ollama app.exe not found in common locations, trying PATH fallback")
            return "ollama app.exe"
            
        except Exception as e:
            logger.error(f"[ID:OLLAMA_PATH] Error finding Ollama app.exe executable: {e}")
            logger.error(f"[ID:OLLAMA_PATH] Error type: {type(e).__name__}")
            return "ollama app.exe"  # Fallback to PATH
    
    def _start_ollama_background(self) -> bool:
        """Start Ollama in the background with progress dialog"""
        try:
            # Find the Ollama executable
            ollama_executable = self._find_ollama_executable()
            
            # Create progress dialog
            progress = QProgressDialog("Starting Ollama...", "Cancel", 0, 100, self.main_window)
            progress.setWindowTitle("Starting Ollama")
            progress.setModal(True)
            progress.setAutoClose(False)
            progress.setMinimumDuration(0)  # Show immediately
            progress.setValue(0)
            progress.setLabelText("Starting Ollama...")
            progress.show()
            progress.raise_()  # Bring to front
            progress.activateWindow()  # Activate the window
            
            # Force the dialog to update and process events
            QApplication.processEvents()
            time.sleep(0.1)  # Small delay to ensure dialog is visible
            
            logger.info(f"[ID:OLLAMA_START] Starting Ollama with executable: {ollama_executable}")
            
            # Start Ollama app.exe process
            try:
                logger.info(f"[ID:OLLAMA_START_DEBUG] Attempting to start Ollama app.exe: {ollama_executable}")
                
                # Start GUI application without capturing output
                self.ollama_process = subprocess.Popen(
                    [ollama_executable],
                    stdout=None,  # Don't capture output for GUI
                    stderr=None,
                    text=True,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
                )
                logger.info(f"[ID:OLLAMA_START_DEBUG] Started Ollama app.exe process with PID: {self.ollama_process.pid}")
                logger.info(f"[ID:0237] Started Ollama app.exe process with PID: {self.ollama_process.pid}")
                
                # Mark that we started this Ollama process
                self.ollama_started_by_app = True
                
            except FileNotFoundError:
                logger.error(f"[ID:OLLAMA_START_ERROR] Ollama app.exe not found: {ollama_executable}")
                progress.close()
                self.show_ollama_connection_error("not_installed", force_show=True)
                return False
            except Exception as e:
                logger.error(f"[ID:OLLAMA_START_ERROR] Failed to start Ollama app.exe: {e}")
                logger.error(f"[ID:OLLAMA_START_ERROR] Error details: {type(e).__name__}: {str(e)}")
                progress.close()
                self.show_ollama_connection_error("startup_failed", force_show=True)
                return False
            
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
                    
                    # Update progress text to show elapsed time
                    progress.setLabelText(f"Starting Ollama... ({elapsed_time}s)")
                    
                    # Force the dialog to update
                    QApplication.processEvents()
                    
                    # Check if Ollama is responding
                    if self.check_ollama_connection():
                        progress.setValue(100)
                        progress.setLabelText("Ollama started successfully!")
                        QApplication.processEvents()
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
            # Check if thread is already running (shouldn't be, but safety check)
            if not wait_thread.is_alive():
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
    
    def _verify_ollama_installation(self) -> bool:
        """Verify that Ollama is installed, running, and accessible"""
        try:
            logger.info("[ID:VERIFY] Starting Ollama installation verification...")
            
            # Step 1: Check if Ollama is installed
            if not self._is_ollama_installed():
                logger.warning("[ID:VERIFY] Ollama is not installed")
                self.show_ollama_connection_error("not_installed", force_show=True)
                return False
            
            # Step 2: Check if Ollama is running
            if not self.is_ollama_running():
                logger.info("[ID:VERIFY] Ollama is installed but not running - attempting to start")
                if not self._start_ollama_background():
                    logger.warning("[ID:VERIFY] Failed to start Ollama")
                    return False
            
            # Step 3: Test connection to Ollama
            if not self.check_ollama_connection():
                logger.warning("[ID:VERIFY] Ollama is running but connection test failed")
                self.show_ollama_connection_error("startup", force_show=True)
                return False
            
            # Step 4: Test getting models (optional but good verification)
            try:
                models = self.get_available_models()
                if not models:
                    logger.warning("[ID:VERIFY] Ollama is running but no models available")
                    # This is not a critical failure, just a warning
                else:
                    logger.info(f"[ID:VERIFY] Found {len(models)} available models")
            except Exception as e:
                logger.warning(f"[ID:VERIFY] Could not retrieve models: {e}")
                # This is not a critical failure, just a warning
            
            logger.info("[ID:VERIFY] Ollama verification completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"[ID:VERIFY] Error during Ollama verification: {e}")
            self.show_ollama_connection_error("startup_failed", force_show=True)
            return False
    
    def _stop_ollama_process(self):
        """Stop the Ollama process if running"""
        if self.ollama_process:
            try:
                logger.info(f"[ID:0245] Stopping Ollama app.exe process (PID: {self.ollama_process.pid})")
                
                # Try graceful termination first
                self.ollama_process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.ollama_process.wait(timeout=10)  # Increased timeout for GUI app
                    logger.info("[ID:0245A] Ollama app.exe process terminated gracefully")
                except subprocess.TimeoutExpired:
                    logger.warning("[ID:0246] Ollama app.exe process did not terminate gracefully, force killing")
                    self.ollama_process.kill()
                    try:
                        self.ollama_process.wait(timeout=5)
                        logger.info("[ID:0246A] Ollama app.exe process force killed successfully")
                    except subprocess.TimeoutExpired:
                        logger.error("[ID:0246B] Failed to force kill Ollama app.exe process")
                except Exception as e:
                    logger.error(f"[ID:0247A] Error during graceful termination: {e}")
                    # Try force kill as fallback
                    try:
                        self.ollama_process.kill()
                        self.ollama_process.wait(timeout=5)
                        logger.info("[ID:0247B] Ollama app.exe process force killed after graceful failure")
                    except Exception as kill_error:
                        logger.error(f"[ID:0247C] Failed to force kill Ollama app.exe process: {kill_error}")
                        
            except Exception as e:
                logger.error(f"[ID:0247] Error stopping Ollama app.exe process: {e}")
            finally:
                self.ollama_process = None
                logger.info("[ID:0248] Ollama app.exe process cleanup completed")
    
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
            logger.debug("[ID:0256C] Ollama crash detection check called")
            
            # Only check if we started Ollama ourselves
            if not self.ollama_process:
                logger.debug("[ID:0256A] No Ollama process to monitor")
                return
            
            # Check if the process is still alive
            process_status = self.ollama_process.poll()
            if process_status is not None:
                logger.warning(f"[ID:0257] Ollama process crashed (PID: {self.ollama_process.pid}, Exit code: {process_status})")
                
                # Try to get any output from the crashed process
                try:
                    if self.ollama_process.stdout:
                        output = self.ollama_process.stdout.read()
                        if output:
                            logger.error(f"[ID:0257A] Ollama process output before crash: {output}")
                except Exception as e:
                    logger.debug(f"[ID:0257B] Could not read Ollama process output: {e}")
                
                # Check if we can still connect to Ollama
                connection_ok = self.check_ollama_connection()
                logger.info(f"[ID:0258] Ollama connection check result: {connection_ok}")
                
                if not connection_ok:
                    logger.error("[ID:0258A] Ollama connection lost, attempting restart")
                    
                    if self.ollama_restart_attempts < self.max_restart_attempts:
                        self.ollama_restart_attempts += 1
                        logger.info(f"[ID:0259] Attempting to restart Ollama (attempt {self.ollama_restart_attempts}/{self.max_restart_attempts})")
                        
                        # Stop the crashed process
                        self._stop_ollama_process()
                        
                        # Wait a moment before restarting
                        time.sleep(2)
                        
                        # Restart Ollama
                        if self._start_ollama_background():
                            logger.info("[ID:0260] Ollama restarted successfully after crash")
                            self.ollama_restart_attempts = 0  # Reset counter on success
                        else:
                            logger.error(f"[ID:0261] Failed to restart Ollama (attempt {self.ollama_restart_attempts})")
                    else:
                        logger.error(f"[ID:0262] Maximum restart attempts ({self.max_restart_attempts}) reached, stopping auto-restart")
                        self.show_ollama_connection_error("crash", force_show=True)
                else:
                    logger.info("[ID:0258B] Ollama connection is still working despite process crash")
                    
        except Exception as e:
            logger.error(f"[ID:0263] Error in Ollama crash detection: {e}")
            logger.error(f"[ID:0263A] Crash detection traceback: {traceback.format_exc()}")
    
    def _reset_ollama_restart_attempts(self):
        """Reset the restart attempts counter (called on successful connection)"""
        self.ollama_restart_attempts = 0
    
    def set_close_ollama_on_exit(self, enabled: bool):
        """Set whether to close Ollama when the application exits"""
        self.service_manager.config_manager.set("close_ollama_on_exit", enabled)
        logger.info(f"[ID:CLOSE_ON_EXIT] Set close_ollama_on_exit to: {enabled}")
    
    def get_close_ollama_on_exit(self) -> bool:
        """Get whether to close Ollama when the application exits"""
        return self.service_manager.config_manager.get("close_ollama_on_exit", True)
    
    def force_close_ollama(self):
        """Force close Ollama immediately (for manual control)"""
        logger.info("[ID:FORCE_CLOSE] User requested to force close Ollama app.exe")
        self._stop_ollama_process()
    
    def was_ollama_started_by_app(self) -> bool:
        """Check if Ollama was started by this application"""
        return self.ollama_started_by_app
    
    def get_ollama_status_info(self) -> dict:
        """Get comprehensive information about Ollama status"""
        info = {
            "running": self.is_ollama_running(),
            "started_by_app": self.ollama_started_by_app,
            "close_on_exit": self.get_close_ollama_on_exit(),
            "process_info": self.get_ollama_process_info()
        }
        
        if self.ollama_process:
            info["pid"] = self.ollama_process.pid
            info["alive"] = self.ollama_process.poll() is None
        else:
            info["pid"] = None
            info["alive"] = False
            
        return info
    
    def _show_custom_path_dialog(self, context="not_installed"):
        """Show dialog to let user specify custom Ollama path"""
        try:
            from PySide6.QtWidgets import QFileDialog, QInputDialog
            
            # Get current custom path from config
            current_path = self.service_manager.config_manager.get("custom_ollama_path", "")
            
            # Show file dialog to select Ollama executable
            file_path, _ = QFileDialog.getOpenFileName(
                self.main_window,
                "Select Ollama app.exe",
                current_path if current_path else "",
                "Executable files (*.exe);;All files (*.*)"
            )
            
            if file_path:
                # Validate the selected file
                if self._validate_ollama_executable(file_path):
                    # Save the custom path
                    self.service_manager.config_manager.set("custom_ollama_path", file_path)
                    self.service_manager.config_manager.save_config()
                    
                    logger.info(f"[ID:CUSTOM_PATH_SAVED] Custom Ollama path saved: {file_path}")
                    
                    # Show success message
                    success_msg = QMessageBox(self.main_window)
                    success_msg.setWindowTitle("Path Saved")
                    success_msg.setIcon(QMessageBox.Information)
                    success_msg.setText("Custom Ollama path saved successfully!")
                    success_msg.setInformativeText(f"Path: {file_path}\n\nThe application will now use this path to start Ollama.")
                    success_msg.exec()
                    
                    # Try to start Ollama with the new path
                    logger.info("[ID:CUSTOM_PATH_START] Attempting to start Ollama with custom path")
                    if self._start_ollama_background():
                        logger.info("[ID:CUSTOM_PATH_SUCCESS] Ollama started successfully with custom path")
                    else:
                        logger.warning("[ID:CUSTOM_PATH_FAIL] Failed to start Ollama with custom path")
                else:
                    # Show error for invalid executable
                    error_msg = QMessageBox(self.main_window)
                    error_msg.setWindowTitle("Invalid Executable")
                    error_msg.setIcon(QMessageBox.Warning)
                    error_msg.setText("The selected file is not a valid Ollama executable.")
                    error_msg.setInformativeText("Please select the correct 'ollama app.exe' file.")
                    error_msg.exec()
                    # Re-show the error dialog after invalid selection
                    self.show_ollama_connection_error(context, force_show=True)
            else:
                logger.info("[ID:CUSTOM_PATH_CANCELLED] User cancelled custom path selection")
                # Re-show the error dialog after cancel
                self.show_ollama_connection_error(context, force_show=True)
        except Exception as e:
            logger.error(f"[ID:CUSTOM_PATH_ERROR] Error showing custom path dialog: {e}")
            error_msg = QMessageBox(self.main_window)
            error_msg.setWindowTitle("Error")
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setText("Error showing custom path dialog.")
            error_msg.setInformativeText(str(e))
            error_msg.exec()
            # Re-show the error dialog after error
            self.show_ollama_connection_error(context, force_show=True)
    
    def _validate_ollama_executable(self, file_path: str) -> bool:
        """Validate that the selected file is a valid Ollama executable"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                logger.warning(f"[ID:VALIDATE_PATH] File does not exist: {file_path}")
                return False
            
            # Check if it's an executable
            if not os.access(file_path, os.X_OK):
                logger.warning(f"[ID:VALIDATE_PATH] File is not executable: {file_path}")
                return False
            
            # Check if filename contains 'ollama' (case insensitive)
            filename = os.path.basename(file_path).lower()
            if 'ollama' not in filename:
                logger.warning(f"[ID:VALIDATE_PATH] Filename does not contain 'ollama': {filename}")
                return False
            
            # Try to get file size (should be reasonable for an executable)
            file_size = os.path.getsize(file_path)
            if file_size < 1000000:  # Less than 1MB
                logger.warning(f"[ID:VALIDATE_PATH] File seems too small for an executable: {file_size} bytes")
                return False
            
            logger.info(f"[ID:VALIDATE_PATH] Valid Ollama executable found: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"[ID:VALIDATE_PATH] Error validating executable: {e}")
            return False
    
    def set_custom_ollama_path(self, path: str):
        """Set a custom path for Ollama executable"""
        if self._validate_ollama_executable(path):
            self.service_manager.config_manager.set("custom_ollama_path", path)
            self.service_manager.config_manager.save_config()
            logger.info(f"[ID:SET_CUSTOM_PATH] Custom Ollama path set: {path}")
            return True
        else:
            logger.warning(f"[ID:SET_CUSTOM_PATH] Invalid Ollama path: {path}")
            return False
    
    def get_custom_ollama_path(self) -> str:
        """Get the custom Ollama path from config"""
        return self.service_manager.config_manager.get("custom_ollama_path", "")
    
    def clear_custom_ollama_path(self):
        """Clear the custom Ollama path and revert to auto-detection"""
        self.service_manager.config_manager.set("custom_ollama_path", "")
        self.service_manager.config_manager.save_config()
        logger.info("[ID:CLEAR_CUSTOM_PATH] Custom Ollama path cleared, reverting to auto-detection")
    
    def get_ollama_path_info(self) -> dict:
        """Get information about Ollama path detection"""
        custom_path = self.get_custom_ollama_path()
        auto_detected_path = self._find_ollama_executable()
        
        info = {
            "custom_path": custom_path,
            "custom_path_exists": os.path.exists(custom_path) if custom_path else False,
            "auto_detected_path": auto_detected_path,
            "auto_detected_exists": os.path.exists(auto_detected_path) if auto_detected_path else False,
            "using_custom_path": bool(custom_path and os.path.exists(custom_path))
        }
        
        return info 