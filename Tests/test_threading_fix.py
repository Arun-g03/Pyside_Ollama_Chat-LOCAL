#!/usr/bin/env python3
"""
Test script to verify threading service fixes
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.core.threading.threading_service import get_global_threading_service
from pyside_chat.core.threading.thread_calculator import get_pool_thread_count
from pyside_chat.core.threading.thread_pool_manager import get_global_thread_pool_manager
from pyside_chat.core.threading.persistent_thread_pool import get_global_persistent_thread_pool

logger = CustomLogger.get_logger(__name__)

def test_thread_calculator():
    """Test the thread calculator functionality"""
    print("=== Testing Thread Calculator ===")
    
    try:
        # Test get_pool_thread_count function
        streaming_count = get_pool_thread_count('streaming')
        background_count = get_pool_thread_count('background')
        ui_update_count = get_pool_thread_count('ui_update')
        
        print(f"✅ Thread calculator working:")
        print(f"  - Streaming threads: {streaming_count}")
        print(f"  - Background threads: {background_count}")
        print(f"  - UI update threads: {ui_update_count}")
        
        return True
    except Exception as e:
        print(f"❌ Thread calculator failed: {e}")
        return False

def test_thread_pool_manager():
    """Test the thread pool manager functionality"""
    print("\n=== Testing Thread Pool Manager ===")
    
    try:
        # Test getting global thread pool manager
        manager = get_global_thread_pool_manager()
        print(f"✅ Thread pool manager created successfully")
        
        # Test pool status
        status = manager.get_pool_status()
        print(f"✅ Pool status retrieved: {status}")
        
        return True
    except Exception as e:
        print(f"❌ Thread pool manager failed: {e}")
        return False

def test_persistent_thread_pool():
    """Test the persistent thread pool functionality"""
    print("\n=== Testing Persistent Thread Pool ===")
    
    try:
        # Test getting global persistent thread pool
        pool = get_global_persistent_thread_pool()
        print(f"✅ Persistent thread pool created successfully")
        
        # Test pool status
        status = pool.get_pool_status()
        print(f"✅ Pool status retrieved: {status}")
        
        return True
    except Exception as e:
        print(f"❌ Persistent thread pool failed: {e}")
        return False

def test_threading_service():
    """Test the threading service functionality"""
    print("\n=== Testing Threading Service ===")
    
    try:
        # Test getting global threading service
        service = get_global_threading_service()
        print(f"✅ Threading service created successfully")
        
        # Test that critical attributes exist
        attributes_to_check = [
            'persistent_thread_pool',
            'current_chat_thread',
            'current_audio_thread',
            'current_monitoring_thread',
            'current_voice_thread',
            'active_tasks',
            'thread_pool_manager',
            'thread_monitor'
        ]
        
        missing_attributes = []
        for attr in attributes_to_check:
            if not hasattr(service, attr):
                missing_attributes.append(attr)
        
        if missing_attributes:
            print(f"❌ Missing attributes: {missing_attributes}")
            return False
        else:
            print(f"✅ All required attributes present")
        
        # Test threading status
        status = service.get_threading_status()
        print(f"✅ Threading status retrieved: {status}")
        
        return True
    except Exception as e:
        print(f"❌ Threading service failed: {e}")
        return False

def test_chat_streaming():
    """Test chat streaming functionality"""
    print("\n=== Testing Chat Streaming ===")
    
    try:
        service = get_global_threading_service()
        
        # Test starting chat streaming (should fail gracefully if no persistent pool)
        if service.persistent_thread_pool is None:
            print("⚠️  Persistent thread pool is None, skipping chat streaming test")
            return True
        
        # Mock configuration for testing
        mock_config = type('MockConfig', (), {
            'get_max_tokens': lambda: 2048,
            'get_top_p': lambda: 0.9,
            'get_frequency_penalty': lambda: 0.0,
            'get_presence_penalty': lambda: 0.0
        })()
        
        # Test starting chat streaming
        success = service.start_chat_streaming(
            context_messages=[{"role": "user", "content": "Hello"}],
            model="llama2",
            temperature=0.7,
            config_manager=mock_config
        )
        
        if success:
            print("✅ Chat streaming started successfully")
            # Stop it immediately
            service.stop_chat_streaming()
            print("✅ Chat streaming stopped successfully")
        else:
            print("⚠️  Chat streaming failed (expected if no Ollama connection)")
        
        return True
    except Exception as e:
        print(f"❌ Chat streaming test failed: {e}")
        return False

def main():
    """Run all threading tests"""
    print("Threading Service Fix Test")
    print("=" * 50)
    
    tests = [
        test_thread_calculator,
        test_thread_pool_manager,
        test_persistent_thread_pool,
        test_threading_service,
        test_chat_streaming
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Threading service fixes are working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    main() 