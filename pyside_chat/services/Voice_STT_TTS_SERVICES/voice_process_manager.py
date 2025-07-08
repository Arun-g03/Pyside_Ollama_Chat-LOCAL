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
        
    def start_voice_process(self):
        """Start the voice services in a separate process"""
        try:
            if self.is_running:
                logger.warning("Voice process is already running")
                return True
            
            # Create communication queues
            self.command_queue = mp.Queue()
            self.response_queue = mp.Queue()
            
            # Start voice process
            self.voice_process = mp.Process(
                target=_voice_process_worker,
                args=(self.command_queue, self.response_queue),
                name="VoiceService"
            )
            self.voice_process.start()
            
            # Start monitoring thread
            self.process_thread = VoiceProcessMonitor(self.response_queue, self)
            # Use QueuedConnection for thread safety
            from PySide6.QtCore import Qt
            self.process_thread.response_received.connect(self._handle_response, Qt.ConnectionType.QueuedConnection)
            self.process_thread.start()
            
            self.is_running = True
            self.process_status_changed.emit("started")
            logger.info("Voice process started successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start voice process: {e}")
            self.process_status_changed.emit("error")
            return False
    
    def stop_voice_process(self):
        """Stop the voice services process"""
        try:
            if not self.is_running:
                return
            
            # Send stop command
            self.send_command("stop")
            
            # Wait for process to stop
            if self.voice_process and self.voice_process.is_alive():
                self.voice_process.join(timeout=5)
                if self.voice_process.is_alive():
                    self.voice_process.terminate()
                    self.voice_process.join(timeout=2)
                    if self.voice_process.is_alive():
                        self.voice_process.kill()
            
            # Stop monitoring thread safely
            if self.process_thread:
                self.process_thread.stop()
                # Use timeout to avoid blocking
                if not self.process_thread.wait(3000):  # 3 second timeout
                    logger.warning("Voice process monitor did not stop within timeout")
                    # Don't use terminate() as it can cause crashes
                    # Instead, mark it for deletion and let it finish naturally
                    self.process_thread.deleteLater()
                else:
                    logger.debug("Voice process monitor stopped successfully")
                    self.process_thread.deleteLater()
            
            self.is_running = False
            self.process_status_changed.emit("stopped")
            logger.info("Voice process stopped")
            
        except Exception as e:
            logger.error(f"Error stopping voice process: {e}")
    
    def send_command(self, command: str, data: Any = None):
        """Send a command to the voice process"""
        if not self.is_running or not self.command_queue:
            logger.warning("Voice process not running, cannot send command")
            return False
        
        try:
            message = {
                "command": command,
                "data": data,
                "timestamp": time.time()
            }
            self.command_queue.put(message)
            return True
        except Exception as e:
            logger.error(f"Failed to send command to voice process: {e}")
            return False
    
    def _handle_response(self, response: Dict[str, Any]):
        """Handle response from voice process"""
        try:
            response_type = response.get("type")
            data = response.get("data")
            
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
                logger.info(f"Voice process status: {data}")
            elif response_type == "state":
                self.state_updated.emit(data)
            else:
                logger.warning(f"Unknown response type: {response_type}")
                
        except Exception as e:
            logger.error(f"Error handling voice process response: {e}")
    
    def is_process_running(self) -> bool:
        """Check if the voice process is running"""
        return self.is_running and self.voice_process and self.voice_process.is_alive()
    
    def get_process_info(self) -> Dict[str, Any]:
        """Get information about the voice process"""
        if not self.voice_process:
            return {"status": "not_started"}
        
        return {
            "status": "running" if self.is_process_running() else "stopped",
            "pid": self.voice_process.pid if self.voice_process.is_alive() else None,
            "name": self.voice_process.name,
            "is_alive": self.voice_process.is_alive()
        }


class VoiceProcessMonitor(QThread):
    """Thread to monitor responses from the voice process"""
    
    response_received = Signal(dict)
    
    def __init__(self, response_queue: mp.Queue, parent=None):
        super().__init__(parent)
        self.response_queue = response_queue
        self.running = True
    
    def run(self):
        """Monitor the response queue"""
        while self.running:
            try:
                # Check for response with timeout using get_nowait
                try:
                    response = self.response_queue.get(timeout=0.1)
                    self.response_received.emit(response)
                except queue.Empty:
                    # No response received, continue loop
                    pass
            except Exception as e:
                logger.error(f"Error in voice process monitor: {e}")
                break
    
    def stop(self):
        """Stop the monitoring thread"""
        self.running = False
        # Give the thread a moment to finish naturally
        time.sleep(0.1)


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