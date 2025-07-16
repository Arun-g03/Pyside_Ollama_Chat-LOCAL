# Shared imports
from pyside_chat.core.shared_imports.pyside_imports import *
from pyside_chat.core.shared_imports.shared_imports import *


"""
Threading Service - Integrates QThread/QRunnable architecture with existing chat system.

This service provides:
- Integration of new QThread and QRunnable components
- Unified interface for all threading operations
- Modern threading architecture without legacy patterns
- Persistent thread pool integration for better resource management
"""

# Import new threading components
from .qthread_workers import ChatStreamingWorker, AudioStreamingWorker, MonitoringWorker, VoiceProcessingWorker
from .qrunnable_tasks import MessageProcessingTask, FileProcessingTask, DataProcessingTask
from .thread_pool_manager import get_global_thread_pool_manager
from .thread_monitor import get_global_thread_monitor
from .persistent_thread_pool import get_global_persistent_thread_pool
from .thread_calculator import get_pool_thread_count

logger = CustomLogger.get_logger(__name__)


class ThreadingService(QObject):
    """
    Service that manages all threading operations in the chat application.

    This service provides:
    - Unified interface for QThread and QRunnable operations
    - Integration with existing event system
    - Monitoring and debugging capabilities
    - Persistent thread pool integration
    """

    # Signals for streaming operations
    # chunk, model_name, msg_id, chunk_index
    chunk_received = Signal(str, str, str, int)
    progress_updated = Signal(str)  # For progress updates
    finished = Signal()  # For completion
    error = Signal(str)  # For errors
    
    # Voice processing signals for UI updates
    voice_audio_level_changed = Signal(float)  # Audio level for UI
    voice_eq_bars_changed = Signal(list)  # EQ bars for UI
    voice_recording_started = Signal()  # Recording started
    voice_recording_stopped = Signal()  # Recording stopped
    voice_recording_error = Signal(str)  # Recording error
    voice_input_received = Signal(str)  # Voice input received
    voice_input_error = Signal(str)  # Voice input error

    def __init__(self, parent=None):
        try:
            super().__init__(parent)

            # Initialize threading managers with error handling
            try:
                self.thread_pool_manager = get_global_thread_pool_manager()
            except Exception as e:
                logger.error(
                    f"[ID:TS001A] Failed to initialize thread_pool_manager: {e}")
                self.thread_pool_manager = None

            try:
                self.thread_monitor = get_global_thread_monitor()
            except Exception as e:
                logger.error(
                    f"[ID:TS001B] Failed to initialize thread_monitor: {e}")
                self.thread_monitor = None

            try:
                self.persistent_thread_pool = get_global_persistent_thread_pool()
            except Exception as e:
                logger.error(
                    f"[ID:TS001C] Failed to initialize persistent_thread_pool: {e}")
                self.persistent_thread_pool = None

            # Initialize persistent thread pools
            self._initialize_persistent_pools()

            # Current active threads from persistent pool
            self.current_chat_thread = None
            self.current_audio_thread = None
            self.current_monitoring_thread = None
            self.current_voice_thread = None

            # QRunnable tasks tracking
            self.active_tasks = {}

            logger.debug(
                "[ID:TS001] ThreadingService initialized with persistent thread pools")
        except Exception as e:
            logger.error(f"[ID:TS001E] Exception in __init__: {e}")
            logger.error(traceback.format_exc())

            # Ensure critical attributes are set even if initialization fails
            if not hasattr(self, 'persistent_thread_pool'):
                self.persistent_thread_pool = None
            if not hasattr(self, 'current_chat_thread'):
                self.current_chat_thread = None
            if not hasattr(self, 'current_audio_thread'):
                self.current_audio_thread = None
            if not hasattr(self, 'current_monitoring_thread'):
                self.current_monitoring_thread = None
            if not hasattr(self, 'current_voice_thread'):
                self.current_voice_thread = None
            if not hasattr(self, 'active_tasks'):
                self.active_tasks = {}
            if not hasattr(self, 'thread_pool_manager'):
                self.thread_pool_manager = None
            if not hasattr(self, 'thread_monitor'):
                self.thread_monitor = None

    def _initialize_persistent_pools(self):
        """Initialize persistent thread pools for different operations."""
        try:
            logger.debug("[ID:TS002] Initializing persistent thread pools")

            # Get recommended sizes with fallback values
            try:
                chat_streaming_size = get_pool_thread_count('streaming')
            except Exception as e:
                logger.error(
                    f"[ID:TS002A] Failed to get chat_streaming_size: {e}")
                chat_streaming_size = 2

            try:
                audio_streaming_size = get_pool_thread_count('background')
            except Exception as e:
                logger.error(
                    f"[ID:TS002B] Failed to get audio_streaming_size: {e}")
                audio_streaming_size = 1

            try:
                monitoring_size = get_pool_thread_count('ui_update')
            except Exception as e:
                logger.error(f"[ID:TS002C] Failed to get monitoring_size: {e}")
                monitoring_size = 1

            try:
                voice_processing_size = get_pool_thread_count('background')
            except Exception as e:
                logger.error(
                    f"[ID:TS002D] Failed to get voice_processing_size: {e}")
                voice_processing_size = 1

            # Only initialize pools if persistent_thread_pool is available
            if self.persistent_thread_pool is None:
                logger.error(
                    "[ID:TS002E] Persistent thread pool is None, skipping initialization")
                return

            # Initialize chat streaming pool
            self.persistent_thread_pool.initialize_pool(
                'chat_streaming',
                ChatStreamingWorker,
                size=chat_streaming_size,
                max_wait_time=30.0,
                idle_timeout=300.0
            )

            # Initialize audio streaming pool
            self.persistent_thread_pool.initialize_pool(
                'audio_streaming',
                AudioStreamingWorker,
                size=audio_streaming_size,
                max_wait_time=10.0,
                idle_timeout=180.0
            )

            # Initialize monitoring pool
            self.persistent_thread_pool.initialize_pool(
                'monitoring',
                MonitoringWorker,
                size=monitoring_size,
                max_wait_time=5.0,
                idle_timeout=600.0
            )

            # Initialize voice processing pool for voice service operations
            self.persistent_thread_pool.initialize_pool(
                'voice_processing',
                VoiceProcessingWorker,  # Use dedicated voice processing worker
                size=voice_processing_size,
                max_wait_time=15.0,
                idle_timeout=240.0
            )

            logger.debug(
                "[ID:TS003] Persistent thread pools initialized successfully")

        except Exception as e:
            logger.error(
                f"[ID:TS004] Error initializing persistent pools: {e}")
            logger.error(traceback.format_exc())

    def start_chat_streaming(self, context_messages: List[Dict], model: str, temperature: float, config_manager, streaming_message_id: str = None) -> bool:
        """
        Start chat streaming using persistent thread pool.

        This method:
        - Gets a thread from the persistent pool
        - Configures the worker for streaming
        - Starts the streaming operation
        - Returns the thread to pool when done
        """
        try:
            logger.debug(
                f"[ID:TS005] Starting chat streaming for model: {model}")

            # Check if persistent thread pool is available
            if self.persistent_thread_pool is None:
                logger.error(
                    "[ID:TS005A] Persistent thread pool is not available")
                return False

            # Stop any existing chat streaming
            self.stop_chat_streaming()

            # Get thread from persistent pool
            thread = self.persistent_thread_pool.get_thread(
                'chat_streaming', timeout=120.0)
            if not thread:
                logger.error(
                    "[ID:TS006] Failed to get chat streaming thread from pool")
                return False

            self.current_chat_thread = thread
            worker = thread.worker

            # Configure worker for streaming with streaming message ID
            logger.debug(
                f"[TS_DEBUG] Configuring worker with streaming_message_id: {streaming_message_id}")
            worker.configure_streaming(
                context_messages=context_messages,
                model=model,
                temperature=temperature,
                config_manager=config_manager,
                streaming_message_id=streaming_message_id
            )

            # Connect signals with QueuedConnection for thread safety
            worker.chunk_received.connect(
                self._on_chat_chunk_received, Qt.ConnectionType.QueuedConnection
            )
            worker.progress_updated.connect(
                self._on_chat_progress_updated, Qt.ConnectionType.QueuedConnection
            )
            worker.finished.connect(
                self._on_chat_streaming_finished, Qt.ConnectionType.QueuedConnection
            )
            worker.error.connect(
                self._on_chat_streaming_error, Qt.ConnectionType.QueuedConnection
            )

            # Start streaming
            worker.start_streaming()

            logger.debug(
                f"[ID:TS007] Chat streaming started with thread: {thread.objectName()}")
            return True

        except Exception as e:
            logger.error(f"[ID:TS008] Error starting chat streaming: {e}")
            logger.error(traceback.format_exc())
            return False

    def stop_chat_streaming(self):
        """Stop chat streaming and return thread to pool."""
        try:
            if self.current_chat_thread and self.current_chat_thread.worker:
                logger.debug("[ID:TS009] Stopping chat streaming")

                # Stop the worker
                self.current_chat_thread.worker.stop()

                # Wait for completion with timeout
                timeout = 5.0
                start_time = time.time()
                while self.current_chat_thread.worker.is_running() and (time.time() - start_time) < timeout:
                    time.sleep(0.1)

                # Return thread to pool if persistent thread pool is available
                if self.persistent_thread_pool is not None:
                    self.persistent_thread_pool.return_thread(
                        self.current_chat_thread)
                else:
                    logger.warning(
                        "[ID:TS009A] Persistent thread pool not available, cannot return thread")

                self.current_chat_thread = None

                logger.debug(
                    "[ID:TS010] Chat streaming stopped and thread returned to pool")

        except Exception as e:
            logger.error(f"[ID:TS011] Error stopping chat streaming: {e}")
            logger.error(traceback.format_exc())

    def start_audio_streaming(self, audio_source: str, sample_rate: int = 16000,
                              chunk_size: int = 1024) -> bool:
        """Start audio streaming using persistent thread pool."""
        try:
            logger.debug(
                f"[ID:TS012] Starting audio streaming from: {audio_source}")

            # Stop any existing audio streaming
            self.stop_audio_streaming()

            # Get thread from persistent pool
            thread = self.persistent_thread_pool.get_thread(
                'audio_streaming', timeout=10.0)
            if not thread:
                logger.error(
                    "[ID:TS013] Failed to get audio streaming thread from pool")
                return False

            self.current_audio_thread = thread
            worker = thread.worker

            # Configure worker for audio streaming
            worker.configure_audio_streaming(
                audio_source=audio_source,
                sample_rate=sample_rate,
                chunk_size=chunk_size
            )

            # Connect signals
            worker.chunk_received.connect(
                self._on_audio_chunk_received, Qt.ConnectionType.QueuedConnection
            )
            worker.finished.connect(
                self._on_audio_streaming_finished, Qt.ConnectionType.QueuedConnection
            )
            worker.error.connect(
                self._on_audio_streaming_error, Qt.ConnectionType.QueuedConnection
            )

            # Start streaming
            worker.start_audio_streaming()

            logger.debug(
                f"[ID:TS014] Audio streaming started with thread: {thread.objectName()}")
            return True

        except Exception as e:
            logger.error(f"[ID:TS015] Error starting audio streaming: {e}")
            logger.error(traceback.format_exc())
            return False

    def stop_audio_streaming(self):
        """Stop audio streaming and return thread to pool."""
        try:
            if self.current_audio_thread and self.current_audio_thread.worker:
                logger.debug("[ID:TS016] Stopping audio streaming")

                # Stop the worker
                self.current_audio_thread.worker.stop()

                # Return thread to pool
                self.persistent_thread_pool.return_thread(
                    self.current_audio_thread)
                self.current_audio_thread = None

                logger.debug(
                    "[ID:TS017] Audio streaming stopped and thread returned to pool")

        except Exception as e:
            logger.error(f"[ID:TS018] Error stopping audio streaming: {e}")
            logger.error(traceback.format_exc())

    def start_monitoring(self, monitor_interval: float = 1.0, alert_threshold: float = 0.8) -> bool:
        """Start system monitoring using persistent thread pool."""
        try:
            logger.debug(
                f"[ID:TS019] Starting system monitoring (interval: {monitor_interval}s)")

            # Stop any existing monitoring
            self.stop_monitoring()

            # Get thread from persistent pool
            thread = self.persistent_thread_pool.get_thread(
                'monitoring', timeout=5.0)
            if not thread:
                logger.error(
                    "[ID:TS020] Failed to get monitoring thread from pool")
                return False

            self.current_monitoring_thread = thread
            worker = thread.worker

            # Configure worker for monitoring
            worker.configure_monitoring(
                monitor_interval=monitor_interval,
                alert_threshold=alert_threshold
            )

            # Connect signals
            worker.resource_updated.connect(
                self._on_resource_updated, Qt.ConnectionType.QueuedConnection
            )
            worker.alert_triggered.connect(
                self._on_alert_triggered, Qt.ConnectionType.QueuedConnection
            )
            worker.finished.connect(
                self._on_monitoring_finished, Qt.ConnectionType.QueuedConnection
            )
            worker.error.connect(
                self._on_monitoring_error, Qt.ConnectionType.QueuedConnection
            )

            # Start monitoring
            worker.start_monitoring()

            logger.debug(
                f"[ID:TS021] Monitoring started with thread: {thread.objectName()}")
            return True

        except Exception as e:
            logger.error(f"[ID:TS022] Error starting monitoring: {e}")
            logger.error(traceback.format_exc())
            return False

    def stop_monitoring(self):
        """Stop monitoring and return thread to pool."""
        try:
            if self.current_monitoring_thread and self.current_monitoring_thread.worker:
                logger.debug("[ID:TS023] Stopping monitoring")

                # Stop the worker
                self.current_monitoring_thread.worker.stop()

                # Return thread to pool
                self.persistent_thread_pool.return_thread(
                    self.current_monitoring_thread)
                self.current_monitoring_thread = None

                logger.debug(
                    "[ID:TS024] Monitoring stopped and thread returned to pool")

        except Exception as e:
            logger.error(f"[ID:TS025] Error stopping monitoring: {e}")
            logger.error(traceback.format_exc())

    def start_voice_processing(self, operation_type: str, **kwargs) -> bool:
        """
        Start voice processing using persistent thread pool.

        Args:
            operation_type: Type of voice operation ('stt', 'tts', 'recording')
            **kwargs: Additional configuration parameters

        Returns:
            bool: True if started successfully, False otherwise
        """
        try:
            logger.debug(
                f"[ID:TS026] Starting voice processing for operation: {operation_type}")

            # Check if persistent thread pool is available
            if self.persistent_thread_pool is None:
                logger.error(
                    "[ID:TS026A] Persistent thread pool is not available")
                return False

            # Stop any existing voice processing
            self.stop_voice_processing()

            # Get thread from persistent pool
            thread = self.persistent_thread_pool.get_thread(
                'voice_processing', timeout=15.0)
            if not thread:
                logger.error(
                    "[ID:TS027] Failed to get voice processing thread from pool")
                return False

            self.current_voice_thread = thread
            worker = thread.worker

            # Configure worker for voice processing
            worker.configure_voice_processing(
                operation_type=operation_type,
                **kwargs
            )

            # Connect signals with QueuedConnection for thread safety
            worker.voice_input_received.connect(
                self._on_voice_input_received, Qt.ConnectionType.QueuedConnection
            )
            worker.voice_input_error.connect(
                self._on_voice_input_error, Qt.ConnectionType.QueuedConnection
            )
            worker.tts_started.connect(
                self._on_tts_started, Qt.ConnectionType.QueuedConnection
            )
            worker.tts_finished.connect(
                self._on_tts_finished, Qt.ConnectionType.QueuedConnection
            )
            worker.tts_error.connect(
                self._on_tts_error, Qt.ConnectionType.QueuedConnection
            )
            worker.recording_started.connect(
                self._on_recording_started, Qt.ConnectionType.QueuedConnection
            )
            worker.recording_stopped.connect(
                self._on_recording_stopped, Qt.ConnectionType.QueuedConnection
            )
            worker.recording_error.connect(
                self._on_recording_error, Qt.ConnectionType.QueuedConnection
            )
            worker.audio_level_changed.connect(
                self._on_audio_level_changed, Qt.ConnectionType.QueuedConnection
            )
            worker.eq_bars_changed.connect(
                self._on_eq_bars_changed, Qt.ConnectionType.QueuedConnection
            )
            worker.user_interrupted.connect(
                self._on_user_interrupted, Qt.ConnectionType.QueuedConnection
            )
            worker.request_cancelled.connect(
                self._on_request_cancelled, Qt.ConnectionType.QueuedConnection
            )
            worker.finished.connect(
                self._on_voice_processing_finished, Qt.ConnectionType.QueuedConnection
            )
            worker.error.connect(
                self._on_voice_processing_error, Qt.ConnectionType.QueuedConnection
            )

            # Start voice processing
            print(f"[THREADING SERVICE] 🎤 Starting voice processing with operation: {operation_type}")
            worker.start_voice_processing()

            logger.debug(
                f"[ID:TS028] Voice processing started with thread: {thread.objectName()}")
            print(f"[THREADING SERVICE] ✅ Voice processing started successfully")
            return True

        except Exception as e:
            logger.error(f"[ID:TS029] Error starting voice processing: {e}")
            logger.error(traceback.format_exc())
            return False

    def stop_voice_processing(self):
        """Stop voice processing and return thread to pool."""
        try:
            if self.current_voice_thread and self.current_voice_thread.worker:
                logger.debug("[ID:TS030] Stopping voice processing")

                # Stop the worker
                self.current_voice_thread.worker.stop()

                # Wait for completion with timeout
                timeout = 5.0
                start_time = time.time()
                while self.current_voice_thread.worker.is_running() and (time.time() - start_time) < timeout:
                    time.sleep(0.1)

                # Return thread to pool if persistent thread pool is available
                if self.persistent_thread_pool is not None:
                    self.persistent_thread_pool.return_thread(
                        self.current_voice_thread)
                else:
                    logger.warning(
                        "[ID:TS030A] Persistent thread pool not available, cannot return thread")

                self.current_voice_thread = None

                logger.debug(
                    "[ID:TS031] Voice processing stopped and thread returned to pool")

        except Exception as e:
            logger.error(f"[ID:TS032] Error stopping voice processing: {e}")
            logger.error(traceback.format_exc())

    # Signal handlers for persistent threads
    def _on_chat_chunk_received(self, chunk: str, model_name: str, msg_id: str, chunk_index: int):
        """Handle chat chunk received from persistent thread."""
        try:
            logger.debug(
                f"[TS_CHUNK_DEBUG] Emitting chunk_received signal: chunk='{chunk[:20]}...', model_name='{model_name}', msg_id='{msg_id}', chunk_index={chunk_index}")
            self.chunk_received.emit(chunk, model_name, msg_id, chunk_index)
            logger.debug(
                f"[TS_CHUNK_DEBUG] Successfully emitted chunk_received signal")
        except Exception as e:
            logger.error(f"[ID:TS026] Error handling chat chunk: {e}")

    def _on_chat_progress_updated(self, progress: str):
        """Handle chat progress update from persistent thread."""
        try:
            self.progress_updated.emit(progress)
        except Exception as e:
            logger.error(f"[ID:TS027] Error handling chat progress: {e}")

    def _on_chat_streaming_finished(self):
        """Handle chat streaming finished from persistent thread."""
        try:
            logger.debug("[ID:TS028] Chat streaming finished")
            self.finished.emit()

            # Return thread to pool
            if self.current_chat_thread:
                self.persistent_thread_pool.return_thread(
                    self.current_chat_thread)
                self.current_chat_thread = None

        except Exception as e:
            logger.error(
                f"[ID:TS029] Error handling chat streaming finished: {e}")

    def _on_chat_streaming_error(self, error_message: str):
        """Handle chat streaming error from persistent thread."""
        try:
            logger.error(f"[ID:TS030] Chat streaming error: {error_message}")
            self.error.emit(error_message)

            # Return thread to pool even on error
            if self.current_chat_thread:
                self.persistent_thread_pool.return_thread(
                    self.current_chat_thread)
                self.current_chat_thread = None

        except Exception as e:
            logger.error(
                f"[ID:TS031] Error handling chat streaming error: {e}")

    def _on_audio_chunk_received(self, chunk: str):
        """Handle audio chunk received from persistent thread."""
        try:
            # Handle audio chunk (could emit different signal)
            pass
        except Exception as e:
            logger.error(f"[ID:TS032] Error handling audio chunk: {e}")

    def _on_audio_streaming_finished(self):
        """Handle audio streaming finished from persistent thread."""
        try:
            logger.debug("[ID:TS033] Audio streaming finished")

            # Return thread to pool
            if self.current_audio_thread:
                self.persistent_thread_pool.return_thread(
                    self.current_audio_thread)
                self.current_audio_thread = None

        except Exception as e:
            logger.error(
                f"[ID:TS034] Error handling audio streaming finished: {e}")

    def _on_audio_streaming_error(self, error_message: str):
        """Handle audio streaming error from persistent thread."""
        try:
            logger.error(f"[ID:TS035] Audio streaming error: {error_message}")

            # Return thread to pool even on error
            if self.current_audio_thread:
                self.persistent_thread_pool.return_thread(
                    self.current_audio_thread)
                self.current_audio_thread = None

        except Exception as e:
            logger.error(
                f"[ID:TS036] Error handling audio streaming error: {e}")

    def _on_resource_updated(self, resource_data: Dict[str, Any]):
        """Handle resource update from monitoring thread."""
        try:
            # Handle resource update
            pass
        except Exception as e:
            logger.error(f"[ID:TS037] Error handling resource update: {e}")

    def _on_alert_triggered(self, alert_message: str):
        """Handle alert from monitoring thread."""
        try:
            logger.warning(f"[ID:TS038] System alert: {alert_message}")
        except Exception as e:
            logger.error(f"[ID:TS039] Error handling alert: {e}")

    def _on_monitoring_finished(self):
        """Handle monitoring finished from persistent thread."""
        try:
            logger.debug("[ID:TS040] Monitoring finished")

            # Return thread to pool
            if self.current_monitoring_thread:
                self.persistent_thread_pool.return_thread(
                    self.current_monitoring_thread)
                self.current_monitoring_thread = None

        except Exception as e:
            logger.error(f"[ID:TS041] Error handling monitoring finished: {e}")

    def _on_monitoring_error(self, error_message: str):
        """Handle monitoring error from persistent thread."""
        try:
            logger.error(f"[ID:TS042] Monitoring error: {error_message}")

            # Return thread to pool even on error
            if self.current_monitoring_thread:
                self.persistent_thread_pool.return_thread(
                    self.current_monitoring_thread)
                self.current_monitoring_thread = None

        except Exception as e:
            logger.error(f"[ID:TS043] Error handling monitoring error: {e}")

    # Voice processing signal handlers
    def _on_voice_input_received(self, text: str):
        """Handle voice input received from persistent thread."""
        try:
            logger.debug(f"[ID:TS044] Voice input received: {text[:50]}...")
            # Forward to voice service or emit signal
            self.voice_input_received.emit(text)
        except Exception as e:
            logger.error(f"[ID:TS045] Error handling voice input: {e}")

    def _on_voice_input_error(self, error_message: str):
        """Handle voice input error from persistent thread."""
        try:
            logger.error(f"[ID:TS046] Voice input error: {error_message}")
            # Forward to voice service or emit signal
            self.voice_input_error.emit(error_message)
        except Exception as e:
            logger.error(f"[ID:TS047] Error handling voice input error: {e}")

    def _on_tts_started(self):
        """Handle TTS started from persistent thread."""
        try:
            logger.debug("[ID:TS048] TTS started")
            # Forward to voice service or emit signal
        except Exception as e:
            logger.error(f"[ID:TS049] Error handling TTS started: {e}")

    def _on_tts_finished(self):
        """Handle TTS finished from persistent thread."""
        try:
            logger.debug("[ID:TS050] TTS finished")
            # Forward to voice service or emit signal
        except Exception as e:
            logger.error(f"[ID:TS051] Error handling TTS finished: {e}")

    def _on_tts_error(self, error_message: str):
        """Handle TTS error from persistent thread."""
        try:
            logger.error(f"[ID:TS052] TTS error: {error_message}")
            # Forward to voice service or emit signal
        except Exception as e:
            logger.error(f"[ID:TS053] Error handling TTS error: {e}")

    def _on_recording_started(self):
        """Handle recording started from persistent thread."""
        try:
            logger.debug("[ID:TS054] Recording started")
            # Forward to voice service or emit signal
            self.voice_recording_started.emit()
        except Exception as e:
            logger.error(f"[ID:TS055] Error handling recording started: {e}")

    def _on_recording_stopped(self):
        """Handle recording stopped from persistent thread."""
        try:
            logger.debug("[ID:TS056] Recording stopped")
            # Forward to voice service or emit signal
            self.voice_recording_stopped.emit()
        except Exception as e:
            logger.error(f"[ID:TS057] Error handling recording stopped: {e}")

    def _on_recording_error(self, error_message: str):
        """Handle recording error from persistent thread."""
        try:
            logger.error(f"[ID:TS058] Recording error: {error_message}")
            # Forward to voice service or emit signal
            self.voice_recording_error.emit(error_message)
        except Exception as e:
            logger.error(f"[ID:TS059] Error handling recording error: {e}")

    def _on_audio_level_changed(self, audio_level: float):
        """Handle audio level changed from persistent thread."""
        try:
            logger.debug(f"[ID:TS060] Audio level changed: {audio_level:.3f}")
            # Forward to voice service or emit signal
            # Get the global voice service and forward the signal
            from pyside_chat.features.voice.voice_service import VoiceService
            voice_service = VoiceService.get_instance()
            
            if voice_service and hasattr(voice_service, 'audio_level_changed'):
                # Emit the signal to the voice service which will forward to UI
                voice_service.audio_level_changed.emit(audio_level)
                logger.debug(f"[ID:TS060A] Forwarded audio level {audio_level:.3f} to voice service")
            else:
                logger.warning("[ID:TS060B] No voice service available to forward audio level")
                
            # Emit signal for voice controls to listen to
            self.voice_audio_level_changed.emit(audio_level)
            print(f"[THREADING SERVICE] 🔊 Audio level: {audio_level:.3f}")
        except Exception as e:
            logger.error(f"[ID:TS061] Error handling audio level changed: {e}")

    def _on_eq_bars_changed(self, bars: list):
        """Handle EQ bars changed from persistent thread."""
        try:
            logger.debug(f"[ID:TS062] EQ bars changed: {len(bars)} bars")
            # Forward to voice service or emit signal
            # Get the global voice service and forward the signal
            from pyside_chat.features.voice.voice_service import VoiceService
            voice_service = VoiceService.get_instance()
            
            if voice_service and hasattr(voice_service, 'eq_bars_changed'):
                # Emit the signal to the voice service which will forward to UI
                voice_service.eq_bars_changed.emit(bars)
                logger.debug(f"[ID:TS062A] Forwarded EQ bars {len(bars)} to voice service")
            else:
                logger.warning("[ID:TS062B] No voice service available to forward EQ bars")
                
            # Emit signal for voice controls to listen to
            self.voice_eq_bars_changed.emit(bars)
        except Exception as e:
            logger.error(f"[ID:TS063] Error handling EQ bars changed: {e}")

    def _on_user_interrupted(self):
        """Handle user interrupted from persistent thread."""
        try:
            logger.debug("[ID:TS064] User interrupted")
            # Forward to voice service or emit signal
        except Exception as e:
            logger.error(f"[ID:TS065] Error handling user interrupted: {e}")

    def _on_request_cancelled(self):
        """Handle request cancelled from persistent thread."""
        try:
            logger.debug("[ID:TS066] Request cancelled")
            # Forward to voice service or emit signal
        except Exception as e:
            logger.error(f"[ID:TS067] Error handling request cancelled: {e}")

    def _on_voice_processing_finished(self):
        """Handle voice processing finished from persistent thread."""
        try:
            logger.debug("[ID:TS068] Voice processing finished")

            # Return thread to pool
            if self.current_voice_thread:
                self.persistent_thread_pool.return_thread(
                    self.current_voice_thread)
                self.current_voice_thread = None

        except Exception as e:
            logger.error(f"[ID:TS069] Error handling voice processing finished: {e}")

    def _on_voice_processing_error(self, error_message: str):
        """Handle voice processing error from persistent thread."""
        try:
            logger.error(f"[ID:TS070] Voice processing error: {error_message}")

            # Return thread to pool even on error
            if self.current_voice_thread:
                self.persistent_thread_pool.return_thread(
                    self.current_voice_thread)
                self.current_voice_thread = None

        except Exception as e:
            logger.error(f"[ID:TS071] Error handling voice processing error: {e}")

    # QRunnable task methods (unchanged)
    def process_message(self, message: str, operation: str = "spell_check",
                        callback: Optional[Callable] = None) -> str:
        """Process message using QRunnable."""
        try:
            logger.debug(
                f"[ID:TS044] Processing message with operation: {operation}")
            task = MessageProcessingTask(message, operation, callback)
            task_id = self.thread_pool_manager.start_task(task)
            self.active_tasks[task_id] = task
            return task_id

        except Exception as e:
            logger.error(f"[ID:TS045] Error processing message: {e}")
            logger.error(traceback.format_exc())
            return ""

    def process_file(self, file_path: str, operation: str = "read",
                     callback: Optional[Callable] = None) -> str:
        """Process file operation using QRunnable."""
        try:
            logger.debug(
                f"[ID:TS046] Processing file with operation: {operation}")
            task = FileProcessingTask(file_path, operation, callback)
            task_id = self.thread_pool_manager.start_task(task)
            self.active_tasks[task_id] = task
            return task_id

        except Exception as e:
            logger.error(f"[ID:TS047] Error processing file: {e}")
            logger.error(traceback.format_exc())
            return ""

    def process_data(self, data: Any, operation: str = "calculate",
                     callback: Optional[Callable] = None) -> str:
        """Process data using QRunnable."""
        try:
            logger.debug(
                f"[ID:TS048] Processing data with operation: {operation}")
            task = DataProcessingTask(data, operation, callback=callback)
            task_id = self.thread_pool_manager.start_task(task)
            self.active_tasks[task_id] = task
            return task_id

        except Exception as e:
            logger.error(f"[ID:TS049] Error processing data: {e}")
            logger.error(traceback.format_exc())
            return ""

    def get_threading_status(self) -> Dict[str, Any]:
        """Get current threading status and statistics."""
        try:
            return {
                'persistent_threads': {
                    'chat_streaming': {
                        'active': self.current_chat_thread is not None,
                        'thread_name': self.current_chat_thread.objectName() if self.current_chat_thread else None
                    },
                    'audio_streaming': {
                        'active': self.current_audio_thread is not None,
                        'thread_name': self.current_audio_thread.objectName() if self.current_audio_thread else None
                    },
                    'monitoring': {
                        'active': self.current_monitoring_thread is not None,
                        'thread_name': self.current_monitoring_thread.objectName() if self.current_monitoring_thread else None
                    },
                    'voice_processing': {
                        'active': self.current_voice_thread is not None,
                        'thread_name': self.current_voice_thread.objectName() if self.current_voice_thread else None
                    }
                },
                'persistent_pool_status': self.persistent_thread_pool.get_pool_status(),
                'qrunnable_tasks': {
                    'active_tasks': len(self.active_tasks),
                    'pool_status': self.thread_pool_manager.get_pool_status()
                },
                'monitoring': {
                    'thread_monitor_stats': self.thread_monitor.stats,
                    'resource_usage': self.thread_monitor.get_resource_usage()
                }
            }

        except Exception as e:
            logger.error(f"[ID:TS050] Error getting threading status: {e}")
            logger.error(traceback.format_exc())
            return {}

    def cleanup(self):
        """Clean up all threading resources."""
        try:
            logger.debug("[ID:TS051] Cleaning up ThreadingService")

            # Stop all persistent threads
            self.stop_chat_streaming()
            self.stop_audio_streaming()
            self.stop_monitoring()
            self.stop_voice_processing()

            # Wait for QRunnable tasks to complete
            if self.active_tasks:
                logger.debug(
                    "[ID:TS052] Waiting for QRunnable tasks to complete")
                timeout = 10.0
                start_time = time.time()
                while self.active_tasks and (time.time() - start_time) < timeout:
                    time.sleep(0.1)

                if self.active_tasks:
                    logger.warning(
                        "[ID:TS053] Some QRunnable tasks did not complete within timeout")

            logger.debug("[ID:TS054] ThreadingService cleanup complete")

        except Exception as e:
            logger.error(
                f"[ID:TS055] Error during ThreadingService cleanup: {e}")
            logger.error(traceback.format_exc())


# Global threading service instance
_global_threading_service: Optional[ThreadingService] = None


def get_global_threading_service() -> ThreadingService:
    """Get the global threading service instance."""
    global _global_threading_service

    if _global_threading_service is None:
        _global_threading_service = ThreadingService()
        logger.debug("[ID:TS056] Created global ThreadingService")

    return _global_threading_service


def shutdown_global_threading_service():
    """Shutdown the global threading service."""
    global _global_threading_service

    if _global_threading_service:
        _global_threading_service.cleanup()
        _global_threading_service = None
        logger.debug("[ID:TS057] Shutdown global ThreadingService")
