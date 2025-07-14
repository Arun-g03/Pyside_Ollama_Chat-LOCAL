from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.shared_imports.pyside_imports import *


"""
QRunnable-based tasks for short-lived, fire-and-forget operations.

These tasks are designed for:
- One-time operations
- Batch processing
- CPU-intensive calculations
- File operations
- Resource cleanup
- UI updates for streaming content
"""

logger = CustomLogger.get_logger(__name__)


class StreamingUpdateTask(QRunnable, QObject):
    """
    Task for handling streaming UI updates.
    
    This task:
    - Executes UI update functions in the main thread
    - Uses invokeMethod for thread-safe UI updates
    - Provides callback mechanism for completion tracking
    """
    
    update_complete = Signal(str)  # task_id
    update_error = Signal(str, str)  # task_id, error_message
    
    def __init__(self, target: Callable, callback: Optional[Callable] = None, task_id: Optional[str] = None):
        QRunnable.__init__(self)
        QObject.__init__(self)
        self.target = target
        self.callback = callback
        self.task_id = task_id or f"streaming_update_{int(time.time() * 1000)}"
        self.setAutoDelete(True)
        
        logger.debug(f"[DEBUG] StreamingUpdateTask created - ID: {self.task_id}")
    
    def run(self):
        """Execute the streaming update task."""
        try:
            logger.debug(f"[DEBUG] StreamingUpdateTask started - ID: {self.task_id}")
            
            # Get the main application instance
            app = QApplication.instance()
            if not app:
                raise RuntimeError("No QApplication instance found")
            
            # Use QTimer.singleShot for safer main thread execution

            logger.debug(f"[DEBUG] StreamingUpdateTask completed - ID: {self.task_id}")
            
        except Exception as e:
            error_msg = f"Streaming update error: {str(e)}"
            logger.error(f"[DEBUG] {error_msg}")
            logger.error(f"[DEBUG] StreamingUpdateTask traceback: {traceback.format_exc()}")
            self.update_error.emit(self.task_id, error_msg)
    
    def _execute_target(self):
        """Execute the target function and handle completion."""
        try:
            # Execute the target function
            result = self.target()
            
            # Emit completion signal
            self.update_complete.emit(self.task_id)
            
            # Call callback if provided
            if self.callback:
                self.callback(self.task_id)
                
        except Exception as e:
            error_msg = f"Target execution error: {str(e)}"
            logger.error(f"[DEBUG] {error_msg}")
            logger.error(f"[DEBUG] Target execution traceback: {traceback.format_exc()}")
            self.update_error.emit(self.task_id, error_msg)


class MessageProcessingTask(QRunnable, QObject):
    """
    Task for processing chat messages (spell check, formatting, etc.).
    
    This is a short-lived task that:
    - Processes a single message
    - Returns processed result
    - Uses invokeMethod for main thread communication
    """
    
    result_ready = Signal(str, object)  # task_type, result
    error_occurred = Signal(str, str)   # task_type, error_message
    
    def __init__(self, message: str, task_type: str = "spell_check"):
        QRunnable.__init__(self)
        QObject.__init__(self)
        self.message = message
        self.task_type = task_type
        self.setAutoDelete(True)
        
        logger.debug(f"[ID:TR001] MessageProcessingTask created - Type: {task_type}")
    
    def run(self):
        """Execute the message processing task."""
        try:
            logger.debug(f"[ID:TR002] MessageProcessingTask started - Type: {self.task_type}")
            
            if self.task_type == "spell_check":
                result = self._spell_check_message()
            elif self.task_type == "formatting":
                result = self._format_message()
            elif self.task_type == "sentiment":
                result = self._analyze_sentiment()
            else:
                result = {"error": f"Unknown task type: {self.task_type}"}
            
            self.result_ready.emit(self.task_type, result)
            
            logger.debug(f"[ID:TR003] MessageProcessingTask completed - Type: {self.task_type}")
            
        except Exception as e:
            error_msg = f"Message processing error: {str(e)}"
            logger.error(f"[ID:TR004] {error_msg}")
            logger.error(f"[ID:TR005] MessageProcessingTask traceback: {traceback.format_exc()}")
            self.error_occurred.emit(self.task_type, error_msg)
    
    def _spell_check_message(self) -> Dict[str, Any]:
        """Perform spell check on the message."""
        # Simple spell check implementation
        # In a real application, you might use a proper spell checker library
        
        # Common misspellings and corrections
        corrections = {
            'teh': 'the',
            'recieve': 'receive',
            'seperate': 'separate',
            'occured': 'occurred',
            'begining': 'beginning',
            'accomodate': 'accommodate',
            'definately': 'definitely',
            'embarass': 'embarrass',
            'existance': 'existence',
            'occassion': 'occasion'
        }
        
        words = self.message.split()
        corrected_words = []
        corrections_made = []
        
        for word in words:
            # Remove punctuation for checking
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if clean_word in corrections:
                corrected_words.append(corrections[clean_word])
                corrections_made.append({
                    'original': word,
                    'corrected': corrections[clean_word]
                })
            else:
                corrected_words.append(word)
        
        corrected_message = ' '.join(corrected_words)
        
        return {
            'original': self.message,
            'corrected': corrected_message,
            'corrections': corrections_made,
            'has_corrections': len(corrections_made) > 0
        }
    
    def _format_message(self) -> Dict[str, Any]:
        """Format the message for better readability."""
        # Simple formatting rules
        formatted = self.message
        
        # Capitalize first letter of sentences
        formatted = re.sub(r'([.!?])\s+([a-z])', lambda m: m.group(1) + ' ' + m.group(2).upper(), formatted)
        
        # Ensure first letter is capitalized
        if formatted and formatted[0].islower():
            formatted = formatted[0].upper() + formatted[1:]
        
        # Add proper spacing around punctuation
        formatted = re.sub(r'([.!?])([A-Z])', r'\1 \2', formatted)
        
        return {
            'original': self.message,
            'formatted': formatted,
            'changes_made': formatted != self.message
        }
    
    def _analyze_sentiment(self) -> Dict[str, Any]:
        """Analyze sentiment of the message."""
        # Simple sentiment analysis
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like', 'happy', 'joy'}
        negative_words = {'bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'angry', 'frustrated'}
        
        words = set(re.findall(r'\b\w+\b', self.message.lower()))
        
        positive_count = len(words.intersection(positive_words))
        negative_count = len(words.intersection(negative_words))
        
        if positive_count > negative_count:
            sentiment = 'positive'
        elif negative_count > positive_count:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'positive_words': positive_count,
            'negative_words': negative_count,
            'confidence': min(positive_count + negative_count, 10) / 10
        }


class FileProcessingTask(QRunnable, QObject):
    """
    Task for file operations (reading, writing, processing).
    
    This is a short-lived task that:
    - Processes files in the background
    - Reports progress and completion
    - Uses invokeMethod for main thread communication
    """
    
    result_ready = Signal(str, str, object)  # operation, file_path, result
    error_occurred = Signal(str, str, str)   # operation, file_path, error_message
    
    def __init__(self, file_path: str, operation: str, **kwargs):
        QRunnable.__init__(self)
        QObject.__init__(self)
        self.file_path = file_path
        self.operation = operation
        self.kwargs = kwargs
        self.setAutoDelete(True)
        
        logger.debug(f"[ID:TR006] FileProcessingTask created - Operation: {operation}, File: {file_path}")
    
    def run(self):
        """Execute the file processing task."""
        try:
            logger.debug(f"[ID:TR007] FileProcessingTask started - Operation: {self.operation}")
            
            if self.operation == "read":
                result = self._read_file()
            elif self.operation == "write":
                result = self._write_file()
            elif self.operation == "process":
                result = self._process_file()
            else:
                result = {"error": f"Unknown file operation: {self.operation}"}
            
            self.result_ready.emit(self.operation, self.file_path, result)
            
            logger.debug(f"[ID:TR008] FileProcessingTask completed - Operation: {self.operation}")
            
        except Exception as e:
            error_msg = f"File processing error: {str(e)}"
            logger.error(f"[ID:TR008] {error_msg}")
            logger.error(f"[ID:TR009] FileProcessingTask traceback: {traceback.format_exc()}")
            self.error_occurred.emit(self.operation, self.file_path, error_msg)
    
    def _read_file(self) -> Dict[str, Any]:
        """Read file content."""
        import os
        
        if not os.path.exists(self.file_path):
            return {"error": f"File not found: {self.file_path}"}
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'content': content,
                'size': len(content),
                'lines': len(content.splitlines())
            }
        except Exception as e:
            return {"error": f"Error reading file: {str(e)}"}
    
    def _write_file(self) -> Dict[str, Any]:
        """Write content to file."""
        content = self.kwargs.get('content', '')
        
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                'success': True,
                'size': len(content)
            }
        except Exception as e:
            return {"error": f"Error writing file: {str(e)}"}
    
    def _process_file(self) -> Dict[str, Any]:
        """Process file content (e.g., JSON parsing, text analysis)."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to parse as JSON
            try:
                data = json.loads(content)
                return {
                    'type': 'json',
                    'keys': list(data.keys()) if isinstance(data, dict) else [],
                    'size': len(content)
                }
            except json.JSONDecodeError:
                # Not JSON, treat as text
                lines = content.splitlines()
                words = content.split()
                
                return {
                    'type': 'text',
                    'lines': len(lines),
                    'words': len(words),
                    'characters': len(content),
                    'size': len(content)
                }
                
        except Exception as e:
            return {"error": f"Error processing file: {str(e)}"}


class DataProcessingTask(QRunnable, QObject):
    """
    Task for data processing operations.
    
    This is a short-lived task that:
    - Processes data in the background
    - Performs calculations or transformations
    - Reports results to main thread
    """
    
    result_ready = Signal(str, object)  # operation, result
    error_occurred = Signal(str, str)   # operation, error_message
    
    def __init__(self, data: Any, operation: str, **kwargs):
        QRunnable.__init__(self)
        QObject.__init__(self)
        self.data = data
        self.operation = operation
        self.kwargs = kwargs
        self.setAutoDelete(True)
        
        logger.debug(f"[ID:TR010] DataProcessingTask created - Operation: {operation}")
    
    def run(self):
        """Execute the data processing task."""
        try:
            logger.debug(f"[ID:TR011] DataProcessingTask started - Operation: {self.operation}")
            
            if self.operation == "calculate":
                result = self._calculate_data()
            elif self.operation == "transform":
                result = self._transform_data()
            elif self.operation == "analyze":
                result = self._analyze_data()
            elif self.operation.startswith("model_"):
                result = self._handle_model_operation()
            else:
                result = {"error": f"Unknown data operation: {self.operation}"}
            
            self.result_ready.emit(self.operation, result)
            
            logger.debug(f"[ID:TR013] DataProcessingTask completed - Operation: {self.operation}")
            
        except Exception as e:
            error_msg = f"Data processing error: {str(e)}"
            logger.error(f"[ID:TR012] {error_msg}")
            logger.error(f"[ID:TR013] DataProcessingTask traceback: {traceback.format_exc()}")
            self.error_occurred.emit(self.operation, error_msg)
    
    def _handle_model_operation(self) -> Dict[str, Any]:
        """Handle model operations for Ollama service."""
        try:
            import subprocess
            import ollama
            
            model_data = self.data
            model_name = model_data.get("model_name")
            operation = model_data.get("operation")
            base_url = self.kwargs.get("base_url", "http://localhost:11434")
            cancellation_requested = self.kwargs.get("cancellation_requested", False)
            progress_callback = self.kwargs.get("progress_callback")
            error_callback = self.kwargs.get("error_callback")
            success_callback = self.kwargs.get("success_callback")
            
            logger.debug(f"[DEBUG] Handling model operation: {operation} for model: {model_name}")
            
            # Try with official library first
            try:
                if operation == "pull":
                    logger.info(f"[DEBUG] Using official library to pull model: {model_name}")
                    ollama.pull(model_name)
                    if success_callback:
                        success_callback(f"Successfully pulled model: {model_name}")
                    return {"success": True, "operation": operation, "model": model_name}
                    
                elif operation == "remove":
                    logger.info(f"[DEBUG] Using official library to remove model: {model_name}")
                    ollama.delete(model_name)
                    if success_callback:
                        success_callback(f"Successfully removed model: {model_name}")
                    return {"success": True, "operation": operation, "model": model_name}
                    
                elif operation == "update":
                    logger.info(f"[DEBUG] Using official library to update model: {model_name}")
                    ollama.pull(model_name)  # Update is same as pull
                    if success_callback:
                        success_callback(f"Successfully updated model: {model_name}")
                    return {"success": True, "operation": operation, "model": model_name}
                    
            except Exception as e:
                logger.debug(f"[DEBUG] Library operation failed, falling back to subprocess: {e}")
            
            # Fall back to subprocess method
            if operation == "pull":
                command = ["ollama", "pull", model_name]
            elif operation == "remove":
                command = ["ollama", "rm", model_name]
            elif operation == "update":
                command = ["ollama", "pull", model_name]  # Update is same as pull
            else:
                raise ValueError(f"Unknown model operation: {operation}")
            
            process = subprocess.Popen(
                command, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                universal_newlines=True, 
                encoding='utf-8', 
                errors='replace', 
                bufsize=1
            )

            for line in iter(process.stdout.readline, ''):
                if cancellation_requested:
                    process.terminate()
                    logger.debug("[DEBUG] Model operation cancelled by user")
                    break
                if progress_callback:
                    progress_callback(line.strip())
            
            process.stdout.close()
            return_code = process.wait()
            
            if return_code:
                error_msg = f"Error in {operation} operation (exit code: {return_code})."
                if error_callback:
                    error_callback(error_msg)
                return {"error": error_msg, "operation": operation, "model": model_name}
            else:
                if success_callback:
                    success_callback(f"Successfully {operation}d model: {model_name}")
                return {"success": True, "operation": operation, "model": model_name}

        except FileNotFoundError as e:
            error_msg = "Ollama command not found. Is it installed and in your PATH?"
            if error_callback:
                error_callback(error_msg)
            return {"error": error_msg, "operation": operation, "model": model_name}
        except Exception as e:
            error_msg = f"An error occurred during {operation}: {str(e)}"
            if error_callback:
                error_callback(error_msg)
            return {"error": error_msg, "operation": operation, "model": model_name}
    
    def _calculate_data(self) -> Dict[str, Any]:
        """Perform calculations on the data."""
        if isinstance(self.data, list):
            if all(isinstance(x, (int, float)) for x in self.data):
                return {
                    'sum': sum(self.data),
                    'average': sum(self.data) / len(self.data),
                    'min': min(self.data),
                    'max': max(self.data),
                    'count': len(self.data)
                }
            else:
                return {
                    'count': len(self.data),
                    'types': list(set(type(x).__name__ for x in self.data))
                }
        elif isinstance(self.data, dict):
            return {
                'keys': list(self.data.keys()),
                'values_count': len(self.data),
                'nested_levels': self._count_nested_levels(self.data)
            }
        else:
            return {
                'type': type(self.data).__name__,
                'value': str(self.data)
            }
    
    def _transform_data(self) -> Dict[str, Any]:
        """Transform the data."""
        transform_type = self.kwargs.get('transform_type', 'default')
        
        if transform_type == 'uppercase' and isinstance(self.data, str):
            return {
                'original': self.data,
                'transformed': self.data.upper(),
                'transform_type': transform_type
            }
        elif transform_type == 'lowercase' and isinstance(self.data, str):
            return {
                'original': self.data,
                'transformed': self.data.lower(),
                'transform_type': transform_type
            }
        elif transform_type == 'reverse' and isinstance(self.data, str):
            return {
                'original': self.data,
                'transformed': self.data[::-1],
                'transform_type': transform_type
            }
        else:
            return {
                'error': f"Cannot apply transform '{transform_type}' to data type {type(self.data).__name__}"
            }
    
    def _analyze_data(self) -> Dict[str, Any]:
        """Analyze the data structure and content."""
        if isinstance(self.data, str):
            return {
                'type': 'string',
                'length': len(self.data),
                'words': len(self.data.split()),
                'lines': len(self.data.splitlines()),
                'has_numbers': any(c.isdigit() for c in self.data),
                'has_uppercase': any(c.isupper() for c in self.data),
                'has_lowercase': any(c.islower() for c in self.data)
            }
        elif isinstance(self.data, list):
            return {
                'type': 'list',
                'length': len(self.data),
                'element_types': list(set(type(x).__name__ for x in self.data)),
                'unique_elements': len(set(self.data)) if all(isinstance(x, (str, int, float)) for x in self.data) else 'N/A'
            }
        elif isinstance(self.data, dict):
            return {
                'type': 'dict',
                'keys': list(self.data.keys()),
                'values_count': len(self.data),
                'nested_levels': self._count_nested_levels(self.data)
            }
        else:
            return {
                'type': type(self.data).__name__,
                'value': str(self.data)
            }
    
    def _count_nested_levels(self, data: Any, current_level: int = 0) -> int:
        """Count the maximum nesting level in a data structure."""
        if isinstance(data, dict):
            if not data:
                return current_level
            return max(self._count_nested_levels(v, current_level + 1) for v in data.values())
        elif isinstance(data, list):
            if not data:
                return current_level
            return max(self._count_nested_levels(item, current_level + 1) for item in data)
        else:
            return current_level


class CalculationTask(QRunnable, QObject):
    """
    Task for CPU-intensive calculations.
    
    This is a short-lived task that:
    - Performs heavy calculations in background
    - Reports progress and results
    - Uses invokeMethod for main thread communication
    """
    
    result_ready = Signal(str, object)  # calculation_type, result
    error_occurred = Signal(str, str)   # calculation_type, error_message
    
    def __init__(self, calculation_type: str, parameters: Dict[str, Any]):
        QRunnable.__init__(self)
        QObject.__init__(self)
        self.calculation_type = calculation_type
        self.parameters = parameters
        self.setAutoDelete(True)
        
        logger.debug(f"[ID:TR014] CalculationTask created - Type: {calculation_type}")
    
    def run(self):
        """Execute the calculation task."""
        try:
            logger.debug(f"[ID:TR015] CalculationTask started - Type: {self.calculation_type}")
            
            if self.calculation_type == "fibonacci":
                result = self._calculate_fibonacci()
            elif self.calculation_type == "prime_factors":
                result = self._calculate_prime_factors()
            elif self.calculation_type == "statistics":
                result = self._calculate_statistics()
            else:
                result = {"error": f"Unknown calculation type: {self.calculation_type}"}
            
            self.result_ready.emit(self.calculation_type, result)
            
            logger.debug(f"[ID:TR018] CalculationTask completed - Type: {self.calculation_type}")
            
        except Exception as e:
            error_msg = f"Calculation error: {str(e)}"
            logger.error(f"[ID:TR016] {error_msg}")
            logger.error(f"[ID:TR017] CalculationTask traceback: {traceback.format_exc()}")
            self.error_occurred.emit(self.calculation_type, error_msg)
    
    def _calculate_fibonacci(self) -> Dict[str, Any]:
        """Calculate Fibonacci numbers."""
        n = self.parameters.get('n', 10)
        
        if n <= 0:
            return {"error": "n must be positive"}
        
        start_time = time.time()
        
        if n <= 2:
            result = [1] * n
        else:
            result = [1, 1]
            for i in range(2, n):
                result.append(result[i-1] + result[i-2])
        
        duration = time.time() - start_time
        
        return {
            'sequence': result,
            'n': n,
            'duration': duration,
            'last_number': result[-1] if result else None
        }
    
    def _calculate_prime_factors(self) -> Dict[str, Any]:
        """Calculate prime factors of a number."""
        number = self.parameters.get('number', 100)
        
        if number <= 1:
            return {"error": "Number must be greater than 1"}
        
        start_time = time.time()
        
        factors = []
        n = number
        divisor = 2
        
        while n > 1:
            while n % divisor == 0:
                factors.append(divisor)
                n //= divisor
            divisor += 1
            if divisor * divisor > n:
                if n > 1:
                    factors.append(n)
                break
        
        duration = time.time() - start_time
        
        return {
            'number': number,
            'factors': factors,
            'duration': duration,
            'is_prime': len(factors) == 1 and factors[0] == number
        }
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """Calculate statistical measures."""
        data = self.parameters.get('data', [])
        
        if not data or not all(isinstance(x, (int, float)) for x in data):
            return {"error": "Data must be a list of numbers"}
        
        start_time = time.time()
        
        n = len(data)
        total = sum(data)
        mean = total / n
        
        # Calculate variance and standard deviation
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = variance ** 0.5
        
        # Calculate median
        sorted_data = sorted(data)
        if n % 2 == 0:
            median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            median = sorted_data[n//2]
        
        duration = time.time() - start_time
        
        return {
            'count': n,
            'sum': total,
            'mean': mean,
            'median': median,
            'variance': variance,
            'std_dev': std_dev,
            'min': min(data),
            'max': max(data),
            'duration': duration
        } 