#!/usr/bin/env python3
"""Convert text dialogues into audio files using Coqui TTS.

This module provides functionality to convert text dialogues into audio files using
different voices for different speakers. It uses the Coqui TTS library for high-quality
offline text-to-speech synthesis.
"""

import contextlib
import io
import os
import platform
import tempfile
import warnings
from datetime import datetime
from typing import Any, Optional

import torch
from pydub import AudioSegment
from TTS.api import TTS

# Filter out the specific FutureWarning about weights_only
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message="You are using `torch.load` with `weights_only=False`",
)


class DialogueToSpeech:
    """A class to handle text-to-speech conversion for dialogues with multiple speakers."""

    def __init__(self) -> None:
        """Initialize TTS models for both male and female voices."""
        try:
            print("\nInitializing Text-to-Speech...")
            print(f"System: {platform.system()}")
            print(f"Python: {platform.python_version()}\n")

            # Print cache location information
            cache_dir = os.path.expanduser("~/Library/Application Support/tts")
            print("Default TTS cache location:", cache_dir)
            print(
                "Note: Models will be downloaded to the default cache location. "
                "This may take a moment on first run.\n"
            )

            # Set torch loading to use weights_only for security
            torch.set_default_tensor_type(torch.FloatTensor)

            # Monkey patch torch.load to always use weights_only=True
            original_torch_load = torch.load

            def secure_torch_load(f: Any, *args: Any, **kwargs: Any) -> Any:
                """Wrap torch.load to enforce weights_only=True."""
                if "weights_only" not in kwargs:
                    kwargs["weights_only"] = True
                return original_torch_load(f, *args, **kwargs)

            torch.load = secure_torch_load

            # Initialize TTS for male voice (British accent)
            print("Initializing Male British voice (VCTK p273)...")
            self.male_tts = TTS(
                model_name="tts_models/en/vctk/vits", progress_bar=False
            ).to("cpu")
            self.male_speaker = "p273"
            print(" Model initialized successfully")

            # Initialize TTS for female voice (American accent)
            print("Initializing Female American voice (VCTK p262)...")
            self.female_tts = TTS(
                model_name="tts_models/en/vctk/vits", progress_bar=False
            ).to("cpu")
            self.female_speaker = "p262"
            print(" Model initialized successfully\n")

            print("TTS initialized successfully!")
            print("Using voices:")
            print(f"PersonA: Male British voice (VCTK {self.male_speaker})")
            print(f"PersonB: Female American voice (VCTK {self.female_speaker})\n")

        except Exception as e:
            print(f"Error initializing TTS model: {str(e)}")
            raise

    def _initialize_tts_model(self, voice_name: str) -> TTS:
        """Initialize a TTS model and ensure it's downloaded to the correct location.

        Args:
            voice_name: Name of the voice model to initialize.

        Returns:
            Initialized TTS model.

        Raises:
            Exception: If there's an error initializing the model.
        """
        print(f"Initializing {voice_name}...")

        try:
            # Suppress TTS initialization output
            with contextlib.redirect_stdout(io.StringIO()):
                with contextlib.redirect_stderr(io.StringIO()):
                    # Initialize TTS with the VCTK model
                    tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False)
            print(" Model initialized successfully")
            return tts

        except Exception as e:
            print(f"Error initializing TTS model: {str(e)}")
            raise

    def create_audio_for_line(self, text: str, speaker: str, output_path: str) -> None:
        """Generate audio for a single line of dialogue.

        Args:
            text: The text to convert to speech.
            speaker: The speaker identifier ('PersonA' or 'PersonB').
            output_path: The path where the audio file will be saved.

        Raises:
            ValueError: If the text is empty or the speaker is invalid.
            Exception: If there's an error generating the audio.
        """
        if not text.strip():
            raise ValueError("Text cannot be empty")

        if speaker not in ["PersonA", "PersonB"]:
            raise ValueError(
                f'Invalid speaker: {speaker}. Must be either "PersonA" or "PersonB"'
            )

        tts_model = self.male_tts if speaker == "PersonA" else self.female_tts
        speaker_id = self.male_speaker if speaker == "PersonA" else self.female_speaker

        try:
            # Select TTS engine and speaker based on the speaker
            # Suppress TTS generation output
            with contextlib.redirect_stdout(io.StringIO()):
                with contextlib.redirect_stderr(io.StringIO()):
                    # Generate audio
                    tts_model.tts_to_file(
                        text=text, file_path=output_path, speaker=speaker_id
                    )
        except Exception as e:
            print(f'Error generating audio for "{text}": {str(e)}')
            raise

    def process_conversation(self, input_file: str) -> Optional[str]:
        """Process the entire conversation and create the final audio file.

        Args:
            input_file: Path to the input text file containing the conversation.

        Returns:
            Path to the generated audio file, or None if no audio was generated.

        Raises:
            FileNotFoundError: If the input file doesn't exist.
            Exception: If there's an error processing the conversation.
        """
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)

        # Create a unique output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join("output", f"conversation_{timestamp}.wav")

        # Create a temporary directory for intermediate files
        with tempfile.TemporaryDirectory() as temp_dir:
            combined_audio = None
            silence = AudioSegment.silent(duration=500)  # 500ms silence between lines

            print("\nProcessing conversation...")

            try:
                # Read and process each line of the conversation
                with open(input_file, "r", encoding="utf-8") as f:
                    for i, line in enumerate(f):
                        if ":" not in line:
                            continue

                        # Split the line into speaker and text
                        speaker, text = line.strip().split(":", 1)
                        text = text.strip()
                        speaker = speaker.strip()

                        # Skip empty lines
                        if not text:
                            continue

                        # Generate temporary audio file for this line
                        temp_audio_path = os.path.join(temp_dir, f"line_{i}.wav")
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
                    combined_audio.export(output_file, format="wav")
                    print(f"\nSuccess! Created dialogue audio file: {output_file}")
                    return output_file

                print(
                    "No dialogue processed. Check if input file is empty or formatted correctly."
                )
                return None

            except Exception as e:
                print(f"Error processing conversation: {str(e)}")
                return None


def main() -> None:
    """Convert a sample conversation text file into an audio dialogue."""
    try:
        # Define input file path
        input_file = "data/conversation.txt"

        print("\nInitializing Text-to-Speech...")
        print(f"System: {platform.system()}")
        print(f"Python: {platform.python_version()}")

        # Create and run the converter
        converter = DialogueToSpeech()
        output_file = converter.process_conversation(input_file)
        if not output_file:
            raise RuntimeError("Failed to process conversation")

    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting tips:")
        print('1. Make sure you have run "poetry install" to install all dependencies')
        print('2. Ensure the "data" directory contains a valid conversation.txt file')
        print(
            "3. If this is your first run, the script needs to download voice models.\n"
            "This may take a few minutes depending on your connection"
        )


if __name__ == "__main__":
    main()
