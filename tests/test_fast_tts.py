import asyncio
import edge_tts
import pygame
import os
import time
from threading import Thread
import queue
import keyboard
import threading



# The story text (properly formatted)
test_text = """



Sometimes I think about things and then I think I know those things but then I think about those things I thought I knew and I realize I dont really know them so now Im thinking about not knowing the things I thought I knew which means Im thinking about things I dont know but if Im thinking about not knowing them then in a way I know that I dont know them so I know something about what I dont know which loops back to me knowing something.

But then if I know that I dont know does that mean I actually do know because if I didnt know anything I wouldnt even know I didnt know so the act of realizing I dont know means I must know something to begin with and that something is the knowledge of my own lack of knowledge this makes me rethink my initial thought that I didnt know because now I know I dont know which is a kind of knowing its like Im stuck in a loop where the more I think about not knowing the more I realize I know something about not knowing which then makes me question if I ever truly didnt know in the first place.

And this thinking about knowing and not knowing and knowing about not knowing just leads me back to thinking about the very first thing I thought about but now its all tangled up with all the other thoughts about not knowing so I think I know but I dont but I know I dont so I do know but not really because what I know is that I dont and around and around we go.

"""




def init_audio():
    """
    Initialize pygame mixer for audio playback.
    """
    pygame.mixer.init()

def play_audio_file_with_skip(file_path):
    """
    Play audio file using pygame mixer with skip functionality.
    Returns True if skipped, False if completed normally.
    """
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        print("Playing... Press 's' to skip, 'q' to quit")
        
        # Wait for the audio to finish playing or skip
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
            # Check for skip or quit keys
            if keyboard.is_pressed('s'):
                pygame.mixer.music.stop()
                print("Skipped!")
                return True
            elif keyboard.is_pressed('q'):
                pygame.mixer.music.stop()
                print("Quitting...")
                return 'quit'
                
        return False
            
    except Exception as e:
        print(f"Error playing audio: {e}")
        return False

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

async def test_edge_tts():
    """
    Test Edge TTS (Microsoft's TTS) which is faster than Google TTS.
    """
    print("Testing Edge TTS (Microsoft) - Fast and Natural...")
    
    # Initialize audio
    init_audio()
    
    
                    
                   
    
    # Male voices to test
    male_voices = [
        "en-US-GuyNeural",       # Natural male voice (US)
        "en-GB-RyanNeural",      # British male
        "en-AU-WilliamNeural",   # Australian male
        "en-US-DavisNeural",     # Another US male
        "en-US-TonyNeural",      # Another US male option
        "en-CA-LiamNeural"       # Canadian male
    ]
    
    # Female voices to test
    female_voices = [
        "en-US-AriaNeural",      # Natural female voice (US) - your favorite
        "en-US-JennyNeural",     # Another natural female (US)
        "en-GB-SoniaNeural",     # British female
        "en-AU-NatashaNeural",   # Australian female
        "en-CA-ClaraNeural",     # Canadian female
        "en-US-SaraNeural",      # Another US female
        "en-US-NancyNeural",     # Another US female option
        "en-GB-LibbyNeural",     # Another British female
        "en-AU-OliviaNeural",    # Another Australian female
        "en-IN-NeerjaNeural"     # Indian English female
    ]
    
    # Ask user for gender preference
    print("\n" + "="*50)
    print("VOICE GENDER SELECTION")
    print("="*50)
    print("Which gender voices would you like to test?")
    print("1. Male voices only")
    print("2. Female voices only") 
    print("3. Both male and female voices")
    print("4. Custom selection")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            voices_to_test = male_voices
            gender_name = "Male"
            break
        elif choice == "2":
            voices_to_test = female_voices
            gender_name = "Female"
            break
        elif choice == "3":
            voices_to_test = male_voices + female_voices
            gender_name = "Male and Female"
            break
        elif choice == "4":
            print("\nCustom selection:")
            print("Available male voices:")
            for i, voice in enumerate(male_voices, 1):
                print(f"  {i}. {voice}")
            print("\nAvailable female voices:")
            for i, voice in enumerate(female_voices, 1):
                print(f"  {i + len(male_voices)}. {voice}")
            
            try:
                selection = input("\nEnter voice numbers separated by commas (e.g., 1,3,7,9): ").strip()
                selected_indices = [int(x.strip()) - 1 for x in selection.split(",")]
                
                all_voices = male_voices + female_voices
                voices_to_test = [all_voices[i] for i in selected_indices if 0 <= i < len(all_voices)]
                
                if voices_to_test:
                    gender_name = "Custom Selection"
                    break
                else:
                    print("Invalid selection. Please try again.")
            except:
                print("Invalid input. Please try again.")
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
    
    print(f"\nTesting {gender_name} voices...")
    print(f"Text: {test_text[:100]}...")  # Show first 100 chars
    print("\nControls:")
    print("- Press 's' during playback to skip to next voice")
    print("- Press 'q' during playback to quit")
    print("- Press Enter after playback to continue")
    
    for i, voice in enumerate(voices_to_test, 1):
        voice_type = "Female" if voice in female_voices else "Male"
        print(f"\n{i}. Testing voice: {voice} ({voice_type})")
        
        try:
            # Create TTS object
            communicate = edge_tts.Communicate(test_text, voice)
            
            # Save to file
            temp_file = f"temp_edge_speech_{i}.mp3"
            print("Generating speech...")
            
            start_time = time.time()
            await communicate.save(temp_file)
            generation_time = time.time() - start_time
            
            print(f"Speech generated in {generation_time:.2f} seconds")
            
            # Play the audio with skip functionality
            print("Playing speech...")
            result = play_audio_file_with_skip(temp_file)
            
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Handle result
            if result == 'quit':
                print("Quitting voice test...")
                return 'quit'
            elif result == True:  # Skipped
                continue  # Go to next voice
            else:  # Completed normally
                # Ask user if they want to continue
                response = input("Press Enter to continue to next voice, or 'q' to quit: ")
                if response.lower() == 'q':
                    break
                
        except Exception as e:
            print(f"Error with voice {voice}: {e}")
            continue
    
    print(f"{gender_name} voices test completed!")
    return True

def test_pyttsx3_fast():
    """
    Test pyttsx3 with optimized settings for speed.
    """
    print("\n" + "="*50)
    print("TESTING PYTTSX3 WITH OPTIMIZED SETTINGS")
    print("="*50)
    
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        
        # Optimize for speed while maintaining quality
        engine.setProperty('rate', 150)      # Faster but still clear
        engine.setProperty('volume', 0.8)
        
        # Try to find a better voice
        voices = engine.getProperty('voices')
        if voices:
            # Look for Microsoft voices which are usually better
            for voice in voices:
                if 'microsoft' in voice.name.lower() or 'david' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    print(f"Using optimized voice: {voice.name}")
                    break
            else:
                engine.setProperty('voice', voices[0].id)
                print(f"Using default voice: {voices[0].name}")
        
        test_text = "This is a test of fast speech synthesis. This is how I sound. 1, 2, 3. Thanks."
        
        print(f"Text: {test_text}")
        print("Speaking (should be instant)...")
        
        start_time = time.time()
        engine.say(test_text)
        engine.runAndWait()
        total_time = time.time() - start_time
        
        print(f"Total time: {total_time:.2f} seconds")
        return total_time
        
    except Exception as e:
        print(f"Error with pyttsx3: {e}")
        return None

def test_gtts_cached():
    """
    Test gTTS with caching to reduce delay on repeated phrases.
    """
    print("\n" + "="*50)
    print("TESTING GTTS WITH CACHING")
    print("="*50)
    
    try:
        from gtts import gTTS
        
        init_audio()
        
        test_text = "This is a test of fast speech synthesis. This is how I sound. 1, 2, 3. Thanks."
        
        # Check if cached file exists
        cached_file = "cached_speech.mp3"
        
        if not os.path.exists(cached_file):
            print("Generating speech (first time - will be slower)...")
            tts = gTTS(text=test_text, lang='en', slow=False)
            tts.save(cached_file)
            print("Speech cached for future use!")
        else:
            print("Using cached speech (should be instant)...")
        
        print(f"Text: {test_text}")
        print("Playing speech...")
        
        start_time = time.time()
        play_audio_file(cached_file)
        play_time = time.time() - start_time
        
        print(f"Playback time: {play_time:.2f} seconds")
        return play_time
        
    except Exception as e:
        print(f"Error with gTTS cached: {e}")
        return None

async def main():
    """
    Main function to test all TTS options and compare speeds.
    """
    print("TTS SPEED COMPARISON TEST")
    print("="*50)
    
    results = {}
    
    # Test Edge TTS (fastest)
    print("\n1. Testing Edge TTS...")
    edge_time = await test_edge_tts()
    if edge_time:
        results['Edge TTS'] = edge_time
    
    # Test pyttsx3 (instant)
    print("\n2. Testing pyttsx3...")
    pyttsx3_time = test_pyttsx3_fast()
    if pyttsx3_time:
        results['pyttsx3'] = pyttsx3_time
    
    # Test gTTS cached
    print("\n3. Testing gTTS cached...")
    gtts_time = test_gtts_cached()
    if gtts_time:
        results['gTTS (cached)'] = gtts_time
    
    # Show results
    print("\n" + "="*50)
    print("SPEED COMPARISON RESULTS")
    print("="*50)
    
    for method, time_taken in results.items():
        print(f"{method}: {time_taken:.2f} seconds")
    
    print("\nRecommendations:")
    print("- Edge TTS: Best balance of speed and quality")
    print("- pyttsx3: Fastest but more robotic")
    print("- gTTS: Best quality but slowest (use caching for repeated phrases)")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        print("Install required packages:")
        print("pip install edge-tts pygame pyttsx3 gtts keyboard") 