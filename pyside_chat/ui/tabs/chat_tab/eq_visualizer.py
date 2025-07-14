from pyside_chat.core.shared_imports.pyside_imports import *
"""
EQ Visualizer Component - Audio visualization for the chat interface
"""

import logging
import random
from typing import Dict, Optional

# Import EQ visualizer components
from pyside_chat.ui.visualizers.widgets.circle_eq_widget import CircleEQWidget
from pyside_chat.ui.visualizers.widgets.bar_eq_widget import BarEQWidget
from pyside_chat.ui.visualizers.widgets.circular_net_eq_widget import CircularNetEQWidget
from pyside_chat.ui.visualizers.widgets.circular_gradient_eq_widget import CircularGradientEQWidget
from pyside_chat.core.logging.logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class EQVisualizer(QObject):
    """EQ Visualizer component for audio visualization"""
    
    # Signals
    eq_mode_changed = Signal(str)  # Emitted when EQ mode changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # Initialize EQ visualizer widgets
        self.eq_widgets = {}
        self.current_eq_widget = None
        self.eq_visualizer_mode = "None"
        self.stored_chat_display = None  # Store the original chat display when switching to EQ
        
        self.setup_eq_visualizers()
        
    def setup_eq_visualizers(self):
        """Initialize EQ visualizer widgets"""
        # Create EQ widgets
        self.eq_widgets = {
            "Circle EQ": CircleEQWidget(),
            "Bar EQ": BarEQWidget(),
            "Waveform EQ": CircularNetEQWidget(),  # Use CircularNetEQWidget for Waveform EQ
            "Waveform Gradient": CircularGradientEQWidget(),  # Use CircularGradientEQWidget for Waveform Gradient
            "Waveform Blue Gradient": CircularGradientEQWidget()  # Use CircularGradientEQWidget for Waveform Blue Gradient
        }
        
        # Set initial EQ visualizer mode
        self.eq_visualizer_mode = "None"
        
    def switch_to_eq_visualizer(self, chat_display, voice_mode: bool):
        """Switch the chat display to EQ visualizer mode"""
        try:
            logger.debug(f"[EQ DEBUG] switch_to_eq_visualizer called - voice_mode: {voice_mode}, eq_visualizer_mode: {self.eq_visualizer_mode}")
            
            # Don't switch if already showing an EQ widget
            if self.current_eq_widget and self.current_eq_widget.isVisible():
                logger.debug(f"[EQ DEBUG] EQ widget already visible, skipping switch")
                return
            
            if not voice_mode or self.eq_visualizer_mode == "None":
                logger.debug(f"[EQ DEBUG] Skipping EQ switch - voice_mode: {voice_mode}, eq_visualizer_mode: {self.eq_visualizer_mode}")
                return
            
            # Get the current EQ widget
            if self.eq_visualizer_mode in self.eq_widgets:
                self.current_eq_widget = self.eq_widgets[self.eq_visualizer_mode]
                logger.debug(f"[EQ DEBUG] Selected EQ widget: {self.eq_visualizer_mode}")
                
                # Find the scroll area containing the chat display
                scroll_area = chat_display.parent()
                logger.debug(f"[EQ DEBUG] Chat display parent found: {scroll_area is not None}, type: {type(scroll_area)}")
                
                if scroll_area:
                    # Check if parent is a QScrollArea
                    if isinstance(scroll_area, QScrollArea):
                        logger.debug(f"[EQ DEBUG] Parent is QScrollArea, current widget: {scroll_area.widget()}")
                        
                        # Store the current widget (chat display) and replace with EQ widget
                        current_widget = scroll_area.widget()
                        scroll_area.takeWidget()
                        logger.debug(f"[EQ DEBUG] Removed current widget from scroll area")
                        
                        scroll_area.setWidget(self.current_eq_widget)
                        logger.debug(f"[EQ DEBUG] Set EQ widget in scroll area")
                        
                        # Store the chat display for later restoration
                        self.stored_chat_display = current_widget
                    else:
                        logger.debug(f"[EQ DEBUG] Parent is not QScrollArea, it's: {type(scroll_area)}")
                        # Try to find the scroll area in the parent hierarchy
                        current_parent = scroll_area
                        scroll_area = None
                        while current_parent:
                            if isinstance(current_parent, QScrollArea):
                                scroll_area = current_parent
                                break
                            current_parent = current_parent.parent()
                        
                        if scroll_area:
                            logger.debug(f"[EQ DEBUG] Found QScrollArea in parent hierarchy, current widget: {scroll_area.widget()}")
                            scroll_area.takeWidget()
                            logger.debug(f"[EQ DEBUG] Removed current widget from scroll area")
                            
                            scroll_area.setWidget(self.current_eq_widget)
                            logger.debug(f"[EQ DEBUG] Set EQ widget in scroll area")
                            
                            # Store the chat display for later restoration
                            self.stored_chat_display = scroll_area.widget()
                        else:
                            logger.error(f"[EQ DEBUG] Could not find QScrollArea in parent hierarchy")
                            return
                    
                    self.current_eq_widget.show()
                    chat_display.hide()
                    logger.debug(f"[EQ DEBUG] Showed EQ widget, hid chat display")
                    
                    # Ensure chat display is completely hidden and doesn't interfere
                    chat_display.setVisible(False)
                    chat_display.setEnabled(False)
                    logger.debug(f"[EQ DEBUG] Disabled chat display completely")
                    
                    # Force layout update
                    scroll_area.updateGeometry()
                    scroll_area.update()
                    self.current_eq_widget.updateGeometry()
                    self.current_eq_widget.update()
                    logger.debug(f"[EQ DEBUG] Forced layout updates")
                    
                    # Start the EQ animation
                    try:
                        self.current_eq_widget.start_animation()
                        logger.debug(f"[EQ DEBUG] Started EQ animation")
                    except Exception as e:
                        logger.error(f"[EQ DEBUG] Error starting EQ animation: {e}")
                    
                    # Force a complete repaint using thread-safe alternative
                    from pyside_chat.core.utils.threading_utils import safe_process_events_alternative
                    safe_process_events_alternative()
                    logger.debug(f"[EQ DEBUG] Processed events")
                    
                    logger.debug(f"[EQ DEBUG] Successfully switched to EQ visualizer: {self.eq_visualizer_mode}")
                else:
                    logger.error(f"[EQ DEBUG] No scroll area found for chat display")
            else:
                logger.error(f"[EQ DEBUG] EQ visualizer mode '{self.eq_visualizer_mode}' not found in available widgets: {list(self.eq_widgets.keys())}")
        except Exception as e:
            logger.error(f"[EQ DEBUG] Error in switch_to_eq_visualizer: {e}")
            import traceback
            logger.error(f"[EQ DEBUG] Traceback: {traceback.format_exc()}")
    
    def switch_to_chat_display(self, chat_display):
        """Switch back to chat display mode"""
        logger.debug(f"[EQ DEBUG] switch_to_chat_display called - current_eq_widget: {self.current_eq_widget is not None}")
        
        # Don't switch if already showing chat display
        if chat_display and chat_display.isVisible():
            logger.debug(f"[EQ DEBUG] Chat display already visible, skipping switch")
            return
        
        if self.current_eq_widget:
            logger.debug(f"[EQ DEBUG] Stopping EQ animation")
            # Stop the EQ animation
            try:
                self.current_eq_widget.stop_animation()
                logger.debug(f"[EQ DEBUG] EQ animation stopped")
            except Exception as e:
                logger.error(f"[EQ DEBUG] Error stopping EQ animation: {e}")
            
            # Find the scroll area and restore the chat display
            scroll_area = self.current_eq_widget.parent()
            logger.debug(f"[EQ DEBUG] EQ widget parent found: {scroll_area is not None}, type: {type(scroll_area)}")
            
            if scroll_area:
                # Check if parent is a QScrollArea
                if isinstance(scroll_area, QScrollArea):
                    logger.debug(f"[EQ DEBUG] Parent is QScrollArea, current widget: {scroll_area.widget()}")
                    
                    scroll_area.takeWidget()
                    logger.debug(f"[EQ DEBUG] Removed EQ widget from scroll area")
                    
                    # Restore the stored chat display
                    if hasattr(self, 'stored_chat_display') and self.stored_chat_display:
                        scroll_area.setWidget(self.stored_chat_display)
                        logger.debug(f"[EQ DEBUG] Restored stored chat display in scroll area")
                        # Update the chat_display reference
                        chat_display = self.stored_chat_display
                        self.stored_chat_display = None
                    else:
                        scroll_area.setWidget(chat_display)
                        logger.debug(f"[EQ DEBUG] Set chat display in scroll area")
                else:
                    logger.debug(f"[EQ DEBUG] Parent is not QScrollArea, it's: {type(scroll_area)}")
                    # Try to find the scroll area in the parent hierarchy
                    current_parent = scroll_area
                    scroll_area = None
                    while current_parent:
                        if isinstance(current_parent, QScrollArea):
                            scroll_area = current_parent
                            break
                        current_parent = current_parent.parent()
                    
                    if scroll_area:
                        logger.debug(f"[EQ DEBUG] Found QScrollArea in parent hierarchy, current widget: {scroll_area.widget()}")
                        scroll_area.takeWidget()
                        logger.debug(f"[EQ DEBUG] Removed EQ widget from scroll area")
                        
                        # Restore the stored chat display
                        if hasattr(self, 'stored_chat_display') and self.stored_chat_display:
                            scroll_area.setWidget(self.stored_chat_display)
                            logger.debug(f"[EQ DEBUG] Restored stored chat display in scroll area")
                            # Update the chat_display reference
                            chat_display = self.stored_chat_display
                            self.stored_chat_display = None
                        else:
                            scroll_area.setWidget(chat_display)
                            logger.debug(f"[EQ DEBUG] Set chat display in scroll area")
                    else:
                        logger.error(f"[EQ DEBUG] Could not find QScrollArea in parent hierarchy")
                        return
                
                self.current_eq_widget.hide()
                chat_display.show()
                chat_display.setVisible(True)
                chat_display.setEnabled(True)
                logger.debug(f"[EQ DEBUG] Hid EQ widget, showed and enabled chat display")
                
                # Force layout update
                scroll_area.updateGeometry()
                scroll_area.update()
                chat_display.updateGeometry()
                chat_display.update()
                logger.debug(f"[EQ DEBUG] Forced layout updates")
                
                # Force a complete repaint using thread-safe alternative
                from pyside_chat.core.utils.threading_utils import safe_process_events_alternative
                safe_process_events_alternative()
                logger.debug(f"[EQ DEBUG] Processed events")
                
                self.current_eq_widget = None
                logger.debug("[EQ DEBUG] Successfully switched back to chat display")
            else:
                logger.error(f"[EQ DEBUG] No scroll area found for EQ widget")
        else:
            logger.debug(f"[EQ DEBUG] No current EQ widget to switch from")
    
    def update_eq_visualizer(self, audio_level: float, tts_playing: bool = False):
        """Update the EQ visualizer with audio level data."""
        logger.debug(f"[EQ DEBUG] update_eq_visualizer called with audio_level: {audio_level:.4f}, tts_playing: {tts_playing}")
        logger.debug(f"[EQ DEBUG] current_eq_widget exists: {self.current_eq_widget is not None}")
        logger.debug(f"[EQ DEBUG] current_eq_widget type: {type(self.current_eq_widget)}")
        
        if not self.current_eq_widget or not hasattr(self.current_eq_widget, 'set_eq_bars'):
            logger.debug("[EQ DEBUG] No EQ visualizer available")
            return
            
        try:
            logger.debug(f"[EQ DEBUG] Received audio level: {audio_level:.4f}")
            
            # Enhanced audio level processing for better EQ responsiveness
            if tts_playing:
                # TTS audio needs special handling - it's often more compressed
                # Use higher amplification and more dynamic response
                base_level = audio_level * 8.0  # Increased from 15.0 to 8.0 for better balance
                logger.debug(f"[EQ DEBUG] TTS playing - base level: {base_level:.4f}")
                
                # Add additional enhancement for TTS audio
                if audio_level > 0.1:
                    # High TTS levels get extra boost for visual impact
                    base_level *= 1.5
                elif audio_level > 0.05:
                    # Medium TTS levels get moderate boost
                    base_level *= 1.2
            else:
                # Microphone levels need more amplification
                base_level = audio_level * 25.0  # Increased from 20.0 to 25.0
                logger.debug(f"[EQ DEBUG] Microphone input - base level: {base_level:.4f}")
            
            # Generate frequency-based bar values for 24 bars (matching BarEQWidget default)
            bar_values = []
            num_bars = 24
            
            # Define frequency bands for 24 bars (20Hz to 20kHz)
            # Each bar represents a specific frequency range
            frequency_bands = [
                (20, 100),      # Bar 0: Sub-bass (20-100 Hz)
                (100, 200),     # Bar 1: Bass (100-200 Hz)
                (200, 300),     # Bar 2: Bass (200-300 Hz)
                (300, 400),     # Bar 3: Bass (300-400 Hz)
                (400, 600),     # Bar 4: Low-mid (400-600 Hz)
                (600, 800),     # Bar 5: Low-mid (600-800 Hz)
                (800, 1000),    # Bar 6: Mid (800-1000 Hz)
                (1000, 1200),   # Bar 7: Mid (1000-1200 Hz)
                (1200, 1500),   # Bar 8: Mid (1200-1500 Hz)
                (1500, 2000),   # Bar 9: Mid (1500-2000 Hz)
                (2000, 2500),   # Bar 10: Upper-mid (2000-2500 Hz)
                (2500, 3000),   # Bar 11: Upper-mid (2500-3000 Hz)
                (3000, 4000),   # Bar 12: Presence (3000-4000 Hz)
                (4000, 5000),   # Bar 13: Presence (4000-5000 Hz)
                (5000, 6000),   # Bar 14: Presence (5000-6000 Hz)
                (6000, 8000),   # Bar 15: Brilliance (6000-8000 Hz)
                (8000, 10000),  # Bar 16: Brilliance (8000-10000 Hz)
                (10000, 12000), # Bar 17: High (10000-12000 Hz)
                (12000, 14000), # Bar 18: High (12000-14000 Hz)
                (14000, 16000), # Bar 19: High (14000-16000 Hz)
                (16000, 18000), # Bar 20: Ultra-high (16000-18000 Hz)
                (18000, 19000), # Bar 21: Ultra-high (18000-19000 Hz)
                (19000, 19500), # Bar 22: Air (19000-19500 Hz)
                (19500, 20000)  # Bar 23: Air (19500-20000 Hz)
            ]
            
            for i, (low_freq, high_freq) in enumerate(frequency_bands):
                # Enhanced frequency response calculation
                # Base response from audio level
                base_response = base_level
                
                # Create more dynamic frequency-specific responses
                # Each bar should respond differently to create realistic EQ movement
                if i < 6:  # Bass frequencies (0-5) - 25% of bars
                    # Bass bars respond more to lower frequencies
                    freq_multiplier = 1.8 + (i * 0.15)  # Increased response for bass
                elif i < 12:  # Low-mid frequencies (6-11) - 25% of bars
                    # Low-mid bars have moderate response
                    freq_multiplier = 1.2 + ((i - 6) * 0.08)
                elif i < 18:  # Mid frequencies (12-17) - 25% of bars
                    # Mid bars have varied response
                    freq_multiplier = 1.0 + ((i - 12) * 0.12)
                else:  # Upper frequencies (18-23) - 25% of bars
                    # Upper bars are more sensitive to changes
                    freq_multiplier = 1.4 + ((i - 18) * 0.18)
                
                # Enhanced frequency-specific variations based on audio level and source
                if tts_playing:
                    # TTS-specific enhancements
                    if audio_level > 0.15:  # High TTS audio level
                        if i < 6:  # Bass gets more prominent for TTS
                            freq_multiplier *= 1.4
                        elif i > 18:  # High frequencies get more sensitive for TTS
                            freq_multiplier *= 1.6
                    elif audio_level > 0.08:  # Medium TTS audio level
                        if i >= 6 and i < 18:  # Mid frequencies get more response for TTS
                            freq_multiplier *= 1.3
                else:
                    # Microphone-specific enhancements
                    if audio_level > 0.1:  # High microphone level
                        if i < 6:  # Bass gets more prominent
                            freq_multiplier *= 1.3
                        elif i > 18:  # High frequencies get more sensitive
                            freq_multiplier *= 1.4
                    elif audio_level > 0.05:  # Medium microphone level
                        if i >= 6 and i < 18:  # Mid frequencies get more response
                            freq_multiplier *= 1.2
                
                # Calculate final value for this frequency band
                value = base_response * freq_multiplier
                
                # Add enhanced randomness for more natural movement
                # More variation for higher audio levels
                variation_factor = 0.6 + (audio_level * 0.8)  # More variation for higher levels
                value *= (0.7 + variation_factor * random.random())
                
                # Clamp to valid range (0.1 to 1.0 as expected by BarEQWidget)
                value = max(0.1, min(1.0, value))
                bar_values.append(value)
            
            logger.debug(f"[EQ DEBUG] Generated {len(bar_values)} bar values: {[f'{v:.3f}' for v in bar_values]}")
            
            # Use QTimer.singleShot to ensure UI update happens in main thread

            QTimer.singleShot(0, lambda: self._update_eq_widget_safe(bar_values))
            logger.debug(f"[EQ DEBUG] Scheduled EQ widget update for main thread")
            
        except Exception as e:
            logger.error(f"[EQ DEBUG] Error updating EQ visualizer: {e}")
            import traceback
            logger.error(f"[EQ DEBUG] EQ error traceback: {traceback.format_exc()}")
    
    def _update_eq_widget_safe(self, bar_values):
        """Update the EQ widget safely in the main thread"""
        try:
            if self.current_eq_widget and hasattr(self.current_eq_widget, 'set_eq_bars'):
                self.current_eq_widget.set_eq_bars(bar_values)
                logger.debug(f"[EQ DEBUG] Updated EQ widget with {len(bar_values)} bar values in main thread")
            else:
                logger.debug("[EQ DEBUG] No EQ widget available for update")
        except Exception as e:
            logger.error(f"[EQ DEBUG] Error in _update_eq_widget_safe: {e}")
            import traceback
            logger.error(f"[EQ DEBUG] Safe update error traceback: {traceback.format_exc()}")
    
    def is_eq_visualizer_active(self, voice_mode: bool, tts_playing: bool = False):
        """Check if EQ visualizer should be active"""
        return ((voice_mode or tts_playing) and 
                self.eq_visualizer_mode != "None" and 
                self.current_eq_widget is not None)

    def update_eq_visualizer_mode(self, mode: str):
        """Update the EQ visualizer mode"""
        logger.debug(f"[EQ DEBUG] update_eq_visualizer_mode called - new_mode: {mode}, current_mode: {self.eq_visualizer_mode}")
        
        self.eq_visualizer_mode = mode
        self.eq_mode_changed.emit(mode)
        logger.debug(f"[EQ DEBUG] EQ visualizer mode updated to: {mode}")
    
    def get_eq_mode(self) -> str:
        """Get the current EQ visualizer mode"""
        return self.eq_visualizer_mode
    
    def get_available_eq_modes(self) -> list:
        """Get list of available EQ visualizer modes"""
        return list(self.eq_widgets.keys()) 