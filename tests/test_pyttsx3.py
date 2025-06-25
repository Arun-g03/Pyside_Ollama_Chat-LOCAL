import pyttsx3
import time

def test_pyttsx3():
    """
    Enhanced test script to demonstrate pyttsx3 text-to-speech functionality
    with more natural-sounding speech by reading a short nursery rhyme.
    """
    
    # Initialize the text-to-speech engine
    print("Initializing pyttsx3 engine...")
    engine = pyttsx3.init()
    
    # Get available voices
    voices = engine.getProperty('voices')
    print(f"Available voices: {len(voices)}")
    
    # List all available voices
    for i, voice in enumerate(voices):
        print(f"Voice {i}: {voice.name} ({voice.id})")
    
    # Try to find a more natural-sounding voice
    # Look for voices that might sound better (Microsoft David, Microsoft Zira, etc.)
    preferred_voices = ['HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0',
                       'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0',
                       'com.apple.speech.synthesis.voice.alex',
                       'com.apple.speech.synthesis.voice.victoria']
    
    selected_voice = None
    for voice in voices:
        if any(pref in voice.id.lower() for pref in ['david', 'zira', 'alex', 'victoria', 'samantha']):
            selected_voice = voice
            break
    
    if selected_voice:
        engine.setProperty('voice', selected_voice.id)
        print(f"Using preferred voice: {selected_voice.name}")
    elif voices:
        engine.setProperty('voice', voices[0].id)
        print(f"Using default voice: {voices[0].name}")
    
    # Set properties for more natural speech
    engine.setProperty('rate', 130)     # Slower rate for more natural speech
    engine.setProperty('volume', 0.8)   # Slightly lower volume
    engine.setProperty('pitch', 1.0)    # Normal pitch
    
    # The nursery rhyme with natural pauses
    nursery_rhyme = """
    Twinkle, twinkle, little star,
    How I wonder what you are!
    Up above the world so high,
    Like a diamond in the sky.
    Twinkle, twinkle, little star,
    How I wonder what you are!
    """
    
    print("\nReading nursery rhyme with natural speech...")
    print(nursery_rhyme)
    
    # Speak the text with natural pauses
    lines = nursery_rhyme.strip().split('\n')
    for line in lines:
        if line.strip():  # Skip empty lines
            engine.say(line.strip())
            engine.runAndWait()
            time.sleep(0.5)  # Add pause between lines for more natural rhythm
    
    print("Test completed!")

def test_different_voices():
    """
    Test different voices to find the most natural-sounding one.
    """
    print("\n" + "="*50)
    print("TESTING DIFFERENT VOICES")
    print("="*50)
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    test_text = "Hello, this is a test of natural speech synthesis."
    
    for i, voice in enumerate(voices):
        print(f"\nTesting voice {i+1}/{len(voices)}: {voice.name}")
        engine.setProperty('voice', voice.id)
        engine.setProperty('rate', 130)
        engine.setProperty('volume', 0.8)
        
        engine.say(test_text)
        engine.runAndWait()
        
        # Ask user if they want to continue
        response = input("Press Enter to continue to next voice, or 'q' to quit: ")
        if response.lower() == 'q':
            break

if __name__ == "__main__":
    try:
        # First run the enhanced test
        test_pyttsx3()
        
        # Ask if user wants to test different voices
        print("\n" + "="*50)
        response = input("Would you like to test different voices to find a more natural one? (y/n): ")
        if response.lower() == 'y':
            test_different_voices()
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure pyttsx3 is installed: pip install pyttsx3") 