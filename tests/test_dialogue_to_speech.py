"""Test suite for DialogueToSpeech class."""

import os
from pathlib import Path
from typing import Generator

import pytest
from pydub import AudioSegment

from main import DialogueToSpeech


@pytest.fixture
def dialogue_to_speech() -> DialogueToSpeech:
    """Fixture to create a DialogueToSpeech instance"""
    return DialogueToSpeech()


@pytest.fixture
def temp_conversation_file() -> Generator[str, None, None]:
    """Fixture to create a temporary conversation file"""
    content = """PersonA: Hello, this is a test.
PersonB: This is a test response."""

    # Create a temporary file
    temp_path = "temp_conversation.txt"
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(content)

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


def test_initialization(dialogue_to_speech: DialogueToSpeech) -> None:
    """Test that DialogueToSpeech initializes correctly"""
    assert dialogue_to_speech.male_tts is not None
    assert dialogue_to_speech.female_tts is not None
    assert dialogue_to_speech.male_speaker == "p273"
    assert dialogue_to_speech.female_speaker == "p262"


def test_create_audio_for_line(
    dialogue_to_speech: DialogueToSpeech, tmp_path: Path
) -> None:
    """Test audio generation for a single line"""
    output_path = os.path.join(tmp_path, "test_output.wav")
    test_text = "Hello, this is a test."

    # Generate audio
    dialogue_to_speech.create_audio_for_line(test_text, "PersonA", output_path)

    # Verify file exists
    assert os.path.exists(output_path)

    # Verify audio content
    audio = AudioSegment.from_wav(output_path)
    assert len(audio) > 0  # Check that audio has content


def test_process_conversation(
    dialogue_to_speech: DialogueToSpeech, temp_conversation_file: str, tmp_path: Path
) -> None:
    """Test processing a complete conversation"""
    # Create output directory in temp path
    output_dir = os.path.join(tmp_path, "output")
    os.makedirs(output_dir)

    # Process conversation
    output_file = dialogue_to_speech.process_conversation(temp_conversation_file)

    # Verify output file exists
    assert output_file is not None
    assert os.path.exists(output_file)

    # Verify audio content
    audio = AudioSegment.from_wav(output_file)
    assert len(audio) > 0  # Check that audio has content


def test_invalid_speaker(dialogue_to_speech: DialogueToSpeech, tmp_path: Path) -> None:
    """Test handling of invalid speaker"""
    output_path = os.path.join(tmp_path, "test_output.wav")
    test_text = "This should fail."

    with pytest.raises(ValueError):
        dialogue_to_speech.create_audio_for_line(
            test_text, "InvalidSpeaker", output_path
        )


def test_empty_text(dialogue_to_speech: DialogueToSpeech, tmp_path: Path) -> None:
    """Test handling of empty text"""
    output_path = os.path.join(tmp_path, "test_output.wav")

    with pytest.raises(ValueError):
        dialogue_to_speech.create_audio_for_line("", "PersonA", output_path)


def test_invalid_conversation_file(
    dialogue_to_speech: DialogueToSpeech, tmp_path: Path
) -> None:
    """Test handling of invalid conversation file"""
    nonexistent_file = os.path.join(tmp_path, "nonexistent.txt")

    with pytest.raises(FileNotFoundError):
        dialogue_to_speech.process_conversation(nonexistent_file)
