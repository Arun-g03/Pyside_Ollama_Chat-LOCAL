from PySide6.QtCore import QObject, Signal, QThread
import requests
import json
import time
import traceback
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class Worker(QObject):
    update_message_signal = Signal(str)
    stream_chunk_signal = Signal(str)
    finished_signal = Signal()
    error_signal = Signal(str)  # New signal for detailed error reporting
    progress_signal = Signal(str)  # Signal for progress updates

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self._should_stop = False
        self._thread_id = None
        self._start_time = None
        self._request_count = 0
        
        # Log worker creation
        logger.debug(f"[ID:0136] Worker created with parent: {parent}")
        logger.debug(f"[ID:0135] Worker thread ID: {QThread.currentThread().objectName() or 'unnamed'}")
    
    def _log_thread_info(self, action: str):
        """Log thread information for debugging"""
        current_thread = QThread.currentThread()
        thread_name = current_thread.objectName() or 'unnamed'
        thread_id = id(current_thread)
        logger.debug(f"[ID:0134] Worker {action} - Thread: {thread_name} (ID: {thread_id})")
    
    def run(self, message):
        """
        Run the worker task.
        """
        try:
            self._log_thread_info("run started")
            self._running = True
            self._start_time = time.time()
            self._request_count += 1
            
            logger.debug(f"[ID:0133] Worker run started - Message: {message[:50]}...")
            
            # Simulate long-running task or response fetching
            response = message
            self.update_message_signal.emit(response)
            
            duration = time.time() - self._start_time
            logger.debug(f"[ID:0132] Worker run completed - Duration: {duration:.2f}s")
            
        except Exception as e:
            error_msg = f"Worker run error: {str(e)}"
            logger.error(f"[ID:0131] {error_msg}")
            logger.error(f"[ID:0130] Worker run traceback: {traceback.format_exc()}")
            self.error_signal.emit(error_msg)
            self.update_message_signal.emit(f"Error: {str(e)}")
        finally:
            self._running = False
            self._start_time = None
            self._log_thread_info("run finished")
            self.finished_signal.emit()

    def stop(self):
        """
        Stop the worker safely.
        """
        try:
            self._log_thread_info("stop requested")
            logger.debug(f"[ID:0129] Worker stop requested - Running: {self._running}")
            
            self._running = False
            self._should_stop = True
            
            # Give the worker a moment to finish naturally
            if self._running:
                logger.debug("[ID:0128] Waiting for worker to finish naturally...")
                time.sleep(0.1)
            
            logger.debug("[ID:0127] Worker stop completed")
            
        except Exception as e:
            logger.error(f"[ID:0126] Error stopping worker: {e}")
            logger.error(f"[ID:0125] Worker stop traceback: {traceback.format_exc()}")

    def is_running(self):
        """
        Check if the worker is currently running.
        """
        return self._running

    def run_stream(
        self,
        messages,
        model,
        temperature,
        ollama_url,
        max_tokens,
        top_p,
        frequency_penalty,
        presence_penalty
    ):
        self._log_thread_info("run_stream started")
        self._running = True
        self._should_stop = False
        self._start_time = time.time()
        self._request_count += 1
        
        logger.debug(f"[ID:0124] Worker run_stream started")
        logger.debug(f"[ID:0123] Model: {model}, Temperature: {temperature}")
        logger.debug(f"[ID:0122] Ollama URL: {ollama_url}")
        logger.debug(f"[ID:0121] Messages count: {len(messages)}")
        
        # Use the correct API endpoint
        base_url = ollama_url.replace('/api', '') if ollama_url.endswith('/api') else ollama_url
        url = f"{base_url}/api/chat"
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stream": True
        }
        
        logger.debug(f"[ID:0120] Making streaming request to: {url}")
        logger.debug(f"[ID:0119] Request data: {json.dumps(data, indent=2)}")
        
        # Emit progress signal
        self.progress_signal.emit("Testing connection to Ollama...")
        
        # Test connection first with better error handling
        try:
            test_response = requests.get(f"{base_url}/api/tags", timeout=10)
            if test_response.status_code != 200:
                raise requests.exceptions.RequestException(f"Ollama not responding properly: {test_response.status_code}")
            logger.debug(f"[ID:0118] Ollama connection test successful")
            self.progress_signal.emit("Connection successful, sending request...")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"[ID:0117] Ollama connection test failed - Connection Error: {e}")
            error_msg = "Cannot connect to Ollama. Please make sure Ollama is running on localhost:11434"
            self.error_signal.emit(error_msg)
            self.update_message_signal.emit(f"Error: {error_msg}")
            return
        except requests.exceptions.Timeout as e:
            logger.error(f"[ID:0117] Ollama connection test failed - Timeout: {e}")
            error_msg = "Ollama connection timed out. Please check if Ollama is running and responding."
            self.error_signal.emit(error_msg)
            self.update_message_signal.emit(f"Error: {error_msg}")
            return
        except Exception as e:
            logger.error(f"[ID:0117] Ollama connection test failed - Unexpected error: {e}")
            error_msg = f"Ollama connection failed: {str(e)}"
            self.error_signal.emit(error_msg)
            self.update_message_signal.emit(f"Error: {error_msg}")
            return
        
        # Use timeout to prevent hanging - increased timeout for slower models
        logger.debug(f"[ID:0119] Making POST request to {url} with timeout 120s")
        try:
            with requests.post(url, json=data, stream=True, timeout=120) as response:
                response.raise_for_status()
                logger.debug(f"[ID:0118] Stream response received - Status: {response.status_code}")
                self.progress_signal.emit("Receiving response...")
                
                # Add debugging for response headers
                logger.debug(f"[ID:0117] Response headers: {dict(response.headers)}")
                logger.debug(f"[ID:0116] Response encoding: {response.encoding}")
                
                chunk_count = 0
                logger.debug(f"[ID:0115] Starting to process streaming response...")
                logger.debug(f"[ID:0114] About to iterate over response lines...")
                
                # Add a timeout mechanism for the streaming loop
                start_time = time.time()
                timeout_seconds = 10  # 30 second timeout for receiving first chunk
                
                for line in response.iter_lines(decode_unicode=True):
                    if self._should_stop:
                        logger.debug("[ID:0116] Worker stop requested during streaming")
                        break
                    
                    # Check for timeout
                    if chunk_count == 0 and (time.time() - start_time) > timeout_seconds:
                        logger.error(f"[ID:0115] Timeout waiting for first response chunk after {timeout_seconds}s")
                        error_msg = f"Timeout waiting for response from Ollama after {timeout_seconds} seconds"
                        self.error_signal.emit(error_msg)
                        self.update_message_signal.emit(f"Error: {error_msg}")
                        return
                    
                    if line:
                        logger.debug(f"[ID:0114] Received line: {line[:100]}...")  # Log first 100 chars
                        try:
                            chunk = json.loads(line)
                            content = chunk.get("message", {}).get("content", "")
                            chunk_count += 1
                            
                            if content:
                                self.stream_chunk_signal.emit(content)
                                if chunk_count % 10 == 0:  # Log every 10th chunk
                                    logger.debug(f"[ID:0113] Streamed {chunk_count} chunks")
                            
                            if chunk.get("done", False):
                                logger.debug(f"[ID:0112] Stream completed - Total chunks: {chunk_count}")
                                break
                                
                        except json.JSONDecodeError as e:
                            logger.warning(f"[ID:0111] JSON decode error in stream chunk: {e}")
                            # Skip malformed JSON lines
                            continue
                        except Exception as e:
                            logger.error(f"[ID:0110] Error processing stream chunk: {e}")
                            continue
                    else:
                        logger.debug(f"[ID:0109] Received empty line")
                
                duration = time.time() - self._start_time
                logger.debug(f"[ID:0113] Stream completed - Duration: {duration:.2f}s, Chunks: {chunk_count}")
                
        except requests.exceptions.Timeout:
            error_msg = "Request timed out after 120 seconds"
            logger.error(f"[ID:0112] {error_msg}")
            logger.error(f"[ID:0111] Timeout occurred for URL: {url}")
            self.error_signal.emit(error_msg)
            self.update_message_signal.emit(f"Error: {error_msg}")
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection lost: {str(e)}"
            logger.error(f"[ID:0111] {error_msg}")
            self.error_signal.emit(error_msg)
            self.update_message_signal.emit(f"Error: {error_msg}")
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error: {str(e)}"
            logger.error(f"[ID:0110] {error_msg}")
            logger.error(f"[ID:0109] Request error traceback: {traceback.format_exc()}")
            self.error_signal.emit(error_msg)
            self.update_message_signal.emit(f"Error: {str(e)}")
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"[ID:0108] {error_msg}")
            logger.error(f"[ID:0107] Unexpected error traceback: {traceback.format_exc()}")
            self.error_signal.emit(error_msg)
            self.update_message_signal.emit(f"Error: {str(e)}")
        finally:
            self._running = False
            self._should_stop = False
            self._start_time = None
            self._log_thread_info("run_stream finished")
            self.finished_signal.emit()
    
    def get_stats(self) -> dict:
        """Get worker statistics for debugging"""
        return {
            "running": self._running,
            "should_stop": self._should_stop,
            "request_count": self._request_count,
            "thread_id": id(QThread.currentThread()),
            "thread_name": QThread.currentThread().objectName() or "unnamed"
        }
