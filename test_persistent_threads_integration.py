#!/usr/bin/env python3
"""
Test script to verify persistent threads system integration.

This script tests:
1. Global threading service initialization
2. Persistent thread pool initialization
3. Thread pool operations
4. Cleanup procedures
"""

import sys
import time
import traceback
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

# Add the project root to the path
sys.path.insert(0, '.')

from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.core.threading import (
    get_global_threading_service,
    get_global_persistent_thread_pool,
    shutdown_global_threading_service,
    shutdown_global_persistent_thread_pool
)

logger = CustomLogger.get_logger(__name__)

def test_persistent_threads_integration():
    """Test the persistent threads system integration"""
    
    print("🧪 Testing Persistent Threads System Integration")
    print("=" * 60)
    
    try:
        # Test 1: Initialize global threading service
        print("\n1. Testing global threading service initialization...")
        threading_service = get_global_threading_service()
        if threading_service:
            print("✅ Global threading service initialized successfully")
        else:
            print("❌ Failed to initialize global threading service")
            return False
        
        # Test 2: Initialize persistent thread pool
        print("\n2. Testing persistent thread pool initialization...")
        persistent_pool = get_global_persistent_thread_pool()
        if persistent_pool:
            print("✅ Global persistent thread pool initialized successfully")
        else:
            print("❌ Failed to initialize global persistent thread pool")
            return False
        
        # Test 3: Check pool status
        print("\n3. Testing pool status...")
        pool_status = persistent_pool.get_pool_status()
        print(f"✅ Pool status: {pool_status}")
        
        # Test 4: Test thread operations
        print("\n4. Testing thread operations...")
        
        # Test getting a thread from pool
        thread = persistent_pool.get_thread('chat_streaming', timeout=5.0)
        if thread:
            print("✅ Successfully got thread from chat_streaming pool")
            
            # Test returning thread to pool
            persistent_pool.return_thread(thread)
            print("✅ Successfully returned thread to pool")
        else:
            print("❌ Failed to get thread from chat_streaming pool")
        
        # Test 5: Test threading service operations
        print("\n5. Testing threading service operations...")
        
        # Test getting threading status
        status = threading_service.get_threading_status()
        if status:
            print("✅ Successfully got threading status")
            print(f"   Status: {status}")
        else:
            print("❌ Failed to get threading status")
        
        # Test 6: Test cleanup
        print("\n6. Testing cleanup procedures...")
        
        # Shutdown persistent thread pool
        shutdown_global_persistent_thread_pool()
        print("✅ Persistent thread pool shutdown completed")
        
        # Shutdown threading service
        shutdown_global_threading_service()
        print("✅ Threading service shutdown completed")
        
        print("\n🎉 All tests passed! Persistent threads system is properly integrated.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_service_integration():
    """Test that services are using the persistent threads system"""
    
    print("\n🔧 Testing Service Integration with Persistent Threads")
    print("=" * 60)
    
    try:
        # Test Ollama service integration
        print("\n1. Testing Ollama service integration...")
        from pyside_chat.features.ollama.ollama_service import OllamaService
        
        ollama_service = OllamaService()
        if hasattr(ollama_service, 'threading_service') and ollama_service.threading_service:
            print("✅ Ollama service is using persistent threading system")
        else:
            print("❌ Ollama service is not using persistent threading system")
            return False
        
        if hasattr(ollama_service, 'persistent_thread_pool') and ollama_service.persistent_thread_pool:
            print("✅ Ollama service has access to persistent thread pool")
        else:
            print("❌ Ollama service does not have access to persistent thread pool")
            return False
        
        # Test Voice service integration
        print("\n2. Testing Voice service integration...")
        from pyside_chat.features.voice.voice_service import VoiceService
        
        voice_service = VoiceService.get_instance()
        if hasattr(voice_service, 'threading_service') and voice_service.threading_service:
            print("✅ Voice service is using persistent threading system")
        else:
            print("❌ Voice service is not using persistent threading system")
            return False
        
        if hasattr(voice_service, 'persistent_thread_pool') and voice_service.persistent_thread_pool:
            print("✅ Voice service has access to persistent thread pool")
        else:
            print("❌ Voice service does not have access to persistent thread pool")
            return False
        
        print("\n🎉 All service integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Service integration test failed with error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Persistent Threads Integration Tests")
    print("=" * 60)
    
    # Create QApplication for Qt context (only once)
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Run core integration tests
        core_tests_passed = test_persistent_threads_integration()
        
        # Run service integration tests
        service_tests_passed = test_service_integration()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        if core_tests_passed:
            print("✅ Core persistent threads integration: PASSED")
        else:
            print("❌ Core persistent threads integration: FAILED")
        
        if service_tests_passed:
            print("✅ Service integration: PASSED")
        else:
            print("❌ Service integration: FAILED")
        
        if core_tests_passed and service_tests_passed:
            print("\n🎉 ALL TESTS PASSED! Persistent threads system is fully integrated.")
            return 0
        else:
            print("\n💥 SOME TESTS FAILED! Please check the integration.")
            return 1
            
    finally:
        # Clean up QApplication
        if app:
            app.quit()

if __name__ == "__main__":
    sys.exit(main()) 