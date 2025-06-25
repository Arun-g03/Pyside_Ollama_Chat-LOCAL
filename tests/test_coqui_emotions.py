import asyncio
import pygame
import os
import time
from TTS.api import TTS
import numpy as np

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

def list_available_models():
    """
    List all available Coqui TTS models.
    """
    print("Available Coqui TTS models:")
    models = TTS.list_models()
    
    # Group models by type
    emotion_models = []
    multi_speaker_models = []
    other_models = []
    
    for model in models:
        if 'emotion' in model.lower() or 'emotional' in model.lower():
            emotion_models.append(model)
        elif 'multi' in model.lower() or 'speaker' in model.lower():
            multi_speaker_models.append(model)
        else:
            other_models.append(model)
    
    if emotion_models:
        print("\n🎭 EMOTION MODELS:")
        for i, model in enumerate(emotion_models, 1):
            print(f"  {i}. {model}")
    
    if multi_speaker_models:
        print("\n👥 MULTI-SPEAKER MODELS:")
        for i, model in enumerate(multi_speaker_models, 1):
            print(f"  {len(emotion_models) + i}. {model}")
    
    if other_models:
        print("\n📝 OTHER MODELS:")
        for i, model in enumerate(other_models, 1):
            print(f"  {len(emotion_models) + len(multi_speaker_models) + i}. {model}")
    
    return models

def test_emotion_control():
    """
    Test Coqui TTS with emotion control.
    """
    print("Testing Coqui TTS Emotion Control...")
    
    # Initialize audio
    init_audio()
    
    # Test text with different emotional contexts
    test_texts = {
        "happy": "I'm so excited to see you! This is absolutely wonderful news that makes me jump for joy!",
        "sad": "I'm feeling quite down today. Everything seems so heavy and difficult to bear.",
        "angry": "I can't believe this happened! This is completely unacceptable and I'm furious!",
        "calm": "Everything is peaceful and serene. Let's take a moment to breathe and relax.",
        "excited": "Oh my goodness! This is incredible! I can hardly contain my enthusiasm!",
        "whisper": "This is a secret that I can only share in the quietest of whispers.",
        "shout": "ATTENTION EVERYONE! THIS IS VERY IMPORTANT INFORMATION!"
    }
    
    try:
        # Try to load an emotion-capable model
        print("Loading Coqui TTS model...")
        
        # Try different emotion-capable models
        emotion_models = [
            "tts_models/en/ljspeech/tacotron2-DDC",
            "tts_models/en/ljspeech/fast_pitch",
            "tts_models/en/vctk/vits",
            "tts_models/en/ljspeech/glow-tts",
            "tts_models/en/ljspeech/speedy-speech"
        ]
        
        tts = None
        for model in emotion_models:
            try:
                print(f"Trying model: {model}")
                tts = TTS(model_name=model)
                print(f"Successfully loaded: {model}")
                break
            except Exception as e:
                print(f"Failed to load {model}: {e}")
                continue
        
        if tts is None:
            print("Could not load any emotion-capable models. Trying default...")
            tts = TTS()
        
        print(f"Using model: {tts.model_name}")
        
        # Test different emotions
        for emotion, text in test_texts.items():
            print(f"\n🎭 Testing emotion: {emotion.upper()}")
            print(f"Text: {text}")
            
            try:
                # Generate speech with emotion
                output_file = f"coqui_emotion_{emotion}.wav"
                
                print("Generating speech...")
                start_time = time.time()
                
                # Try different approaches for emotion control
                if hasattr(tts, 'synthesizer') and hasattr(tts.synthesizer, 'emotion'):
                    # If model supports direct emotion control
                    tts.tts_to_file(text=text, file_path=output_file, emotion=emotion)
                else:
                    # Use speed and pitch variations to simulate emotions
                    if emotion == "happy":
                        tts.tts_to_file(text=text, file_path=output_file, speed=1.2)
                    elif emotion == "sad":
                        tts.tts_to_file(text=text, file_path=output_file, speed=0.8)
                    elif emotion == "angry":
                        tts.tts_to_file(text=text, file_path=output_file, speed=1.3)
                    elif emotion == "calm":
                        tts.tts_to_file(text=text, file_path=output_file, speed=0.9)
                    elif emotion == "excited":
                        tts.tts_to_file(text=text, file_path=output_file, speed=1.4)
                    elif emotion == "whisper":
                        tts.tts_to_file(text=text, file_path=output_file, speed=0.7)
                    elif emotion == "shout":
                        tts.tts_to_file(text=text, file_path=output_file, speed=1.5)
                    else:
                        tts.tts_to_file(text=text, file_path=output_file)
                
                generation_time = time.time() - start_time
                print(f"Speech generated in {generation_time:.2f} seconds")
                
                # Play the audio
                print("Playing speech...")
                play_audio_file(output_file)
                
                # Clean up
                if os.path.exists(output_file):
                    os.remove(output_file)
                
                # Ask user if they want to continue
                response = input("Press Enter to continue to next emotion, or 'q' to quit: ")
                if response.lower() == 'q':
                    break
                    
            except Exception as e:
                print(f"Error with emotion {emotion}: {e}")
                continue
        
        print("Emotion control test completed!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Coqui TTS is installed:")
        print("pip install TTS==0.26.2")

def test_multi_speaker():
    """
    Test Coqui TTS with multiple speakers.
    """
    print("\n" + "="*50)
    print("TESTING MULTI-SPEAKER CAPABILITIES")
    print("="*50)
    
    try:
        # Try to load a multi-speaker model
        multi_speaker_models = [
            "tts_models/en/vctk/vits",
            "tts_models/en/vctk/fast_pitch",
            "tts_models/en/vctk/tacotron2-DDC"
        ]
        
        tts = None
        for model in multi_speaker_models:
            try:
                print(f"Trying multi-speaker model: {model}")
                tts = TTS(model_name=model)
                print(f"Successfully loaded: {model}")
                break
            except Exception as e:
                print(f"Failed to load {model}: {e}")
                continue
        
        if tts is None:
            print("Could not load multi-speaker model. Skipping this test.")
            return
        
        # Get available speakers
        speakers = tts.speakers if hasattr(tts, 'speakers') else []
        if not speakers:
            print("No speakers available in this model.")
            return
        
        print(f"Available speakers: {speakers[:5]}...")  # Show first 5
        
        test_text = "Hello, this is a test of multi-speaker voice synthesis."
        
        # Test first few speakers
        for i, speaker in enumerate(speakers[:5]):
            print(f"\n👤 Testing speaker: {speaker}")
            
            try:
                output_file = f"coqui_speaker_{i}.wav"
                
                print("Generating speech...")
                start_time = time.time()
                
                tts.tts_to_file(text=test_text, file_path=output_file, speaker=speaker)
                
                generation_time = time.time() - start_time
                print(f"Speech generated in {generation_time:.2f} seconds")
                
                # Play the audio
                print("Playing speech...")
                play_audio_file(output_file)
                
                # Clean up
                if os.path.exists(output_file):
                    os.remove(output_file)
                
                # Ask user if they want to continue
                response = input("Press Enter to continue to next speaker, or 'q' to quit: ")
                if response.lower() == 'q':
                    break
                    
            except Exception as e:
                print(f"Error with speaker {speaker}: {e}")
                continue
        
        print("Multi-speaker test completed!")
        
    except Exception as e:
        print(f"Error in multi-speaker test: {e}")

def main():
    """
    Main function to run Coqui TTS tests.
    """
    print("COQUI TTS EMOTION CONTROL TEST")
    print("="*50)
    
    # List available models
    print("1. Listing available models...")
    models = list_available_models()
    
    # Ask user what to test
    print("\n" + "="*50)
    print("TEST OPTIONS")
    print("="*50)
    print("1. Test emotion control")
    print("2. Test multi-speaker capabilities")
    print("3. Test both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        test_emotion_control()
    elif choice == "2":
        test_multi_speaker()
    elif choice == "3":
        test_emotion_control()
        test_multi_speaker()
    else:
        print("Invalid choice. Running emotion control test...")
        test_emotion_control()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("Install required packages:")
        print("pip install TTS==0.26.2 pygame") 