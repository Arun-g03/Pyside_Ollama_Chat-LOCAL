# Shared imports
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *

from pyside_chat.core.shared_imports.audio_imports import *

"""
Voice Service Module

Handles voice input/output functionality including:
- Speech-to-Text (STT) for user voice input
- Text-to-Speech (TTS) for AI responses
- Voice recording and playback
"""

import wave
import speech_recognition as sr
from typing import Optional, Callable

logger = CustomLogger.get_logger(__name__)


class VoiceService(QObject):
    """Voice service for handling voice input/output functionality using persistent threading architecture"""
    # Signals
    voice_input_received = Signal(str)  # Emitted when voice input is received
    voice_input_error = Signal(str)     # Emitted when voice input fails
    tts_started = Signal()              # Emitted when TTS starts
    tts_finished = Signal()             # Emitted when TTS finishes
    tts_error = Signal(str)             # Emitted when TTS fails
    recording_started = Signal()        # Emitted when recording starts
    recording_stopped = Signal()        # Emitted when recording stops
    recording_error = Signal(str)       # Emitted when recording fails
    voice_processing_started = Signal()  # Emitted when voice processing starts
    voice_processing_finished = Signal()  # Emitted when voice processing finishes
    audio_level_changed = Signal(float)  # Emitted when audio level changes
    eq_bars_changed = Signal(list)      # NEW: EQ bar array for visualization
    user_interrupted = Signal()         # Emitted when user interrupts AI response
    request_cancelled = Signal()        # Emitted when Ollama request is cancelled
    voice_status_changed = Signal(str)  # Emitted when voice status changes
    voice_service_ready = Signal()      # Emitted when voice service is ready

    _instance = None

    @staticmethod
    def get_instance(*args, **kwargs):
        if VoiceService._instance is None:
            VoiceService._instance = VoiceService(*args, **kwargs)
        return VoiceService._instance

    def __init__(self):
        super().__init__()

        # Initialize persistent threading system for voice operations
        self.threading_service = get_global_threading_service()
        self.persistent_thread_pool = get_global_persistent_thread_pool()

        # Track active voice operations
        self._active_voice_operations = set()

        # Check if we're in a Qt context
        try:

            self.in_qt_context = QCoreApplication.instance() is not None
        except Exception as e:
            logger.warning(f"Failed to check Qt context: {e}")
            self.in_qt_context = False

        # Services
        self.recording_service = None
        self.stt_service = None
        self.tts_service = None
        self.response_queue = None

        # Initialize services
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
        self._max_concurrent_requests = 2  # Allow both voice input and TTS simultaneously
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

        logger.info(
            "VoiceService initialized successfully with persistent threading", print_to_terminal=True)

    def _setup_connections(self):
        """Setup signal connections"""
        # Connect STT service signals
        if self.stt_service:
            try:
                self.stt_service.text_received.connect(
                    self._on_stt_text_received)
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
                self.tts_service.audio_level_changed.connect(
                    self.audio_level_changed.emit)
                # NEW: Connect eq_bars_changed
                self.tts_service.eq_bars_changed.connect(
                    self.eq_bars_changed.emit)
                logger.debug("TTS service signals connected")
            except Exception as e:
                logger.error(f"Failed to connect TTS signals: {e}")

        # Connect recording service signals
        if self.recording_service:
            try:
                self.recording_service.recording_started.connect(
                    self._on_recording_started)
                self.recording_service.recording_stopped.connect(
                    self._on_recording_stopped)
                self.recording_service.recording_error.connect(
                    self._on_recording_error)
                self.recording_service.audio_level_changed.connect(
                    self._on_audio_level_changed)
                # NEW: Connect eq_bars_changed from mic
                self.recording_service.eq_bars_changed.connect(
                    self.eq_bars_changed.emit)
                logger.debug("Recording service signals connected")
            except Exception as e:
                logger.error(f"Failed to connect recording signals: {e}")

    def _setup_service_connections(self):
        """Setup connections for newly initialized services"""
        logger.info("Setting up voice service connections...",
                    print_to_terminal=True)
        if self.in_qt_context:
            if self.stt_service:
                try:
                    self.stt_service.text_received.connect(
                        self._on_stt_text_received)
                    self.stt_service.error_occurred.connect(self._on_stt_error)
                    logger.info("STT service signals connected",
                                print_to_terminal=True)
                except Exception as e:
                    logger.error(
                        f"Failed to connect STT signals: {e}", print_to_terminal=True)

            if self.tts_service:
                try:
                    # Connect TTS signals with QueuedConnection for thread safety

                    logger.info("TTS service signals connected",
                                print_to_terminal=True)
                except Exception as e:
                    logger.error(
                        f"Failed to connect TTS signals: {e}", print_to_terminal=True)

            if self.recording_service:
                try:
                    # Connect recording signals
                    self.recording_service.recording_started.connect(
                        self.recording_started.emit)
                    self.recording_service.recording_stopped.connect(
                        self.recording_stopped.emit)
                    self.recording_service.recording_error.connect(
                        self.recording_error.emit)
                    self.recording_service.audio_level_changed.connect(
                        self.audio_level_changed.emit)
                    self.recording_service.recording_auto_stopped.connect(
                        self._on_recording_auto_stopped)

                    # Connect recording auto_stop to trigger STT processing (only this one)
                    self.recording_service.recording_auto_stopped.connect(
                        self._on_recording_auto_stopped_for_stt)

                    # Connect recording signals to response queue forwarding
                    if self.response_queue:
                        self.recording_service.recording_started.connect(
                            self._forward_recording_started)
                        self.recording_service.recording_stopped.connect(
                            self._forward_recording_stopped)
                        self.recording_service.recording_error.connect(
                            self._forward_recording_error)
                    logger.info("Recording service signals connected",
                                print_to_terminal=True)
                except Exception as e:
                    logger.error(
                        f"Failed to connect recording signals: {e}", print_to_terminal=True)

        logger.info("Voice service connections setup completed",
                    print_to_terminal=True)

    def _on_recording_started(self):
        """Handle recording started signal"""
        logger.debug("Recording started")
        self.is_recording = True
        self.recording_started.emit()

    def _on_recording_stopped(self):
        """Handle recording stopped signal"""
        logger.debug("Recording stopped")
        self.is_recording = False
        self.recording_stopped.emit()

    def _on_recording_error(self, error: str):
        """Handle recording error signal"""
        logger.error(f"Recording error: {error}")
        self.is_recording = False
        self.recording_error.emit(error)

    def _on_recording_auto_stopped(self):
        """Handle automatic recording stop"""
        logger.debug("Recording auto-stopped")
        self.is_recording = False

    def _on_recording_auto_stopped_for_stt(self):
        """Handle automatic recording stop for STT processing"""
        logger.debug("Recording auto-stopped for STT processing",
                     print_to_terminal=True)
        self.is_recording = False

        # Process the recorded audio with STT
        if self.recording_service and self.stt_service:
            try:
                # Get the recorded audio file
                result = self.recording_service.stop_recording()
                if result and result[0]:  # Audio file path and speech detected
                    audio_file_path, speech_detected = result
                    if speech_detected:
                        logger.debug(
                            f"Processing recorded audio with STT: {audio_file_path}", print_to_terminal=True)
                        # Process the audio file with STT
                        self.stt_service.process_audio_file(audio_file_path)
                    else:
                        logger.debug(
                            "No speech detected in recording, skipping STT", print_to_terminal=True)
                        self._complete_request()
                else:
                    logger.debug("No audio file to process",
                                 print_to_terminal=True)
                    self._complete_request()
            except Exception as e:
                logger.error(
                    f"Error processing recorded audio with STT: {e}", print_to_terminal=True)
                self._complete_request()
        else:
            logger.error(
                "Recording service or STT service not available", print_to_terminal=True)
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

        # Debug logging to see which service is failing
        logger.debug(
            f"Voice availability check - STT: {stt_ready}, TTS: {tts_ready}, Recording: {recording_ready}")
        if not stt_ready:
            logger.debug(
                f"STT service not ready - exists: {self.stt_service is not None}, has method: {hasattr(self.stt_service, 'is_initialized') if self.stt_service else False}")
            if self.stt_service:
                logger.debug(
                    f"STT is_initialized result: {self.stt_service.is_initialized()}")
        if not tts_ready:
            logger.debug(
                f"TTS service not ready - exists: {self.tts_service is not None}, has method: {hasattr(self.tts_service, 'is_initialized') if self.tts_service else False}")
            if self.tts_service:
                logger.debug(
                    f"TTS is_initialized result: {self.tts_service.is_initialized()}")
        if not recording_ready:
            logger.debug(
                f"Recording service not ready - exists: {self.recording_service is not None}, has method: {hasattr(self.recording_service, 'is_initialized') if self.recording_service else False}")
            if self.recording_service:
                logger.debug(
                    f"Recording is_initialized result: {self.recording_service.is_initialized()}")

        return stt_ready and tts_ready and recording_ready

    def can_handle_new_request(self) -> bool:
        """Check if we can handle a new request without overload"""
        can_handle = self._active_requests < self._max_concurrent_requests
        if not can_handle:
            logger.debug(
                f"Cannot handle new request - active: {self._active_requests}, max: {self._max_concurrent_requests}")
        return can_handle

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
                logger.debug(
                    f"Waiting for interruption cooldown ({self._interruption_cooldown - time_since_interruption:.1f}s remaining)")
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
                logger.debug("Starting recording service",
                             print_to_terminal=True)
                self.recording_service.start_recording()
                self.is_recording = True
                logger.debug("Recording started successfully",
                             print_to_terminal=True)
            else:
                logger.error("Recording service not available",
                             print_to_terminal=True)
                self._complete_request()

        except Exception as e:
            logger.error(
                f"Error handling voice input request: {e}", print_to_terminal=True)
            self._complete_request()

    def _handle_tts_request(self, data: dict):
        """Handle TTS request"""
        try:
            text = data.get("text", "")
            if text and self.tts_service:
                logger.debug(
                    f"Processing TTS request for text: {text[:50]}...")

                # Directly call TTS service instead of going through speak_text()
                # This avoids double-queueing issues
                try:
                    # Set playing flag
                    self.is_playing_tts = True

                    # Call TTS service directly
                    self.tts_service.speak_text(text)

                    # Emit TTS started signal
                    self.tts_started.emit()

                    logger.debug("TTS request processed successfully")

                except Exception as e:
                    logger.error(f"Error in TTS service call: {e}")
                    self.is_playing_tts = False
                    self.tts_error.emit(f"TTS service error: {str(e)}")
                    self._complete_request()
            else:
                logger.warning("TTS request with empty text or no TTS service")
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

    def clear_request_queue(self):
        """Clear all requests and reset voice service state"""
        logger.info("Clearing request queue and resetting voice service state")

        try:
            # Stop all current operations
            if self.is_playing_tts:
                self.stop_tts()
            if self.is_recording:
                self.stop_voice_input()
            if self.is_processing_voice:
                self.is_processing_voice = False
                self.voice_processing_finished.emit()

            # Clear all request state
            self._current_request_id = None
            self._request_queue.clear()
            self._active_requests = 0
            self._interruption_detected = False

            # Disable continuous voice mode
            self.continuous_voice_mode = False

            logger.debug("Request queue cleared and voice service state reset")

        except Exception as e:
            logger.error(f"Error clearing request queue: {e}")

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
            log_thread_info("Emitting request_cancelled signal", logger)
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
            logger.debug(
                "Interruption ignored - too soon after last interruption")
            return

        self._interruption_detected = True
        self._last_interruption_time = current_time

        logger.info(
            "User interruption detected - cancelling current operations")

        # Cancel current request
        self.cancel_current_request()

        # Emit interruption signal
        log_thread_info("Emitting user_interrupted signal", logger)
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

            logger.debug(
                f"High audio level detected ({audio_level:.3f}) during TTS - potential interruption")
            self.handle_user_interruption()

        # Emit audio level for visualization
        log_thread_info(
            f"Emitting audio_level_changed signal: {audio_level:.3f}", logger)
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
                LoggingHelpers.log_audio_operation(
                    "start_voice_input", False, Exception("Recording service not available"))
                logger.error("[VOICE ERROR] Recording service not available")
                self.voice_input_error.emit("Recording service not available")
                return

            if self.is_recording:
                LoggingHelpers.log_warning_with_context("Voice recording already in progress", {
                                                        "is_recording": self.is_recording})
                logger.debug("[VOICE DEBUG] Already recording, skipping")
                return

            if self.is_processing_voice:
                LoggingHelpers.log_warning_with_context("Voice processing already in progress", {
                                                        "is_processing_voice": self.is_processing_voice})
                logger.debug(
                    "[VOICE DEBUG] Already processing voice, skipping")
                return

            # Check if we can handle new requests
            if not self.can_handle_new_request():
                logger.warning(
                    "Cannot handle new voice input - request queue full")
                self.voice_input_error.emit("Request queue full - please wait")
                return

            # Queue the voice input request
            request_id = self.queue_request("voice_input", {})
            logger.debug(
                f"[VOICE DEBUG] Queued voice input request: {request_id}")

        except Exception as e:
            logger.error(f"[VOICE ERROR] Error in start_voice_input: {e}")
            self.voice_input_error.emit(
                f"Failed to start voice input: {str(e)}")

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
        try:
            print(f"[DEBUG] STT result: {text}")
            self.is_processing_voice = False
            self.voice_processing_finished.emit()

            # Forward to response queue if in separate process
            if self.response_queue:
                self.response_queue.put({
                    "type": "voice_processing_finished",
                    "data": None
                })

            # Clean and validate the text
            cleaned_text = text.strip()

            # Only emit if text is not empty and meets minimum length requirements
            if cleaned_text and len(cleaned_text) >= 2:  # Minimum 2 characters
                # Check for common noise patterns and filter them out
                noise_patterns = [
                    "um", "uh", "ah", "er", "hmm", "huh", "what", "yeah", "okay", "right",
                    "so", "well", "like", "you know", "i mean", "basically", "actually"
                ]

                # Convert to lowercase for comparison
                text_lower = cleaned_text.lower()

                # Skip if it's just noise
                if any(pattern in text_lower for pattern in noise_patterns) and len(cleaned_text) < 10:
                    logger.info(
                        f"Filtered out noise: '{cleaned_text}'", print_to_terminal=True)
                    return

                # Log voice input received
                logger.info(
                    f"Voice input received: '{cleaned_text}'", print_to_terminal=True)

                log_thread_info(
                    f"Emitting voice_input_received signal: '{cleaned_text}'", logger)
                self.voice_input_received.emit(cleaned_text)
                # Forward to response queue if in separate process
                if self.response_queue:
                    self.response_queue.put({
                        "type": "voice_input_received",
                        "data": cleaned_text
                    })
            else:
                if cleaned_text:
                    logger.info(
                        f"Voice input too short ({len(cleaned_text)} chars): '{cleaned_text}'", print_to_terminal=True)
                else:
                    logger.info(
                        "STT result was empty, skipping message emission.", print_to_terminal=True)

            # Complete the request
            self._complete_request()

            # In continuous mode, don't restart voice input immediately
            # Wait for TTS to start, then restart voice input during TTS playback
            # This creates the non-interruptive flow: user speaks → stop mic → process → enable mic during TTS
            if self.continuous_voice_mode:
                logger.debug(
                    "Continuous voice mode: voice input stopped during processing, will restart during TTS")
                # Voice input will be restarted in _on_tts_started for non-interruptive flow
        except Exception as e:
            logger.error(f"Error in _on_stt_text_received: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Try to complete request even on error
            try:
                self._complete_request()
            except:
                pass

    def _restart_voice_input_safely(self):
        """Safely restart voice input after ensuring queue is processed"""
        try:
            # Prevent multiple simultaneous restarts
            if hasattr(self, '_restarting_voice_input') and self._restarting_voice_input:
                logger.debug(
                    "Voice input restart already in progress, skipping")
                return

            self._restarting_voice_input = True

            # Check if we can handle new requests before starting
            if self.can_handle_new_request():
                logger.debug(
                    "Safely restarting voice input after queue processing")
                self.start_voice_input()
            else:
                logger.debug(
                    "Cannot restart voice input - queue still full, will retry later")
                # Retry after another delay
                QTimer.singleShot(200, self._restart_voice_input_safely)

            # Reset the flag after a short delay
            QTimer.singleShot(100, lambda: setattr(
                self, '_restarting_voice_input', False))

        except Exception as e:
            logger.error(f"Error in _restart_voice_input_safely: {e}")
            # Reset the flag on error
            if hasattr(self, '_restarting_voice_input'):
                self._restarting_voice_input = False

    def _on_stt_error(self, error: str):
        """Handle STT error"""
        try:
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

            # In continuous mode, restart voice input after error (but with delay)
            if self.continuous_voice_mode:
                logger.debug(
                    "Continuous voice mode: restarting voice input after STT error")
                # Longer delay after error
                QTimer.singleShot(1000, self._restart_voice_input_safely)
        except Exception as e:
            logger.error(f"Error in _on_stt_error: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Try to complete request even on error
            try:
                self._complete_request()
            except:
                pass

    def _on_tts_started(self):
        """Handle TTS started"""
        try:
            self.is_playing_tts = True
            logger.debug("TTS started, setting playing flag")
            self.tts_started.emit()

            # Forward to response queue if in separate process
            if self.response_queue:
                self.response_queue.put({
                    "type": "tts_started",
                    "data": None
                })

            # In continuous mode, restart voice input during TTS for non-interruptive flow
            if self.continuous_voice_mode:
                logger.debug(
                    "Continuous voice mode: restarting voice input during TTS for non-interruptive flow")
                # 1 second delay to let TTS start
                QTimer.singleShot(1000, self._restart_voice_input_safely)
        except Exception as e:
            logger.error(f"Error in _on_tts_started: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Don't re-raise to prevent crashes

    def _on_tts_finished(self):
        """Handle TTS finished event with comprehensive error handling"""
        try:
            log_thread_info("TTS finished signal received")

            # Reset playing flag with thread safety
            if hasattr(self, 'is_playing_tts'):
                self.is_playing_tts = False
                logger.debug("TTS finished, resetting playing flag")

            # Safely restart voice input for continuous mode
            if self.continuous_voice_mode:
                try:
                    logger.debug(
                        "Continuous voice mode: restarting voice input after TTS completion")
                    # Use a timer to ensure TTS cleanup is complete before restarting
                    QTimer.singleShot(100, self._restart_voice_input_safely)
                except Exception as e:
                    logger.error(
                        f"Error restarting voice input after TTS: {e}")

            # Emit finished signal with thread safety
            try:
                self.tts_finished.emit()
            except Exception as e:
                logger.error(f"Error emitting TTS finished signal: {e}")

        except Exception as e:
            logger.error(f"Error in _on_tts_finished: {e}")
            import traceback
            logger.error(
                f"TTS finished error traceback: {traceback.format_exc()}")
        finally:
            # Always ensure playing flag is reset
            try:
                self.is_playing_tts = False
            except Exception as e:
                logger.error(f"Error resetting playing flag: {e}")

    def _on_tts_error(self, error: str):
        """Handle TTS error with comprehensive error handling"""
        try:
            log_thread_info(f"TTS error received: {error}")

            # Reset playing flag
            self.is_playing_tts = False

            # Log the error
            logger.error(f"TTS error: {error}")

            # Emit error signal with thread safety
            try:
                self.tts_error.emit(error)
            except Exception as e:
                logger.error(f"Error emitting TTS error signal: {e}")

            # Restart voice input for continuous mode even on error
            if self.continuous_voice_mode:
                try:
                    logger.debug(
                        "Continuous voice mode: restarting voice input after TTS error")
                    QTimer.singleShot(200, self._restart_voice_input_safely)
                except Exception as e:
                    logger.error(
                        f"Error restarting voice input after TTS error: {e}")

        except Exception as e:
            logger.error(f"Error in _on_tts_error: {e}")
            import traceback
            logger.error(
                f"TTS error handler traceback: {traceback.format_exc()}")

    def speak_text(self, text: str):
        """Speak text with comprehensive error handling and thread safety"""
        try:
            log_thread_info(f"Speak text called: {text[:50]}...")

            if not text or not text.strip():
                logger.warning("Empty text provided to speak_text")
                return

            # Check if TTS is already in progress
            if self.is_playing_tts:
                logger.warning(
                    "TTS already in progress, stopping current playback")
                try:
                    self.stop_tts()
                    # Wait a bit for cleanup
                    QTimer.singleShot(100, lambda: self._speak_text_impl(text))
                except Exception as e:
                    logger.error(f"Error stopping current TTS: {e}")
                    # Try to speak anyway
                    self._speak_text_impl(text)
            else:
                self._speak_text_impl(text)

        except Exception as e:
            logger.error(f"Error in speak_text: {e}")
            import traceback
            logger.error(
                f"Speak text error traceback: {traceback.format_exc()}")
            try:
                self.tts_error.emit(f"TTS failed: {str(e)}")
            except Exception as emit_error:
                logger.error(f"Error emitting TTS error signal: {emit_error}")

    def _speak_text_impl(self, text: str):
        """Implementation of speak_text with thread safety"""
        try:
            log_thread_info(f"Direct TTS call for text: {text[:50]}...")

            # Set playing flag
            self.is_playing_tts = True
            logger.debug("TTS started, setting playing flag")

            # Use TTS service with error handling
            if self.tts_service and self.tts_service.is_available():
                try:
                    # Check if continuous voice mode is enabled
                    if self.continuous_voice_mode:
                        logger.debug(
                            "Continuous voice mode: restarting voice input during TTS for non-interruptive flow")
                        # Restart voice input during TTS for continuous mode
                        QTimer.singleShot(50, self._restart_voice_input_safely)

                    # Use streaming TTS if available
                    if hasattr(self.tts_service, 'speak_text_streaming'):
                        self.tts_service.speak_text_streaming(text)
                    else:
                        self.tts_service.speak_text(text)

                    logger.debug("Direct TTS call completed successfully")

                except Exception as e:
                    logger.error(f"Error calling TTS service: {e}")
                    self.is_playing_tts = False
                    self.tts_error.emit(f"TTS service error: {str(e)}")
            else:
                logger.error("TTS service not available")
                self.is_playing_tts = False
                self.tts_error.emit("TTS service not available")

        except Exception as e:
            logger.error(f"Error in _speak_text_impl: {e}")
            self.is_playing_tts = False
            try:
                self.tts_error.emit(f"TTS implementation error: {str(e)}")
            except Exception as emit_error:
                logger.error(f"Error emitting TTS error signal: {emit_error}")

    def stop_tts(self):
        """Stop TTS with comprehensive error handling"""
        try:
            log_thread_info("Stop TTS called")

            # Reset playing flag first
            self.is_playing_tts = False

            # Stop TTS service with error handling
            if self.tts_service:
                try:
                    self.tts_service.stop_playback()
                    logger.debug("TTS playback stopped successfully")
                except Exception as e:
                    logger.error(f"Error stopping TTS service: {e}")
            else:
                logger.warning("TTS service not available for stopping")

        except Exception as e:
            logger.error(f"Error in stop_tts: {e}")
            import traceback
            logger.error(f"Stop TTS error traceback: {traceback.format_exc()}")

    def set_continuous_voice_mode(self, enabled: bool):
        """Set continuous voice mode"""
        self.continuous_voice_mode = enabled
        logger.debug(
            f"Continuous voice mode: {'enabled' if enabled else 'disabled'}")

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

    def get_silence_threshold(self) -> float:
        """Get silence threshold setting"""
        return self.voice_settings.get("silence_threshold", 0.005)

    def get_recording_timeout(self) -> float:
        """Get recording timeout setting"""
        return self.voice_settings.get("recording_timeout", 10.0)

    def get_current_audio_level(self) -> float:
        """Get current audio level from recording service"""
        if self.recording_service and hasattr(self.recording_service, 'get_current_audio_level'):
            return self.recording_service.get_current_audio_level()
        return 0.0

    def set_recording_timeout(self, timeout: float):
        """Set recording timeout setting"""
        self.voice_settings["recording_timeout"] = timeout

    def set_silence_duration(self, duration: float):
        """Set silence duration setting"""
        self.voice_settings["silence_duration"] = duration

    def set_silence_threshold(self, threshold: float):
        """Set silence threshold setting"""
        self.voice_settings["silence_threshold"] = threshold

    def set_audio_gate_enabled(self, enabled: bool):
        """Set audio gate enabled setting"""
        # This would be implemented in the recording service
        if self.recording_service and hasattr(self.recording_service, 'set_audio_gate_enabled'):
            self.recording_service.set_audio_gate_enabled(enabled)

    def cleanup_on_exit(self):
        """Comprehensive cleanup with error handling"""
        try:
            log_thread_info("Starting comprehensive cleanup")

            # Stop all active operations
            try:
                self.stop_voice_input()
            except Exception as e:
                logger.error(f"Error stopping voice input during cleanup: {e}")

            try:
                self.stop_tts()
            except Exception as e:
                logger.error(f"Error stopping TTS during cleanup: {e}")

            # Clear request queue
            try:
                self.clear_request_queue()
            except Exception as e:
                logger.error(
                    f"Error clearing request queue during cleanup: {e}")

            # Clean up services with error handling
            try:
                if self.recording_service:
                    self.recording_service.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up recording service: {e}")

            try:
                if self.tts_service:
                    self.tts_service.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up TTS service: {e}")

            try:
                if self.stt_service:
                    self.stt_service.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up STT service: {e}")

            # Clean up thread pool
            try:
                if hasattr(self, 'threading_service') and hasattr(self.threading_service, 'cleanup'):
                    self.threading_service.cleanup()
                if hasattr(self, 'persistent_thread_pool') and hasattr(self.persistent_thread_pool, 'cleanup'):
                    self.persistent_thread_pool.cleanup()
            except Exception as e:
                logger.error(
                    f"Error cleaning up threading/persistent thread pool: {e}")

            # Clean up audio files
            try:
                self.cleanup_old_audio_files()
            except Exception as e:
                logger.error(f"Error cleaning up audio files: {e}")

            logger.info("Comprehensive cleanup completed")

        except Exception as e:
            logger.error(f"Error in cleanup_on_exit: {e}")
            import traceback
            logger.error(f"Cleanup error traceback: {traceback.format_exc()}")

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
        cutoff_time = time.time() - (max_age_days * 24 * 60 * 60)

        files_to_delete = []

        # Mark files for deletion based on age
        for file_info in audio_files:
            if file_info['modified'] < cutoff_time:
                files_to_delete.append(file_info)

        # If we still have too many files, delete the oldest ones
        if len(audio_files) - len(files_to_delete) > max_files:
            remaining_files = [
                f for f in audio_files if f not in files_to_delete]
            files_to_delete.extend(remaining_files[max_files:])

        # Delete the marked files
        for file_info in files_to_delete:
            try:
                os.remove(file_info['path'])
                logger.debug(
                    f"Deleted old audio file: {file_info['filename']}")
            except Exception as e:
                logger.error(
                    f"Failed to delete audio file {file_info['filename']}: {e}")

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
                logger.error(
                    f"Failed to delete audio file {file_info['filename']}: {e}")

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
        """Clean up resources with error handling"""
        try:
            log_thread_info("Cleaning up voice service resources")

            # Reset state flags
            try:
                self.is_recording = False
                self.is_processing_voice = False
                self.is_playing_tts = False
                self._interruption_detected = False
            except Exception as e:
                logger.error(f"Error resetting state flags: {e}")

            # Clear active operations
            try:
                self._active_voice_operations.clear()
            except Exception as e:
                logger.error(f"Error clearing active operations: {e}")

            # Reset request tracking
            try:
                self._current_request_id = None
                self._active_requests = 0
            except Exception as e:
                logger.error(f"Error resetting request tracking: {e}")

            logger.debug("Voice service resources cleaned up")

        except Exception as e:
            logger.error(f"Error in _cleanup_resources: {e}")
            import traceback
            logger.error(
                f"Resource cleanup error traceback: {traceback.format_exc()}")

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
            logger.info("STT service initialized successfully",
                        print_to_terminal=True)
        except Exception as e:
            logger.error(
                f"Failed to initialize STT service: {e}", print_to_terminal=True)

        try:
            logger.info("Initializing TTS service...", print_to_terminal=True)
            from pyside_chat.features.voice.tts.tts_service import TTSService
            self.tts_service = TTSService.get_instance()
            logger.info("TTS service initialized successfully",
                        print_to_terminal=True)
        except Exception as e:
            logger.error(
                f"Failed to initialize TTS service: {e}", print_to_terminal=True)

        try:
            logger.info("Initializing Recording service...",
                        print_to_terminal=True)
            from pyside_chat.features.voice.audio.recording_service import RecordingService
            self.recording_service = RecordingService()
            logger.info("Recording service initialized successfully",
                        print_to_terminal=True)
        except Exception as e:
            logger.error(
                f"Failed to initialize Recording service: {e}", print_to_terminal=True)

        # Setup service connections
        self._setup_service_connections()

        # State tracking
        self.is_recording = False
        self.is_playing_tts = False
        self.is_processing_voice = False  # Track if voice processing is in progress
        self.continuous_voice_mode = False  # Track if continuous voice mode is enabled

        # Recording settings
        # Increased from 10.0 to 15.0 seconds (fallback)
        self.recording_timeout = 15.0
        self.silence_threshold = 0.005  # Lowered from 0.01 for better sensitivity
        # Reduced from 4.0 to 3.0 seconds for better responsiveness
        self.silence_duration = 3.0
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
            logger.info(
                "All voice services ready, emitting ready signal", print_to_terminal=True)
            self.voice_service_ready.emit()
        else:
            logger.warning(
                "Voice services not ready yet, will emit signal when ready", print_to_terminal=True)
            # Set up a timer to check again
            if self.in_qt_context:
                QTimer.singleShot(1000, self._check_and_emit_ready)
            else:
                self._check_and_emit_ready()

    def _check_and_emit_ready(self):
        """Check if all services are ready and emit signal if they are"""
        # Add a timeout counter to prevent infinite loops
        if not hasattr(self, '_ready_check_count'):
            self._ready_check_count = 0

        self._ready_check_count += 1

        if self.is_voice_available():
            logger.info(
                "All voice services are now ready, emitting ready signal", print_to_terminal=True)
            self.voice_service_ready.emit()
        elif self._ready_check_count >= 30:  # 30 second timeout
            logger.warning(
                "Voice services not ready after 30 seconds, forcing ready state", print_to_terminal=True)
            self.voice_service_ready.emit()
        else:
            logger.debug(
                f"Voice services still not ready, checking again in 1 second (attempt {self._ready_check_count}/30)")
            if self.in_qt_context:
                QTimer.singleShot(1000, self._check_and_emit_ready)
