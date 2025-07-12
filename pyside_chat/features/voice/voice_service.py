"""
Voice Service Module

Handles voice input/output functionality including:
- Speech-to-Text (STT) for user voice input
- Text-to-Speech (TTS) for AI responses
- Voice recording and playback
"""

import os
import tempfile
import threading
import time
import wave
import pyaudio
import speech_recognition as sr
from typing import Optional, Callable
from PySide6.QtCore import QObject, Signal, QTimer, Qt
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
import subprocess
import platform
import json

from pyside_chat.core.logging.logger import CustomLogger
from pyside_chat.core.logging.helpers import LoggingHelpers

logger = CustomLogger.get_logger(__name__)


class VoiceService(QObject):
    """Main voice service that orchestrates STT and TTS functionality"""
    
    # Signals
    voice_input_received = Signal(str)  # Emitted when voice is converted to text
    voice_input_error = Signal(str)     # Emitted when voice input fails
    tts_started = Signal()              # Emitted when TTS starts
    tts_finished = Signal()             # Emitted when TTS finishes
    tts_error = Signal(str)             # Emitted when TTS fails
    recording_started = Signal()        # Emitted when recording starts
    recording_stopped = Signal()        # Emitted when recording stops
    recording_error = Signal(str)       # Emitted when recording fails
    voice_processing_started = Signal() # Emitted when voice processing starts
    voice_processing_finished = Signal() # Emitted when voice processing finishes
    audio_level_changed = Signal(float)
    user_interrupted = Signal()         # Emitted when user interrupts AI response
    request_cancelled = Signal()        # Emitted when Ollama request is cancelled
    voice_service_ready = Signal()      # Emitted when voice service is ready
    
    def __init__(self, recording_service=None, stt_service=None, tts_service=None, response_queue=None):
        super().__init__()
        
        # Check if we're in a Qt context
        try:
            from PySide6.QtCore import QCoreApplication
            self.in_qt_context = QCoreApplication.instance() is not None
        except Exception as e:
            logger.warning(f"Failed to check Qt context: {e}")
            self.in_qt_context = False

        # Services
        self.recording_service = recording_service
        self.stt_service = stt_service
        self.tts_service = tts_service
        self.response_queue = response_queue
        
        # Initialize services if not provided
        if not all([recording_service, stt_service, tts_service]):
            logger.info("Initializing voice services...", print_to_terminal=True)
            self._initialize_services()

        # State tracking
        self.is_recording = False
        self.is_processing_voice = False
        self.is_playing_tts = False
        self.continuous_voice_mode = False

        # Interruption and request management
        self._interruption_detected = False
        self._current_request_id = None
        self._request_queue = []
        self._max_concurrent_requests = 1  # Prevent overload
        self._active_requests = 0
        self._interruption_cooldown = 1.0  # Seconds to wait after interruption
        self._last_interruption_time = 0

        # Voice settings
        self.voice_settings = {
            "stt_api": "Vosk (Offline)",
            "tts_api": "Coqui TTS",
            "tts_voice": "default",
            "auto_speak": True,
            "voice_speed": 1.0,
            "recording_timeout": 10.0,
            "silence_duration": 2.0,
            "silence_threshold": 0.005,
            "coqui_model": "tts_models/en/vctk/vits",
            "coqui_speaker": "ED",
            "eq_visualizer": "None",
            "tts_streaming": True,
            "allow_interruptions": True,  # New setting
            "interruption_threshold": 0.5  # Audio level threshold for interruption
        }

        # Setup connections
        self._setup_connections()

        logger.info("VoiceService initialized successfully", print_to_terminal=True)
        
    def _setup_connections(self):
        """Setup signal connections"""
        # Connect STT service signals
        if self.stt_service:
            try:
                self.stt_service.text_received.connect(self._on_stt_text_received)
                self.stt_service.error_occurred.connect(self._on_stt_error)
                logger.debug("STT service signals connected")
            except Exception as e:
                logger.error(f"Failed to connect STT signals: {e}")
            
        # Connect TTS service signals
        if self.tts_service:
            try:
                self.tts_service.tts_started.connect(self._on_tts_started)
                self.tts_service.tts_finished.connect(self._on_tts_finished)
                self.tts_service.tts_error.connect(self._on_tts_error)
                logger.debug("TTS service signals connected")
            except Exception as e:
                logger.error(f"Failed to connect TTS signals: {e}")
            
        # Connect recording service signals
        if self.recording_service:
            try:
                self.recording_service.recording_started.connect(self._on_recording_started)
                self.recording_service.recording_stopped.connect(self._on_recording_stopped)
                self.recording_service.recording_error.connect(self._on_recording_error)
                self.recording_service.audio_level_changed.connect(self._on_audio_level_changed)
                logger.debug("Recording service signals connected")
            except Exception as e:
                logger.error(f"Failed to connect recording signals: {e}")

    def _setup_service_connections(self):
        """Setup connections for newly initialized services"""
        logger.info("Setting up voice service connections...", print_to_terminal=True)
        if self.in_qt_context:
            if self.stt_service:
                try:
                    self.stt_service.text_received.connect(self._on_stt_text_received)
                    self.stt_service.error_occurred.connect(self._on_stt_error)
                    logger.info("STT service signals connected", print_to_terminal=True)
                except Exception as e:
                    logger.error(f"Failed to connect STT signals: {e}", print_to_terminal=True)
            
            if self.tts_service:
                try:
                    # Connect TTS signals with QueuedConnection for thread safety
                    from PySide6.QtCore import Qt
                    self.tts_service.tts_started.connect(self.tts_started.emit, Qt.ConnectionType.QueuedConnection)
                    self.tts_service.tts_finished.connect(self._on_tts_finished, Qt.ConnectionType.QueuedConnection)
                    self.tts_service.tts_error.connect(self._on_tts_error, Qt.ConnectionType.QueuedConnection)
                    self.tts_service.audio_level_changed.connect(self.audio_level_changed.emit, Qt.ConnectionType.QueuedConnection)
                    logger.info("TTS service signals connected", print_to_terminal=True)
                except Exception as e:
                    logger.error(f"Failed to connect TTS signals: {e}", print_to_terminal=True)
            
            if self.recording_service:
                try:
                    # Connect recording signals
                    self.recording_service.recording_started.connect(self.recording_started.emit)
                    self.recording_service.recording_stopped.connect(self.recording_stopped.emit)
                    self.recording_service.recording_error.connect(self.recording_error.emit)
                    self.recording_service.audio_level_changed.connect(self.audio_level_changed.emit)
                    self.recording_service.recording_auto_stopped.connect(self._on_recording_auto_stopped)
                    
                    # Connect recording auto_stop to trigger STT processing (only this one)
                    self.recording_service.recording_auto_stopped.connect(self._on_recording_auto_stopped_for_stt)
                    
                    # Connect recording signals to response queue forwarding
                    if self.response_queue:
                        self.recording_service.recording_started.connect(self._forward_recording_started)
                        self.recording_service.recording_stopped.connect(self._forward_recording_stopped)
                        self.recording_service.recording_error.connect(self._forward_recording_error)
                    logger.info("Recording service signals connected", print_to_terminal=True)
                except Exception as e:
                    logger.error(f"Failed to connect recording signals: {e}", print_to_terminal=True)
        
        logger.info("Voice service connections setup completed", print_to_terminal=True)

    def _on_recording_auto_stopped(self):
        """Handle automatic recording stop"""
        logger.debug("Recording auto-stopped")
        self.is_recording = False

    def _on_recording_auto_stopped_for_stt(self):
        """Handle automatic recording stop for STT processing"""
        logger.debug("Recording auto-stopped for STT processing", print_to_terminal=True)
        self.is_recording = False
        
        # Process the recorded audio with STT
        if self.recording_service and self.stt_service:
            try:
                # Get the recorded audio file
                result = self.recording_service.stop_recording()
                if result and result[0]:  # Audio file path and speech detected
                    audio_file_path, speech_detected = result
                    if speech_detected:
                        logger.debug(f"Processing recorded audio with STT: {audio_file_path}", print_to_terminal=True)
                        # Process the audio file with STT
                        self.stt_service.process_audio_file(audio_file_path)
                    else:
                        logger.debug("No speech detected in recording, skipping STT", print_to_terminal=True)
                        self._complete_request()
                else:
                    logger.debug("No audio file to process", print_to_terminal=True)
                    self._complete_request()
            except Exception as e:
                logger.error(f"Error processing recorded audio with STT: {e}", print_to_terminal=True)
                self._complete_request()
        else:
            logger.error("Recording service or STT service not available", print_to_terminal=True)
            self._complete_request()

    def _on_recording_timeout(self):
        """Handle recording timeout"""
        logger.debug("Recording timeout reached")
        if self.is_recording:
            self.stop_voice_input()

    def is_voice_available(self) -> bool:
        """Check if voice functionality is available"""
        # Check that all services exist and are properly initialized
        stt_ready = (self.stt_service is not None and 
                    hasattr(self.stt_service, 'is_initialized') and 
                    self.stt_service.is_initialized())
        tts_ready = (self.tts_service is not None and 
                    hasattr(self.tts_service, 'is_initialized') and 
                    self.tts_service.is_initialized())
        recording_ready = (self.recording_service is not None and 
                          hasattr(self.recording_service, 'is_initialized') and 
                          self.recording_service.is_initialized())
        
        return stt_ready and tts_ready and recording_ready

    def can_handle_new_request(self) -> bool:
        """Check if we can handle a new request without overload"""
        return self._active_requests < self._max_concurrent_requests

    def queue_request(self, request_type: str, data: dict) -> str:
        """Queue a new request and return request ID"""
        import uuid
        request_id = str(uuid.uuid4())
        
        request = {
            "id": request_id,
            "type": request_type,
            "data": data,
            "timestamp": time.time()
        }
        
        self._request_queue.append(request)
        logger.debug(f"Queued request {request_id} ({request_type})")
        
        # Process queue if we can handle it
        self._process_request_queue()
        
        return request_id

    def _process_request_queue(self):
        """Process queued requests if capacity allows"""
        if not self.can_handle_new_request() or not self._request_queue:
            return
            
        # Check if enough time has passed since last interruption
        if self._interruption_detected:
            time_since_interruption = time.time() - self._last_interruption_time
            if time_since_interruption < self._interruption_cooldown:
                logger.debug(f"Waiting for interruption cooldown ({self._interruption_cooldown - time_since_interruption:.1f}s remaining)")
                return
        
        # Process next request
        request = self._request_queue.pop(0)
        self._active_requests += 1
        self._current_request_id = request["id"]
        
        logger.debug(f"Processing request {request['id']} ({request['type']})")
        
        # Handle different request types
        if request["type"] == "voice_input":
            self._handle_voice_input_request(request["data"])
        elif request["type"] == "tts":
            self._handle_tts_request(request["data"])
        else:
            logger.warning(f"Unknown request type: {request['type']}")

    def _handle_voice_input_request(self, data: dict):
        """Handle voice input request"""
        try:
            self.is_processing_voice = True
            self.voice_processing_started.emit()
            
            # Forward to response queue if in separate process
            if self.response_queue:
                self.response_queue.put({
                    "type": "voice_processing_started",
                    "data": None
                })
            
            # Start actual recording
            if self.recording_service:
                logger.debug("Starting recording service", print_to_terminal=True)
                self.recording_service.start_recording()
                self.is_recording = True
                logger.debug("Recording started successfully", print_to_terminal=True)
            else:
                logger.error("Recording service not available", print_to_terminal=True)
                self._complete_request()
            
        except Exception as e:
            logger.error(f"Error handling voice input request: {e}", print_to_terminal=True)
            self._complete_request()

    def _handle_tts_request(self, data: dict):
        """Handle TTS request"""
        try:
            text = data.get("text", "")
            if text:
                self.speak_text(text)
            else:
                self._complete_request()
                
        except Exception as e:
            logger.error(f"Error handling TTS request: {e}")
            self._complete_request()

    def _complete_request(self):
        """Complete current request and process next"""
        self._active_requests = max(0, self._active_requests - 1)
        self._current_request_id = None
        
        # Process next request if available
        if self._request_queue:
            self._process_request_queue()

    def cancel_current_request(self):
        """Cancel the current request"""
        if self._current_request_id:
            logger.info(f"Cancelling request {self._current_request_id}")
            
            # Stop current operations
            if self.is_playing_tts:
                self.stop_tts()
            if self.is_recording:
                self.stop_voice_input()
            if self.is_processing_voice:
                self.is_processing_voice = False
                self.voice_processing_finished.emit()
            
            # Clear current request
            self._current_request_id = None
            self._active_requests = max(0, self._active_requests - 1)
            
            # Emit cancellation signal
            self.request_cancelled.emit()
            
            # Process next request
            self._process_request_queue()

    def handle_user_interruption(self):
        """Handle user interruption during AI response"""
        if not self.voice_settings.get("allow_interruptions", True):
            return
            
        current_time = time.time()
        time_since_last_interruption = current_time - self._last_interruption_time
        
        # Prevent rapid-fire interruptions
        if time_since_last_interruption < 0.5:  # 500ms minimum between interruptions
            logger.debug("Interruption ignored - too soon after last interruption")
            return
            
        self._interruption_detected = True
        self._last_interruption_time = current_time
        
        logger.info("User interruption detected - cancelling current operations")
        
        # Cancel current request
        self.cancel_current_request()
        
        # Emit interruption signal
        self.user_interrupted.emit()
        
        # Forward to response queue if in separate process
        if self.response_queue:
            self.response_queue.put({
                "type": "user_interrupted",
                "data": None
            })

    def _on_audio_level_changed(self, audio_level: float):
        """Handle audio level changes for interruption detection"""
        # Check for interruption during TTS playback
        if (self.is_playing_tts and 
            self.voice_settings.get("allow_interruptions", True) and
            audio_level > self.voice_settings.get("interruption_threshold", 0.5)):
            
            logger.debug(f"High audio level detected ({audio_level:.3f}) during TTS - potential interruption")
            self.handle_user_interruption()
        
        # Emit audio level for visualization
        self.audio_level_changed.emit(audio_level)
        
        # Forward to response queue if in separate process
        if self.response_queue:
            self.response_queue.put({
                "type": "audio_level_changed",
                "data": audio_level
            })
        
    def start_voice_input(self):
        """Start voice recording and convert to text"""
        logger.debug("[VOICE DEBUG] start_voice_input called")
        try:
            if not self.recording_service:
                LoggingHelpers.log_audio_operation("start_voice_input", False, Exception("Recording service not available"))
                logger.error("[VOICE ERROR] Recording service not available")
                self.voice_input_error.emit("Recording service not available")
                return
                
            if self.is_recording:
                LoggingHelpers.log_warning_with_context("Voice recording already in progress", {"is_recording": self.is_recording})
                logger.debug("[VOICE DEBUG] Already recording, skipping")
                return
                
            if self.is_processing_voice:
                LoggingHelpers.log_warning_with_context("Voice processing already in progress", {"is_processing_voice": self.is_processing_voice})
                logger.debug("[VOICE DEBUG] Already processing voice, skipping")
                return
            
            # Check if we can handle new requests
            if not self.can_handle_new_request():
                logger.warning("Cannot handle new voice input - request queue full")
                self.voice_input_error.emit("Request queue full - please wait")
                return
            
            # Queue the voice input request
            request_id = self.queue_request("voice_input", {})
            logger.debug(f"[VOICE DEBUG] Queued voice input request: {request_id}")
            
        except Exception as e:
            logger.error(f"[VOICE ERROR] Error in start_voice_input: {e}")
            self.voice_input_error.emit(f"Failed to start voice input: {str(e)}")
    
    def stop_voice_input(self):
        """Stop voice recording and process the audio"""
        logger.debug("[VOICE DEBUG] stop_voice_input called")
        try:
            if not self.recording_service:
                logger.error("[VOICE ERROR] Recording service not available")
                return
                
            if not self.is_recording:
                logger.debug("[VOICE DEBUG] Not recording, nothing to stop")
                return
            
            self.is_recording = False
            self.recording_service.stop_recording()
            logger.debug("[VOICE DEBUG] Voice recording stopped")
            
        except Exception as e:
            logger.error(f"[VOICE ERROR] Error stopping voice input: {e}")
    
    def _on_stt_text_received(self, text: str):
        print(f"[DEBUG] STT result: {text}")
        self.is_processing_voice = False
        self.voice_processing_finished.emit()
        
        # Forward to response queue if in separate process
        if self.response_queue:
            self.response_queue.put({
                "type": "voice_processing_finished",
                "data": None
            })
        
        # Only emit if text is not empty or whitespace
        if text.strip():
            # Log voice input received
            logger.info(f"Voice input received: '{text}'", print_to_terminal=True)
            
            self.voice_input_received.emit(text)
            # Forward to response queue if in separate process
            if self.response_queue:
                self.response_queue.put({
                    "type": "voice_input_received",
                    "data": text
                })
        else:
            logger.info("STT result was empty, skipping message emission.", print_to_terminal=True)
        
        # Complete the request
        self._complete_request()
        
        # If continuous voice mode is enabled, restart recording automatically
        if self.continuous_voice_mode:
            logger.debug("Continuous voice mode enabled, restarting recording")
            QTimer.singleShot(100, self.start_voice_input)  # Small delay to ensure processing is complete
    
    def _on_stt_error(self, error: str):
        """Handle STT error"""
        self.is_processing_voice = False
        self.voice_processing_finished.emit()
        self.voice_input_error.emit(error)
        
        # Forward to response queue if in separate process
        if self.response_queue:
            self.response_queue.put({
                "type": "voice_processing_finished",
                "data": None
            })
            self.response_queue.put({
                "type": "voice_input_error",
                "data": error
            })
        
        # Complete the request
        self._complete_request()
        
        # If continuous voice mode is enabled, restart recording even after error
        if self.continuous_voice_mode:
            logger.debug("Continuous voice mode enabled, restarting recording after error")
            QTimer.singleShot(100, self.start_voice_input)  # Small delay to ensure processing is complete
    
    def _on_tts_finished(self):
        """Handle TTS finished"""
        self.is_playing_tts = False
        logger.debug("TTS finished, resetting playing flag")
        self.tts_finished.emit()
        
        # Forward to response queue if in separate process
        if self.response_queue:
            self.response_queue.put({
                "type": "tts_finished",
                "data": None
            })
        
        # Complete the request
        self._complete_request()
        
        # If continuous voice mode is enabled, restart voice input after TTS
        if self.continuous_voice_mode:
            logger.debug("Continuous voice mode enabled, restarting voice input after TTS")
            QTimer.singleShot(500, self.start_voice_input)  # Longer delay to ensure TTS is completely finished
    
    def _on_tts_started(self):
        """Handle TTS started"""
        self.is_playing_tts = True
        logger.debug("TTS started, setting playing flag")
        self.tts_started.emit()
        
        # Forward to response queue if in separate process
        if self.response_queue:
            self.response_queue.put({
                "type": "tts_started",
                "data": None
            })

    def _on_tts_error(self, error: str):
        """Handle TTS error"""
        self.is_playing_tts = False
        logger.error(f"TTS error: {error}")
        self.tts_error.emit(error)
        
        # Forward to response queue if in separate process
        if self.response_queue:
            self.response_queue.put({
                "type": "tts_error",
                "data": error
            })
        
        # Complete the request
        self._complete_request()
    
    def speak_text(self, text: str):
        """Convert text to speech and play it"""
        if not self.tts_service:
            logger.error("TTS service not available")
            self.tts_error.emit("TTS service not available")
            return
            
        if self.is_playing_tts:
            logger.warning("TTS already in progress, stopping current playback")
            self.stop_tts()
        
        try:
            # Queue the TTS request
            request_id = self.queue_request("tts", {"text": text})
            logger.debug(f"Queued TTS request: {request_id}")
                
        except Exception as e:
            logger.error(f"Failed to queue TTS request: {e}")
            self.tts_error.emit(f"Failed to start TTS: {str(e)}")
    
    def stop_tts(self):
        """Stop current TTS playback"""
        if self.tts_service:
            self.tts_service.stop_playback()
        self.is_playing_tts = False
    
    def set_continuous_voice_mode(self, enabled: bool):
        """Set continuous voice mode"""
        self.continuous_voice_mode = enabled
        logger.debug(f"Continuous voice mode: {'enabled' if enabled else 'disabled'}")
    
    def is_continuous_voice_mode(self) -> bool:
        """Check if continuous voice mode is enabled"""
        return self.continuous_voice_mode
        
    def update_settings(self, settings: dict):
        """Update voice settings"""
        self.voice_settings.update(settings)
        logger.debug(f"Updated voice settings: {settings}")

    def get_silence_duration(self) -> float:
        """Get silence duration setting"""
        return self.voice_settings.get("silence_duration", 2.0)
    
    def cleanup_on_exit(self):
        """Cleanup resources on exit"""
        try:
            if self.recording_service:
                self.recording_service.cleanup()
            if self.tts_service:
                self.tts_service.cleanup()
            logger.debug("Voice service cleanup completed")
        except Exception as e:
            logger.error(f"Error during voice service cleanup: {e}")
            
    def get_audio_folder_path(self) -> str:
        """Get the path to the audio folder"""
        return os.path.join(os.getcwd(), "User_history", "audio")
    
    def list_audio_files(self) -> list:
        """List all audio files in the audio folder"""
        audio_folder = self.get_audio_folder_path()
        if not os.path.exists(audio_folder):
            return []
        
        audio_files = []
        for filename in os.listdir(audio_folder):
            if filename.endswith(('.wav', '.mp3')):
                file_path = os.path.join(audio_folder, filename)
                file_info = {
                    'filename': filename,
                    'path': file_path,
                    'size': os.path.getsize(file_path),
                    'modified': os.path.getmtime(file_path)
                }
                audio_files.append(file_info)
        
        # Sort by modification time (newest first)
        audio_files.sort(key=lambda x: x['modified'], reverse=True)
        return audio_files
    
    def cleanup_old_audio_files(self, max_files: int = 100, max_age_days: int = 7):
        """Clean up old audio files to prevent folder from getting too large"""
        audio_files = self.list_audio_files()
        
        if len(audio_files) <= max_files:
            return
        
        # Calculate cutoff time for age-based cleanup
        import time
        cutoff_time = time.time() - (max_age_days * 24 * 60 * 60)
        
        files_to_delete = []
        
        # Mark files for deletion based on age
        for file_info in audio_files:
            if file_info['modified'] < cutoff_time:
                files_to_delete.append(file_info)
        
        # If we still have too many files, delete the oldest ones
        if len(audio_files) - len(files_to_delete) > max_files:
            remaining_files = [f for f in audio_files if f not in files_to_delete]
            files_to_delete.extend(remaining_files[max_files:])
        
        # Delete the marked files
        for file_info in files_to_delete:
            try:
                os.remove(file_info['path'])
                logger.debug(f"Deleted old audio file: {file_info['filename']}")
            except Exception as e:
                logger.error(f"Failed to delete audio file {file_info['filename']}: {e}")
        
        if files_to_delete:
            logger.info(f"Cleaned up {len(files_to_delete)} old audio files")
    
    def cleanup_all_audio_files(self):
        """Clean up all audio files (since they're only for STT processing)"""
        audio_files = self.list_audio_files()
        
        if not audio_files:
            return
        
        deleted_count = 0
        for file_info in audio_files:
            try:
                os.remove(file_info['path'])
                deleted_count += 1
                logger.debug(f"Deleted audio file: {file_info['filename']}")
            except Exception as e:
                logger.error(f"Failed to delete audio file {file_info['filename']}: {e}")
        
        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} audio files on startup")
    
    def _forward_recording_started(self):
        """Forward recording started signal to response queue"""
        if self.response_queue:
            self.response_queue.put({
                "type": "recording_started",
                "data": None
            })
    
    def _forward_recording_stopped(self):
        """Forward recording stopped signal to response queue"""
        if self.response_queue:
            self.response_queue.put({
                "type": "recording_stopped",
                "data": None
            })
    
    def _forward_recording_error(self, error: str):
        """Forward recording error signal to response queue"""
        if self.response_queue:
            self.response_queue.put({
                "type": "recording_error",
                "data": error
            })
    
    def _forward_voice_processing_started(self):
        """Forward voice processing started signal to response queue"""
        if self.response_queue:
            self.response_queue.put({
                "type": "voice_processing_started",
                "data": None
            })
    
    def _cleanup_resources(self):
        """Clean up resources when the cleanup timer fires"""
        logger.info("Cleaning up resources")
        self.cleanup_all_audio_files()
        
        # Clean up recording service
        if hasattr(self, 'recording_service'):
            self.recording_service.cleanup()
    
    def _reset_error_count(self):
        """Reset error count after a delay"""
        self._error_count = 0
        logger.info("Error count reset")
    
    def _connect_signals(self):
        """Connect signals from voice services"""
        # This method is called after services are initialized
        # The actual signal connections are handled in _initialize_services
        pass
    
    def _initialize_services(self):
        """Initialize voice services with error handling"""
        self.stt_service = None
        self.tts_service = None
        self.recording_service = None
        
        try:
            logger.info("Initializing STT service...", print_to_terminal=True)
            from pyside_chat.features.voice.stt.stt_service import STTService
            self.stt_service = STTService()
            logger.info("STT service initialized successfully", print_to_terminal=True)
        except Exception as e:
            logger.error(f"Failed to initialize STT service: {e}", print_to_terminal=True)
        
        try:
            logger.info("Initializing TTS service...", print_to_terminal=True)
            from pyside_chat.features.voice.tts.tts_service import TTSService
            self.tts_service = TTSService()
            logger.info("TTS service initialized successfully", print_to_terminal=True)
        except Exception as e:
            logger.error(f"Failed to initialize TTS service: {e}", print_to_terminal=True)
        
        try:
            logger.info("Initializing Recording service...", print_to_terminal=True)
            from pyside_chat.features.voice.audio.recording_service import RecordingService
            self.recording_service = RecordingService()
            logger.info("Recording service initialized successfully", print_to_terminal=True)
        except Exception as e:
            logger.error(f"Failed to initialize Recording service: {e}", print_to_terminal=True)
        
        # Setup service connections
        self._setup_service_connections()
        
        # State tracking
        self.is_recording = False
        self.is_playing_tts = False
        self.is_processing_voice = False  # Track if voice processing is in progress
        self.continuous_voice_mode = False  # Track if continuous voice mode is enabled
        
        # Recording settings
        self.recording_timeout = 15.0  # Increased from 10.0 to 15.0 seconds (fallback)
        self.silence_threshold = 0.005  # Lowered from 0.01 for better sensitivity
        self.silence_duration = 3.0    # Reduced from 4.0 to 3.0 seconds for better responsiveness
        self.min_speech_duration = 0.5  # Minimum speech duration before considering valid
        
        # Recording timer (only if in Qt context)
        if self.in_qt_context:
            self.recording_timer = QTimer()
            self.recording_timer.setSingleShot(True)
            self.recording_timer.timeout.connect(self._on_recording_timeout)
        else:
            self.recording_timer = None
        
        # EQ Visualizer setting
        self.eq_visualizer = "None"  # Default to no EQ visualizer
        
        # Clean up all audio files on startup (since they're only for STT processing)
        if self.in_qt_context:
            QTimer.singleShot(1000, lambda: self.cleanup_all_audio_files()) 
        else:
            # For non-Qt contexts, clean up immediately
            self.cleanup_all_audio_files() 
        
        # Check if all services are ready before emitting signal
        if self.is_voice_available():
            logger.info("All voice services ready, emitting ready signal", print_to_terminal=True)
            self.voice_service_ready.emit()
        else:
            logger.warning("Voice services not ready yet, will emit signal when ready", print_to_terminal=True)
            # Set up a timer to check again
            if self.in_qt_context:
                QTimer.singleShot(1000, self._check_and_emit_ready)
            else:
                self._check_and_emit_ready()
    
    def _check_and_emit_ready(self):
        """Check if all services are ready and emit signal if they are"""
        if self.is_voice_available():
            logger.info("All voice services are now ready, emitting ready signal", print_to_terminal=True)
            self.voice_service_ready.emit()
        else:
            logger.debug("Voice services still not ready, checking again in 1 second")
            if self.in_qt_context:
                QTimer.singleShot(1000, self._check_and_emit_ready) 