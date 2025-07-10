import sys
import math
import random
import threading
import os
from PySide6.QtCore import Qt, QTimer, QMetaObject, Slot, Signal
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QBrush, QRadialGradient, QPainterPath, QTransform, QPen
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QComboBox, QCheckBox
)
import sounddevice as sd
import soundfile as sf
import numpy as np

# Import EQ widgets
from pyside_chat.ui.Audio_visualisers.eq_widgets import *




# Optional: Hardcode an audio path here
HARDCODED_AUDIO_PATH = r"C:\Users\arun-\iCloudDrive\notaBIGFAN.mp3"

# Additional audio file paths for presets
AUDIO_PRESETS = {
    "Nota BIGFAN": r"C:\Users\arun-\iCloudDrive\notaBIGFAN.mp3",
    "TTS Output": r"C:\Users\arun-\AppData\Local\Temp\tts_user_models\tts_output.wav",
    "LOTR Passage": r"C:\Users\arun-\AppData\Local\Temp\tts_user_models\Lord_Of_rings_Passage_tts_output.wav",
    "Sample 2": r"C:\Users\arun-\Music\sample2.mp3",
    "Sample 3": r"C:\Users\arun-\Music\sample3.mp3",
    "Test Audio": r"C:\Users\arun-\Downloads\test_audio.wav"
}

BAR_EQ_MULTIPLIER = 1

# Frequency band mapping for proper EQ visualization
FREQ_BANDS = {
    'bass': (20, 250),      # Bass: 20-250 Hz
    'low_mid': (250, 500),   # Low Mid: 250-500 Hz  
    'mid': (500, 2000),      # Mid: 500-2000 Hz
    'high_mid': (2000, 4000), # High Mid: 2000-4000 Hz
    'treble': (4000, 20000)  # Treble: 4000-20000 Hz
}

# Bar distribution across frequency bands
BAR_DISTRIBUTION = {
    'bass': 0.25,        # 25% of bars for bass (bars 0-11)
    'low_mid': 0.15,     # 15% of bars for low mid (bars 12-19)
    'mid': 0.25,         # 25% of bars for mid (bars 20-31)
    'high_mid': 0.15,    # 15% of bars for high mid (bars 32-39)
    'treble': 0.20       # 20% of bars for treble (bars 40-47)
}

def map_frequency_to_bars(fft_magnitude, sample_rate, num_bars=48):
    """
    Map FFT frequency bins to bar ranges based on frequency bands.
    
    Args:
        fft_magnitude: FFT magnitude array
        sample_rate: Audio sample rate
        num_bars: Number of bars to generate
        
    Returns:
        list: Bar values mapped to frequency bands
    """
    # Calculate frequency resolution
    freq_resolution = sample_rate / (2 * len(fft_magnitude))
    
    # Calculate bar distribution
    bars_per_band = {}
    current_bar = 0
    for band, ratio in BAR_DISTRIBUTION.items():
        bars_in_band = int(num_bars * ratio)
        bars_per_band[band] = (current_bar, current_bar + bars_in_band)
        current_bar += bars_in_band
    
    # Ensure we use all bars
    if current_bar < num_bars:
        bars_per_band['treble'] = (bars_per_band['treble'][0], num_bars)
    
    # Map frequency bins to bars
    bar_values = [0.1] * num_bars  # Start with minimum values
    
    for band, (low_freq, high_freq) in FREQ_BANDS.items():
        if band not in bars_per_band:
            continue
            
        start_bar, end_bar = bars_per_band[band]
        bars_in_band = end_bar - start_bar
        
        # Find frequency bin range for this band
        low_bin = int(low_freq / freq_resolution)
        high_bin = int(high_freq / freq_resolution)
        high_bin = min(high_bin, len(fft_magnitude) - 1)
        
        if low_bin >= high_bin:
            continue
            
        # Get magnitude values for this frequency band
        band_magnitude = fft_magnitude[low_bin:high_bin + 1]
        
        if len(band_magnitude) == 0:
            continue
            
        # Split band magnitude into bars
        if bars_in_band > 0:
            bins_per_bar = max(1, len(band_magnitude) // bars_in_band)
            
            for i in range(bars_in_band):
                start_idx = i * bins_per_bar
                end_idx = min(start_idx + bins_per_bar, len(band_magnitude))
                
                if start_idx < len(band_magnitude):
                    # Calculate RMS energy for this bar's frequency range
                    bar_bins = band_magnitude[start_idx:end_idx]
                    if len(bar_bins) > 0:
                        energy = float(np.sqrt(np.mean(bar_bins**2))) * BAR_EQ_MULTIPLIER
                        bar_values[start_bar + i] = energy
    
    return bar_values

def band_energy(mag, sr, n_points, f_lo, f_hi):
    """Calculate energy for a specific frequency band."""
    freq_res = sr / (2 * len(mag))
    lo_bin = int(f_lo / freq_res)
    hi_bin = int(f_hi / freq_res)
    hi_bin = min(hi_bin, len(mag)-1)
    band = mag[lo_bin:hi_bin+1]
    minval = 0.25
    if len(band) == 0:
        return [minval]*n_points
    bins_per = max(1, len(band)//n_points)
    vals = []
    for i in range(n_points):
        s = i*bins_per
        e = min(s+bins_per, len(band))
        if s < len(band):
            v = float(np.sqrt(np.mean(band[s:e]**2)))
            vals.append(v)
        else:
            vals.append(minval)
    if max(vals) > 0:
        maxv = max(vals)
        return [minval+(1.0-minval)*(v/maxv) for v in vals]
    else:
        return [minval]*n_points

class MainWindow(QMainWindow):
    # Signal to update bar values from audio thread
    bar_values_updated = Signal(list)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EQ Visualizer - Mode Switcher")
        main_widget = QWidget(self)
        vbox = QVBoxLayout(main_widget)
        
        # Mode switcher
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Circle EQ", "Bar EQ", "Waveform EQ", "Waveform Gradient", "Waveform Blue Gradient"])
        self.mode_combo.currentIndexChanged.connect(self.switch_mode)
        vbox.addWidget(self.mode_combo)
        
        # Audio controls
        hbox = QHBoxLayout()
        self.audio_path_label = QLabel("No audio file selected", self)
        self.audio_path_label.setWordWrap(True)
        self.select_btn = QPushButton("Select Audio File", self)
        self.select_btn.clicked.connect(self.select_audio_file)
        self.play_btn = QPushButton("Play", self)
        self.play_btn.clicked.connect(self.play_audio)
        self.mute_btn = QPushButton("Mute", self)
        self.mute_btn.setCheckable(True)
        self.mute_btn.clicked.connect(self.toggle_mute)
        self.system_audio_checkbox = QCheckBox("Use Microphone Input", self)
        self.system_audio_checkbox.stateChanged.connect(self.toggle_system_audio)
        
        # Device dropdown
        self.device_combo = QComboBox(self)
        self.device_combo.setMinimumWidth(220)
        self.device_combo.addItem("Select microphone device...")
        self.device_combo.currentIndexChanged.connect(self.on_device_selected)
        self.system_audio_device_index = None
        
        # Refresh button for devices
        self.refresh_devices_btn = QPushButton("Refresh Devices", self)
        self.refresh_devices_btn.clicked.connect(self.refresh_device_list)
        
        hbox.addWidget(self.select_btn)
        hbox.addWidget(self.audio_path_label)
        hbox.addWidget(self.play_btn)
        hbox.addWidget(self.mute_btn)
        hbox.addWidget(self.system_audio_checkbox)
        hbox.addWidget(self.device_combo)
        hbox.addWidget(self.refresh_devices_btn)
        vbox.addLayout(hbox)
        
        # Audio presets
        preset_label = QLabel("Audio Presets:", self)
        vbox.addWidget(preset_label)
        
        # Create preset buttons in a grid layout
        preset_layout = QHBoxLayout()
        self.preset_buttons = {}
        
        for preset_name, preset_path in AUDIO_PRESETS.items():
            btn = QPushButton(preset_name, self)
            btn.setMaximumWidth(120)
            btn.clicked.connect(lambda checked, path=preset_path, name=preset_name: self.load_audio_preset(path, name))
            preset_layout.addWidget(btn)
            self.preset_buttons[preset_name] = btn
        
        vbox.addLayout(preset_layout)
        
        # Visualizer area
        self.visualizer_stack = QWidget()
        self.visualizer_layout = QVBoxLayout(self.visualizer_stack)
        self.visualizer_layout.setContentsMargins(0, 0, 0, 0)
        
        # Initialize EQ widgets
        self.circle_widget = CircleEQWidget(self)
        self.bar_widget = BarEQWidget(self)
        
        # Three overlapping nets for bass, mid, treble
        self.waveform_net_container = QWidget(self)
        self.waveform_net_container.setAttribute(Qt.WA_TranslucentBackground)
        self.waveform_net_container.setLayout(None)
        self.waveform_bg = QWidget(self.waveform_net_container)
        self.waveform_bg.setStyleSheet('background: black;')
        self.waveform_bg.lower()
        self.waveform_bass = CircularNetEQWidget(self.waveform_net_container, num_points=64, color=(80,180,255))
        self.waveform_mid = CircularNetEQWidget(self.waveform_net_container, num_points=64, color=(255,80,180))
        self.waveform_treble = CircularNetEQWidget(self.waveform_net_container, num_points=64, color=(220,255,120))
        
        # Three overlapping gradient widgets for bass, mid, treble
        self.waveform_grad_container = QWidget(self)
        self.waveform_grad_container.setAttribute(Qt.WA_TranslucentBackground)
        self.waveform_grad_container.setLayout(None)
        self.waveform_grad_bg = QWidget(self.waveform_grad_container)
        self.waveform_grad_bg.setStyleSheet('background: black;')
        self.waveform_grad_bg.lower()
        self.waveform_grad_bass = CircularGradientEQWidget(self.waveform_grad_container, num_points=64, color=(80,180,255))
        self.waveform_grad_mid = CircularGradientEQWidget(self.waveform_grad_container, num_points=64, color=(255,80,180))
        self.waveform_grad_treble = CircularGradientEQWidget(self.waveform_grad_container, num_points=64, color=(220,255,120))
        
        # Three overlapping blue gradient widgets for bass, mid, treble
        self.waveform_bluegrad_container = QWidget(self)
        self.waveform_bluegrad_container.setAttribute(Qt.WA_TranslucentBackground)
        self.waveform_bluegrad_container.setLayout(None)
        self.waveform_bluegrad_bg = QWidget(self.waveform_bluegrad_container)
        self.waveform_bluegrad_bg.setStyleSheet('background: black;')
        self.waveform_bluegrad_bg.lower()
        self.waveform_blue_bass = CircularGradientEQWidget(self.waveform_bluegrad_container, num_points=64, color=(80,180,255), alpha=255, radius_scale=1.0, radius_ratio=0.30, energy_mult=1.5)
        self.waveform_blue_mid = CircularGradientEQWidget(self.waveform_bluegrad_container, num_points=64, color=(100,140,255), alpha=255, radius_scale=0.9, radius_ratio=0.30, energy_mult=1.5)
        self.waveform_blue_treble = CircularGradientEQWidget(self.waveform_bluegrad_container, num_points=64, color=(120,220,255), alpha=255, radius_scale=0.81, radius_ratio=0.30, energy_mult=1.5)
        
        # Add widgets to layout
        self.visualizer_layout.addWidget(self.circle_widget)
        self.visualizer_layout.addWidget(self.bar_widget)
        self.visualizer_layout.addWidget(self.waveform_net_container)
        self.visualizer_layout.addWidget(self.waveform_grad_container)
        self.visualizer_layout.addWidget(self.waveform_bluegrad_container)
        
        # Hide all widgets initially
        self.bar_widget.hide()
        self.waveform_net_container.hide()
        self.waveform_bass.hide()
        self.waveform_mid.hide()
        self.waveform_treble.hide()
        self.waveform_grad_container.hide()
        self.waveform_grad_bass.hide()
        self.waveform_grad_mid.hide()
        self.waveform_grad_treble.hide()
        self.waveform_bluegrad_container.hide()
        self.waveform_blue_bass.hide()
        self.waveform_blue_mid.hide()
        self.waveform_blue_treble.hide()
        
        # Connect signal to update bar values
        self.bar_values_updated.connect(self.bar_widget.set_eq_bars)
        
        vbox.addWidget(self.visualizer_stack, stretch=1)
        self.setCentralWidget(main_widget)
        self.resize(900, 600)
        
        # Audio state
        if HARDCODED_AUDIO_PATH:
            self.selected_audio_path = HARDCODED_AUDIO_PATH
            self.audio_path_label.setText(f"Selected: {HARDCODED_AUDIO_PATH}")
            # Highlight the default preset button if it exists
            for preset_name, preset_path in AUDIO_PRESETS.items():
                if preset_path == HARDCODED_AUDIO_PATH:
                    self.preset_buttons[preset_name].setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
                    break
        else:
            self.selected_audio_path = None
        self.is_playing = False
        self.is_muted = False
        self.play_thread = None
        self.use_system_audio = False
        
        # Auto-select first microphone if available
        QTimer.singleShot(100, self.auto_select_microphone)

    def switch_mode(self, idx):
        was_playing = self.is_playing
        if was_playing:
            self.stop_audio()
        
        # Hide all widgets first
        self.circle_widget.hide()
        self.circle_widget.stop_animation()
        self.bar_widget.hide()
        self.bar_widget.stop_animation()
        self.waveform_net_container.hide()
        self.waveform_bass.hide()
        self.waveform_mid.hide()
        self.waveform_treble.hide()
        self.waveform_grad_container.hide()
        self.waveform_grad_bass.hide()
        self.waveform_grad_mid.hide()
        self.waveform_grad_treble.hide()
        self.waveform_bluegrad_container.hide()
        self.waveform_blue_bass.hide()
        self.waveform_blue_mid.hide()
        self.waveform_blue_treble.hide()
        
        # Show and start appropriate widgets based on mode
        if idx == 0:  # Circle EQ
            self.circle_widget.show()
            self.circle_widget.start_animation()
        elif idx == 1:  # Bar EQ
            self.bar_widget.show()
            self.bar_widget.start_animation()
        elif idx == 2:  # Waveform EQ
            self.waveform_net_container.show()
            self.waveform_bass.show()
            self.waveform_bass.start_animation()
            self.waveform_mid.show()
            self.waveform_mid.start_animation()
            self.waveform_treble.show()
            self.waveform_treble.start_animation()
        elif idx == 3:  # Waveform Gradient
            self.waveform_grad_container.show()
            self.waveform_grad_bass.show()
            self.waveform_grad_bass.start_animation()
            self.waveform_grad_mid.show()
            self.waveform_grad_mid.start_animation()
            self.waveform_grad_treble.show()
            self.waveform_grad_treble.start_animation()
        elif idx == 4:  # Waveform Blue Gradient
            self.waveform_bluegrad_container.show()
            self.waveform_blue_bass.show()
            self.waveform_blue_bass.start_animation()
            self.waveform_blue_mid.show()
            self.waveform_blue_mid.start_animation()
            self.waveform_blue_treble.show()
            self.waveform_blue_treble.start_animation()
        
        if was_playing:
            self.play_audio()

    def select_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", "", "Audio Files (*.wav *.mp3 *.flac *.ogg);;All Files (*)")
        if file_path:
            self.selected_audio_path = file_path
            self.audio_path_label.setText(f"Selected: {file_path}")
        else:
            self.audio_path_label.setText("No audio file selected")

    def load_audio_preset(self, file_path, preset_name):
        """Load an audio file from a preset."""
        if os.path.exists(file_path):
            self.selected_audio_path = file_path
            self.audio_path_label.setText(f"Selected: {preset_name}")
            print(f"Loaded preset: {preset_name} - {file_path}")
            
            # Highlight the selected preset button
            for name, btn in self.preset_buttons.items():
                if name == preset_name:
                    btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
                else:
                    btn.setStyleSheet("")
        else:
            print(f"Audio file not found: {file_path}")
            self.audio_path_label.setText(f"Error: File not found - {preset_name}")

    def play_audio(self):
        if not self.use_system_audio and not self.selected_audio_path:
            return
        if not self.is_playing:
            self.is_playing = True
            self.play_btn.setText("Stop")
            self.play_thread = threading.Thread(target=self._play_audio_thread, daemon=True)
            self.play_thread.start()
        else:
            self.stop_audio()

    def stop_audio(self):
        self.is_playing = False
        self.play_btn.setText("Play")
        self.circle_widget.set_eq_sections([0.1] * self.circle_widget.num_sections)
        self.bar_widget.set_idle()
        self.waveform_bass.set_idle()
        self.waveform_mid.set_idle()
        self.waveform_treble.set_idle()
        self.waveform_grad_bass.set_idle()
        self.waveform_grad_mid.set_idle()
        self.waveform_grad_treble.set_idle()
        self.waveform_blue_bass.set_idle()
        self.waveform_blue_mid.set_idle()
        self.waveform_blue_treble.set_idle()

    def toggle_mute(self):
        self.is_muted = self.mute_btn.isChecked()
        self.mute_btn.setText("Unmute" if self.is_muted else "Mute")

    def toggle_system_audio(self, state):
        self.use_system_audio = bool(state)
        if self.use_system_audio:
            if self.system_audio_device_index is None and self.device_combo.count() > 1:
                self.device_combo.setCurrentIndex(1)
            elif self.system_audio_device_index is not None:
                device_name = self.device_combo.currentText()
                self.audio_path_label.setText(f"Microphone: {device_name}")
            else:
                self.audio_path_label.setText("Microphone input will be visualized. (Select a device)")
        else:
            if self.selected_audio_path:
                self.audio_path_label.setText(f"Selected: {self.selected_audio_path}")
            else:
                self.audio_path_label.setText("No audio file selected")

    def on_device_selected(self, idx):
        if idx > 0:
            self.system_audio_device_index = self.device_combo.itemData(idx)
            device_name = self.device_combo.currentText()
            if self.use_system_audio:
                self.audio_path_label.setText(f"Microphone: {device_name}")
        else:
            self.system_audio_device_index = None
            if self.use_system_audio:
                self.audio_path_label.setText("Microphone input will be visualized.")

    def _play_audio_thread(self):
        if self.use_system_audio:
            self._play_microphone_audio()
        else:
            self._play_file_audio()

    def _play_microphone_audio(self):
        device_index = self.system_audio_device_index
        if device_index is None:
            print("[MIC] No microphone device selected!")
            self.is_playing = False
            self.play_btn.setText("Play")
            return
        
        print(f"[MIC] Using device index {device_index} for microphone input.")
        try:
            samplerate = 44100
            channels = 1
            blocksize = 2048
            with sd.InputStream(
                device=device_index,
                channels=channels,
                samplerate=samplerate,
                dtype='float32',
                blocksize=blocksize,
                latency='low'
            ) as stream:
                audio_counter = 0
                while self.is_playing:
                    data, overflowed = stream.read(blocksize)
                    if np.any(data != 0):
                        audio_counter = min(audio_counter + 1, 10)
                    
                    chunk = data[:, 0] if data.shape[1] > 0 else np.zeros(blocksize)
                    self._process_audio_chunk(chunk, samplerate)
                    sd.sleep(20)
        except Exception as e:
            print(f"Microphone error: {e}")
        finally:
            self._reset_visualizers()

    def _play_file_audio(self):
        try:
            data, samplerate = sf.read(self.selected_audio_path, dtype='float32')
            frames_per_update = int(samplerate * 0.05)
            total_frames = len(data)
            idx = 0
            
            def callback(outdata, frames, time, status):
                nonlocal idx
                if self.is_muted:
                    outdata[:] = 0
                else:
                    chunk = data[idx:idx+frames]
                    if len(chunk.shape) > 1:
                        chunk = chunk.mean(axis=1)
                    outdata[:len(chunk), 0] = chunk
                    if chunk.shape[0] < frames:
                        outdata[chunk.shape[0]:, 0] = 0
                
                self._process_audio_chunk(chunk, samplerate)
                idx += frames
            
            with sd.OutputStream(channels=1, samplerate=samplerate, callback=callback, blocksize=frames_per_update):
                while idx < total_frames and self.is_playing:
                    sd.sleep(50)
        except Exception as e:
            print(f"Audio playback error: {e}")
        finally:
            self._reset_visualizers()

    def _process_audio_chunk(self, chunk, samplerate):
        """Process audio chunk and update appropriate visualizer based on current mode."""
        mode = self.mode_combo.currentIndex()
        
        if len(chunk) == 0:
            return
        
        try:
            fft = np.fft.rfft(chunk, n=2048)
            mag = np.abs(fft)
            
            if mode == 0:  # Circle EQ
                raw_circle_values = map_frequency_to_bars(mag, samplerate, self.circle_widget.num_sections)
                if raw_circle_values and max(raw_circle_values) > 0:
                    max_val = max(raw_circle_values)
                    normalized_circle_vals = [0.1 + 0.9 * (v / max_val) for v in raw_circle_values]
                else:
                    normalized_circle_vals = [0.1] * len(raw_circle_values)
                
                if len(normalized_circle_vals) != self.circle_widget.num_sections:
                    if len(normalized_circle_vals) > self.circle_widget.num_sections:
                        normalized_circle_vals = normalized_circle_vals[:self.circle_widget.num_sections]
                    else:
                        normalized_circle_vals.extend([0.1] * (self.circle_widget.num_sections - len(normalized_circle_vals)))
                
                self.circle_widget.set_eq_sections(normalized_circle_vals)
                
            elif mode == 1:  # Bar EQ
                raw_bar_values = map_frequency_to_bars(mag, samplerate, self.bar_widget.num_bars)
                if raw_bar_values and max(raw_bar_values) > 0:
                    max_val = max(raw_bar_values)
                    normalized_vals = [0.1 + 0.9 * (v / max_val) for v in raw_bar_values]
                else:
                    normalized_vals = [0.1] * len(raw_bar_values)
                
                if len(normalized_vals) != self.bar_widget.num_bars:
                    if len(normalized_vals) > self.bar_widget.num_bars:
                        normalized_vals = normalized_vals[:self.bar_widget.num_bars]
                    else:
                        normalized_vals.extend([0.1] * (self.bar_widget.num_bars - len(normalized_vals)))
                
                self.bar_values_updated.emit(normalized_vals)
                
            elif mode in [2, 3, 4]:  # Waveform modes
                npts = 64
                bass_vals = band_energy(mag, samplerate, npts, 20, 250)
                mid_vals = band_energy(mag, samplerate, npts, 250, 2000)
                treb_vals = band_energy(mag, samplerate, npts, 2000, 20000)
                
                if mode == 2:  # Waveform EQ
                    self.waveform_bass.set_net_radii(bass_vals)
                    self.waveform_mid.set_net_radii(mid_vals)
                    self.waveform_treble.set_net_radii(treb_vals)
                elif mode == 3:  # Waveform Gradient
                    self.waveform_grad_bass.set_net_radii(bass_vals)
                    self.waveform_grad_mid.set_net_radii(mid_vals)
                    self.waveform_grad_treble.set_net_radii(treb_vals)
                elif mode == 4:  # Waveform Blue Gradient
                    self.waveform_blue_bass.set_net_radii(bass_vals)
                    self.waveform_blue_mid.set_net_radii(mid_vals)
                    self.waveform_blue_treble.set_net_radii(treb_vals)
                    
        except Exception as e:
            print(f"Audio processing error: {e}")
            self._reset_visualizers()

    def _reset_visualizers(self):
        """Reset all visualizers to idle state."""
        self.is_playing = False
        self.play_btn.setText("Play")
        self.circle_widget.set_eq_sections([0.1] * self.circle_widget.num_sections)
        self.bar_widget.set_idle()
        self.waveform_bass.set_idle()
        self.waveform_mid.set_idle()
        self.waveform_treble.set_idle()
        self.waveform_grad_bass.set_idle()
        self.waveform_grad_mid.set_idle()
        self.waveform_grad_treble.set_idle()
        self.waveform_blue_bass.set_idle()
        self.waveform_blue_mid.set_idle()
        self.waveform_blue_treble.set_idle()

    def populate_device_list(self):
        self.device_combo.clear()
        self.device_combo.addItem("Select microphone device...")
        self._device_list = sd.query_devices()
        for idx, dev in enumerate(self._device_list):
            if dev['max_input_channels'] > 0:
                label = f"[{idx}] {dev['name']} (Channels: {dev['max_input_channels']})"
                self.device_combo.addItem(label, idx)
    
    def refresh_device_list(self):
        """Refresh the device list and repopulate the dropdown."""
        self.populate_device_list()
        if self.use_system_audio and self.device_combo.count() > 1:
            self.device_combo.setCurrentIndex(1)
        else:
            self.system_audio_device_index = None

    def auto_select_microphone(self):
        """Auto-select the first available microphone device."""
        if self.device_combo.count() > 1:
            self.device_combo.setCurrentIndex(1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Make the net container and all nets fill the available space
        if hasattr(self, 'waveform_net_container'):
            rect = self.visualizer_stack.geometry()
            self.waveform_net_container.setGeometry(0, 0, rect.width(), rect.height())
            if hasattr(self, 'waveform_bg'):
                self.waveform_bg.setGeometry(0, 0, rect.width(), rect.height())
            for net in (self.waveform_bass, self.waveform_mid, self.waveform_treble):
                net.setGeometry(0, 0, rect.width(), rect.height())
        
        if hasattr(self, 'waveform_grad_container'):
            rect = self.visualizer_stack.geometry()
            self.waveform_grad_container.setGeometry(0, 0, rect.width(), rect.height())
            if hasattr(self, 'waveform_grad_bg'):
                self.waveform_grad_bg.setGeometry(0, 0, rect.width(), rect.height())
            for grad in (self.waveform_grad_bass, self.waveform_grad_mid, self.waveform_grad_treble):
                grad.setGeometry(0, 0, rect.width(), rect.height())
        
        if hasattr(self, 'waveform_bluegrad_container'):
            rect = self.visualizer_stack.geometry()
            self.waveform_bluegrad_container.setGeometry(0, 0, rect.width(), rect.height())
            if hasattr(self, 'waveform_bluegrad_bg'):
                self.waveform_bluegrad_bg.setGeometry(0, 0, rect.width(), rect.height())
            for grad in (self.waveform_blue_bass, self.waveform_blue_mid, self.waveform_blue_treble):
                grad.setGeometry(0, 0, rect.width(), rect.height())

def print_sound_devices():
    devices = sd.query_devices()
    print("\n=== Sound Devices ===")
    for idx, dev in enumerate(devices):
        inout = []
        if dev['max_input_channels'] > 0:
            inout.append(f"IN:{dev['max_input_channels']}")
        if dev['max_output_channels'] > 0:
            inout.append(f"OUT:{dev['max_output_channels']}")
        marker = " <-- MICROPHONE" if dev['max_input_channels'] > 0 else " (no input)"
        print(f"[{idx}] {dev['name']} | {' '.join(inout) if inout else 'NO IN/OUT'}{marker}")
    print("====================\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.populate_device_list()
    win.show()
    sys.exit(app.exec()) 