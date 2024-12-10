#!/usr/bin/env python3
import os
import asyncio
import tempfile
import edge_tts
from pydub import AudioSegment

class DialogueToSpeech:
    def __init__(self):
        """Initialize TTS with different voices"""
        # Select voices for each speaker
        self.voice_a = "en-US-JennyNeural"  # Female voice
        self.voice_b = "en-US-ChristopherNeural"  # Male voice
        
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        print("TTS initialized successfully!")

    async def create_audio_for_line(self, text, speaker, output_path):
        """Generate audio file for a single line of dialogue"""
        voice = self.voice_a if speaker == "PersonA" else self.voice_b
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)

    async def process_conversation(self, input_file, output_file):
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
                    temp_audio_path = os.path.join(temp_dir, f'line_{i}.mp3')
                    print(f"Generating audio for {speaker}: {text}")
                    await self.create_audio_for_line(text, speaker, temp_audio_path)
                    
                    # Load the audio segment
                    audio_segment = AudioSegment.from_mp3(temp_audio_path)
                    
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

async def main():
    try:
        # Define file paths
        input_file = 'data/conversation.txt'
        output_file = 'output/final_conversation.wav'
        
        print("\nInitializing Text-to-Speech...")
        
        # Create and run the converter
        converter = DialogueToSpeech()
        await converter.process_conversation(input_file, output_file)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have run 'poetry install' to install all dependencies")
        print("2. Ensure the 'data' directory contains a valid conversation.txt file")
        print("3. Check that you have sufficient disk space")

if __name__ == "__main__":
    asyncio.run(main())
