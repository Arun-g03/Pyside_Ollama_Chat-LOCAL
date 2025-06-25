from gtts import gTTS
import pygame
import os
import time

def init_audio():
    """
    Initialize pygame mixer for audio playback.
    """
    pygame.mixer.init()

def play_audio_file(file_path):
    """
    Play audio file using pygame mixer.
    """
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    except Exception as e:
        print(f"Error playing audio: {e}")

def test_gtts():
    """
    Test script using gTTS (Google Text-to-Speech) for natural-sounding speech
    by reading a short nursery rhyme.
    """
    
    print("Initializing gTTS (Google Text-to-Speech)...")
    
    # Initialize audio system
    init_audio()
    
    # The nursery rhyme to read
    nursery_rhyme = """
    This is a test of natural speech synthesis. This is how i sound. 1, 2, 3. Thanks.
    """
    
    print("\nReading nursery rhyme with Google TTS...")
    print(nursery_rhyme)
    
    try:
        # Create gTTS object with natural speech
        tts = gTTS(text=nursery_rhyme, lang='en', slow=False)
        
        # Save to temporary file
        temp_file = "temp_speech.mp3"
        print("Generating speech...")
        tts.save(temp_file)
        
        # Play the audio
        print("Playing speech...")
        play_audio_file(temp_file)
        
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        print("Test completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure gTTS and pygame are installed:")
        print("pip install gtts pygame")

def test_different_languages():
    """
    Test gTTS with different languages and accents for variety.
    """
    print("\n" + "="*50)
    print("TESTING DIFFERENT LANGUAGES/ACCENTS")
    print("="*50)
    
    test_text = "Hello, this is a test of natural speech synthesis."
    
    # Different language options
    languages = [
        ('en', 'English (US)'),
        ('en-gb', 'English (UK)'),
        ('en-au', 'English (Australia)'),
        ('en-in', 'English (India)'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German')
    ]
    
    for lang_code, lang_name in languages:
        print(f"\nTesting {lang_name}...")
        
        try:
            tts = gTTS(text=test_text, lang=lang_code, slow=False)
            temp_file = f"temp_speech_{lang_code}.mp3"
            
            tts.save(temp_file)
            play_audio_file(temp_file)
            
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
            # Ask user if they want to continue
            response = input("Press Enter to continue to next language, or 'q' to quit: ")
            if response.lower() == 'q':
                break
                
        except Exception as e:
            print(f"Error with {lang_name}: {e}")
            continue

def test_speech_speed():
    """
    Test different speech speeds (normal vs slow).
    """
    print("\n" + "="*50)
    print("TESTING SPEECH SPEEDS")
    print("="*50)
    
    test_text = "This is a test of speech speed variations."
    
    speeds = [
        (False, "Normal Speed"),
        (True, "Slow Speed")
    ]
    
    for slow, speed_name in speeds:
        print(f"\nTesting {speed_name}...")
        
        try:
            tts = gTTS(text=test_text, lang='en', slow=slow)
            temp_file = f"temp_speech_speed_{slow}.mp3"
            
            tts.save(temp_file)
            play_audio_file(temp_file)
            
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
            # Ask user if they want to continue
            response = input("Press Enter to continue to next speed, or 'q' to quit: ")
            if response.lower() == 'q':
                break
                
        except Exception as e:
            print(f"Error with {speed_name}: {e}")
            continue

if __name__ == "__main__":
    try:
        # First run the main test
        test_gtts()
        
        # Ask if user wants to test different languages
        print("\n" + "="*50)
        response = input("Would you like to test different languages/accents? (y/n): ")
        if response.lower() == 'y':
            test_different_languages()
        
        # Ask if user wants to test speech speeds
        print("\n" + "="*50)
        response = input("Would you like to test different speech speeds? (y/n): ")
        if response.lower() == 'y':
            test_speech_speed()
            
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure gTTS and pygame are installed:")
        print("pip install gtts pygame") 