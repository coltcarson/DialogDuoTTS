# DialogDuoTTS

A Python-based text-to-speech application that converts two-person dialogues into conversations using offline TTS.

## Features

- Works completely offline - no internet connection required
- Uses high-quality offline TTS models for natural-sounding voices
- Different voices for each speaker
- Cross-platform support (Windows, macOS, Linux)
- Automatic handling of conversation turn-taking with appropriate pauses

## Prerequisites

- Python 3.10 or higher
- Poetry (Python package manager)
- espeak-ng (Text-to-Speech engine)

### Installing espeak-ng

- **macOS**:
  ```bash
  brew install espeak
  ```

- **Linux**:
  ```bash
  sudo apt-get install espeak-ng
  ```

- **Windows**:
  Download the installer from [espeak-ng releases](https://github.com/espeak-ng/espeak-ng/releases)

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

## Voice Configuration

The script uses two different voices:
- PersonA: US English, default pitch
- PersonB: British English, slightly lower pitch

You can modify the voice settings in the `DialogueToSpeech.__init__` method:
- `voice`: Language/accent (e.g., 'en-us', 'en-gb')
- `pitch`: Voice pitch (0-99)
- `speed`: Speaking rate in words per minute

## Troubleshooting

1. If you get an error about espeak-ng not being found:
   - Make sure you've installed espeak-ng using the instructions above
   - On Windows, ensure the espeak-ng installation directory is in your PATH

2. If the audio quality isn't satisfactory:
   - Try adjusting the pitch and speed settings in the voice configuration
   - Different voices may sound better for different types of text

3. If you get permission errors:
   - Ensure you have write permissions in the output directory
   - Try running the script with appropriate permissions
