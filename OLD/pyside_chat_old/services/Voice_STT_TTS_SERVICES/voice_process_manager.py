"""
Voice Process Manager

Manages voice services in a separate process to improve performance and stability.
Handles communication between the main application and voice services via multiprocessing.
"""

import multiprocessing as mp
import pickle
import time
import os
import sys
from typing import Dict, Any, Optional, Callable
from PySide6.QtCore import QObject, Signal, QThread, QTimer
from PySide6.QtWidgets import QApplication
import queue
import traceback

from pyside_chat.utils.Logging.Custom_Logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class VoiceProcessManager(QObject):
    """Manages voice services in a separate process"""
    
    # Signals for communication with main process
    voice_input_received = Signal(str)
    voice_input_error = Signal(str)
    tts_started = Signal()
    tts_finished = Signal()
    tts_error = Signal(str)
    recording_started = Signal()
    recording_stopped = Signal()
    recording_error = Signal(str)
    voice_processing_started = Signal()
    voice_processing_finished = Signal()
    process_status_changed = Signal(str)  # "started", "stopped", "error"
    state_updated = Signal(dict)  # Voice service state update
    
    def __init__(self):
        super().__init__()
        self.voice_process = None
        self.command_queue = None
        self.response_queue = None
        self.is_running = False
        self.process_thread = None
        
        # Initialize multiprocessing
        mp.set_start_method('spawn', force=True)
        
    def start_voice_process(self) -> bool:
        """Start the voice process and monitoring thread"""
        try:
            logger.debug("[ID:0520] Starting voice process")
            
            # Clean up any existing process first
            if self.voice_process and self.voice_process.is_alive():
                logger.debug("[ID:0521] Stopping existing voice process before starting new one")
                self.stop_voice_process()
            
            # Create command and response queues
            self.command_queue = mp.Queue()
            self.response_queue = mp.Queue()
            
            # Start the voice process
            self.voice_process = mp.Process(
                target=_voice_process_worker,
                args=(self.command_queue, self.response_queue),
                name="VoiceProcess"
            )
            
            logger.debug(f"[ID:0522] Creating voice process - PID: {self.voice_process.pid if self.voice_process.is_alive() else 'not started'}")
            self.voice_process.start()
            
            # Wait a moment for the process to start
            time.sleep(0.5)
            
            if not self.voice_process.is_alive():
                logger.error("[ID:0523] Voice process failed to start")
                return False
            
            logger.debug(f"[ID:0524] Voice process started successfully - PID: {self.voice_process.pid}")
            
            # Start the monitoring thread
            self.monitor_thread = VoiceProcessMonitor(self.response_queue, self)
            self.monitor_thread.response_received.connect(self._handle_response)
            self.monitor_thread.monitor_error.connect(self._handle_monitor_error)
            
            logger.debug("[ID:0525] Starting voice process monitor thread")
            self.monitor_thread.start()
            
            # Test the connection
            self.send_command("test_connection")
            
            self.is_running = True
            logger.debug("[ID:0526] Voice process and monitor started successfully")
            return True
            
        except Exception as e:
            logger.error(f"[ID:0527] Error starting voice process: {e}")
            logger.error(f"[ID:0528] Voice process start error traceback: {traceback.format_exc()}")
            return False
    
    def stop_voice_process(self):
        """Stop the voice process and monitoring thread safely"""
        try:
            logger.debug("[ID:0529] Stopping voice process")
            
            # Stop the monitoring thread first
            if hasattr(self, 'monitor_thread') and self.monitor_thread:
                logger.debug("[ID:0530] Stopping monitor thread")
                try:
                    self.monitor_thread.stop()
                    
                    # Get monitor stats before cleanup
                    stats = self.monitor_thread.get_stats()
                    logger.debug(f"[ID:0531] Monitor thread stats before cleanup: {stats}")
                    
                    if self.monitor_thread.isRunning():
                        logger.debug("[ID:0532] Waiting for monitor thread to finish")
                        if not self.monitor_thread.wait(2000):  # 2 second timeout
                            logger.warning("[ID:0533] Monitor thread did not finish within timeout")
                        else:
                            logger.debug("[ID:0534] Monitor thread finished successfully")
                    
                    self.monitor_thread.deleteLater()
                    
                except Exception as e:
                    logger.error(f"[ID:0535] Error stopping monitor thread: {e}")
                    logger.error(f"[ID:0536] Monitor thread stop error traceback: {traceback.format_exc()}")
                finally:
                    self.monitor_thread = None
            
            # Stop the voice process
            if self.voice_process and self.voice_process.is_alive():
                logger.debug(f"[ID:0537] Stopping voice process - PID: {self.voice_process.pid}")
                
                try:
                    # Send stop command
                    self.send_command("stop")
                    
                    # Wait for process to finish naturally
                    self.voice_process.join(timeout=5.0)
                    
                    if self.voice_process.is_alive():
                        logger.warning("[ID:0538] Voice process did not stop naturally, terminating")
                        self.voice_process.terminate()
                        self.voice_process.join(timeout=2.0)
                        
                        if self.voice_process.is_alive():
                            logger.error("[ID:0539] Voice process could not be terminated, killing")
                            self.voice_process.kill()
                    
                    logger.debug("[ID:0540] Voice process stopped successfully")
                    
                except Exception as e:
                    logger.error(f"[ID:0541] Error stopping voice process: {e}")
                    logger.error(f"[ID:0542] Voice process stop error traceback: {traceback.format_exc()}")
            
            # Clean up queues
            if hasattr(self, 'command_queue'):
                try:
                    while not self.command_queue.empty():
                        self.command_queue.get_nowait()
                except:
                    pass
                self.command_queue = None
            
            if hasattr(self, 'response_queue'):
                try:
                    while not self.response_queue.empty():
                        self.response_queue.get_nowait()
                except:
                    pass
                self.response_queue = None
            
            self.is_running = False
            logger.debug("[ID:0543] Voice process cleanup completed")
            
        except Exception as e:
            logger.error(f"[ID:0544] Error in voice process cleanup: {e}")
            logger.error(f"[ID:0545] Voice process cleanup error traceback: {traceback.format_exc()}")
    
    def send_command(self, command: str, data: Any = None):
        """Send a command to the voice process"""
        try:
            if not self.is_running or not self.voice_process or not self.voice_process.is_alive():
                logger.warning(f"[ID:0546] Cannot send command '{command}' - voice process not running")
                return False
            
            message = {"command": command, "data": data}
            self.command_queue.put(message)
            logger.debug(f"[ID:0547] Sent command: {command}")
            return True
            
        except Exception as e:
            logger.error(f"[ID:0548] Error sending command '{command}': {e}")
            logger.error(f"[ID:0549] Send command error traceback: {traceback.format_exc()}")
            return False
    
    def _handle_response(self, response: Dict[str, Any]):
        """Handle response from the voice process"""
        try:
            response_type = response.get("type")
            data = response.get("data")
            
            logger.debug(f"[ID:0550] Handling voice process response: {response_type}")
            
            if response_type == "voice_input_received":
                self.voice_input_received.emit(data)
            elif response_type == "voice_input_error":
                self.voice_input_error.emit(data)
            elif response_type == "tts_started":
                self.tts_started.emit()
            elif response_type == "tts_finished":
                self.tts_finished.emit()
            elif response_type == "tts_error":
                self.tts_error.emit(data)
            elif response_type == "recording_started":
                self.recording_started.emit()
            elif response_type == "recording_stopped":
                self.recording_stopped.emit()
            elif response_type == "recording_error":
                self.recording_error.emit(data)
            elif response_type == "voice_processing_started":
                self.voice_processing_started.emit()
            elif response_type == "voice_processing_finished":
                self.voice_processing_finished.emit()
            elif response_type == "status":
                logger.info(f"[ID:0551] Voice process status: {data}")
            elif response_type == "state":
                self.state_updated.emit(data)
            else:
                logger.warning(f"[ID:0552] Unknown response type: {response_type}")
                
        except Exception as e:
            logger.error(f"[ID:0553] Error handling voice process response: {e}")
            logger.error(f"[ID:0554] Response handling error traceback: {traceback.format_exc()}")
    
    def _handle_monitor_error(self, error_message: str):
        """Handle monitor thread error"""
        logger.error(f"[ID:0555] Voice process monitor error: {error_message}")
        logger.error(f"[ID:0556] Monitor error occurred in thread: {QThread.currentThread().objectName()}")
        
        # Emit process status change
        self.process_status_changed.emit("error")
    
    def is_process_running(self) -> bool:
        """Check if the voice process is running"""
        is_running = self.is_running and self.voice_process and self.voice_process.is_alive()
        logger.debug(f"[ID:0557] Voice process running check: {is_running}")
        return is_running
    
    def get_process_info(self) -> Dict[str, Any]:
        """Get information about the voice process"""
        if not self.voice_process:
            logger.debug("[ID:0558] No voice process to get info for")
            return {"status": "not_started"}
        
        info = {
            "status": "running" if self.is_process_running() else "stopped",
            "pid": self.voice_process.pid if self.voice_process.is_alive() else None,
            "name": self.voice_process.name,
            "is_alive": self.voice_process.is_alive()
        }
        
        logger.debug(f"[ID:0559] Voice process info: {info}")
        return info


class VoiceProcessMonitor(QThread):
    """Thread to monitor responses from the voice process"""
    
    response_received = Signal(dict)
    monitor_error = Signal(str)  # New signal for error reporting
    
    def __init__(self, response_queue: mp.Queue, parent=None):
        super().__init__(parent)
        self.response_queue = response_queue
        self.running = True
        self._monitor_id = id(self)
        
        # Set thread name for debugging
        self.setObjectName(f"VoiceProcessMonitor_{self._monitor_id}")
        
        logger.debug(f"[ID:0500] VoiceProcessMonitor created - ID: {self._monitor_id}")
    
    def run(self):
        """Monitor the response queue"""
        try:
            logger.debug(f"[ID:0501] VoiceProcessMonitor started - Thread: {QThread.currentThread().objectName()}")
            
            response_count = 0
            while self.running:
                try:
                    # Check for response with timeout using get_nowait
                    try:
                        response = self.response_queue.get(timeout=0.1)
                        response_count += 1
                        
                        if response_count % 10 == 0:  # Log every 10th response
                            logger.debug(f"[ID:0502] VoiceProcessMonitor processed {response_count} responses")
                        
                        self.response_received.emit(response)
                        
                    except queue.Empty:
                        # No response received, continue loop
                        pass
                        
                except Exception as e:
                    logger.error(f"[ID:0503] Error in voice process monitor loop: {e}")
                    logger.error(f"[ID:0504] VoiceProcessMonitor loop error traceback: {traceback.format_exc()}")
                    self.monitor_error.emit(f"Monitor loop error: {str(e)}")
                    break
            
            logger.debug(f"[ID:0505] VoiceProcessMonitor finished - Total responses: {response_count}")
            
        except Exception as e:
            logger.error(f"[ID:0506] Error in voice process monitor: {e}")
            logger.error(f"[ID:0507] VoiceProcessMonitor error traceback: {traceback.format_exc()}")
            self.monitor_error.emit(f"Monitor error: {str(e)}")
    
    def stop(self):
        """Stop the monitoring thread safely"""
        try:
            logger.debug(f"[ID:0508] Stopping VoiceProcessMonitor - ID: {self._monitor_id}")
            self.running = False
            
            # Give the thread a moment to finish naturally
            time.sleep(0.1)
            
            logger.debug(f"[ID:0509] VoiceProcessMonitor stop completed - ID: {self._monitor_id}")
            
        except Exception as e:
            logger.error(f"[ID:0510] Error stopping VoiceProcessMonitor: {e}")
            logger.error(f"[ID:0511] VoiceProcessMonitor stop error traceback: {traceback.format_exc()}")
    
    def get_stats(self) -> dict:
        """Get monitor statistics for debugging"""
        return {
            "monitor_id": self._monitor_id,
            "running": self.running,
            "thread_id": id(QThread.currentThread()),
            "thread_name": QThread.currentThread().objectName() or "unnamed"
        }


def _voice_process_worker(command_queue: mp.Queue, response_queue: mp.Queue):
    """Worker function that runs in the separate voice process"""
    try:
        # Import voice services in the worker process
        from pyside_chat.services.Voice_STT_TTS_SERVICES.voice_service import VoiceService
        
        # Create QApplication for the voice process
        app = QApplication.instance()
        if not app:
            app = QApplication([])
        
        # Initialize voice service with response queue
        voice_service = VoiceService(response_queue)
        
        # Send ready signal
        response_queue.put({
            "type": "status",
            "data": "Voice process started and ready"
        })
        
        logger.info("Voice process worker started")
        
        # Main command loop
        while True:
            try:
                # Check for commands with timeout using get_nowait
                try:
                    message = command_queue.get(timeout=0.1)
                    command = message.get("command")
                    data = message.get("data")
                    
                    if command == "stop":
                        logger.info("Received stop command")
                        break
                    elif command == "start_voice_input":
                        voice_service.start_voice_input()
                    elif command == "stop_voice_input":
                        voice_service.stop_voice_input()
                    elif command == "speak_text":
                        voice_service.speak_text(data)
                    elif command == "speak_text_streaming":
                        voice_service.speak_text_streaming(data)
                    elif command == "speak_text_non_streaming":
                        voice_service.speak_text_non_streaming(data)
                    elif command == "stop_tts":
                        voice_service.stop_tts()
                    elif command == "update_settings":
                        voice_service.update_settings(data)
                    elif command == "set_continuous_voice_mode":
                        voice_service.set_continuous_voice_mode(data)
                    elif command == "test_connection":
                        response_queue.put({
                            "type": "status",
                            "data": "Connection test successful"
                        })
                    elif command == "get_state":
                        state = {
                            "is_recording": voice_service.is_recording,
                            "is_processing_voice": voice_service.is_processing_voice,
                            "is_playing_tts": voice_service.is_playing_tts
                        }
                        response_queue.put({
                            "type": "state",
                            "data": state
                        })
                    else:
                        logger.warning(f"Unknown command: {command}")
                        
                except queue.Empty:
                    # No command received, continue loop
                    pass
                
                # Process Qt events
                app.processEvents()
                
            except Exception as e:
                logger.error(f"Error in voice process worker: {e}")
                response_queue.put({
                    "type": "error",
                    "data": str(e)
                })
                break
        
        # Cleanup
        voice_service.cleanup_on_exit()
        logger.info("Voice process worker stopped")
        
    except Exception as e:
        logger.error(f"Failed to start voice process worker: {e}")
        response_queue.put({
            "type": "error",
            "data": f"Failed to start voice process: {str(e)}"
        })


# Convenience functions for the main application
def create_voice_process_manager() -> VoiceProcessManager:
    """Create and start a voice process manager"""
    try:
        manager = VoiceProcessManager()
        if manager.start_voice_process():
            return manager
        else:
            logger.error("Failed to start voice process manager")
            # Return a manager that will use direct service fallback
            return manager
    except Exception as e:
        logger.error(f"Failed to create voice process manager: {e}")
        # Return a manager that will use direct service fallback
        manager = VoiceProcessManager()
        return manager


def stop_voice_process_manager(manager: VoiceProcessManager):
    """Stop a voice process manager"""
    if manager:
        manager.stop_voice_process() 