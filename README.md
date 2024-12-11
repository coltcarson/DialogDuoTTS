# 🎭 DialogDuoTTS

> 🗣️ Transform text dialogues into lifelike conversations using state-of-the-art offline Text-to-Speech technology!

## ✨ Features

- 🌐 Works completely offline using Coqui TTS for high-quality voice synthesis
- 🎭 Different voices for each speaker in the dialogue
- 💻 Cross-platform support (Windows, macOS, Linux)
- ⚡ Automatic handling of conversation turn-taking with appropriate pauses
- 🛡️ Type-checked and well-tested codebase with comprehensive quality checks

## 🎙️ Voice Models

### Model Details
- **Model Type**: VITS (Conditional Variational Autoencoder with Adversarial Learning)
- **Dataset**: VCTK (Voice Cloning Toolkit)
- **Model Size**: ~100MB per voice model
- **Quality**: High-quality neural TTS with natural-sounding voices
- **Language**: English (with British and American accents)

### Included Voices
1. **PersonA - Male British Voice**
   - Model: `tts_models/en/vctk/vits`
   - Speaker ID: `p273`
   - Accent: British English
   - Characteristics: Clear, professional male voice

2. **PersonB - Female American Voice**
   - Model: `tts_models/en/vctk/vits`
   - Speaker ID: `p262`
   - Accent: American English
   - Characteristics: Natural, engaging female voice

### Model Storage
The TTS models are automatically downloaded and cached locally:
- **macOS**: `~/Library/Application Support/tts`
- **Windows**: `%LOCALAPPDATA%\tts`
- **Linux**: `~/.cache/tts`

Models are downloaded only once and work completely offline afterward.

### Security & Updates
- Models are downloaded securely through Coqui TTS's API
- Downloads are verified for integrity
- Models are cached locally for offline use
- Updates can be forced by clearing the cache directory

## 🚀 Getting Started

### Prerequisites

- 🐍 Python 3.10 or higher
- 📦 Poetry (Python package manager)

### Installation

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

## 📝 Usage

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

3. Find your generated audio files in the `output/` directory! 🎉

## 📂 Project Structure

```
DialogDuoTTS/
├── 📄 .pre-commit-config.yaml  # Pre-commit hook configuration
├── 📄 .pylintrc               # Pylint configuration
├── 📄 mypy.ini               # MyPy type checking configuration
├── 📄 pyproject.toml         # Project dependencies and settings
├── 🐍 main.py               # Main script for TTS conversion
├── 📁 data/                 # Input dialogue files
│   └── 📝 conversation.txt
├── 📁 output/               # Generated audio files
└── 🧪 tests/               # Test suite
    ├── __init__.py
    └── test_dialogue_to_speech.py
```

## 👩‍💻 Development

### 🛠️ Code Quality Tools

We use industry-standard tools to maintain high code quality:

- ⚫ **black**: Code formatting
- 🔄 **isort**: Import sorting
- ✨ **flake8**: Style guide enforcement
- 🔍 **mypy**: Static type checking
- 🐛 **pylint**: Code analysis

These tools run automatically as pre-commit hooks when you commit changes.

### 🧪 Running Tests

Run the test suite using:
```bash
poetry run python -m unittest discover tests
```

### ✅ Type Checking

Run static type checking with:
```bash
poetry run mypy .
```

## ❓ Troubleshooting

1. 📥 Model Download Issues:
   - Ensure you have internet connection for the first run
   - Models are downloaded from Coqui TTS's HuggingFace repository
   - Each model is approximately 100MB
   - Check your disk space (need ~200MB for both models)
   - Models are cached at:
     - macOS: `~/Library/Application Support/tts`
     - Windows: `%LOCALAPPDATA%\tts`
     - Linux: `~/.cache/tts`

2. 🔊 Audio Quality Issues:
   - Try using a different speaker ID from the VCTK dataset
   - Adjust the synthesis parameters in the code
   - Ensure the input text is properly formatted
   - Check if the audio file is not corrupted

3. 🔒 Permission Issues:
   - Ensure you have write permissions in the output directory
   - Check that the TTS cache directory is accessible
   - Try running with elevated permissions if needed

## 🤝 Contributing

1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. ✍️ Make your changes
4. 🧪 Run the test suite
5. ✅ Ensure all pre-commit hooks pass
6. 📤 Submit a pull request

## 📄 License

[Add your license information here]

---

<div align="center">
Made with ❤️ using Coqui TTS

Powered by [🗣️ Coqui TTS](https://github.com/coqui-ai/TTS)
</div>
