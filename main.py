#!/usr/bin/env python3
import os
import tempfile
import platform
from TTS.api import TTS
from pydub import AudioSegment

class DialogueToSpeech:
    def __init__(self):
        """Initialize TTS with different voices"""
        # Create models directory if it doesn't exist
        models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
        os.makedirs(models_dir, exist_ok=True)
        
        # Set the cache directory for TTS models
        os.environ['COQUI_TTS_CACHE_DIR'] = models_dir
        
        # Initialize TTS engines for different voices
        print("\nInitializing Text-to-Speech...")
        print(f"Models will be downloaded to: {models_dir}")
        print("This may take a moment to download the voice models on first run.")
        
        # Initialize male voice (VCTK model with p273 speaker - male British accent)
        self.male_tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True)
        self.male_speaker = "p273"  # VCTK male speaker
        
        # Initialize female voice (VCTK model with p262 speaker - female American accent)
        self.female_tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True)
        self.female_speaker = "p262"  # VCTK female speaker
        
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        print("\nTTS initialized successfully!")
        print(f"Using voices:")
        print(f"PersonA: Male British voice (VCTK p273)")
        print(f"PersonB: Female American voice (VCTK p262)")

    def create_audio_for_line(self, text, speaker, output_path):
        """Generate audio file for a single line of dialogue"""
        # Select TTS engine and speaker based on the speaker
        if speaker == "PersonA":
            tts = self.male_tts
            speaker_id = self.male_speaker
        else:
            tts = self.female_tts
            speaker_id = self.female_speaker
        
        # Generate audio
        tts.tts_to_file(
            text=text,
            speaker=speaker_id,
            file_path=output_path
        )

    def process_conversation(self, input_file, output_file):
        """Process the entire conversation and create the final audio file"""
        # Create a temporary directory for intermediate files
        with tempfile.TemporaryDirectory() as temp_dir:
            combined_audio = None
            silence = AudioSegment.silent(duration=500)  # 500ms silence between lines
            
            print("\nProcessing conversation...")
            
            # Read and process each line of the conversation
            with open(input_file, 'r') as f:
                for i, line in enumerate(f):
                    if ':' not in line:
                        continue
                        
                    # Split the line into speaker and text
                    speaker, text = line.strip().split(':', 1)
                    text = text.strip()
                    speaker = speaker.strip()
                    
                    # Generate temporary audio file for this line
                    temp_audio_path = os.path.join(temp_dir, f'line_{i}.wav')
                    print(f"Generating audio for {speaker}: {text}")
                    self.create_audio_for_line(text, speaker, temp_audio_path)
                    
                    # Load the audio segment
                    audio_segment = AudioSegment.from_wav(temp_audio_path)
                    
                    # Add to combined audio
                    if combined_audio is None:
                        combined_audio = audio_segment
                    else:
                        combined_audio = combined_audio + silence + audio_segment

            # Export the final audio file
            if combined_audio:
                combined_audio.export(output_file, format='wav')
                print(f"\nSuccess! Created dialogue audio file: {output_file}")
            else:
                print("No dialogue was processed. Check if the input file is empty or formatted correctly.")

def main():
    try:
        # Define file paths
        input_file = 'data/conversation.txt'
        output_file = 'output/final_conversation.wav'
        
        print("\nInitializing Text-to-Speech...")
        print(f"System: {platform.system()}")
        print(f"Python: {platform.python_version()}")
        
        # Create and run the converter
        converter = DialogueToSpeech()
        converter.process_conversation(input_file, output_file)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have run 'poetry install' to install all dependencies")
        print("2. Ensure the 'data' directory contains a valid conversation.txt file")
        print("3. If this is your first run, the script needs to download voice models")
        print("   This may take a few minutes depending on your internet connection")

if __name__ == "__main__":
    main()
