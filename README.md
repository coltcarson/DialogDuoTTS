# 🎭 DialogDuoTTS

> 🗣️ Transform text dialogues into lifelike conversations using state-of-the-art offline Text-to-Speech technology!

## ✨ Features

- 🌐 Works completely offline using Coqui TTS for high-quality voice synthesis
- 🎭 Different voices for each speaker in the dialogue
- 💻 Cross-platform support (Windows, macOS, Linux)
- ⚡ Automatic handling of conversation turn-taking with appropriate pauses
- 🛡️ Type-checked and well-tested codebase with comprehensive quality checks

## 🎙️ Voice Models

### 📊 Model Details
- **🔍 Model Type**: VITS (Conditional Variational Autoencoder with Adversarial Learning)
- **📚 Dataset**: VCTK (Voice Cloning Toolkit)
- **📈 Model Size**: ~100MB per voice model
- **🎯 Quality**: High-quality neural TTS with natural-sounding voices
- **🇬🇧 Language**: English (with British and American accents)
- **👥 Speakers**: 109 different speakers with various English accents
- **📜 License**: Apache 2.0
- **👨‍💻 Author**: Eren @erogol (egolge@coqui.ai)
- **📈 Model Version**: v0.6.1
- **🔗 Source**: [Coqui TTS Models Repository](https://github.com/coqui-ai/TTS/blob/dev/TTS/.models.json)

### 🎤 Included Voices
1. **👨 PersonA - Male British Voice**
   - Model: `tts_models/en/vctk/vits`
   - Speaker ID: `p273`
   - Accent: British English
   - Characteristics: Clear, professional male voice

2. **👩 PersonB - Female American Voice**
   - Model: `tts_models/en/vctk/vits`
   - Speaker ID: `p262`
   - Accent: American English
   - Characteristics: Natural, engaging female voice

### 🗂️ Model Storage
The TTS models are automatically downloaded and cached locally:
- **macOS**: `~/Library/Application Support/tts`
- **Windows**: `%LOCALAPPDATA%\tts`
- **Linux**: `~/.cache/tts`

Models are downloaded only once and work completely offline afterward.

### 🔒 Security & Updates
- Models are downloaded securely through Coqui TTS's API
- Downloads are verified for integrity
- Models are cached locally for offline use
- Updates can be forced by clearing the cache directory

## 🚀 Getting Started

### 🔧 Prerequisites

- 🐍 Python 3.10 or higher
- 📦 Poetry (Python package manager)
- 🗣️ eSpeak NG (Required for Windows users)

#### 🪟 Windows-specific Setup

1. 📥 Install eSpeak NG:
   - Download the latest version from [eSpeak NG Releases](https://github.com/espeak-ng/espeak-ng/releases)
   - Run the installer and follow the installation steps

2. 🛠️ Add eSpeak NG to System PATH:
   - Press `Windows key + X` and select "System"
   - Click on "Advanced system settings"
   - Click the "Environment Variables" button
   - Under "System Variables", find and select "Path"
   - Click "Edit"
   - Click "New"
   - Add the path: `C:\Program Files\eSpeak NG` (or your installation directory)
   - Click "OK" on all windows to save
   - Restart any open terminals for the changes to take effect

3. ✅ Verify Installation:
   - Open a new terminal
   - Run `espeak-ng --version`
   - If you see the version number, eSpeak NG is properly installed

### 📦 Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd DialogDuoTTS
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Set up pre-commit hooks:
   ```bash
   poetry run pre-commit install
   ```

## 📚 Usage

### 📖 Basic Usage 

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

3. Find your generated audio files in the `output/` directory! 

### 📝 Command-Line Options 

The script supports several command-line options for flexibility:

```bash
# Use a custom input file
poetry run python main.py -i path/to/your/dialogue.txt

# Show verbose output
poetry run python main.py -v

# Combine options
poetry run python main.py -i custom_dialogue.txt -v
```

Available options:
- `-i, --input`: Specify the input text file path (default: data/conversation.txt)
- `-v, --verbose`: Show detailed output during processing

### 📚 Example Workflows 

1. **Using the Default Configuration** :
   ```bash
   poetry run python main.py
   ```
   This will process `data/conversation.txt` and create an audio file in the `output/` directory.

2. **Processing a Custom Dialogue** :
   ```bash
   poetry run python main.py -i data/project_podcast.txt
   ```
   This will process your custom dialogue file and create an audio file with a timestamp.

3. **Debug Mode with Verbose Output** :
   ```bash
   poetry run python main.py -i custom_dialogue.txt -v
   ```
   This will show detailed information about the conversion process, useful for troubleshooting.

## 🗂️ Project Structure

```
DialogDuoTTS/
├── .pre-commit-config.yaml  # Pre-commit hook configuration
├── .pylintrc               # Pylint configuration
├── mypy.ini               # MyPy type checking configuration
├── pyproject.toml         # Project dependencies and settings
├── main.py               # Main script for TTS conversion
├── data/                 # Input dialogue files
│   └── conversation.txt
├── output/               # Generated audio files
└── tests/               # Test suite
    ├── __init__.py
    └── test_dialogue_to_speech.py
```

## 🔧 Development

### 🛠️ Code Quality Tools

We use industry-standard tools to maintain high code quality:

- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Style guide enforcement
- **mypy**: Static type checking
- **pylint**: Code analysis

These tools run automatically as pre-commit hooks when you commit changes.

### 📊 Running Tests

Run the test suite using:
```bash
poetry run python -m unittest discover tests
```

### 🔍 Type Checking

Run static type checking with:
```bash
poetry run mypy .
```

## 🚨 Troubleshooting

1. Model Download Issues:
   - Ensure you have internet connection for the first run
   - Models are downloaded from Coqui TTS's HuggingFace repository
   - Each model is approximately 100MB
   - Check your disk space (need ~200MB for both models)
   - Models are cached at:
     - macOS: `~/Library/Application Support/tts`
     - Windows: `%LOCALAPPDATA%\tts`
     - Linux: `~/.cache/tts`

2. Audio Quality Issues:
   - Try using a different speaker ID from the VCTK dataset
   - Adjust the synthesis parameters in the code
   - Ensure the input text is properly formatted
   - Check if the audio file is not corrupted

3. Permission Issues:
   - Ensure you have write permissions in the output directory
   - Check that the TTS cache directory is accessible
   - Try running with elevated permissions if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Ensure all pre-commit hooks pass
6. Submit a pull request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The project uses the Coqui TTS VITS model which is licensed under the Apache 2.0 License. For more information about the model license, visit the [Coqui TTS Models page](https://github.com/coqui-ai/TTS/blob/dev/TTS/.models.json).

---

<div align="center">
Made with ❤️ using Coqui TTS
