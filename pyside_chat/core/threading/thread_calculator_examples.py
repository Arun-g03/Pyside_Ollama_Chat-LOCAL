#!/usr/bin/env python3
"""
Examples of using the Thread Calculator with existing threading components
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from pyside_chat.core.threading import (
    get_thread_recommendations,
    get_pool_thread_count,
    thread_calculator,
    ThreadPoolManager,
    PersistentThreadPool
)

def example_thread_pool_manager():
    """Example: Using thread calculator with ThreadPoolManager"""
    print("=== ThreadPoolManager Example ===")
    
    # Get recommendations for different pool types
    worker_threads = get_pool_thread_count('worker')
    streaming_threads = get_pool_thread_count('streaming')
    memory_safe_threads = get_pool_thread_count('memory_safe')
    
    print(f"Recommended thread counts:")
    print(f"  Worker threads: {worker_threads}")
    print(f"  Streaming threads: {streaming_threads}")
    print(f"  Memory-safe threads: {memory_safe_threads}")
    
    # Create thread pool manager with calculated thread counts
    pool_manager = ThreadPoolManager(
        max_threads=worker_threads
    )
    print(f"Created ThreadPoolManager with {worker_threads} max threads")
    return pool_manager

def example_persistent_thread_pool():
    """Example: Using thread calculator with PersistentThreadPool"""
    print("\n=== PersistentThreadPool Example ===")
    
    # Get recommendations for persistent threads
    background_threads = get_pool_thread_count('background')
    ui_update_threads = get_pool_thread_count('ui_update')
    
    print(f"Recommended thread counts:")
    print(f"  Background threads: {background_threads}")
    print(f"  UI update threads: {ui_update_threads}")
    
    # Create persistent thread pool
    persistent_pool = PersistentThreadPool()
    print(f"Created PersistentThreadPool")
    
    # Example: Set pool sizes for different thread types
    # (Assume DummyWorker is a placeholder for a real worker class)
    class DummyWorker: pass
    persistent_pool.initialize_pool('chat_streaming', DummyWorker, size=background_threads)
    persistent_pool.initialize_pool('monitoring', DummyWorker, size=ui_update_threads)
    print(f"Initialized chat_streaming pool with {background_threads} threads")
    print(f"Initialized monitoring pool with {ui_update_threads} threads")
    return persistent_pool

def example_streaming_configuration():
    """Example: Using thread calculator for streaming configuration"""
    print("\n=== Streaming Configuration Example ===")
    
    recommendations = get_thread_recommendations()
    
    # Configure streaming-specific settings
    streaming_config = {
        'streaming_threads': recommendations.streaming_threads,
        'chunk_processing_threads': recommendations.chunk_processing_threads,
        'ui_update_threads': recommendations.ui_update_threads,
        'max_concurrent_streams': min(recommendations.streaming_threads, 3)
    }
    
    print(f"Streaming configuration:")
    for key, value in streaming_config.items():
        print(f"  {key}: {value}")
    
    return streaming_config

def example_memory_optimization():
    """Example: Using thread calculator for memory optimization"""
    print("\n=== Memory Optimization Example ===")
    
    recommendations = get_thread_recommendations()
    
    # Choose thread count based on available memory
    if recommendations.memory_gb < 8.0:
        # Low memory system
        thread_count = recommendations.conservative_threads
        print(f"Low memory system ({recommendations.memory_gb:.1f} GB), using conservative thread count: {thread_count}")
    elif recommendations.memory_gb < 16.0:
        # Medium memory system
        thread_count = recommendations.memory_safe_threads
        print(f"Medium memory system ({recommendations.memory_gb:.1f} GB), using memory-safe thread count: {thread_count}")
    else:
        # High memory system
        thread_count = recommendations.max_worker_threads
        print(f"High memory system ({recommendations.memory_gb:.1f} GB), using max thread count: {thread_count}")
    
    return thread_count

def example_dynamic_adjustment():
    """Example: Dynamically adjusting thread counts based on system load"""
    print("\n=== Dynamic Adjustment Example ===")
    
    import psutil
    
    # Get current system load
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    
    print(f"Current system load:")
    print(f"  CPU usage: {cpu_percent:.1f}%")
    print(f"  Memory usage: {memory_percent:.1f}%")
    
    # Adjust thread count based on system load
    base_threads = get_pool_thread_count('worker')
    
    if cpu_percent > 80 or memory_percent > 80:
        # High load - reduce threads
        adjusted_threads = max(2, base_threads // 2)
        print(f"High system load detected, reducing threads from {base_threads} to {adjusted_threads}")
    elif cpu_percent < 30 and memory_percent < 50:
        # Low load - can use more threads
        adjusted_threads = min(base_threads + 2, get_pool_thread_count('max'))
        print(f"Low system load detected, increasing threads from {base_threads} to {adjusted_threads}")
    else:
        # Normal load - use recommended threads
        adjusted_threads = base_threads
        print(f"Normal system load, using recommended threads: {adjusted_threads}")
    
    return adjusted_threads

def main():
    """Run all examples"""
    print("Thread Calculator Usage Examples")
    print("=" * 50)
    
    # Run examples
    example_thread_pool_manager()
    example_persistent_thread_pool()
    example_streaming_configuration()
    example_memory_optimization()
    example_dynamic_adjustment()
    
    print("\n" + "=" * 50)
    print("All examples completed successfully!")

if __name__ == "__main__":
    main() 