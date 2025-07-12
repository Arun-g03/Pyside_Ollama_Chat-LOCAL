"""
Coqui TTS Model Selection Dialog

Allows users to select Coqui TTS models and speakers with download functionality.
"""

import os
from typing import List, Dict, Optional
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QPushButton, QGroupBox, QListWidget,
                               QListWidgetItem, QProgressBar, QMessageBox,
                               QSplitter, QWidget, QTextEdit)
from PySide6.QtCore import Qt, Signal, QThread, QTimer
from PySide6.QtGui import QFont

from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)


class ModelDownloadThread(QThread):
    """Thread for downloading Coqui TTS models"""
    download_progress = Signal(str)
    download_completed = Signal(bool, str)
    
    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name
        
    def run(self):
        try:
            from pyside_chat.features.voice.tts.coqui_tts_service import CoquiTTSService
            
            self.download_progress.emit(f"Starting download of {self.model_name}...")
            
            coqui_service = CoquiTTSService.get_instance()
            success = coqui_service.download_model(self.model_name)
            
            if success:
                self.download_completed.emit(True, f"Successfully downloaded {self.model_name}")
            else:
                self.download_completed.emit(False, f"Failed to download {self.model_name}")
                
        except Exception as e:
            self.download_completed.emit(False, f"Download error: {str(e)}")


class CoquiModelDialog(QDialog):
    """Dialog for selecting Coqui TTS models and speakers"""
    
    # Signals
    model_selected = Signal(str, str)  # model_name, speaker_name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Coqui TTS Model Selection")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        self.coqui_service = None
        self.available_models = []
        self.selected_model = None
        self.selected_speaker = None
        self.download_thread = None
        
        self.setup_ui()
        self.load_models()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Create splitter for model and speaker selection
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Model selection panel (left)
        model_panel = self.create_model_panel()
        splitter.addWidget(model_panel)
        
        # Speaker selection panel (right)
        speaker_panel = self.create_speaker_panel()
        splitter.addWidget(speaker_panel)
        
        # Set splitter proportions
        splitter.setSizes([300, 300])
        
        # Progress bar for downloads
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status text
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.status_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton("Refresh Models")
        self.refresh_button.clicked.connect(self.load_models)
        button_layout.addWidget(self.refresh_button)
        
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.select_button = QPushButton("Select Model & Speaker")
        self.select_button.clicked.connect(self.accept_selection)
        self.select_button.setEnabled(False)
        button_layout.addWidget(self.select_button)
        
        layout.addLayout(button_layout)
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #232323;
                color: #ffffff;
            }
            QGroupBox {
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 16px;
                font-weight: bold;
                color: #fff;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px;
                background: #232323;
                color: #fff;
            }
            QListWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #333;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QListWidget::item:hover {
                background-color: #2d2d2d;
            }
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #888;
            }
            QProgressBar {
                border: 1px solid #444;
                border-radius: 5px;
                text-align: center;
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 5px;
            }
        """)
    
    def create_model_panel(self):
        """Create the model selection panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Model selection group
        model_group = QGroupBox("Available Models")
        model_layout = QVBoxLayout(model_group)
        
        # Model list
        self.model_list = QListWidget()
        self.model_list.itemClicked.connect(self.on_model_selected)
        model_layout.addWidget(self.model_list)
        
        # Model info
        self.model_info_label = QLabel("Select a model to see details")
        self.model_info_label.setWordWrap(True)
        self.model_info_label.setStyleSheet("color: #ccc; font-style: italic;")
        model_layout.addWidget(self.model_info_label)
        
        # Download button
        self.download_button = QPushButton("Download Selected Model")
        self.download_button.clicked.connect(self.download_selected_model)
        self.download_button.setEnabled(False)
        model_layout.addWidget(self.download_button)
        
        layout.addWidget(model_group)
        return widget
    
    def create_speaker_panel(self):
        """Create the speaker selection panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Speaker selection group
        speaker_group = QGroupBox("Available Speakers")
        speaker_layout = QVBoxLayout(speaker_group)
        
        # Speaker list
        self.speaker_list = QListWidget()
        self.speaker_list.itemClicked.connect(self.on_speaker_selected)
        speaker_layout.addWidget(self.speaker_list)
        
        # Speaker info
        self.speaker_info_label = QLabel("Select a model first to see available speakers")
        self.speaker_info_label.setWordWrap(True)
        self.speaker_info_label.setStyleSheet("color: #ccc; font-style: italic;")
        speaker_layout.addWidget(self.speaker_info_label)
        
        layout.addWidget(speaker_group)
        return widget
    
    def load_models(self):
        """Load available Coqui TTS models"""
        try:
            from pyside_chat.features.voice.tts.coqui_tts_service import CoquiTTSService
            
            self.coqui_service = CoquiTTSService.get_instance()
            self.available_models = self.coqui_service.get_available_models()
            
            self.model_list.clear()
            for model in self.available_models:
                item = QListWidgetItem(model)
                
                # Check if model is downloaded
                if self.coqui_service.is_model_downloaded(model):
                    item.setText(f"✅ {model}")
                    item.setData(Qt.UserRole, {"downloaded": True})
                else:
                    size = self.coqui_service.get_model_download_size(model)
                    item.setText(f"⬇️ {model} ({size})")
                    item.setData(Qt.UserRole, {"downloaded": False, "size": size})
                
                self.model_list.addItem(item)
            
            self.log_status(f"Loaded {len(self.available_models)} available models")
            
        except Exception as e:
            self.log_status(f"Failed to load models: {str(e)}")
            QMessageBox.warning(self, "Error", f"Failed to load Coqui TTS models:\n{str(e)}")
    
    def on_model_selected(self, item):
        """Handle model selection"""
        model_name = item.text().replace("✅ ", "").replace("⬇️ ", "").split(" (")[0]
        self.selected_model = model_name
        
        # Update model info
        item_data = item.data(Qt.UserRole)
        if item_data.get("downloaded", False):
            self.model_info_label.setText(f"✅ Model '{model_name}' is downloaded and ready to use")
            self.download_button.setEnabled(False)
        else:
            size = item_data.get("size", "unknown size")
            self.model_info_label.setText(f"⬇️ Model '{model_name}' needs to be downloaded ({size})")
            self.download_button.setEnabled(True)
        
        # Load speakers for this model
        self.load_speakers_for_model(model_name)
        
        # Update selection button
        self.update_selection_button()
    
    def load_speakers_for_model(self, model_name: str):
        """Load available speakers for the selected model"""
        try:
            if not self.coqui_service:
                return
            
            # Try to load the model to get speakers
            if self.coqui_service.load_model(model_name):
                speakers = self.coqui_service.get_available_voices()
                
                self.speaker_list.clear()
                if speakers:
                    for speaker in speakers:
                        item = QListWidgetItem(speaker)
                        self.speaker_list.addItem(item)
                    
                    self.speaker_info_label.setText(f"Found {len(speakers)} speakers for model '{model_name}'")
                else:
                    self.speaker_info_label.setText(f"Model '{model_name}' has no multiple speakers (single voice)")
                    # Add a default speaker item
                    item = QListWidgetItem("default")
                    self.speaker_list.addItem(item)
                
                self.log_status(f"Loaded {len(speakers) if speakers else 1} speakers for model '{model_name}'")
                
            else:
                self.speaker_list.clear()
                self.speaker_info_label.setText(f"Failed to load model '{model_name}'")
                self.log_status(f"Failed to load speakers for model '{model_name}'")
                
        except Exception as e:
            self.log_status(f"Error loading speakers: {str(e)}")
    
    def on_speaker_selected(self, item):
        """Handle speaker selection"""
        self.selected_speaker = item.text()
        self.speaker_info_label.setText(f"Selected speaker: {self.selected_speaker}")
        self.update_selection_button()
    
    def download_selected_model(self):
        """Download the selected model"""
        if not self.selected_model:
            return
        
        reply = QMessageBox.question(
            self, 
            "Download Model", 
            f"Download model '{self.selected_model}'?\n\n"
            "This may take several minutes depending on your internet connection.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.start_download(self.selected_model)
    
    def start_download(self, model_name: str):
        """Start downloading a model"""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.download_button.setEnabled(False)
        self.refresh_button.setEnabled(False)
        
        self.download_thread = ModelDownloadThread(model_name)
        self.download_thread.download_progress.connect(self.log_status)
        self.download_thread.download_completed.connect(self.on_download_completed)
        self.download_thread.start()
    
    def on_download_completed(self, success: bool, message: str):
        """Handle download completion"""
        self.progress_bar.setVisible(False)
        self.download_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
        
        self.log_status(message)
        
        if success:
            QMessageBox.information(self, "Download Complete", message)
            # Reload models to update download status
            self.load_models()
        else:
            QMessageBox.critical(self, "Download Failed", message)
    
    def update_selection_button(self):
        """Update the selection button state"""
        self.select_button.setEnabled(
            self.selected_model is not None and 
            self.selected_speaker is not None
        )
    
    def accept_selection(self):
        """Accept the current model and speaker selection"""
        if self.selected_model and self.selected_speaker:
            self.model_selected.emit(self.selected_model, self.selected_speaker)
            self.accept()
        else:
            QMessageBox.warning(self, "Selection Required", "Please select both a model and a speaker.")
    
    def log_status(self, message: str):
        """Log a status message"""
        self.status_text.append(f"[{self.get_current_time()}] {message}")
        # Auto-scroll to bottom
        self.status_text.verticalScrollBar().setValue(
            self.status_text.verticalScrollBar().maximum()
        )
    
    def get_current_time(self):
        """Get current time string"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S") 