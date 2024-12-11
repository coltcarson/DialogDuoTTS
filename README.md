# 🎭 DialogDuoTTS

> 🗣️ Transform text dialogues into lifelike conversations using state-of-the-art offline Text-to-Speech technology!

## ✨ Features

- 🌐 Works completely offline using Coqui TTS for high-quality voice synthesis
- 🎭 Different voices for each speaker in the dialogue
- 💻 Cross-platform support (Windows, macOS, Linux)
- ⚡ Automatic handling of conversation turn-taking with appropriate pauses
- 🛡️ Type-checked and well-tested codebase with comprehensive quality checks

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

## 🎙️ Voice Configuration

The script leverages Coqui TTS for premium voice synthesis:

- 🤖 Default model: `tts_models/en/ljspeech/tacotron2-DDC`
- 💾 Models are automatically downloaded and cached locally
- 🗣️ Different voices can be configured for each speaker

## ❓ Troubleshooting

1. 📥 Model Download Issues:
   - Check your internet connection during first run
   - Models are cached at `~/Library/Application Support/tts` on macOS

2. 🔊 Audio Quality Issues:
   - Try using a different Coqui TTS model
   - Adjust the synthesis parameters in the code

3. 🔒 Permission Issues:
   - Ensure you have write permissions in the output directory
   - Check that the TTS cache directory is accessible

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
</div>
