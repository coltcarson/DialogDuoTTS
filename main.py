#!/usr/bin/env python3
import os
import tempfile
from gtts import gTTS
from pydub import AudioSegment

class DialogueToSpeech:
    def __init__(self):
        # Define different languages/accents for each speaker
        self.voice_a = {'lang': 'en', 'tld': 'com'}  # US English
        self.voice_b = {'lang': 'en', 'tld': 'co.uk'}  # UK English

    def create_audio_for_line(self, text, voice_params, output_path):
        """Generate audio file for a single line of dialogue"""
        tts = gTTS(text=text, lang=voice_params['lang'], tld=voice_params['tld'])
        tts.save(output_path)

    def process_conversation(self, input_file, output_file):
        """Process the entire conversation and create the final audio file"""
        # Create a temporary directory for intermediate files
        with tempfile.TemporaryDirectory() as temp_dir:
            combined_audio = None
            silence = AudioSegment.silent(duration=500)  # 500ms silence between lines
            
            # Read and process each line of the conversation
            with open(input_file, 'r') as f:
                for i, line in enumerate(f):
                    if ':' not in line:
                        continue
                        
                    # Split the line into speaker and text
                    speaker, text = line.strip().split(':', 1)
                    text = text.strip()
                    
                    # Determine which voice to use
                    voice_params = self.voice_a if speaker.strip() == 'PersonA' else self.voice_b
                    
                    # Generate temporary audio file for this line
                    temp_audio_path = os.path.join(temp_dir, f'line_{i}.mp3')
                    print(f"Generating audio for: {text}")
                    self.create_audio_for_line(text, voice_params, temp_audio_path)
                    
                    # Load the audio segment
                    audio_segment = AudioSegment.from_mp3(temp_audio_path)
                    
                    # Add to combined audio
                    if combined_audio is None:
                        combined_audio = audio_segment
                    else:
                        combined_audio = combined_audio + silence + audio_segment

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Export the final audio file
            if combined_audio:
                combined_audio.export(output_file, format='wav')
                print(f"Successfully created dialogue audio file: {output_file}")
            else:
                print("No dialogue was processed. Check if the input file is empty or formatted correctly.")

def main():
    # Define file paths
    input_file = 'data/conversation.txt'
    output_file = 'output/final_conversation.wav'
    
    # Create and run the converter
    converter = DialogueToSpeech()
    converter.process_conversation(input_file, output_file)

if __name__ == "__main__":
    main()
