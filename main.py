# Shared imports
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.shared_imports.pyside_imports import *


from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.app.main import OllamaChat
from pyside_chat.core.threading import get_global_threading_service, shutdown_global_threading_service
from pyside_chat.core.threading import get_global_persistent_thread_pool, shutdown_global_persistent_thread_pool
from pyside_chat.startup.dependency_checker import check_and_install_dependencies

logger = CustomLogger.get_logger(__name__)

def configure_logging():
    """Configure logging for the application, including disabling specific modules."""
    try:
        logger.info("[ID:LOGGING_CONFIG] Configuring application logging...", print_to_terminal=True)
        
        # Try to read logging configuration from config.json
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        disabled_modules = []
        enabled_modules = []
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Get logging configuration from config file
            logging_config = config.get("logging_config", {})
            disabled_modules = logging_config.get("disabled_modules", [])
            enabled_modules = logging_config.get("enabled_modules", [])
            
            logger.info(f"[ID:LOGGING_CONFIG] Loaded logging config from {config_path}")
            
        except Exception as e:
            logger.warning(f"[ID:LOGGING_CONFIG] Could not load logging config from {config_path}: {e}")
            # Fallback to hardcoded list
            disabled_modules = [
                # Voice-related modules (often verbose)
                "pyside_chat.features.voice.voice_service",
                "pyside_chat.features.voice.tts.coqui_tts_service",
                "pyside_chat.features.voice.tts.streaming_audio_player",
                "pyside_chat.features.voice.tts.streaming_audio_worker",
                "pyside_chat.features.voice.audio.recording_service",
                "pyside_chat.features.voice.stt.stt_service",
                
                # UI components that are very verbose
                "pyside_chat.ui.tabs.chat_tab.voice_controls",
                "pyside_chat.ui.tabs.chat_tab.chat_display",
                "pyside_chat.ui.tabs.chat_tab.chat_renderer",
                "pyside_chat.ui.tabs.chat_tab.input_controls",
                
                # Threading and background services
                "pyside_chat.core.threading.thread_monitor",
                "pyside_chat.core.threading.persistent_thread_pool",
                "pyside_chat.core.threading.qthread_workers",
                "pyside_chat.core.threading.thread_calculator",
                
                # Memory and search services
                "pyside_chat.features.memory.semantic_search",
                "pyside_chat.features.memory.memory_service",
                
                # Enhancement and conversation services
                "pyside_chat.features.chat.conversation_service",
                "pyside_chat.features.chat.enhancers.enhancement_service",
                
                # Event bus and app lifecycle
                "pyside_chat.app.event_bus",
                "pyside_chat.app.app_lifecycle",
            ]
        
        # Disable logging for specified modules
        for module in disabled_modules:
            CustomLogger.disable_logging_for_module(module)
            logger.debug(f"[ID:LOGGING_CONFIG] Disabled logging for module: {module}")
        
        # Enable logging for specified modules (overrides disabled list)
        for module in enabled_modules:
            CustomLogger.enable_logging_for_module(module)
            logger.debug(f"[ID:LOGGING_CONFIG] Enabled logging for module: {module}")
        
        logger.info(f"[ID:LOGGING_CONFIG] Disabled logging for {len(disabled_modules)} modules, enabled for {len(enabled_modules)} modules", print_to_terminal=True)
        
    except Exception as e:
        logger.error(f"[ID:LOGGING_CONFIG] Error configuring logging: {e}")
        logger.error(traceback.format_exc())

def parse_arguments():
    """Parse command line arguments."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ollama Chat Application")
    parser.add_argument("--skip-deps", action="store_true", 
                       help="Skip dependency checking")
    parser.add_argument("--no-auto-install", action="store_true",
                       help="Don't automatically install missing dependencies")
    
    return parser.parse_args()

def main_check_dependencies(auto_install=True):
    """Check if all required dependencies are available."""
    try:
        logger.info("[ID:0280] 🔍 Checking dependencies...", print_to_terminal=True)
        
        # Use the dependency checker from startup module
        result = check_and_install_dependencies(auto_install=auto_install)
        
        if result:
            logger.info("[ID:0281] ✅ All dependencies are available", print_to_terminal=True)
        else:
            logger.error("[ID:0282] ❌ Missing dependencies detected", print_to_terminal=True)
        
        return result
        
    except Exception as e:
        logger.error(f"[ID:0279] Error checking dependencies: {str(e)}")
        logger.error(traceback.format_exc())
        logger.info(f"[ID:0278] ❌ Error checking dependencies: {str(e)}")
        return False

def initialize_persistent_threading_system():
    """Initialize the persistent threading system for the application."""
    try:
        logger.info("[DEBUG] Initializing persistent threading system...", print_to_terminal=True)
        
        # Initialize the global threading service (includes persistent thread pools)
        threading_service = get_global_threading_service()
        
        # Initialize the global persistent thread pool
        persistent_pool = get_global_persistent_thread_pool()
        
        logger.info("[DEBUG] Persistent threading system initialized successfully", print_to_terminal=True)
        return threading_service, persistent_pool
        
    except Exception as e:
        logger.error(f"[DEBUG] Error initializing persistent threading system: {e}")
        logger.error(traceback.format_exc())
        return None, None

def cleanup_persistent_threading_system():
    """Clean up the persistent threading system."""
    try:
        logger.info("[DEBUG] Cleaning up persistent threading system...", print_to_terminal=True)
        
        # Shutdown the global threading service
        shutdown_global_threading_service()
        
        # Shutdown the global persistent thread pool
        shutdown_global_persistent_thread_pool()
        
        logger.info("[DEBUG] Persistent threading system cleanup completed", print_to_terminal=True)
        
    except Exception as e:
        logger.error(f"[DEBUG] Error cleaning up persistent threading system: {e}")
        logger.error(traceback.format_exc())

def main():
    try:
        # Parse command line arguments
        try:
            args = parse_arguments()
        except Exception as e:
            logger.error(f"[ID:PARSE_ARGS_MAIN] Exception in parse_arguments: {e}")
            logger.error(traceback.format_exc())
            raise

        # Configure logging for the application
        try:
            configure_logging()
        except Exception as e:
            logger.error(f"[ID:LOGGING_CONFIG_MAIN] Exception configuring logging: {e}")
            logger.error(traceback.format_exc())
            # Don't raise here - logging is not critical for app startup

        # Check dependencies before starting the application (unless skipped)
        try:
            if not args.skip_deps:
                logger.info("[ID:0277] 🔍 Checking dependencies...", print_to_terminal=True)
                if not main_check_dependencies(auto_install=not args.no_auto_install):
                    logger.error("[ID:0276] ❌ Cannot start application due to missing dependencies.")
                    sys.exit(1)
            else:
                logger.error("[ID:0275] ⚠️  Skipping dependency check (--skip-deps flag used)")
        except Exception as e:
            logger.error(f"[ID:CHECK_DEPS_MAIN] Exception during dependency check: {e}")
            logger.error(traceback.format_exc())
            raise

        try:
            logger.info("[ID:0274] 🚀 Starting QApplication...",print_to_terminal=True)
            app = QApplication(sys.argv)
            logger.info("[ID:0273] Application started",print_to_terminal=True)
        except Exception as e:
            logger.error(f"[ID:QAPP_MAIN] Exception starting QApplication: {e}")
            logger.error(traceback.format_exc())
            raise

        # Initialize persistent threading system
        try:
            threading_service, persistent_pool = initialize_persistent_threading_system()
            if not threading_service or not persistent_pool:
                logger.error("[ID:THREAD_INIT_MAIN] Failed to initialize persistent threading system")
                raise RuntimeError("Failed to initialize persistent threading system")
        except Exception as e:
            logger.error(f"[ID:THREAD_INIT_MAIN] Exception initializing persistent threading system: {e}")
            logger.error(traceback.format_exc())
            raise

        # Set application properties
        try:
            app.setApplicationName("Ollama Chat - Local LLM Chat Application")
            app.setApplicationVersion("0.4.0")
        except Exception as e:
            logger.error(f"[ID:QAPP_PROPS_MAIN] Exception setting app properties: {e}")
            logger.error(traceback.format_exc())
            raise

        logger.info("[ID:0272] 🏗️  Creating main window...",print_to_terminal=True)
        # Create the main window (but don't show it yet)
        try:
            window = OllamaChat()
            logger.info("[ID:0271] 📱 Main window created successfully")
            
            # Check if initialization was successful (Ollama verification)
            if window.lifecycle_manager.initialization_complete:
                logger.info("[ID:0271A] 📱 Ollama verification successful - showing main window...")
                window.show()
            else:
                logger.info("[ID:0271B] 📱 Ollama verification failed - main window will be shown after verification")
                # The window will be shown later when Ollama verification succeeds
                
        except Exception as e:
            logger.error(f"[ID:WINDOW_MAIN] Exception creating main window: {e}")
            logger.error(traceback.format_exc())
            raise
        
        # Connect window close signal to cleanup
        def on_window_closed():
            try:
                logger.info("[DEBUG] Window closed, cleaning up...", print_to_terminal=True)
                
                # Get the EventBus from the window and clean it up
                try:
                    event_handler = window.get_event_handler()
                    if event_handler:
                        logger.info("[DEBUG] Cleaning up EventBus on window close...", print_to_terminal=True)
                        event_handler.cleanup_on_exit()
                except Exception as e_inner:
                    logger.error(f"[DEBUG] Error during window close cleanup (event_handler): {e_inner}")
                    logger.error(traceback.format_exc())
                
            except Exception as e:
                logger.error(f"[DEBUG] Error during window close cleanup: {e}")
                logger.error(traceback.format_exc())
        
        # Connect the window's destroyed signal to cleanup
        try:
            window.destroyed.connect(on_window_closed)
        except Exception as e:
            logger.error(f"[ID:CONNECT_DESTROYED] Exception connecting destroyed signal: {e}")
            logger.error(traceback.format_exc())
        
        # Connect the application's aboutToQuit signal to ensure cleanup
        def cleanup_on_exit():
            try:
                logger.info("[DEBUG] Application about to quit, cleaning up...", print_to_terminal=True)
                
                # Clean up the main window and EventBus
                try:
                    if window:
                        # Get the EventBus from the window and clean it up
                        try:
                            event_handler = window.get_event_handler()
                            if event_handler:
                                logger.info("[DEBUG] Cleaning up EventBus...", print_to_terminal=True)
                                event_handler.cleanup_on_exit()
                        except Exception as e_inner:
                            logger.error(f"[DEBUG] Error cleaning up EventBus in aboutToQuit: {e_inner}")
                            logger.error(traceback.format_exc())
                        
                        # Close the window
                        try:
                            window.close()
                        except Exception as e_inner2:
                            logger.error(f"[DEBUG] Error closing window in aboutToQuit: {e_inner2}")
                            logger.error(traceback.format_exc())
                except Exception as e_mid:
                    logger.error(f"[DEBUG] Error in main window/EventBus cleanup in aboutToQuit: {e_mid}")
                    logger.error(traceback.format_exc())
                
                # Clean up persistent threading system
                try:
                    cleanup_persistent_threading_system()
                except Exception as e_inner3:
                    logger.error(f"[DEBUG] Error cleaning up persistent threading system in aboutToQuit: {e_inner3}")
                    logger.error(traceback.format_exc())
                
                logger.info("[DEBUG] Application cleanup completed", print_to_terminal=True)
                
            except Exception as e:
                logger.error(f"[DEBUG] Error during application cleanup: {e}")
                logger.error(traceback.format_exc())
        
        try:
            app.aboutToQuit.connect(cleanup_on_exit)
        except Exception as e:
            logger.error(f"[ID:CONNECT_ABOUTTOQUIT] Exception connecting aboutToQuit: {e}")
            logger.error(traceback.format_exc())
        
        logger.info("[ID:0270] 🔄 Starting application event loop...",print_to_terminal=True)
        # Start the application event loop
        try:
            result = app.exec()
            logger.info(f"[ID:0269] 👋 QApplication event loop exited with code: {result}",print_to_terminal=True)
            return result
        except Exception as e:
            logger.error(f"[ID:APP_EXEC] Exception in app.exec(): {e}")
            logger.error(traceback.format_exc())
            # Ensure cleanup even on error
            cleanup_persistent_threading_system()
            raise
        
    except Exception as e:
        logger.error(f"[ID:0268] Error in main: {str(e)}",print_to_terminal=True)
        logger.error(traceback.format_exc())
        
        # Ensure cleanup even on error
        try:
            cleanup_persistent_threading_system()
        except Exception as e_cleanup:
            logger.error(f"[ID:0268CLEANUP] Error during cleanup in main: {e_cleanup}")
            logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("[DEBUG] Application interrupted by user", print_to_terminal=True)
        sys.exit(0)
    except Exception as e:
        logger.error(f"[DEBUG] Unhandled exception in main: {e}", print_to_terminal=True)
        logger.error(traceback.format_exc())
        sys.exit(1)
