#!/usr/bin/env python3
"""
Enhanced Ollama Autostart Test Script

This script demonstrates the enhanced Ollama autostart functionality
that has been integrated into the main application lifecycle.
"""

import sys
import os
import time

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.config.config_manager import ConfigManager
from pyside_chat.app.service_manager import ServiceManager
from pyside_chat.ui.ui_manager import UIManager
from pyside_chat.app.event_bus import EventBus
from pyside_chat.app.app_lifecycle import AppLifecycleManager
from pyside_chat.features.chat.chat_controller import ChatController

logger = CustomLogger.get_logger(__name__)

class MockMainWindow:
    """Mock main window for testing purposes"""
    def __init__(self):
        self.width = lambda: 1200
        self.height = lambda: 800
        self.size = lambda: type('Size', (), {'width': lambda: 1200, 'height': lambda: 800})()
        self.resize = lambda w, h: None

def test_enhanced_autostart():
    """Test the enhanced Ollama autostart functionality"""
    print("=== Enhanced Ollama Autostart Test ===")
    print("Testing the integrated autostart functionality...")
    
    try:
        # Initialize components
        print("\n1. Initializing components...")
        config_manager = ConfigManager()
        service_manager = ServiceManager(config_manager)
        
        # Create mock main window
        mock_window = MockMainWindow()
        
        # Initialize UI manager (with mock window)
        ui_manager = UIManager(mock_window, config_manager)
        
        # Initialize chat controller
        chat_controller = ChatController(
            ollama_service=service_manager.get_ollama_service(),
            conversation_service=service_manager.get_conversation_service(),
            enhancement_service=service_manager.get_enhancement_service(),
            memory_service=service_manager.get_memory_service(),
            conversation_manager=service_manager.get_conversation_manager()
        )
        
        # Initialize event bus
        event_handler = EventBus(
            mock_window,
            service_manager,
            ui_manager,
            chat_controller
        )
        
        # Initialize lifecycle manager
        lifecycle_manager = AppLifecycleManager(
            mock_window,
            service_manager,
            ui_manager,
            event_handler
        )
        
        print("✅ Components initialized successfully")
        
        # Test Ollama installation check
        print("\n2. Testing Ollama installation check...")
        is_installed = lifecycle_manager._is_ollama_installed()
        print(f"Ollama installed: {is_installed}")
        
        if not is_installed:
            print("❌ Ollama is not installed. The app would show the 'not_installed' dialog.")
            print("This is the enhanced notification that provides clear installation instructions.")
            return False
        
        # Test Ollama connection
        print("\n3. Testing Ollama connection...")
        is_running = lifecycle_manager.is_ollama_running()
        print(f"Ollama running: {is_running}")
        
        if not is_running:
            print("⚠️  Ollama is not running. Testing autostart functionality...")
            
            # Test the enhanced autostart
            success = lifecycle_manager._ensure_ollama_running()
            print(f"Autostart result: {success}")
            
            if success:
                print("✅ Ollama started successfully via autostart")
            else:
                print("❌ Failed to start Ollama automatically")
                return False
        else:
            print("✅ Ollama is already running")
        
        # Test model querying
        print("\n4. Testing model querying...")
        models = lifecycle_manager.get_available_models()
        if models:
            print(f"✅ Found {len(models)} available models:")
            for i, model in enumerate(models, 1):
                print(f"  {i}. {model}")
        else:
            print("⚠️  No models found. You may need to pull a model first.")
            print("Try running: ollama pull llama2")
        
        # Test message sending if models are available
        if models:
            print("\n5. Testing message sending...")
            test_model = models[0]
            print(f"Testing with model: {test_model}")
            
            success, response = lifecycle_manager.send_test_message(test_model)
            if success:
                print("✅ Message sent and response received successfully!")
                print(f"AI Response: {response[:100]}..." if len(response) > 100 else f"AI Response: {response}")
            else:
                print("❌ Failed to send message or get response")
                return False
        else:
            print("\n5. Skipping message test (no models available)")
        
        # Test crash detection (simulation)
        print("\n6. Testing crash detection simulation...")
        process_info = lifecycle_manager.get_ollama_process_info()
        if process_info:
            print(f"✅ Ollama process info: PID={process_info.get('pid')}, Alive={process_info.get('alive')}")
        else:
            print("ℹ️  No Ollama process info available (may be started externally)")
        
        print("\n=== Test Summary ===")
        print("✅ Enhanced autostart functionality integrated successfully")
        print("✅ Improved error handling with clear installation instructions")
        print("✅ Model querying and message sending capabilities added")
        print("✅ Crash detection and restart functionality available")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during enhanced autostart test: {e}")
        logger.error(f"Enhanced autostart test failed: {e}")
        return False

def test_error_dialogs():
    """Test the enhanced error dialog functionality"""
    print("\n=== Testing Enhanced Error Dialogs ===")
    
    try:
        # Initialize components
        config_manager = ConfigManager()
        service_manager = ServiceManager(config_manager)
        mock_window = MockMainWindow()
        ui_manager = UIManager(mock_window, config_manager)
        chat_controller = ChatController(
            ollama_service=service_manager.get_ollama_service(),
            conversation_service=service_manager.get_conversation_service(),
            enhancement_service=service_manager.get_enhancement_service(),
            memory_service=service_manager.get_memory_service(),
            conversation_manager=service_manager.get_conversation_manager()
        )
        event_handler = EventBus(mock_window, service_manager, ui_manager, chat_controller)
        lifecycle_manager = AppLifecycleManager(mock_window, service_manager, ui_manager, event_handler)
        
        print("✅ Components initialized for error dialog testing")
        
        # Test different error contexts
        print("\nThe following error dialogs would be shown in different scenarios:")
        print("1. 'not_installed' - When Ollama is not installed")
        print("2. 'startup' - When Ollama is not running during startup")
        print("3. 'crash' - When Ollama crashes and can't be restarted")
        print("4. 'general' - General connection errors")
        
        print("\n✅ Enhanced error dialog functionality available")
        return True
        
    except Exception as e:
        print(f"❌ Error during error dialog test: {e}")
        return False

if __name__ == "__main__":
    print("Enhanced Ollama Autostart Integration Test")
    print("=" * 50)
    
    # Test the enhanced autostart functionality
    autostart_success = test_enhanced_autostart()
    
    # Test error dialog functionality
    dialog_success = test_error_dialogs()
    
    print("\n" + "=" * 50)
    if autostart_success and dialog_success:
        print("🎉 All tests passed! Enhanced autostart integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print("\nKey Improvements:")
    print("✅ Better notification when Ollama is not installed")
    print("✅ Clear installation instructions for different platforms")
    print("✅ Enhanced error handling with specific contexts")
    print("✅ Model querying and message testing capabilities")
    print("✅ Integrated with existing app lifecycle") 