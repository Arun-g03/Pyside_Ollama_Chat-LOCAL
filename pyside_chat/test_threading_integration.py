#!/usr/bin/env python3
"""
Test script for threading integration.

This script tests the integration of the new QThread/QRunnable architecture
with the existing chat system.
"""

import sys
import os
import time
from typing import Dict, List, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyside_chat.core.threading import (
    get_global_threading_service,
    get_global_thread_pool_manager,
    get_global_thread_monitor,
    MessageProcessingTask,
    FileProcessingTask
)
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class MockEventBus:
    """Mock Event Bus for testing."""
    
    def __init__(self):
        self.service_manager = MockServiceManager()
        self.message_processed = False
        self.processing_error = None
    
    def on_message_processed(self, task_type: str, result: Dict[str, Any]):
        """Handle message processing completion."""
        logger.info(f"Message processing completed: {task_type}")
        logger.info(f"Result: {result}")
        self.message_processed = True
    
    def on_message_processing_error(self, task_type: str, error_message: str):
        """Handle message processing error."""
        logger.error(f"Message processing error ({task_type}): {error_message}")
        self.processing_error = error_message


class MockServiceManager:
    """Mock service manager for testing."""
    
    def __init__(self):
        self.config_manager = MockConfigManager()


class MockConfigManager:
    """Mock config manager for testing."""
    
    def get_ollama_url(self):
        return "http://localhost:11434"
    
    def get_max_tokens(self):
        return 1000
    
    def get_top_p(self):
        return 0.9
    
    def get_frequency_penalty(self):
        return 0.0
    
    def get_presence_penalty(self):
        return 0.0


def test_threading_service():
    """Test the threading service functionality."""
    logger.info("=== Testing Threading Service ===")
    
    try:
        # Get global threading service
        threading_service = get_global_threading_service()
        logger.info("✓ Threading service initialized")
        
        # Test message processing
        test_message = "Hello, how are you doing today?"
        task_id = threading_service.process_message_spell_check(test_message)
        logger.info(f"✓ Spell check task started: {task_id}")
        
        # Wait for task completion
        thread_pool = get_global_thread_pool_manager()
        success = thread_pool.wait_for_task(task_id, timeout=10.0)
        
        if success:
            logger.info("✓ Spell check task completed successfully")
        else:
            logger.error("✗ Spell check task failed or timed out")
        
        # Test file processing
        test_file_path = "test_file.txt"
        with open(test_file_path, "w") as f:
            f.write("This is a test file for processing.")
        
        file_task_id = threading_service.process_file_operation(test_file_path, "read")
        logger.info(f"✓ File processing task started: {file_task_id}")
        
        # Wait for file task completion
        success = thread_pool.wait_for_task(file_task_id, timeout=10.0)
        
        if success:
            logger.info("✓ File processing task completed successfully")
        else:
            logger.error("✗ File processing task failed or timed out")
        
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
        
        # Get threading status
        status = threading_service.get_threading_status()
        logger.info(f"✓ Threading status: {status}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Threading service test failed: {e}")
        return False


def test_thread_pool_manager():
    """Test the thread pool manager functionality."""
    logger.info("=== Testing Thread Pool Manager ===")
    
    try:
        # Get global thread pool manager
        thread_pool = get_global_thread_pool_manager()
        logger.info("✓ Thread pool manager initialized")
        
        # Test pool status
        status = thread_pool.get_pool_status()
        logger.info(f"✓ Pool status: {status}")
        
        # Test task creation and execution
        mock_handler = MockEventBus()
        
        # Create a test task
        task = MessageProcessingTask("Test message", mock_handler, "spell_check")
        task_id = thread_pool.start_task(task)
        logger.info(f"✓ Test task started: {task_id}")
        
        # Wait for task completion
        success = thread_pool.wait_for_task(task_id, timeout=10.0)
        
        if success and mock_handler.message_processed:
            logger.info("✓ Test task completed successfully")
        else:
            logger.error("✗ Test task failed or timed out")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Thread pool manager test failed: {e}")
        return False


def test_thread_monitor():
    """Test the thread monitor functionality."""
    logger.info("=== Testing Thread Monitor ===")
    
    try:
        # Get global thread monitor
        monitor = get_global_thread_monitor()
        logger.info("✓ Thread monitor initialized")
        
        # Get monitoring status
        status = monitor.get_threading_status()
        logger.info(f"✓ Monitor status: {status}")
        
        # Get resource usage
        usage = monitor.get_resource_usage()
        logger.info(f"✓ Resource usage: {usage}")
        
        # Generate report
        report = monitor.generate_report()
        logger.info(f"✓ Monitor report: {report}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Thread monitor test failed: {e}")
        return False


def test_integration():
    """Test the complete integration."""
    logger.info("=== Testing Complete Integration ===")
    
    try:
        # Test all components together
        threading_service = get_global_threading_service()
        thread_pool = get_global_thread_pool_manager()
        monitor = get_global_thread_monitor()
        
        logger.info("✓ All threading components initialized")
        
        # Test multiple concurrent tasks
        mock_handler = MockEventBus()
        task_ids = []
        
        # Start multiple tasks
        for i in range(3):
            message = f"Test message {i+1}"
            task = MessageProcessingTask(message, mock_handler, "spell_check")
            task_id = thread_pool.start_task(task)
            task_ids.append(task_id)
            logger.info(f"✓ Started task {i+1}: {task_id}")
        
        # Wait for all tasks to complete
        success = thread_pool.wait_for_all_tasks(timeout=30.0)
        
        if success:
            logger.info("✓ All concurrent tasks completed successfully")
        else:
            logger.error("✗ Some concurrent tasks failed or timed out")
        
        # Get final status
        threading_status = threading_service.get_threading_status()
        pool_status = thread_pool.get_pool_status()
        monitor_status = monitor.get_threading_status()
        
        logger.info(f"✓ Final threading status: {threading_status}")
        logger.info(f"✓ Final pool status: {pool_status}")
        logger.info(f"✓ Final monitor status: {monitor_status}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Integration test failed: {e}")
        return False


def main():
    """Run all threading integration tests."""
    logger.info("Starting threading integration tests...")
    
    tests = [
        ("Threading Service", test_threading_service),
        ("Thread Pool Manager", test_thread_pool_manager),
        ("Thread Monitor", test_thread_monitor),
        ("Complete Integration", test_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running {test_name} Test")
        logger.info(f"{'='*50}")
        
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                logger.info(f"✓ {test_name} test PASSED")
            else:
                logger.error(f"✗ {test_name} test FAILED")
                
        except Exception as e:
            logger.error(f"✗ {test_name} test ERROR: {e}")
            results.append((test_name, False))
    
    # Print summary
    logger.info(f"\n{'='*50}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*50}")
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "PASSED" if success else "FAILED"
        logger.info(f"{test_name}: {status}")
        if success:
            passed += 1
    
    logger.info(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Threading integration is working correctly.")
        return 0
    else:
        logger.error("❌ Some tests failed. Please check the logs for details.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 