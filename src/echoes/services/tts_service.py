"""Service for text-to-speech using OpenAI TTS with character roles."""

import os
import re
from openai import OpenAI
from ..app.settings import OPENAI_API_KEY
from .storage import save_binary, public_url

# Valid OpenAI TTS voices
VALID_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

# Enhanced voice mapping based on historical context and character analysis
VOICE_MAP = {
    # Historical Context + Character Type
    "ancient_ruler": "fable",      # Elegant, authoritative (Cleopatra, Egyptian Pharaohs)
    "ancient_warrior": "onyx",     # Deep, menacing voice (Hannibal, Gladiators)
    "ancient_priest": "onyx",      # Deep, wise (Ancient intellectuals)
    "ancient_female": "nova",      # Youthful, mysterious (Ancient women)
    "medieval_knight": "onyx",     # Deep, battle-hardened (Knights, warriors)
    "medieval_ruler": "fable",     # Regal, authoritative (Queens, nobles)
    "modern_figure": "alloy",      # Contemporary, clear (20th century figures)
    "elderly_resident": "shimmer", # Mature, experienced (80-year-old narrators)
    "deadly_warrior": "onyx",      # Deep, menacing voice for intense warriors
    "intense_ruler": "echo",       # Strong, commanding for powerful rulers

    # Direct character mappings
    "cleopatra": "fable",          # Ancient Egyptian Queen
    "hannibal": "onyx",            # Ancient Carthaginian General (deep voice)
    "caesar": "echo",              # Roman Emperor (commanding voice)
    "alexander": "onyx",           # Macedonian Conqueror (deep voice)
    "napoleon": "echo",            # French Emperor
    "elizabeth": "fable",          # Queen Elizabeth
    "churchill": "onyx",           # British Prime Minister

    # Generic roles
    "narrator": "alloy",          # Clear, neutral narrator
    "warrior": "onyx",            # Deep, menacing warrior voice
    "ruler": "echo",              # Strong, commanding ruler
    "elderly": "shimmer",         # Mature elderly voice
    "male": "onyx",               # Generic male
    "female": "nova",             # Generic female
    "default": "alloy"            # Fallback
}

def _resolve_voice_name(voice_key: str) -> str:
    """
    Resolve a voice key to a valid OpenAI TTS voice name.
    Handles invalid voice names by mapping them to valid ones.
    """
    voice_key_lower = voice_key.lower()

    # If it's already a valid OpenAI voice, return it
    if voice_key_lower in VALID_VOICES:
        return voice_key_lower

    # Look up in VOICE_MAP
    if voice_key_lower in VOICE_MAP:
        mapped_voice = VOICE_MAP[voice_key_lower]
        # If the mapped voice is also valid, return it
        if mapped_voice in VALID_VOICES:
            return mapped_voice
        # If mapped voice is another key, resolve recursively
        return _resolve_voice_name(mapped_voice)

    # Handle invalid voice names by mapping to similar valid ones
    if "warrior" in voice_key_lower or "deadly" in voice_key_lower:
        return "onyx"   # Deep, menacing voice
    elif "ruler" in voice_key_lower or "intense" in voice_key_lower:
        return "echo"   # Strong, commanding voice
    elif "female" in voice_key_lower or "woman" in voice_key_lower:
        return "nova"   # Female voice
    elif "elderly" in voice_key_lower or "mature" in voice_key_lower:
        return "shimmer" # Mature voice
    elif "mystical" in voice_key_lower or "story" in voice_key_lower:
        return "fable"  # Story-like voice
    else:
        return "alloy"  # Default fallback

def synthesize_voice(script: str, topic: str = "story") -> str:
    """
    Synthesize voice from text script using OpenAI TTS with character role support.
    
    Supports character roles with voice markers like:
    [NARRATOR]: Text here
    [CLEOPATRA]: Text here
    [ELDERLY]: Text here
    
    Args:
        script: Text script to convert to speech (may contain voice markers)
        topic: Topic name for filename
    
    Returns:
        Public URL to the audio file
    """
    if not OPENAI_API_KEY:
        print("OpenAI API key not configured. Using mock TTS.")
        return _synthesize_mock_voice(script, topic)
    
    try:
        # Check if script has character markers
        if _has_character_markers(script):
            return _synthesize_multi_voice(script, topic)
        else:
            return _synthesize_single_voice(script, topic)
        
    except Exception as e:
        print(f"OpenAI TTS failed: {e}. Using mock TTS.")
        return _synthesize_mock_voice(script, topic)

def _has_character_markers(script: str) -> bool:
    """Check if script contains character voice markers."""
    # Look for patterns like [NARRATOR], [CLEOPATRA], [ELDERLY], etc.
    marker_pattern = r'\[([A-Z][A-Z\s]+)\]:'
    return bool(re.search(marker_pattern, script))

def _synthesize_single_voice(script: str, topic: str) -> str:
    """Synthesize with single voice (alloy), applying menacing styling if detected."""
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Apply menacing styling even for single voice if the content suggests it
    processed_script = _apply_menacing_styling_if_needed(_clean_script(script), topic)

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=processed_script
    )
    
    safe_topic = topic.lower().replace(" ", "_").replace("'", "").replace('"', '')
    filename = f"audio_{safe_topic}.mp3"
    
    audio_data = response.content
    file_path = save_binary(filename, audio_data)
    
    return public_url(file_path)

def _synthesize_multi_voice(script: str, topic: str) -> str:
    """
    Synthesize with multiple voices based on character markers and context analysis.
    Uses intelligent voice selection based on historical context and character types.
    """
    print("🎭 Detected character roles! Using dynamic voice analysis...")

    # Extract voice recommendations from script (if any)
    recommended_voices = _extract_voice_recommendations(script)

    if recommended_voices:
        # Use the most recommended voice
        primary_voice = recommended_voices[0]
        print(f"🎤 Using recommended voice '{primary_voice}' from story analysis")
    else:
        # Analyze context and characters to select voice
        primary_voice = _analyze_context_for_voice(script, topic)
        print(f"🎤 Auto-selected voice '{primary_voice}' based on context analysis")

    # Ensure we have a valid OpenAI TTS voice
    primary_voice = _resolve_voice_name(primary_voice)
    print(f"🎵 Final voice selection: '{primary_voice}'")

    client = OpenAI(api_key=OPENAI_API_KEY)

    # Apply voice-specific text processing for deeper/more menacing voices
    processed_script = _apply_voice_styling(script, primary_voice)

    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice=primary_voice,
            input=processed_script
        )

        safe_topic = topic.lower().replace(" ", "_").replace("'", "").replace('"', '')
        filename = f"audio_{safe_topic}.mp3"

        audio_data = response.content
        file_path = save_binary(filename, audio_data)

        print(f"✅ Audio file created successfully: {file_path}")
        return public_url(file_path)

    except Exception as e:
        print(f"❌ OpenAI TTS API failed for voice '{primary_voice}': {e}")
        raise e

def _extract_voice_recommendations(script: str) -> list:
    """Extract voice recommendations from script markers like [CLEOPATRA:FABLE]."""
    # Look for patterns like [CLEOPATRA:FABLE] or [WARRIOR:ECHO]
    voice_pattern = r'\[([A-Z_]+):([A-Z]+)\]'
    matches = re.findall(voice_pattern, script)

    voices = []
    for char_type, voice in matches:
        voice_lower = voice.lower()
        if voice_lower in VOICE_MAP.values():
            voices.append(voice_lower)

    return voices

def _determine_story_gender(script: str, topic: str) -> str:
    """
    Analyze the story content and topic to determine if it's primarily about a male or female figure.

    Returns:
        "male", "female", or "neutral"
    """
    script_lower = script.lower()
    topic_lower = topic.lower()
    combined_text = f"{script_lower} {topic_lower}"

    # Count gender-specific pronouns and references
    male_indicators = [
        " he ", " him ", " his ", " himself ", " man ", " men ", " male ", " boy ", " boys ",
        " king ", " lord ", " emperor ", " duke ", " prince ", " sir ", " mr ", " father ",
        " brother ", " son ", " uncle ", " grandfather ", " husband "
    ]

    female_indicators = [
        " she ", " her ", " hers ", " herself ", " woman ", " women ", " female ", " girl ", " girls ",
        " queen ", " lady ", " empress ", " duchess ", " princess ", " madam ", " mrs ", " ms ",
        " mother ", " sister ", " daughter ", " aunt ", " grandmother ", " wife "
    ]

    # Count occurrences
    male_count = sum(combined_text.count(indicator) for indicator in male_indicators)
    female_count = sum(combined_text.count(indicator) for indicator in female_indicators)

    # Check for specific female historical figures
    female_figures = [
        "cleopatra", "queen", "empress", "princess", "lady", "madam", "mrs", "ms",
        "elizabeth", "victoria", "catherine", "mary", "anne", "isabella", "joan",
        "marie", "theresa", "eleanor", "margaret", "pharaoh", "cleopatra"
    ]

    # Check for specific male historical figures
    male_figures = [
        "king", "emperor", "prince", "lord", "sir", "mr", "father", "brother", "son",
        "caesar", "alexander", "hannibal", "napoleon", "churchill", "lincoln",
        "washington", "gandhi", "mandela", "mlk", "martin luther king"
    ]

    # Check topic for gender-specific names
    female_figure_count = sum(1 for figure in female_figures if figure in topic_lower)
    male_figure_count = sum(1 for figure in male_figures if figure in topic_lower)

    # Add weight for named figures in topic
    male_count += male_figure_count * 3  # Weight named figures more heavily
    female_count += female_figure_count * 3

    # Determine gender based on counts
    if female_count > male_count and female_count > 2:
        return "female"
    elif male_count > female_count and male_count > 2:
        return "male"
    elif female_count == male_count and female_count > 0:
        # If equal, check for stronger female indicators
        if any(figure in topic_lower for figure in ["cleopatra", "queen", "empress", "pharaoh"]):
            return "female"
        elif any(figure in topic_lower for figure in ["king", "emperor", "caesar", "hannibal"]):
            return "male"
        else:
            return "neutral"
    else:
        return "neutral"

def _analyze_context_for_voice(script: str, topic: str) -> str:
    """
    Analyze the script content and topic to intelligently select the best voice.
    Considers historical era, character types, cultural context, and gender.
    """
    script_lower = script.lower()
    topic_lower = topic.lower()

    # First, determine the primary gender of the story
    story_gender = _determine_story_gender(script, topic)
    print(f"👤 Story gender analysis: {story_gender}")

    # Ancient historical figures
    if any(name in topic_lower for name in ["cleopatra", "hannibal", "caesar", "alexander", "pharaoh"]):
        if "cleopatra" in topic_lower or "queen" in script_lower or "pharaoh" in script_lower:
            return "fable"  # Elegant, authoritative for ancient rulers
        elif "hannibal" in topic_lower or "warrior" in script_lower or "general" in script_lower:
            return "echo"   # Strong, commanding for ancient warriors
        else:
            return "onyx"   # Deep, wise for other ancient figures

    # Time period detection
    if any(word in script_lower for word in ["ancient", "bce", "egypt", "rome", "greece", "pharaoh"]):
        if "warrior" in script_lower or "soldier" in script_lower or "battle" in script_lower:
            return "echo"   # Ancient warrior
        elif "queen" in script_lower or "ruler" in script_lower or "pharaoh" in script_lower:
            return "fable"  # Ancient ruler
        else:
            return "alloy"  # Ancient narrator

    # Medieval period
    if any(word in script_lower for word in ["medieval", "knight", "castle", "king", "queen", "middle ages"]):
        if "knight" in script_lower or "warrior" in script_lower:
            return "onyx"   # Medieval knight
        else:
            return "fable"  # Medieval ruler

    # Elderly resident narratives (80-year-old perspective)
    if "80 years old" in script_lower or "elderly" in script_lower or "lived in" in script_lower:
        return "shimmer"  # Mature, experienced voice

    # Modern/contemporary
    if any(word in script_lower for word in ["modern", "contemporary", "20th century", "21st century"]):
        return "alloy"  # Contemporary voice

    # Character-based detection
    primary_character = _detect_primary_character(script)
    char_lower = primary_character.lower()

    # Direct character mappings
    if char_lower in VOICE_MAP:
        return VOICE_MAP[char_lower]

    # Gender-based voice selection based on story analysis
    if story_gender == "female":
        return "nova"   # Female voice for female-centric stories
    elif story_gender == "male":
        return "onyx"   # Male voice for male-centric stories

    # Legacy gender detection as fallback
    if any(word in char_lower for word in ["queen", "woman", "female", "lady", "empress"]):
        return "nova"   # Female voice
    elif any(word in char_lower for word in ["king", "man", "male", "lord", "emperor"]):
        return "onyx"   # Male voice

    # Default fallback
    return "alloy"

def _detect_primary_character(script: str) -> str:
    """Detect the primary character from voice markers and context."""
    # First, check for explicit voice markers like [CLEOPATRA:FABLE]
    voice_marker_pattern = r'\[([A-Z_]+):([A-Z]+)\]'
    voice_matches = re.findall(voice_marker_pattern, script)
    if voice_matches:
        # Return the first character type found
        return voice_matches[0][0]

    # Then check for character name markers like [CLEOPATRA]
    marker_pattern = r'\[([A-Z][A-Z\s]+)\]:'
    markers = re.findall(marker_pattern, script)

    if not markers:
        return "narrator"

    # Count frequency and return most common (excluding generic markers)
    from collections import Counter
    marker_counts = Counter(markers)

    # Remove generic markers
    for generic in ["NARRATOR", "SCENE", "VISUAL", "DESCRIPTION"]:
        marker_counts.pop(generic, None)

    if marker_counts:
        return marker_counts.most_common(1)[0][0]

    return "narrator"

def _apply_voice_styling(script: str, voice: str) -> str:
    """
    Apply voice-specific text styling to enhance the menacing/deep quality of certain voices.
    Simplified to avoid API failures.
    """
    cleaned_script = _clean_script(script)

    # Only apply styling to voices that should sound menacing/deep
    menacing_voices = ["onyx", "echo"]  # Valid OpenAI voices that sound deep/commanding

    if voice not in menacing_voices:
        return cleaned_script

    # Apply simple menacing voice styling
    return _add_menacing_styling(cleaned_script)

def _add_menacing_styling(script: str) -> str:
    """
    Add subtle text modifications to encourage deeper, more menacing voice delivery.
    Simplified to avoid API failures while maintaining voice character.
    """
    # Simple emphasis markers for key words (TTS engines may interpret *word* as emphasis)
    menacing_words = [
        "warrior", "battle", "conquer", "defeat", "power", "strength", "command",
        "rule", "dominate", "crush", "destroy", "victory", "glory", "honor"
    ]

    styled_script = script

    # Add emphasis to menacing words (avoid over-processing)
    for word in menacing_words:
        # Only emphasize if the word appears as a standalone word
        styled_script = re.sub(rf'\b({word})\b', r'*\1*', styled_script, flags=re.IGNORECASE)

    return styled_script

def _apply_menacing_styling_if_needed(script: str, topic: str) -> str:
    """
    Apply menacing styling to single-voice scripts if the content suggests it.
    Used for topics that should have deep, menacing delivery.
    """
    script_lower = script.lower()
    topic_lower = topic.lower()

    # Check if this content should have menacing styling
    menacing_indicators = [
        "warrior", "battle", "conquer", "hannibal", "caesar", "alexander",
        "deadly", "menacing", "intense", "commanding", "ruler", "general"
    ]

    should_style = any(indicator in script_lower or indicator in topic_lower
                      for indicator in menacing_indicators)

    if should_style:
        return _add_menacing_styling(script)
    else:
        return script

def _clean_script(script: str) -> str:
    """Remove voice markers from script for TTS."""
    # Remove markers like [CLEOPATRA]: or [NARRATOR]:
    cleaned = re.sub(r'\[([A-Z][A-Z\s]+)\]:\s*', '', script)
    return cleaned.strip()

def _synthesize_mock_voice(script: str, topic: str = "story") -> str:
    """Fallback mock TTS implementation."""
    from .storage import save_text, public_url
    
    safe_topic = topic.lower().replace(" ", "_").replace("'", "").replace('"', '')
    filename = f"audio_{safe_topic}.mp3"
    
    audio_content = f"[MOCK AUDIO NARRATION]\n\n{script}\n\n[END AUDIO]"
    file_path = save_text(filename, audio_content)
    
    return public_url(file_path)