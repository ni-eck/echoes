"""Test script to check voice selection logic."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from echoes.services.tts_service import _analyze_context_for_voice

def test_voice_selection():
    print("🎭 Testing Dynamic Voice Selection Logic")
    print("=" * 50)

    test_cases = [
        ("Cleopatra", "I am Cleopatra, the last pharaoh of Egypt..."),
        ("Hannibal", "I am Hannibal, the Carthaginian general..."),
        ("Alexander the Great", "I am Alexander, the Macedonian conqueror..."),
        ("Paris", "I am 80 years old and have lived in Paris all my life..."),
        ("Medieval Knight", "I am a knight in shining armor from the Middle Ages..."),
        ("Modern Scientist", "I am Albert Einstein, the physicist..."),
    ]

    for topic, script_sample in test_cases:
        voice = _analyze_context_for_voice(script_sample, topic)
        print(f"📝 Topic: {topic}")
        print(f"   Script: {script_sample[:50]}...")
        print(f"   Selected Voice: {voice}")
        print()

if __name__ == "__main__":
    test_voice_selection()