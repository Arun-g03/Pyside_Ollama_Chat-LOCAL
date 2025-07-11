# Migration Guide: QThread to QThread/QRunnable Architecture

## Overview

This guide helps you migrate from the current QThread-only implementation to the new architecture that clearly distinguishes between QThread and QRunnable usage.

## Current State Analysis

### Current Implementation Issues
1. **Single QThread approach**: All tasks use QThread, even short-lived ones
2. **Resource inefficiency**: Higher overhead for simple tasks
3. **Complex cleanup**: Manual thread management for all operations
4. **Limited scalability**: Thread count limited by system resources

### Current Worker Structure
```python
# Current: pyside_chat/workers/worker.py
class Worker(QObject):
    # Used for both streaming and simple tasks
    # Higher overhead for simple operations
    # Manual thread lifecycle management
```

## Migration Strategy

### Phase 1: Identify Task Types

#### QThread Candidates (Keep as QThread)
- **Chat streaming**: Long-running, continuous communication
- **Audio streaming**: Real-time audio processing
- **File monitoring**: Continuous file system watching
- **Background services**: Persistent operations

#### QRunnable Candidates (Migrate to QRunnable)
- **Message processing**: Spell check, formatting
- **File operations**: Read, write, process files
- **Data calculations**: Statistics, transformations
- **One-time tasks**: Quick operations

### Phase 2: Create New Architecture

#### Step 1: Update Imports
```python
# Old imports
from pyside_chat.workers.worker import Worker

# New imports
from pyside_chat.core.threading import (
    ChatStreamingWorker,  # QThread for streaming
    MessageProcessingTask,  # QRunnable for processing
    ThreadPoolManager,
    ThreadMonitor
)
```

#### Step 2: Replace Worker Usage

**Before (QThread for everything):**
```python
# Old approach
def _create_worker_thread(self, context_messages, chosen_model, temperature):
    self.worker_thread = QThread()
    self.worker = Worker()
    self.worker.moveToThread(self.worker_thread)
    # ... complex setup
    self.worker_thread.start()
```

**After (QThread for streaming, QRunnable for processing):**
```python
# New approach - QThread for streaming
def start_chat_streaming(self, messages, model, temperature):
    self.chat_streaming_worker = ChatStreamingWorker()
    self.chat_streaming_thread = QThread()
    self.chat_streaming_worker.moveToThread(self.chat_streaming_thread)
    # ... setup signals
    self.chat_streaming_thread.start()

# New approach - QRunnable for processing
def process_message(self, message):
    task = MessageProcessingTask(message, self, "spell_check")
    self.thread_pool_manager.start_task(task)
```

### Phase 3: Update Event Bus

#### Current Event Bus Changes

**File: `pyside_chat/app/event_bus.py`**

**Before:**
```python
def _create_worker_thread(self, context_messages, chosen_model, temperature):
    # Single QThread approach for all operations
    self.worker_thread = QThread()
    self.worker = Worker()
    # ... complex setup
```

**After:**
```python
def _create_chat_streaming_worker(self, context_messages, chosen_model, temperature):
    # QThread for streaming only
    self.chat_streaming_worker = ChatStreamingWorker()
    self.chat_streaming_thread = QThread()
    # ... setup for streaming

def _process_message_background(self, message):
    # QRunnable for processing
    task = MessageProcessingTask(message, self, "spell_check")
    self.thread_pool_manager.start_task(task)
```

### Phase 4: Update Signal Handlers

#### QThread Signal Handlers (Keep)
```python
def _on_worker_chunk(self, chunk):
    # Keep for streaming operations
    self.chat_controller.accumulate_assistant_response(chunk)

def _on_worker_finished(self):
    # Keep for streaming completion
    self.chat_controller.handle_ai_response()
```

#### QRunnable Callback Methods (Add)
```python
def on_message_processed(self, task_type: str, result: Dict[str, Any]):
    # New callback for QRunnable tasks
    if task_type == "spell_check":
        # Handle spell check results
        pass
    elif task_type == "formatting":
        # Handle formatting results
        pass

def on_message_processing_error(self, task_type: str, error_message: str):
    # New error callback for QRunnable tasks
    logger.error(f"Message processing error: {error_message}")
```

## Implementation Examples

### Example 1: Chat Streaming (QThread)

```python
# Keep as QThread - long-running, persistent
class ChatStreamingHandler:
    def __init__(self):
        self.thread_pool_manager = get_global_thread_pool_manager()
        self.thread_monitor = get_global_thread_monitor()
    
    def start_streaming(self, messages, model, temperature):
        # Use QThread for streaming
        self.chat_streaming_worker = ChatStreamingWorker()
        self.chat_streaming_thread = QThread()
        
        # Register for monitoring
        self.thread_monitor.register_thread(
            self.chat_streaming_thread, 
            thread_type="chat_streaming"
        )
        
        # Setup signals
        self.chat_streaming_worker.chunk_received.connect(
            self._on_chunk_received, Qt.ConnectionType.QueuedConnection
        )
        
        # Start streaming
        self.chat_streaming_thread.started.connect(
            lambda: self.chat_streaming_worker.start_streaming(
                messages=messages, model=model, temperature=temperature
            )
        )
        
        self.chat_streaming_thread.start()
```

### Example 2: Message Processing (QRunnable)

```python
# Migrate to QRunnable - short-lived, fire-and-forget
class MessageProcessingHandler:
    def __init__(self):
        self.thread_pool_manager = get_global_thread_pool_manager()
    
    def process_message_spell_check(self, message):
        # Use QRunnable for processing
        task = MessageProcessingTask(message, self, "spell_check")
        self.thread_pool_manager.start_task(task)
    
    def process_message_formatting(self, message):
        # Use QRunnable for processing
        task = MessageProcessingTask(message, self, "formatting")
        self.thread_pool_manager.start_task(task)
    
    # Callback methods for QRunnable results
    def on_message_processed(self, task_type: str, result: Dict[str, Any]):
        if task_type == "spell_check":
            # Apply spell check corrections
            if result.get('has_corrections', False):
                self.apply_corrections(result['corrections'])
        
        elif task_type == "formatting":
            # Apply formatting changes
            if result.get('changes_made', False):
                self.apply_formatting(result['formatted'])
```

## Migration Checklist

### Phase 1: Preparation
- [ ] Identify all current Worker usage
- [ ] Categorize tasks as QThread or QRunnable candidates
- [ ] Create new threading module structure
- [ ] Set up ThreadPoolManager and ThreadMonitor

### Phase 2: QThread Migration
- [ ] Migrate streaming operations to ChatStreamingWorker
- [ ] Update signal handlers for streaming
- [ ] Test streaming functionality
- [ ] Update thread monitoring

### Phase 3: QRunnable Migration
- [ ] Migrate message processing to MessageProcessingTask
- [ ] Migrate file operations to FileProcessingTask
- [ ] Add callback methods for QRunnable results
- [ ] Test processing functionality

### Phase 4: Cleanup
- [ ] Remove old Worker class usage
- [ ] Update imports throughout codebase
- [ ] Test all functionality
- [ ] Update documentation

## Testing Strategy

### QThread Testing
```python
def test_chat_streaming():
    # Test streaming functionality
    handler = ChatStreamingHandler()
    handler.start_streaming(messages, model, temperature)
    
    # Verify signals are emitted
    # Verify thread lifecycle
    # Verify cleanup
```

### QRunnable Testing
```python
def test_message_processing():
    # Test processing functionality
    handler = MessageProcessingHandler()
    handler.process_message_spell_check("test message")
    
    # Verify callback is called
    # Verify results are correct
    # Verify error handling
```

## Performance Benefits

### Before Migration
- All tasks use QThread
- Higher memory overhead per task
- Manual thread management
- Limited scalability

### After Migration
- QThread only for persistent tasks
- QRunnable for quick tasks
- Automatic thread pool management
- Better resource utilization

## Error Handling

### QThread Error Handling
```python
def _on_chat_streaming_error(self, error: str):
    logger.error(f"Chat streaming error: {error}")
    # Clean up thread
    self.stop_chat_streaming()
    # Show error to user
```

### QRunnable Error Handling
```python
def on_message_processing_error(self, task_type: str, error_message: str):
    logger.error(f"Message processing error ({task_type}): {error_message}")
    # Show error to user
    # No cleanup needed (automatic)
```

## Monitoring and Debugging

### Thread Monitoring
```python
# Monitor all threads
thread_monitor = get_global_thread_monitor()
status = thread_monitor.get_threading_status()
print(f"Active threads: {status['active_threads']}")
print(f"Thread errors: {status['thread_errors']}")
```

### Pool Monitoring
```python
# Monitor thread pool
thread_pool_manager = get_global_thread_pool_manager()
status = thread_pool_manager.get_pool_status()
print(f"Pool utilization: {status['utilization']}%")
print(f"Active tasks: {status['active_tasks']}")
```

## Conclusion

This migration provides:
1. **Clear separation of concerns**: QThread for persistent tasks, QRunnable for quick tasks
2. **Better resource management**: Automatic thread pool management
3. **Improved scalability**: More efficient use of system resources
4. **Enhanced monitoring**: Better debugging and performance tracking
5. **Cleaner code**: Simpler architecture with clear responsibilities

The migration should be done incrementally, testing each phase thoroughly before proceeding to the next. 