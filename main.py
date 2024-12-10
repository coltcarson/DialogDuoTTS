#!/usr/bin/env python3
import os
import tempfile
import subprocess
from pydub import AudioSegment

class DialogueToSpeech:
    def __init__(self):
        """Initialize TTS with different voices"""
        # Check if espeak is installed and get its path
        try:
            # On macOS with Homebrew, espeak is typically installed here
            if os.path.exists('/opt/homebrew/bin/espeak'):
                self.espeak_path = '/opt/homebrew/bin/espeak'
            else:
                # Try to find espeak in PATH
                result = subprocess.run(['which', 'espeak'], capture_output=True, text=True)
                if result.returncode == 0:
                    self.espeak_path = result.stdout.strip()
                else:
                    raise FileNotFoundError("espeak not found in PATH")
            
            # Test espeak
            subprocess.run([self.espeak_path, '--version'], capture_output=True, check=True)
            print("TTS initialized successfully!")
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError("espeak not found. Please install it using 'brew install espeak'") from e
        
        # Configure voices for each speaker
        self.voice_a = {
            'voice': 'en-us',  # US English
            'pitch': 50,       # Default pitch
            'speed': 150       # Words per minute
        }
        self.voice_b = {
            'voice': 'en-gb',  # British English
            'pitch': 30,       # Lower pitch for contrast
            'speed': 150       # Words per minute
        }
        
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)

    def create_audio_for_line(self, text, speaker, output_path):
        """Generate audio file for a single line of dialogue"""
        # Select voice configuration
        voice_config = self.voice_a if speaker == "PersonA" else self.voice_b
        
        # Build espeak command
        cmd = [
            self.espeak_path,
            '-v', voice_config['voice'],
            '-p', str(voice_config['pitch']),
            '-s', str(voice_config['speed']),
            '-w', output_path,  # Write to WAV file
            text
        ]
        
        # Run espeak command
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running espeak: {e.stderr}")
            raise

    def process_conversation(self, input_file, output_file):
        """Process the entire conversation and create the final audio file"""
        # Create a temporary directory for intermediate files
        with tempfile.TemporaryDirectory() as temp_dir:
            combined_audio = None
            silence = AudioSegment.silent(duration=500)  # 500ms silence between lines
            
            print("Processing conversation...")
            
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
        
        # Create and run the converter
        converter = DialogueToSpeech()
        converter.process_conversation(input_file, output_file)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have run 'poetry install' to install all dependencies")
        print("2. Ensure the 'data' directory contains a valid conversation.txt file")
        print("3. Check that espeak is installed on your system:")
        print("   - macOS: brew install espeak")
        print("   - Linux: sudo apt-get install espeak")
        print("   - Windows: Download from https://github.com/espeak/espeak/releases")

if __name__ == "__main__":
    main()
