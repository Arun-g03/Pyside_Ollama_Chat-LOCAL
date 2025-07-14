# Shared imports
from pyside_chat.core.shared_imports.shared_imports import *
from pyside_chat.core.shared_imports.pyside_imports import *


"""
Ollama Service Module

Handles all communication with the Ollama API using both the official library
and requests as fallback, with proper threading support.
"""

logger = CustomLogger.get_logger(__name__)

# Check if official Ollama library is available
try:
    import ollama
    OLLAMA_LIBRARY_AVAILABLE = True
    logger.debug("[ID:0016] Official Ollama library is available")
except ImportError:
    OLLAMA_LIBRARY_AVAILABLE = False
    logger.debug("[ID:0016] Official Ollama library not available, using requests")


class OllamaService(QObject):
    """Enhanced service for handling all Ollama API communication with official library support using persistent threading"""
    
    # Signals for async operations
    model_list_updated = Signal(list)  # Emits list of model names
    model_operation_started = Signal(str)  # Emits operation name
    model_operation_finished = Signal(str)  # Emits operation name
    model_operation_progress = Signal(str)  # Emits progress message
    model_operation_error = Signal(str)  # Emits error message
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        super().__init__()
        try:
            self.base_url = base_url.rstrip('/')
            self.request_in_progress = False
            self.cancellation_requested = False
            
            # Initialize persistent threading system for async operations
            self.threading_service = get_global_threading_service()
            self.persistent_thread_pool = get_global_persistent_thread_pool()
            
            # Track active operations
            self._active_operations = set()
            
            # Initialize official Ollama client if available
            if OLLAMA_LIBRARY_AVAILABLE:
                try:
                    # Try to set the host for the official library (may not be available in all versions)
                    if hasattr(ollama, 'set_host'):
                        ollama.set_host(self.base_url)
                        logger.info(f"[ID:0017] Official Ollama client initialized with host: {self.base_url}")
                    else:
                        logger.info(f"[ID:0017] Official Ollama client available but set_host not supported")
                except Exception as e:
                    logger.warning(f"[ID:0018] Failed to initialize official Ollama client: {e}")
            
            LoggingHelpers.log_service_initialization("OllamaService", True)
        except Exception as e:
            LoggingHelpers.log_service_initialization("OllamaService", False, e)
            raise
    
    def get_models(self) -> List[str]:
        """Get list of available models from Ollama using the best available method"""
        if OLLAMA_LIBRARY_AVAILABLE:
            return self._get_models_with_library()
        else:
            return self._get_models_with_requests()
    
    def _get_models_with_library(self) -> List[str]:
        """Get models using the official Ollama library"""
        try:
            LoggingHelpers.log_network_request(f"{self.base_url}/tags", "GET")
            logger.debug(f"[ID:0019] Using official library to get models from: {self.base_url}")
            
            models = ollama.list()
            model_names = []
            
            # Handle different response formats from the official library
            # Some versions return an object with .models attribute, others return a dict
            if hasattr(models, 'models'):
                # Object format with .models attribute
                for model in models.models:
                    # Try different possible attribute names for the model name
                    if hasattr(model, 'name'):
                        model_names.append(model.name)
                    elif hasattr(model, 'model'):
                        model_names.append(model.model)
                    elif hasattr(model, 'id'):
                        model_names.append(model.id)
                    else:
                        # Fallback: try to get the name from the model object's dict representation
                        model_dict = model.dict() if hasattr(model, 'dict') else model.__dict__
                        model_name = model_dict.get('name') or model_dict.get('model') or model_dict.get('id')
                        if model_name:
                            model_names.append(model_name)
            elif isinstance(models, dict) and 'models' in models:
                # Dict format with 'models' key
                for model in models['models']:
                    if isinstance(model, dict):
                        model_name = model.get('name') or model.get('model') or model.get('id')
                        if model_name:
                            model_names.append(model_name)
                    else:
                        # Handle case where model might be a string
                        model_names.append(str(model))
            else:
                # Unknown format, try to extract models from the response
                logger.warning(f"[ID:0020A] Unknown models response format: {type(models)}")
                if isinstance(models, dict):
                    # Try to find models in the dict
                    for key, value in models.items():
                        if isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict) and ('name' in item or 'model' in item):
                                    model_name = item.get('name') or item.get('model')
                                    if model_name:
                                        model_names.append(model_name)
            
            self.model_list_updated.emit(model_names)
            LoggingHelpers.log_info_with_context("Successfully retrieved models using official library", {"count": len(model_names)})
            return model_names
            
        except Exception as e:
            logger.debug(f"[ID:0020] Official library failed, falling back to requests: {e}")
            LoggingHelpers.log_exception_with_context("get_models_with_library", e, {"base_url": self.base_url})
            # Fall back to requests method
            return self._get_models_with_requests()
    
    def _get_models_with_requests(self) -> List[str]:
        """Get models using requests (fallback method)"""
        try:
            LoggingHelpers.log_network_request(f"{self.base_url}/api/tags", "GET")
            logger.debug(f"[ID:0013] DEBUG: Attempting to connect to Ollama at: {self.base_url}/api/tags")
            
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)  # Add timeout
            logger.debug(f"[ID:0012] DEBUG: Response status: {response.status_code}")
            
            LoggingHelpers.log_network_request(f"{self.base_url}/api/tags", "GET", response.status_code)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.debug(f"[ID:0011] DEBUG: Response data: {data}")
                    model_names = [model['name'] for model in data.get('models', [])]
                    self.model_list_updated.emit(model_names)
                    LoggingHelpers.log_info_with_context("Successfully retrieved models using requests", {"count": len(model_names)})
                    return model_names
                except json.JSONDecodeError as e:
                    LoggingHelpers.log_exception_with_context("JSON parsing in get_models", e, {"response_text": response.text})
                    error_msg = f"Invalid JSON response from Ollama: {e}"
                    self.model_operation_error.emit(error_msg)
                    return []
            else:
                logger.debug(f"[ID:0010] DEBUG: Error response: {response.text}")
                error_msg = f"Error fetching models (HTTP {response.status_code}). Is Ollama running?"
                self.model_operation_error.emit(error_msg)
                return []
                
        except requests.exceptions.ConnectionError as e:
            logger.debug(f"[ID:0009] DEBUG: Connection error: {e}", print_to_terminal=True)
            LoggingHelpers.log_network_request(f"{self.base_url}/tags", "GET", error=e)
            error_msg = "Cannot connect to Ollama. Make sure it's running on localhost:11434"
            self.model_operation_error.emit(error_msg)
            return []
        except requests.exceptions.Timeout as e:
            logger.debug(f"[ID:0008] DEBUG: Timeout error: {e}", print_to_terminal=True)
            LoggingHelpers.log_network_request(f"{self.base_url}/tags", "GET", error=e)
            error_msg = "Connection to Ollama timed out. Is it running and responding?"
            self.model_operation_error.emit(error_msg)
            return []
        except Exception as e:
            logger.debug(f"[ID:0007] DEBUG: Unexpected error: {e}", print_to_terminal=True)
            LoggingHelpers.log_exception_with_context("get_models", e, {"base_url": self.base_url})
            error_msg = f"Unexpected error connecting to Ollama: {e}"
            self.model_operation_error.emit(error_msg)
            return []
    
    def test_connection(self) -> bool:
        """Test if Ollama is running and accessible without emitting signals"""
        if OLLAMA_LIBRARY_AVAILABLE:
            try:
                # Try with official library first
                models = ollama.list()
                # Handle different response formats from the official library
                # Some versions return an object with .models attribute, others return a dict
                if hasattr(models, 'models'):
                    return len(models.models) >= 0
                elif isinstance(models, dict) and 'models' in models:
                    return len(models['models']) >= 0
                else:
                    # If we can't determine the format, assume it's working if we got a response
                    return True
            except Exception:
                # Fall back to requests
                pass
        
        try:
            LoggingHelpers.log_network_request(f"{self.base_url}/api/tags", "GET")
            response = requests.get(f"{self.base_url}/api/tags", timeout=3)
            success = response.status_code == 200
            LoggingHelpers.log_network_request(f"{self.base_url}/api/tags", "GET", response.status_code)
            return success
        except Exception as e:
            LoggingHelpers.log_network_request(f"{self.base_url}/api/tags", "GET", error=e)
            return False
    
    def send_chat_message(self, model: str, messages: List[Dict], 
                         temperature: float = 0.7, stream: bool = True,
                         session_variables: Optional[Dict] = None) -> Generator[str, None, None]:
        """
        Send a chat message to Ollama and yield streaming responses.
        Uses the official library if available, otherwise falls back to requests.
        
        Args:
            model: The model to use
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            stream: Whether to stream the response
            session_variables: Optional session variables to apply
            
        Yields:
            Response chunks as they arrive
        """
        if OLLAMA_LIBRARY_AVAILABLE:
            yield from self._send_chat_message_with_library(model, messages, temperature, stream, session_variables)
        else:
            yield from self._send_chat_message_with_requests(model, messages, temperature, stream, session_variables)
    
    def _send_chat_message_with_library(self, model: str, messages: List[Dict], 
                                       temperature: float = 0.7, stream: bool = True,
                                       session_variables: Optional[Dict] = None) -> Generator[str, None, None]:
        """Send chat message using the official Ollama library"""
        start_time = time.time()
        
        try:
            # Check for cancellation before starting
            if self.cancellation_requested:
                LoggingHelpers.log_debug("Request cancelled before sending")
                return
            
            # Build comprehensive system prompt if available
            system_prompt = self._extract_system_prompt(messages)
            
            # Prepare the request data for the library
            request_data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "top_p": 0.9,
                "stream": stream,
            }
            
            # Add session variables if provided
            if session_variables:
                try:
                    session_commands = self._build_session_commands(session_variables)
                    if session_commands:
                        session_system_message = "\n".join(session_commands)
                        request_data["messages"].insert(0, {"role": "system", "content": session_system_message})
                        logger.debug(f"[ID:0021] SESSION: Sending session commands: {session_commands}")
                except Exception as e:
                    LoggingHelpers.log_exception_with_context("session_variables processing", e, {"session_variables": session_variables})
            
            # Log the user's message (last user message in the list)
            user_message = next((m['content'] for m in reversed(messages) if m.get('role') == 'user'), None)
            if user_message:
                logger.info(f"[ID:0004] User: {user_message}")
            
            # Check for cancellation before making the request
            if self.cancellation_requested:
                LoggingHelpers.log_debug("Request cancelled before library call")
                return
                
            logger.debug(f"[ID:0022] ====================SENDING TO OLLAMA (LIBRARY)====================\n{json.dumps(request_data, indent=2)}\n=========================================================")

            LoggingHelpers.log_network_request(f"{self.base_url}/chat", "POST")
            
            try:
                # Create options object with temperature and top_p
                options = ollama.Options(temperature=temperature, top_p=0.9)
                
                if stream:
                    # Use streaming with the library
                    for chunk in ollama.chat(model=model, messages=messages, stream=True, options=options):
                        if self.cancellation_requested:
                            break
                        
                        content = chunk.get("message", {}).get("content", "")
                        if content:
                            logger.info(f"[ID:0002] AI: {content}")
                        yield content
                else:
                    # Non-streaming response
                    response = ollama.chat(model=model, messages=messages, stream=False, options=options)
                    content = response.get("message", {}).get("content", "")
                    if content:
                        logger.info(f"[ID:0001] AI: {content}")
                    yield content
                    
            except Exception as e:
                LoggingHelpers.log_exception_with_context("Library chat request", e, {"model": model})
                # Fall back to requests method
                logger.debug(f"[ID:0023] Library failed, falling back to requests: {e}")
                yield from self._send_chat_message_with_requests(model, messages, temperature, stream, session_variables)
                
        except Exception as e:
            LoggingHelpers.log_exception_with_context("send_chat_message_with_library", e, {"model": model})
            yield f"Error: {e}"
    
    def _send_chat_message_with_requests(self, model: str, messages: List[Dict], 
                                       temperature: float = 0.7, stream: bool = True,
                                       session_variables: Optional[Dict] = None) -> Generator[str, None, None]:
        """Send chat message using requests (fallback method)"""
        start_time = time.time()
        
        try:
            # Check for cancellation before starting
            if self.cancellation_requested:
                LoggingHelpers.log_debug("Request cancelled before sending")
                return
            
            # Build comprehensive system prompt if available
            system_prompt = self._extract_system_prompt(messages)
            
            # Prepare the request data
            data = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "top_p": 0.9,
                "stream": stream,
            }
            logger.debug(f"[ID:0006] DEBUG: Sending data: {data}")
            
            # Add session variables if provided
            if session_variables:
                try:
                    session_commands = self._build_session_commands(session_variables)
                    if session_commands:
                        session_system_message = "\n".join(session_commands)
                        data["messages"].insert(0, {"role": "system", "content": session_system_message})
                        logger.debug(f"[ID:0005] SESSION: Sending session commands: {session_commands}")
                except Exception as e:
                    LoggingHelpers.log_exception_with_context("session_variables processing", e, {"session_variables": session_variables})
            
            # Log the user's message (last user message in the list)
            user_message = next((m['content'] for m in reversed(messages) if m.get('role') == 'user'), None)
            if user_message:
                logger.info(f"[ID:0004] User: {user_message}")
            
            # Check for cancellation before making the request
            if self.cancellation_requested:
                LoggingHelpers.log_debug("Request cancelled before network call")
                return
                
            logger.debug(f"[ID:0003] ====================SENDING TO OLLAMA====================\n{json.dumps(data, indent=2)}\n=========================================================")

            url = f"{self.base_url}/chat"
            LoggingHelpers.log_network_request(url, "POST")
            
            try:
                with requests.post(url, json=data, stream=stream, timeout=120) as response:
                    response.raise_for_status()
                    LoggingHelpers.log_network_request(url, "POST", response.status_code)
                    
                    if stream:
                        for line in response.iter_lines(decode_unicode=True):
                            if line and not self.cancellation_requested:
                                try:
                                    # Each line is a JSON object with a 'content' field
                                    chunk = json.loads(line)
                                    content = chunk.get("message", {}).get("content", "")
                                    if content:
                                        logger.info(f"[ID:0002] AI: {content}")
                                    yield content
                                except json.JSONDecodeError as e:
                                    LoggingHelpers.log_exception_with_context("JSON parsing in streaming response", e, {"line": line})
                                    continue
                                except Exception as e:
                                    LoggingHelpers.log_exception_with_context("Streaming response processing", e, {"line": line})
                                    continue
                    else:
                        # Non-streaming response
                        try:
                            data = response.json()
                            content = data.get("message", {}).get("content", "")
                            if content:
                                logger.info(f"[ID:0001] AI: {content}")
                            yield content
                        except json.JSONDecodeError as e:
                            LoggingHelpers.log_exception_with_context("JSON parsing in non-streaming response", e, {"response_text": response.text})
                            yield "Error: Invalid response from Ollama"
                            
            except requests.exceptions.ConnectionError as e:
                LoggingHelpers.log_network_request(url, "POST", error=e)
                yield "Cannot connect to Ollama. Make sure it's running."
            except requests.exceptions.Timeout as e:
                LoggingHelpers.log_network_request(url, "POST", error=e)
                yield "Connection to Ollama timed out."
            except Exception as e:
                LoggingHelpers.log_exception_with_context("send_chat_message_with_requests", e, {"model": model})
                yield f"Error: {e}"
                
        except Exception as e:
            LoggingHelpers.log_exception_with_context("send_chat_message_with_requests", e, {"model": model})
            yield f"Error: {e}"
    
    def pull_model(self, model_name: str) -> None:
        """Pull a model from Ollama using the best available method"""
        if not model_name.strip():
            self.model_operation_error.emit("Please enter a model name")
            return
        
        self.model_operation_started.emit(f"Pulling model: {model_name}")
        
        # Create data processing task for model pull operation
        task = DataProcessingTask(
            data={"model_name": model_name, "operation": "pull"},
            operation="model_pull",
            base_url=self.base_url,
            cancellation_requested=self.cancellation_requested,
            progress_callback=self.model_operation_progress.emit,
            error_callback=self.model_operation_error.emit,
            success_callback=self.model_operation_finished.emit
        )
        
        # Submit to persistent thread pool using threading service
        task_id = self.threading_service.process_data(
            data={"model_name": model_name, "operation": "pull"},
            operation="model_pull"
        )
        self._active_operations.add(task_id)
        
        logger.debug(f"[DEBUG] Scheduled model pull task: {task_id}")

    def _pull_model_thread(self, model_name: str) -> None:
        """Background thread for pulling models"""
        try:
            LoggingHelpers.log_thread_operation("pull_model_thread", f"pull {model_name}", True)
            
            if OLLAMA_LIBRARY_AVAILABLE:
                # Try with official library first
                try:
                    logger.info(f"[ID:0024] Using official library to pull model: {model_name}")
                    ollama.pull(model_name)
                    LoggingHelpers.log_thread_operation("pull_model_thread", f"pull {model_name}", True)
                    self.model_operation_finished.emit(f"Successfully pulled model: {model_name}")
                    return
                except Exception as e:
                    logger.debug(f"[ID:0025] Library pull failed, falling back to subprocess: {e}")
            
            # Fall back to subprocess method
            command = ["ollama", "pull", model_name]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, universal_newlines=True, encoding='utf-8', 
                                     errors='replace', bufsize=1)

            for line in iter(process.stdout.readline, ''):
                if self.cancellation_requested:
                    process.terminate()
                    LoggingHelpers.log_debug("Model pull cancelled by user")
                    break
                self.model_operation_progress.emit(line.strip())
            
            process.stdout.close()
            return_code = process.wait()
            
            if return_code:
                error_msg = f"Error pulling model (exit code: {return_code})."
                LoggingHelpers.log_thread_operation("pull_model_thread", f"pull {model_name}", False, Exception(error_msg))
                self.model_operation_error.emit(error_msg)
            else:
                LoggingHelpers.log_thread_operation("pull_model_thread", f"pull {model_name}", True)
                self.model_operation_finished.emit(f"Successfully pulled model: {model_name}")

        except FileNotFoundError as e:
            LoggingHelpers.log_thread_operation("pull_model_thread", f"pull {model_name}", False, e)
            self.model_operation_error.emit("Ollama command not found. Is it installed and in your PATH?")
        except Exception as e:
            LoggingHelpers.log_thread_operation("pull_model_thread", f"pull {model_name}", False, e)
            self.model_operation_error.emit(f"An error occurred: {str(e)}")
        finally:
            self.model_operation_finished.emit("pull")
    
    def remove_model(self, model_name: str) -> None:
        """Remove a model from Ollama using the best available method"""
        if not model_name.strip():
            self.model_operation_error.emit("Please enter a model name")
            return
        
        self.model_operation_started.emit(f"Removing model: {model_name}")
        
        # Create data processing task for model remove operation
        task = DataProcessingTask(
            data={"model_name": model_name, "operation": "remove"},
            operation="model_remove",
            base_url=self.base_url,
            cancellation_requested=self.cancellation_requested,
            progress_callback=self.model_operation_progress.emit,
            error_callback=self.model_operation_error.emit,
            success_callback=self.model_operation_finished.emit
        )
        
        # Submit to persistent thread pool using threading service
        task_id = self.threading_service.process_data(
            data={"model_name": model_name, "operation": "remove"},
            operation="model_remove"
        )
        self._active_operations.add(task_id)
        
        logger.debug(f"[DEBUG] Scheduled model remove task: {task_id}")

    def _remove_model_thread(self, model_name: str) -> None:
        """Background thread for removing models"""
        try:
            LoggingHelpers.log_thread_operation("remove_model_thread", f"remove {model_name}", True)
            
            if OLLAMA_LIBRARY_AVAILABLE:
                # Try with official library first
                try:
                    logger.info(f"[ID:0026] Using official library to remove model: {model_name}")
                    ollama.delete(model_name)
                    LoggingHelpers.log_thread_operation("remove_model_thread", f"remove {model_name}", True)
                    self.model_operation_finished.emit(f"Successfully removed model: {model_name}")
                    return
                except Exception as e:
                    logger.debug(f"[ID:0027] Library remove failed, falling back to subprocess: {e}")
            
            # Fall back to subprocess method
            command = ["ollama", "rm", model_name]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, universal_newlines=True, encoding='utf-8', 
                                     errors='replace', bufsize=1)

            for line in iter(process.stdout.readline, ''):
                if self.cancellation_requested:
                    process.terminate()
                    LoggingHelpers.log_debug("Model removal cancelled by user")
                    break
                self.model_operation_progress.emit(line.strip())
            
            process.stdout.close()
            return_code = process.wait()
            
            if return_code:
                error_msg = f"Error removing model (exit code: {return_code})."
                LoggingHelpers.log_thread_operation("remove_model_thread", f"remove {model_name}", False, Exception(error_msg))
                self.model_operation_error.emit(error_msg)
            else:
                LoggingHelpers.log_thread_operation("remove_model_thread", f"remove {model_name}", True)
                self.model_operation_finished.emit(f"Successfully removed model: {model_name}")

        except FileNotFoundError as e:
            LoggingHelpers.log_thread_operation("remove_model_thread", f"remove {model_name}", False, e)
            self.model_operation_error.emit("Ollama command not found. Is it installed and in your PATH?")
        except Exception as e:
            LoggingHelpers.log_thread_operation("remove_model_thread", f"remove {model_name}", False, e)
            self.model_operation_error.emit(f"An error occurred: {str(e)}")
        finally:
            self.model_operation_finished.emit("remove")
    
    def update_model(self, model_name: str) -> None:
        """Update a model from Ollama using the best available method"""
        if not model_name.strip():
            self.model_operation_error.emit("Please enter a model name")
            return
        
        self.model_operation_started.emit(f"Updating model: {model_name}")
        
        # Create data processing task for model update operation
        task = DataProcessingTask(
            data={"model_name": model_name, "operation": "update"},
            operation="model_update",
            base_url=self.base_url,
            cancellation_requested=self.cancellation_requested,
            progress_callback=self.model_operation_progress.emit,
            error_callback=self.model_operation_error.emit,
            success_callback=self.model_operation_finished.emit
        )
        
        # Submit to persistent thread pool using threading service
        task_id = self.threading_service.process_data(
            data={"model_name": model_name, "operation": "update"},
            operation="model_update"
        )
        self._active_operations.add(task_id)
        
        logger.debug(f"[DEBUG] Scheduled model update task: {task_id}")

    def _update_model_thread(self, model_name: str) -> None:
        """Background thread for updating models"""
        try:
            LoggingHelpers.log_thread_operation("update_model_thread", f"update {model_name}", True)
            
            if OLLAMA_LIBRARY_AVAILABLE:
                # Try with official library first (update is same as pull)
                try:
                    logger.info(f"[ID:0028] Using official library to update model: {model_name}")
                    ollama.pull(model_name)  # Update is same as pull
                    LoggingHelpers.log_thread_operation("update_model_thread", f"update {model_name}", True)
                    self.model_operation_finished.emit(f"Successfully updated model: {model_name}")
                    return
                except Exception as e:
                    logger.debug(f"[ID:0029] Library update failed, falling back to subprocess: {e}")
            
            # Fall back to subprocess method
            command = ["ollama", "pull", model_name]  # Update is same as pull
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, universal_newlines=True, encoding='utf-8', 
                                     errors='replace', bufsize=1)

            for line in iter(process.stdout.readline, ''):
                if self.cancellation_requested:
                    process.terminate()
                    LoggingHelpers.log_debug("Model update cancelled by user")
                    break
                self.model_operation_progress.emit(line.strip())
            
            process.stdout.close()
            return_code = process.wait()
            
            if return_code:
                error_msg = f"Error updating model (exit code: {return_code})."
                LoggingHelpers.log_thread_operation("update_model_thread", f"update {model_name}", False, Exception(error_msg))
                self.model_operation_error.emit(error_msg)
            else:
                LoggingHelpers.log_thread_operation("update_model_thread", f"update {model_name}", True)
                self.model_operation_finished.emit(f"Successfully updated model: {model_name}")

        except FileNotFoundError as e:
            LoggingHelpers.log_thread_operation("update_model_thread", f"update {model_name}", False, e)
            self.model_operation_error.emit("Ollama command not found. Is it installed and in your PATH?")
        except Exception as e:
            LoggingHelpers.log_thread_operation("update_model_thread", f"update {model_name}", False, e)
            self.model_operation_error.emit(f"An error occurred: {str(e)}")
        finally:
            self.model_operation_finished.emit("update")
    
    def _extract_system_prompt(self, messages: List[Dict]) -> str:
        """Extract system prompt from messages"""
        try:
            system_messages = [msg for msg in messages if msg.get('role') == 'system']
            return system_messages[0]['content'] if system_messages else ""
        except Exception as e:
            LoggingHelpers.log_exception_with_context("extract_system_prompt", e, {"messages_count": len(messages)})
            return ""
    
    def _build_session_commands(self, session_variables: Dict) -> List[str]:
        """Build session commands from variables"""
        try:
            commands = []
            for key, value in session_variables.items():
                if isinstance(value, (str, int, float, bool)):
                    commands.append(f"/set {key} {value}")
                elif isinstance(value, list):
                    commands.append(f"/set {key} {','.join(map(str, value))}")
                elif isinstance(value, dict):
                    commands.append(f"/set {key} {json.dumps(value)}")
            return commands
        except Exception as e:
            LoggingHelpers.log_exception_with_context("build_session_commands", e, {"session_variables": session_variables})
            return []
    
    def cancel_request(self) -> None:
        """Cancel any ongoing request"""
        self.cancellation_requested = True
        self.request_in_progress = False
        logger.debug("[DEBUG] Request cancellation requested")
    
    def reset_cancellation(self) -> None:
        """Reset cancellation flag"""
        self.cancellation_requested = False
        logger.debug("[DEBUG] Cancellation flag reset")
    
    def is_connected(self) -> bool:
        """Check if Ollama is running and accessible"""
        return self.test_connection()
    
    def cleanup(self):
        """Clean up resources and stop all active operations"""
        try:
            logger.debug("[DEBUG] Cleaning up Ollama service")
            
            # Cancel any ongoing operations
            self.cancellation_requested = True
            
            # Wait for active operations to complete
            if self._active_operations:
                logger.debug(f"[DEBUG] Waiting for {len(self._active_operations)} active operations to complete")
                # Use threading service to wait for tasks
                if hasattr(self, 'threading_service') and self.threading_service:
                    # The threading service handles its own cleanup
                    pass
            
            # Clean up persistent thread pool (handled by global shutdown)
            if hasattr(self, 'persistent_thread_pool') and self.persistent_thread_pool:
                # The persistent thread pool is managed globally
                pass
            
            logger.debug("[DEBUG] Ollama service cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during Ollama service cleanup: {e}")
            logger.error(traceback.format_exc()) 