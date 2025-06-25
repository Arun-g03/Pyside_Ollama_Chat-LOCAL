import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf
import pygame
import os
import random

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

# Complete list of all possible Parler-TTS speakers
ALL_SPEAKERS = [
    "Laura", "Gary", "Jon", "Lea", "Karen", "Rick", "Brenda", "David", "Eileen", "Jordan", 
    "Mike", "Yann", "Joy", "James", "Eric", "Lauren", "Rose", "Will", "Jason", "Aaron", 
    "Naomie", "Alisa", "Patrick", "Jerry", "Tina", "Jenna", "Bill", "Tom", "Carol", "Barbara", 
    "Rebecca", "Anna", "Bruce", "Emily"
]

def get_available_speakers(model):
    """
    Get the list of speakers that are actually available in the loaded model.
    """
    try:
        # Try to get speakers from model config
        if hasattr(model.config, 'speakers'):
            return model.config.speakers
        elif hasattr(model, 'speakers'):
            return model.speakers
        else:
            # Fallback to checking if there's a speakers attribute or method
            if hasattr(model, 'get_speakers'):
                return model.get_speakers()
            else:
                # If we can't determine, return a subset of common speakers
                return ["Laura", "Gary", "Jon", "Lea", "Karen", "Rick", "Brenda", "David"]
    except Exception as e:
        print(f"Could not determine available speakers: {e}")
        # Return a minimal set as fallback
        return ["Laura", "Gary", "Jon", "Lea"]

def display_speakers(available_speakers):
    """
    Display all speakers organized by availability.
    """
    print("\n" + "="*60)
    print("SPEAKER SELECTION")
    print("="*60)
    
    # Separate available and unavailable speakers
    available = [s for s in ALL_SPEAKERS if s in available_speakers]
    unavailable = [s for s in ALL_SPEAKERS if s not in available_speakers]
    
    print(f"✅ AVAILABLE SPEAKERS ({len(available)}):")
    print("-" * 40)
    for i, name in enumerate(available, 1):
        print(f"{i:2d}. {name}", end='  ')
        if i % 6 == 0:
            print()
    if len(available) % 6 != 0:
        print()
    
    if unavailable:
        print(f"\n❌ UNAVAILABLE SPEAKERS ({len(unavailable)}):")
        print("-" * 40)
        for i, name in enumerate(unavailable, 1):
            print(f"   {name}", end='  ')
            if i % 6 == 0:
                print()
        if len(unavailable) % 6 != 0:
            print()
    
    print(f"\nR. Random voice (from available speakers)")
    print("="*60)

def main():
    print("PARLER-TTS OFFICIAL TEST SCRIPT")
    print("="*50)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load model first to check available speakers
    print("\nLoading Parler-TTS model (parler-tts/parler-tts-mini-v1)...")
    model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(device)
    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")
    print("Model loaded!")
    
    # Get available speakers from the model
    available_speakers = get_available_speakers(model)
    print(f"\nFound {len(available_speakers)} available speakers in the model")
    
    # User input for prompt
    prompt = input("Enter the text to speak (prompt): ").strip()
    if not prompt:
        prompt = "Hey, how are you doing today. That's funny, I'm not even sure what I'm doing here. Sometimes I feel like I'm just a puppet on a string, and I'm not even sure who's pulling the strings."
    
    # Display speakers organized by availability
    display_speakers(available_speakers)
    
    speaker_choice = input("\nChoose a speaker by number, name, or 'R' for random: ").strip()
    
    if speaker_choice.lower() == 'r' or speaker_choice == '':
        speaker = random.choice(available_speakers)
        print(f"Randomly selected speaker: {speaker}")
    elif speaker_choice.isdigit() and 1 <= int(speaker_choice) <= len(available_speakers):
        # Get the available speakers list for numbering
        available = [s for s in ALL_SPEAKERS if s in available_speakers]
        speaker = available[int(speaker_choice)-1]
    else:
        # Try to match by name
        matches = [s for s in available_speakers if s.lower() == speaker_choice.lower()]
        if matches:
            speaker = matches[0]
        else:
            print("Invalid choice, using random speaker.")
            speaker = random.choice(available_speakers)
    
    # User input for style
    print("\nDescribe the style/emotion (or leave blank for default):")
    print("Example: 'slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up.'")
    style = input("Description: ").strip()
    if not style:
        style = "slightly expressive and animated speech with a moderate speed and pitch. The recording is of very high quality, with the speaker's voice sounding clear and very close up."
    
    # Compose description
    description = f"{speaker}'s voice is {style}"
    print(f"\n[Prompt]: {prompt}")
    print(f"[Description]: {description}")
    
    # Tokenize
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    
    print("Generating speech...")
    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()
    out_file = "parler_tts_out.wav"
    sf.write(out_file, audio_arr, model.config.sampling_rate)
    print(f"Saved to {out_file}")
    
    # Play
    init_audio()
    print("Playing audio...")
    play_audio_file(out_file)
    
    # Clean up
    if os.path.exists(out_file):
        os.remove(out_file)
    print("Done!")

if __name__ == "__main__":
    main() 