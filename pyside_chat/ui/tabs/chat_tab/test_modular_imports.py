"""
Test file to verify modular imports work correctly
"""

def test_imports():
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
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports() 