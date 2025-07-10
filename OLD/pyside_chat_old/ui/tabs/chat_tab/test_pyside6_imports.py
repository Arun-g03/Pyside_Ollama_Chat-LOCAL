"""
Test file to verify PySide6 imports and enums work correctly
"""

def test_pyside6_imports():
    """Test that all PySide6 imports and enums work correctly"""
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import (
            QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, 
            QLabel, QComboBox, QSpinBox, QGroupBox, QSlider, QScrollArea,
            QSplitter, QProgressBar
        )
        
        # Test Qt enums
        print("Testing Qt enums...")
        
        # Test alignment
        alignment = Qt.AlignmentFlag.AlignCenter
        print(f"✅ Alignment: {alignment}")
        
        # Test orientation
        horizontal = Qt.Orientation.Horizontal
        vertical = Qt.Orientation.Vertical
        print(f"✅ Horizontal orientation: {horizontal}")
        print(f"✅ Vertical orientation: {vertical}")
        
        # Test key events
        return_key = Qt.Key.Key_Return
        shift_modifier = Qt.KeyboardModifier.ShiftModifier
        print(f"✅ Return key: {return_key}")
        print(f"✅ Shift modifier: {shift_modifier}")
        
        # Test scroll bar policy
        scroll_policy = QScrollArea.ScrollBarAsNeeded
        print(f"✅ Scroll bar policy: {scroll_policy}")
        
        # Test line wrap mode
        line_wrap = QTextEdit.WidgetWidth
        print(f"✅ Line wrap mode: {line_wrap}")
        
        print("✅ All PySide6 imports and enums work correctly!")
        return True
        
    except Exception as e:
        print(f"❌ PySide6 import/enum error: {e}")
        return False

def test_component_imports():
    """Test that all modular components can be imported"""
    try:
        from .chat_tab import ChatTab
        from .chat_display import ChatDisplay
        from .voice_controls import VoiceControls
        from .eq_visualizer import EQVisualizer
        from .input_controls import InputControls
        
        print("✅ All modular components imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Component import error: {e}")
        return False

if __name__ == "__main__":
    print("Testing PySide6 imports and enums...")
    pyside6_ok = test_pyside6_imports()
    
    print("\nTesting component imports...")
    components_ok = test_component_imports()
    
    if pyside6_ok and components_ok:
        print("\n🎉 All tests passed! The modular chat tab should work correctly.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.") 