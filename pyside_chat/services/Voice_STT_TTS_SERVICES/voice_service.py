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
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
import subprocess
import platform
import json

from pyside_chat.utils.Logging.Custom_Logger import CustomLogger
from .STT_Service import STTService
from .TTS_Service import TTSService
from .Recording_Service import RecordingService

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
    
    def __init__(self):
        super().__init__()
        self.stt_service = STTService()
        self.tts_service = TTSService()
        self.recording_service = RecordingService()
        
        # Connect signals
        self.stt_service.text_received.connect(self._on_stt_text_received)
        self.stt_service.error_occurred.connect(self._on_stt_error)
        self.tts_service.tts_started.connect(self.tts_started.emit)
        self.tts_service.tts_finished.connect(self._on_tts_finished)
        self.tts_service.tts_error.connect(self._on_tts_error)
        self.recording_service.recording_started.connect(self.recording_started.emit)
        self.recording_service.recording_stopped.connect(self.recording_stopped.emit)
        self.recording_service.recording_error.connect(self.recording_error.emit)
        self.recording_service.recording_auto_stopped.connect(self._on_recording_auto_stopped)
        
        # State tracking
        self.is_recording = False
        self.is_playing_tts = False
        self.is_processing_voice = False  # Track if voice processing is in progress
        self.continuous_voice_mode = False  # Track if continuous voice mode is enabled
        
        # Recording settings
        self.recording_timeout = 10.0  # Default 10 seconds (fallback)
        self.silence_threshold = 0.01  # Audio level threshold for silence detection
        self.silence_duration = 4.0    # Seconds of silence before stopping
        self.recording_timer = QTimer()
        self.recording_timer.setSingleShot(True)
        self.recording_timer.timeout.connect(self._on_recording_timeout)
        
        # Clean up all audio files on startup (since they're only for STT processing)
        QTimer.singleShot(1000, lambda: self.cleanup_all_audio_files())
    
    def __del__(self):
        """Cleanup when voice service is destroyed"""
        try:
            self.cleanup_all_audio_files()
            if hasattr(self, 'recording_service'):
                self.recording_service.cleanup()
        except:
            pass  # Ignore errors during cleanup
        
    def start_voice_input(self):
        """Start voice recording and convert to text"""
        if self.is_recording:
            logger.warning("Voice recording already in progress")
            return
            
        if self.is_processing_voice:
            logger.warning("Voice processing already in progress, please wait")
            return
            
        try:
            self.is_recording = True
            
            # Update recording service with audio gate settings
            self.recording_service.silence_threshold = self.silence_threshold
            self.recording_service.silence_duration = self.silence_duration
            
            self.recording_service.start_recording()
            
            # Start fallback recording timeout timer (in case audio gate fails)
            timeout_ms = int(self.recording_timeout * 1000)
            self.recording_timer.start(timeout_ms)
            
            logger.debug(f"Voice input started with audio gate (silence: {self.silence_duration}s, threshold: {self.silence_threshold})")
        except Exception as e:
            self.is_recording = False
            logger.error(f"Failed to start voice input: {e}")
            self.voice_input_error.emit(f"Failed to start voice input: {str(e)}")
    
    def stop_voice_input(self):
        """Stop voice recording and process the audio"""
        if not self.is_recording and not self.recording_service.frames:
            logger.warning("No voice recording in progress")
            return
            
        if self.is_processing_voice:
            logger.warning("Voice processing already in progress")
            return
            
        try:
            self.recording_timer.stop()
            result = self.recording_service.stop_recording()
            self.is_recording = False
            if result is None:
                logger.warning("No audio file generated")
                self.voice_input_error.emit("No audio recorded")
                return
            audio_file, speech_detected = result
            if audio_file and os.path.exists(audio_file) and speech_detected:
                self.is_processing_voice = True
                self.voice_processing_started.emit()
                self.stt_service.convert_audio_to_text(audio_file)
            else:
                logger.info("No speech detected during recording. Doing nothing.")
                return
        except Exception as e:
            if self.is_recording:
                self.is_recording = False
            self.is_processing_voice = False
            logger.error(f"Failed to stop voice input: {e}")
            self.voice_input_error.emit(f"Failed to process voice input: {str(e)}")
    
    def _on_recording_timeout(self):
        """Handle recording timeout - automatically stop recording"""
        if self.is_recording:
            logger.debug("Recording timeout reached, stopping automatically")
            self.stop_voice_input()
    
    def _on_recording_auto_stopped(self):
        """Handle recording auto-stopped due to silence detection"""
        if self.is_recording:
            logger.debug("Recording auto-stopped due to silence, processing voice input")
            self.stop_voice_input()
    
    def _on_stt_text_received(self, text: str):
        """Handle STT text received"""
        self.is_processing_voice = False
        self.voice_processing_finished.emit()
        
        # Only emit if text is not empty or whitespace
        if text.strip():
            self.voice_input_received.emit(text)
        else:
            logger.info("STT result was empty, skipping message emission.")
        
        # If continuous voice mode is enabled, restart recording automatically
        if self.continuous_voice_mode:
            logger.debug("Continuous voice mode enabled, restarting recording")
            QTimer.singleShot(100, self.start_voice_input)  # Small delay to ensure processing is complete
    
    def _on_stt_error(self, error: str):
        """Handle STT error"""
        self.is_processing_voice = False
        self.voice_processing_finished.emit()
        self.voice_input_error.emit(error)
        
        # If continuous voice mode is enabled, restart recording even after error
        if self.continuous_voice_mode:
            logger.debug("Continuous voice mode enabled, restarting recording after error")
            QTimer.singleShot(100, self.start_voice_input)  # Small delay to ensure processing is complete
    
    def _on_tts_finished(self):
        """Handle TTS finished"""
        self.is_playing_tts = False
        logger.debug("TTS finished, resetting playing flag")
        self.tts_finished.emit()
    
    def _on_tts_error(self, error: str):
        """Handle TTS error"""
        self.is_playing_tts = False
        logger.error(f"TTS error: {error}")
        self.tts_error.emit(error)
    
    def speak_text(self, text: str):
        """Convert text to speech and play it"""
        if self.is_playing_tts:
            logger.warning("TTS already in progress")
            return
            
        try:
            self.is_playing_tts = True
            self.tts_service.speak_text(text)
            logger.debug(f"TTS started for text: {text[:50]}...")
        except Exception as e:
            self.is_playing_tts = False
            logger.error(f"Failed to start TTS: {e}")
            self.tts_error.emit(f"Failed to start TTS: {str(e)}")
    
    def stop_tts(self):
        """Stop current TTS playback"""
        self.tts_service.stop_playback()
        self.is_playing_tts = False
    
    def is_voice_available(self) -> bool:
        """Check if voice functionality is available"""
        return (self.stt_service.is_available() and 
                self.tts_service.is_available() and 
                self.recording_service.is_available())
    
    def update_settings(self, settings: dict):
        """Update voice service settings"""
        logger.debug(f"Updating voice service settings: {settings}")
        
        # Update STT service settings
        if "stt_api" in settings:
            self.stt_service.update_api(settings["stt_api"])
            
        # Update TTS service settings
        if "tts_api" in settings:
            self.tts_service.update_api(settings["tts_api"])
            
        if "tts_voice" in settings:
            self.tts_service.update_voice(settings["tts_voice"])
            
        if "voice_speed" in settings:
            # Convert speed setting to TTS speed (1.0 = normal, higher = faster)
            speed = settings["voice_speed"]
            if speed < 1.0:
                # Slower than normal
                tts_speed = 1.0 / speed
            else:
                # Faster than normal
                tts_speed = speed
            self.tts_service.update_speed(tts_speed)
            
        # Update recording settings
        if "recording_timeout" in settings:
            self.recording_timeout = settings["recording_timeout"]
            logger.debug(f"Recording timeout updated to {self.recording_timeout}s")
            
        if "silence_duration" in settings:
            self.silence_duration = settings["silence_duration"]
            logger.debug(f"Silence duration updated to {self.silence_duration}s")
            
        if "silence_threshold" in settings:
            self.silence_threshold = settings["silence_threshold"]
            logger.debug(f"Silence threshold updated to {self.silence_threshold}")
    
    def get_recording_timeout(self) -> float:
        """Get current recording timeout in seconds"""
        return self.recording_timeout
    
    def set_recording_timeout(self, timeout: float):
        """Set recording timeout in seconds"""
        self.recording_timeout = max(1.0, min(60.0, timeout))  # Clamp between 1-60 seconds
        logger.debug(f"Recording timeout set to {self.recording_timeout}s")
    
    def get_silence_duration(self) -> float:
        """Get current silence duration in seconds"""
        return self.silence_duration
    
    def set_silence_duration(self, duration: float):
        """Set silence duration in seconds"""
        self.silence_duration = max(0.5, min(10.0, duration))  # Clamp between 0.5-10 seconds
        logger.debug(f"Silence duration set to {self.silence_duration}s")
    
    def get_silence_threshold(self) -> float:
        """Get current silence threshold (0-1)"""
        return self.silence_threshold
    
    def set_silence_threshold(self, threshold: float):
        """Set silence threshold (0-1)"""
        self.silence_threshold = max(0.001, min(0.1, threshold))  # Clamp between 0.001-0.1
        logger.debug(f"Silence threshold set to {self.silence_threshold}")
    
    def set_audio_gate_enabled(self, enabled: bool):
        """Enable or disable audio gate detection"""
        self.recording_service.set_audio_gate_enabled(enabled)
        logger.debug(f"Audio gate {'enabled' if enabled else 'disabled'} for voice service")
    
    def get_current_audio_level(self) -> float:
        """Get current audio level for debugging"""
        return self.recording_service.get_current_audio_level()
    
    def set_continuous_voice_mode(self, enabled: bool):
        """Enable or disable continuous voice mode"""
        self.continuous_voice_mode = enabled
        logger.debug(f"Continuous voice mode {'enabled' if enabled else 'disabled'}")
    
    def is_continuous_voice_mode(self) -> bool:
        """Check if continuous voice mode is enabled"""
        return self.continuous_voice_mode
    
    def cleanup_on_exit(self):
        """Clean up audio files on application exit"""
        logger.info("Cleaning up audio files on application exit")
        self.cleanup_all_audio_files()
        
        # Clean up recording service
        if hasattr(self, 'recording_service'):
            self.recording_service.cleanup()
    
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