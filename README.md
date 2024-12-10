# DialogDuoTTS

A Python-based text-to-speech application that converts two-person dialogues into natural-sounding conversations using offline TTS models.

## Features

- Works completely offline - no internet connection required
- Uses high-quality Mozilla TTS models for natural-sounding voices
- Different voices for each speaker
- Cross-platform support (Windows, macOS, Linux)
- Automatic handling of conversation turn-taking with appropriate pauses

## Prerequisites

- Python 3.10 or higher
- Poetry (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd DialogDuoTTS
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

   Note: The first run will download the TTS models (approximately 1GB total).

## Usage

1. Create a conversation file in `data/conversation.txt` with the following format:
   ```
   PersonA: Hello, how are you?
   PersonB: I'm doing well, thanks. How about you?
   PersonA: Great, thanks for asking!
   ```

2. Run the script:
   ```bash
   poetry run python main.py
   ```

3. Find the generated audio file in `output/final_conversation.wav`

## Project Structure

- `main.py`: Main script that handles TTS conversion
- `data/conversation.txt`: Input dialogue file
- `output/`: Directory for generated audio files
- `pyproject.toml`: Project dependencies and configuration

## Troubleshooting

1. If you encounter memory issues:
   - Close other applications
   - Ensure you have at least 4GB of free RAM

2. If you get model loading errors:
   - Delete the cached models in ~/.cache/torch/hub/ (Linux/Mac) or %USERPROFILE%/.cache/torch/hub/ (Windows)
   - Run the script again to redownload the models

3. For audio playback issues:
   - Ensure your system's audio output is properly configured
   - Try playing the output file with VLC or another media player

## Technical Details

- Uses Mozilla TTS for speech synthesis
- PersonA uses the LJSpeech model (female voice)
- PersonB uses the VCTK model with speaker p335 (male voice)
- Audio files are generated in WAV format
- 500ms pause between dialogue turns
