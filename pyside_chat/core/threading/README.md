# QThread vs QRunnable: Clear Distinction and Implementation

## Overview

This module provides a clear distinction between QThread and QRunnable usage in PySide6 applications, with proper architecture for both approaches.

## Quick Reference

### When to Use QThread
- **Long-running operations**: Streaming, monitoring, continuous tasks
- **Signal/slot communication**: Complex state management
- **Persistent workers**: Operations that stay alive
- **UI-intensive operations**: Frequent UI updates

### When to Use QRunnable
- **Short-lived tasks**: One-time operations, quick processing
- **Batch operations**: Multiple independent tasks
- **CPU-intensive tasks**: Calculations, data processing
- **Fire-and-forget**: Tasks that don't need ongoing communication

## Architecture

```
pyside_chat/core/threading/
├── __init__.py                 # Module exports
├── threading_guide.md          # Comprehensive guide
├── qthread_workers.py          # QThread-based workers
├── qrunnable_tasks.py          # QRunnable-based tasks
├── thread_pool_manager.py      # Thread pool management
├── thread_monitor.py           # Thread monitoring
├── usage_examples.py           # Practical examples
├── migration_guide.md          # Migration instructions
└── README.md                   # This file
```

## Key Components

### QThread Workers (`qthread_workers.py`)
- `StreamingWorker`: Base class for streaming operations
- `ChatStreamingWorker`: Chat response streaming
- `AudioStreamingWorker`: Audio processing streaming
- `MonitoringWorker`: System resource monitoring

### QRunnable Tasks (`qrunnable_tasks.py`)
- `MessageProcessingTask`: Message spell check, formatting
- `FileProcessingTask`: File read, write, processing
- `DataProcessingTask`: Data calculations, transformations
- `CalculationTask`: CPU-intensive calculations

### Thread Management
- `ThreadPoolManager`: Manages QRunnable tasks
- `ThreadMonitor`: Tracks and monitors all threads

## Usage Examples

### QThread for Streaming
```python
from pyside_chat.core.threading import ChatStreamingWorker

# Create streaming worker
worker = ChatStreamingWorker()
thread = QThread()
worker.moveToThread(thread)

# Connect signals
worker.chunk_received.connect(self.handle_chunk)
worker.finished.connect(self.handle_finished)

# Start streaming
thread.started.connect(lambda: worker.start_streaming(messages, model))
thread.start()
```

### QRunnable for Processing
```python
from pyside_chat.core.threading import MessageProcessingTask, get_global_thread_pool_manager

# Create processing task
task = MessageProcessingTask(message, self, "spell_check")
thread_pool = get_global_thread_pool_manager()

# Start task
task_id = thread_pool.start_task(task)

# Handle results via callback
def on_message_processed(self, task_type, result):
    if task_type == "spell_check":
        # Apply corrections
        pass
```

## Performance Comparison

| Aspect | QThread | QRunnable |
|--------|---------|-----------|
| **Memory Overhead** | Higher | Lower |
| **Thread Management** | Manual | Automatic |
| **Communication** | Signals/Slots | invokeMethod |
| **Lifespan** | Persistent | Short-lived |
| **Use Case** | Streaming, Monitoring | Processing, Calculations |

## Best Practices

### QThread Best Practices
1. **Always clean up**: Call quit() and wait() before deleting
2. **Use QueuedConnection**: For thread-safe signal/slot connections
3. **Move objects to thread**: Use moveToThread() for worker objects
4. **Handle thread lifecycle**: Connect to started/finished signals
5. **Avoid blocking**: Don't block the main thread waiting for worker threads

### QRunnable Best Practices
1. **Set autoDelete**: Use setAutoDelete(True) for automatic cleanup
2. **Use invokeMethod**: For main thread communication
3. **Keep tasks short**: QRunnable is for quick tasks, not long-running operations
4. **Handle exceptions**: Always wrap run() method in try/catch
5. **Don't store state**: QRunnable objects should be stateless

## Monitoring and Debugging

### Thread Monitoring
```python
from pyside_chat.core.threading import get_global_thread_monitor

monitor = get_global_thread_monitor()
status = monitor.get_threading_status()
print(f"Active threads: {status['active_threads']}")
print(f"Total runtime: {status['total_runtime']}")
```

### Pool Monitoring
```python
from pyside_chat.core.threading import get_global_thread_pool_manager

pool = get_global_thread_pool_manager()
status = pool.get_pool_status()
print(f"Pool utilization: {status['utilization']}%")
print(f"Active tasks: {status['active_tasks']}")
```

## Migration from Current Implementation

The current implementation uses QThread for all operations. To migrate:

1. **Identify task types**: Categorize as QThread or QRunnable candidates
2. **Migrate streaming**: Keep chat streaming as QThread
3. **Migrate processing**: Move message processing to QRunnable
4. **Update signal handlers**: Add callback methods for QRunnable results
5. **Test thoroughly**: Verify all functionality works correctly

See `migration_guide.md` for detailed migration instructions.

## Error Handling

### QThread Error Handling
```python
def handle_worker_error(self, error_msg):
    logger.error(f"Worker error: {error_msg}")
    # Clean up thread
    self.worker_thread.quit()
    self.worker_thread.wait()
    self.worker_thread.deleteLater()
```

### QRunnable Error Handling
```python
def run(self):
    try:
        # Task logic
        pass
    except Exception as e:
        # Use invokeMethod to report error to main thread
        QMetaObject.invokeMethod(self.callback, 'on_error',
                               Qt.ConnectionType.QueuedConnection,
                               Q_ARG(str, str(e)))
```

## Thread Safety

### QThread Safety
- Use `Qt.ConnectionType.QueuedConnection` for signal/slot connections
- Move objects to thread using `moveToThread()`
- Avoid direct access to objects from different threads

### QRunnable Safety
- Use `QMetaObject.invokeMethod()` for main thread communication
- Don't access UI elements directly from QRunnable
- Pass data by value, not by reference

## Resource Management

### QThread Resources
- Each QThread has its own event loop
- Higher memory overhead per thread
- Limited by system thread count
- Manual cleanup required

### QRunnable Resources
- Uses thread pool (shared threads)
- Lower memory overhead
- Automatic cleanup
- Better resource utilization

## Testing

### QThread Testing
```python
def test_streaming_worker():
    worker = ChatStreamingWorker()
    thread = QThread()
    worker.moveToThread(thread)
    
    # Test signals
    worker.chunk_received.connect(self.handle_chunk)
    worker.finished.connect(self.handle_finished)
    
    # Start and verify
    thread.start()
    # ... test logic
```

### QRunnable Testing
```python
def test_processing_task():
    task = MessageProcessingTask("test message", self, "spell_check")
    thread_pool = get_global_thread_pool_manager()
    
    # Start task
    task_id = thread_pool.start_task(task)
    
    # Wait for completion
    thread_pool.wait_for_task(task_id)
    
    # Verify callback was called
    assert self.callback_called
```

## Configuration

### Thread Pool Configuration
```python
# Global thread pool (default: 4 threads)
thread_pool = get_global_thread_pool_manager()
thread_pool.thread_pool.setMaxThreadCount(8)  # Increase if needed
```

### Monitoring Configuration
```python
# Thread monitoring
monitor = get_global_thread_monitor()
# Monitor updates every 2 seconds by default
```

## Troubleshooting

### Common Issues

1. **QThread not starting**
   - Check if worker is moved to thread
   - Verify signal connections
   - Check thread object name

2. **QRunnable not executing**
   - Verify autoDelete is set
   - Check thread pool is not full
   - Verify callback object exists

3. **Memory leaks**
   - Ensure proper cleanup of QThread objects
   - Check for circular references
   - Verify autoDelete is enabled for QRunnable

4. **Signal/slot not working**
   - Use QueuedConnection for cross-thread signals
   - Verify object ownership
   - Check thread affinity

### Debug Tips

1. **Enable thread monitoring**
   ```python
   monitor = get_global_thread_monitor()
   monitor.thread_registered.connect(lambda name: print(f"Thread registered: {name}"))
   ```

2. **Check thread pool status**
   ```python
   pool = get_global_thread_pool_manager()
   status = pool.get_pool_status()
   print(f"Pool status: {status}")
   ```

3. **Monitor resource usage**
   ```python
   monitor = get_global_thread_monitor()
   usage = monitor.get_resource_usage()
   print(f"Resource usage: {usage}")
   ```

## Conclusion

This architecture provides:
- **Clear separation of concerns**: QThread for persistent tasks, QRunnable for quick tasks
- **Better resource management**: Automatic thread pool management
- **Improved scalability**: More efficient use of system resources
- **Enhanced monitoring**: Better debugging and performance tracking
- **Cleaner code**: Simpler architecture with clear responsibilities

Choose the right tool for the job:
- **QThread**: For long-running, communication-heavy tasks
- **QRunnable**: For short-lived, independent tasks 