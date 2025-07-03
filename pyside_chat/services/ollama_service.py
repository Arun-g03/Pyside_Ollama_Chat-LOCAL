"""
Ollama Service - Extracted from ollama_chat.py
Handles all communication with the Ollama API.
"""

import json
import requests
import subprocess
from threading import Thread
from typing import List, Dict, Optional, Generator
from PySide6.QtCore import QObject, Signal
from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)
logger.info("OllamaService logger initialized")


class OllamaService(QObject):
    """Service for handling all Ollama API communication"""
    
    # Signals for async operations
    model_list_updated = Signal(list)  # Emits list of model names
    model_operation_started = Signal(str)  # Emits operation name
    model_operation_finished = Signal(str)  # Emits operation name
    model_operation_progress = Signal(str)  # Emits progress message
    model_operation_error = Signal(str)  # Emits error message
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        super().__init__()
        self.base_url = base_url.rstrip('/')
        self.request_in_progress = False
        self.cancellation_requested = False
    
    def get_models(self) -> List[str]:
        """Get list of available models from Ollama"""
        try:
            logger.debug(f" DEBUG: Attempting to connect to Ollama at: {self.base_url}/tags")
            response = requests.get(f"{self.base_url}/tags", timeout=5)  # Add timeout
            logger.debug(f" DEBUG: Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.debug(f"DEBUG: Response data: {data}")
                model_names = [model['name'] for model in data.get('models', [])]
                self.model_list_updated.emit(model_names)
                return model_names
            else:
                logger.debug(f" DEBUG: Error response: {response.text}")
                error_msg = f"Error fetching models (HTTP {response.status_code}). Is Ollama running?"
                self.model_operation_error.emit(error_msg)
                return []
                
        except requests.exceptions.ConnectionError as e:
            logger.debug(f" DEBUG: Connection error: {e}", print_to_terminal=True)
            error_msg = "Cannot connect to Ollama. Make sure it's running on localhost:11434"
            self.model_operation_error.emit(error_msg)
            return []
        except requests.exceptions.Timeout as e:
            logger.debug(f" DEBUG: Timeout error: {e}", print_to_terminal=True)
            error_msg = "Connection to Ollama timed out. Is it running and responding?"
            self.model_operation_error.emit(error_msg)
            return []
        except Exception as e:
            logger.debug(f" DEBUG: Unexpected error: {e}", print_to_terminal=True)
            error_msg = f"Unexpected error connecting to Ollama: {e}"
            self.model_operation_error.emit(error_msg)
            return []
    
    def test_connection(self) -> bool:
        """Test if Ollama is running and accessible without emitting signals"""
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def send_chat_message(self, model: str, messages: List[Dict], 
                         temperature: float = 0.7, stream: bool = True,
                         session_variables: Optional[Dict] = None) -> Generator[str, None, None]:
        """
        Send a chat message to Ollama and yield streaming responses.
        
        Args:
            model: The model to use
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            stream: Whether to stream the response
            session_variables: Optional session variables to apply
            
        Yields:
            Response chunks as they arrive
        """
        # Check for cancellation before starting
        if self.cancellation_requested:
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
        logger.debug(f" DEBUG: Sending data: {data}")
        # Add session variables if provided
        if session_variables:
            session_commands = self._build_session_commands(session_variables)
            if session_commands:
                session_system_message = "\n".join(session_commands)
                data["messages"].insert(0, {"role": "system", "content": session_system_message})
                logger.debug(f" SESSION: Sending session commands: {session_commands}")
        
        # Log the user's message (last user message in the list)
        user_message = next((m['content'] for m in reversed(messages) if m.get('role') == 'user'), None)
        if user_message:
            logger.info(f"User: {user_message}")
        
        try:
            # Check for cancellation before making the request
            if self.cancellation_requested:
                return
                
            logger.debug("====================SENDING TO OLLAMA====================")
            logger.debug(json.dumps(data, indent=2))
            logger.debug("=========================================================")

            url = f"{self.base_url}/chat"
            
            with requests.post(url, json=data, stream=stream) as response:
                response.raise_for_status()
                
                if stream:
                    for line in response.iter_lines(decode_unicode=True):
                        if line and not self.cancellation_requested:
                            # Each line is a JSON object with a 'content' field
                            chunk = json.loads(line)
                            content = chunk.get("message", {}).get("content", "")
                            if content:
                                logger.info(f"AI: {content}")
                            yield content
                else:
                    # Non-streaming response
                    data = response.json()
                    content = data.get("message", {}).get("content", "")
                    if content:
                        logger.info(f"AI: {content}")
                    yield content
                    
        except requests.exceptions.ConnectionError:
            yield "Cannot connect to Ollama. Make sure it's running."
        except Exception as e:
            if not self.cancellation_requested:
                logger.debug(f"Error in send_chat_message: {e}", print_to_terminal=True)
                yield f"An error occurred while processing your request: {e}"
    
    def pull_model(self, model_name: str) -> None:
        """Pull a model from Ollama"""
        if not model_name.strip():
            self.model_operation_error.emit("Please enter a model name")
            return
        
        self.model_operation_started.emit(f"Pulling model: {model_name}")
        
        # Run in background thread
        thread = Thread(target=self._pull_model_thread, args=(model_name,), daemon=True)
        thread.start()
    
    def _pull_model_thread(self, model_name: str) -> None:
        """Background thread for pulling models"""
        try:
            command = ["ollama", "pull", model_name]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, universal_newlines=True, encoding='utf-8', 
                                     errors='replace', bufsize=1)

            for line in iter(process.stdout.readline, ''):
                if self.cancellation_requested:
                    process.terminate()
                    break
                self.model_operation_progress.emit(line.strip())
            
            process.stdout.close()
            return_code = process.wait()
            
            if return_code:
                self.model_operation_error.emit(f"Error pulling model (exit code: {return_code}).")
            else:
                self.model_operation_finished.emit(f"Successfully pulled model: {model_name}")

        except FileNotFoundError:
            self.model_operation_error.emit("Ollama command not found. Is it installed and in your PATH?")
        except Exception as e:
            self.model_operation_error.emit(f"An error occurred: {str(e)}")
        finally:
            self.model_operation_finished.emit("pull")
    
    def remove_model(self, model_name: str) -> None:
        """Remove a model from Ollama"""
        self.model_operation_started.emit(f"Removing model: {model_name}")
        
        # Run in background thread
        thread = Thread(target=self._remove_model_thread, args=(model_name,), daemon=True)
        thread.start()
    
    def _remove_model_thread(self, model_name: str) -> None:
        """Background thread for removing models"""
        try:
            result = subprocess.run(["ollama", "rm", model_name], 
                                  capture_output=True, text=True, encoding='utf-8', errors='replace')
            
            if result.stdout:
                self.model_operation_progress.emit(result.stdout.strip())
            if result.stderr:
                self.model_operation_progress.emit(result.stderr.strip())

            if result.returncode == 0:
                self.model_operation_progress.emit(f"Successfully removed model: {model_name}")
            else:
                self.model_operation_error.emit(f"Error removing model: {model_name}")
                
        except FileNotFoundError:
            self.model_operation_error.emit("Ollama command not found. Is it installed and in your PATH?")
        except Exception as e:
            self.model_operation_error.emit(f"An error occurred: {str(e)}")
        finally:
            self.model_operation_finished.emit("remove")
    
    def update_model(self, model_name: str) -> None:
        """Update a model in Ollama"""
        self.model_operation_started.emit(f"Updating model: {model_name}")
        
        # Run in background thread
        thread = Thread(target=self._update_model_thread, args=(model_name,), daemon=True)
        thread.start()
    
    def _update_model_thread(self, model_name: str) -> None:
        """Background thread for updating models"""
        try:
            result = subprocess.run(["ollama", "pull", model_name], 
                                  capture_output=True, text=True, encoding='utf-8', errors='replace')
            
            if result.stdout:
                self.model_operation_progress.emit(result.stdout.strip())
            if result.stderr:
                self.model_operation_progress.emit(result.stderr.strip())

            if result.returncode == 0:
                self.model_operation_progress.emit(f"Successfully updated model: {model_name}")
            else:
                self.model_operation_error.emit(f"Error updating model: {model_name}")
                
        except FileNotFoundError:
            self.model_operation_error.emit("Ollama command not found. Is it installed and in your PATH?")
        except Exception as e:
            self.model_operation_error.emit(f"An error occurred: {str(e)}")
        finally:
            self.model_operation_finished.emit("update")
    
    def _extract_system_prompt(self, messages: List[Dict]) -> str:
        """Extract system prompt from messages if present"""
        for message in messages:
            if message.get("role") == "system":
                return message.get("content", "")
        return ""
    
    def _build_session_commands(self, session_variables: Dict) -> List[str]:
        """Build session commands from session variables"""
        commands = []
        
        if not session_variables.get('history', True):
            commands.append("/set nohistory")
        else:
            commands.append("/set history")
            
        if not session_variables.get('wordwrap', True):
            commands.append("/set nowordwrap")
        else:
            commands.append("/set wordwrap")
            
        if session_variables.get('json_format', False):
            commands.append("/set format json")
        else:
            commands.append("/set noformat")
            
        if session_variables.get('verbose', False):
            commands.append("/set verbose")
        else:
            commands.append("/set quiet")
            
        if session_variables.get('think', False):
            commands.append("/set think")
        else:
            commands.append("/set nothink")
        
        return commands
    
    def cancel_request(self) -> None:
        """Cancel any ongoing request"""
        self.cancellation_requested = True
    
    def reset_cancellation(self) -> None:
        """Reset cancellation flag"""
        self.cancellation_requested = False
    
    def is_connected(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=5)
            return response.status_code == 200
        except:
            return False 