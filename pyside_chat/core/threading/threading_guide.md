# QThread vs QRunnable: Clear Distinction and Best Practices

## Overview

This guide explains the proper use of QThread and QRunnable in PySide6 applications, with clear distinctions and best practices for each approach.

## QThread vs QRunnable: Key Differences

### QThread
- **Purpose**: Dedicated thread for long-running, persistent tasks
- **Use Case**: Tasks that need their own thread lifecycle and signal/slot communication
- **Characteristics**:
  - Own thread with event loop
  - Can emit signals and connect to slots
  - Persistent - stays alive until explicitly stopped
  - Good for continuous operations (streaming, monitoring, etc.)
  - Higher overhead per thread
  - Limited by system resources

### QRunnable
- **Purpose**: Lightweight task execution using thread pool
- **Use Case**: Short-lived, fire-and-forget tasks
- **Characteristics**:
  - No own thread - uses thread pool
  - No signal/slot communication (use QMetaObject.invokeMethod for main thread communication)
  - Auto-cleanup after completion
  - Good for batch processing, calculations, file operations
  - Lower overhead
  - Better resource management

## When to Use Each

### Use QThread for:
1. **Streaming Operations**: Real-time data processing (chat streaming, audio streaming)
2. **Continuous Monitoring**: Background services that need to stay alive
3. **Complex Signal/Slot Communication**: Tasks that need to emit multiple signals
4. **Persistent Workers**: Workers that handle multiple requests over time
5. **UI-Intensive Operations**: Tasks that need frequent UI updates

### Use QRunnable for:
1. **One-Time Tasks**: File operations, data processing, calculations
2. **Batch Operations**: Processing multiple items
3. **Resource-Intensive Tasks**: CPU-heavy operations
4. **Fire-and-Forget**: Tasks that don't need ongoing communication
5. **Parallel Processing**: Multiple independent tasks

## Implementation Patterns

### QThread Pattern
```python
class StreamingWorker(QObject):
    chunk_received = Signal(str)
    finished = Signal()
    error = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._running = False
    
    def start_streaming(self, url, data):
        self._running = True
        # Streaming logic here
        # Emit signals as data arrives
        self.chunk_received.emit(chunk)
    
    def stop(self):
        self._running = False

# Usage
worker = StreamingWorker()
thread = QThread()
worker.moveToThread(thread)
worker.chunk_received.connect(self.handle_chunk)
thread.started.connect(lambda: worker.start_streaming(url, data))
thread.start()
```

### QRunnable Pattern
```python
class ProcessingTask(QRunnable):
    def __init__(self, data, callback):
        super().__init__()
        self.data = data
        self.callback = callback
        self.setAutoDelete(True)
    
    def run(self):
        try:
            result = self.process_data(self.data)
            # Use invokeMethod to communicate with main thread
            QMetaObject.invokeMethod(self.callback, 'on_task_complete',
                                   Qt.ConnectionType.QueuedConnection,
                                   Q_ARG(object, result))
        except Exception as e:
            QMetaObject.invokeMethod(self.callback, 'on_task_error',
                                   Qt.ConnectionType.QueuedConnection,
                                   Q_ARG(str, str(e)))

# Usage
task = ProcessingTask(data, self)
QThreadPool.globalInstance().start(task)
```

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

## Thread Pool Management

### Global Thread Pool
```python
# Use global thread pool for QRunnable tasks
thread_pool = QThreadPool.globalInstance()
thread_pool.setMaxThreadCount(4)  # Limit concurrent threads
```

### Custom Thread Pool
```python
# Create custom thread pool for specific task types
class CustomThreadPool:
    def __init__(self, max_threads=4):
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(max_threads)
    
    def start_task(self, task):
        self.thread_pool.start(task)
```

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

## Performance Considerations

### QThread Performance
- Higher memory overhead per thread
- Good for I/O-bound tasks
- Suitable for continuous operations
- Limited by system thread count

### QRunnable Performance
- Lower memory overhead
- Good for CPU-bound tasks
- Efficient for batch processing
- Better resource utilization

## Migration Strategy

### From QThread to QRunnable
1. Identify short-lived tasks
2. Remove signal/slot dependencies
3. Use invokeMethod for main thread communication
4. Implement autoDelete cleanup
5. Test thread safety

### From QRunnable to QThread
1. Identify long-running tasks
2. Add signal/slot communication
3. Implement thread lifecycle management
4. Add proper cleanup procedures
5. Test signal/slot connections

## Example: Chat Application

### Streaming Chat (QThread)
```python
class ChatStreamingWorker(QObject):
    chunk_received = Signal(str)
    finished = Signal()
    error = Signal(str)
    
    def stream_chat(self, messages, model):
        # Long-running streaming operation
        # Emits chunks as they arrive
        pass
```

### Message Processing (QRunnable)
```python
class MessageProcessingTask(QRunnable):
    def __init__(self, message, callback):
        super().__init__()
        self.message = message
        self.callback = callback
        self.setAutoDelete(True)
    
    def run(self):
        # Process message (spell check, formatting, etc.)
        processed = self.process_message(self.message)
        QMetaObject.invokeMethod(self.callback, 'on_message_processed',
                               Qt.ConnectionType.QueuedConnection,
                               Q_ARG(str, processed))
```

## Conclusion

Choose QThread for persistent, communication-heavy tasks and QRunnable for short-lived, independent tasks. This distinction leads to better resource management and cleaner code architecture. 