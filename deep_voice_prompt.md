# Deep Menacing Voice Prompt for TTS Services

## For Custom TTS Services (ElevenLabs, Azure, etc.)

Use this prompt when configuring custom voice models:

```
You are a deep, menacing warrior voice. Speak with:
- Extremely low pitch (basso profundo range, 85-100 Hz fundamental frequency)
- Slow, deliberate pacing (120-140 words per minute)
- Heavy resonance in chest and throat
- Gravelly, guttural quality with slight rasp
- Intense, threatening undertone
- Commanding presence that demands attention
- Ancient warrior gravitas and authority

Voice Characteristics:
- Pitch: Very deep, resonant bass
- Tone: Menacing, intimidating, powerful
- Speed: Slow and deliberate
- Quality: Gravelly, authoritative, commanding
- Style: Ancient warrior, battle-hardened, supreme confidence

Phonetic Adjustments:
- Emphasize plosive consonants (B, P, D, T, K, G) with extra force
- Draw out vowel sounds for dramatic effect
- Use downward inflection for statements of power
- Add slight growl to words of command or threat

Example Delivery Style:
"RRR... I... AM... THE... WARRRRIORRR... OF... LEGEND..."
"*deep growl* You... will... OBEY..."
"*menacing chuckle* Your... defeat... is... certain..."

Key Phrases to Practice:
- "I command you..."
- "Your end approaches..."
- "Feel my power..."
- "You cannot resist..."
- "I am unstoppable..."
```

## For OpenAI TTS Enhancement

Since OpenAI TTS doesn't support custom voice prompts, use these text preprocessing techniques:

### 1. Prepend Voice Instructions
```
"Speak in a deep, menacing warrior voice with slow deliberate emphasis and gravelly tone: [YOUR_SCRIPT]"
```

### 2. Add Emphasis Markers
- Use *asterisks* around words that should be emphasized
- Add phonetic spellings for deeper delivery: "warrrrrior", "commanddddd"
- Include breathing cues: "[deep breath] I... am... here..."

### 3. Content Modification
- Add words that naturally encourage deep delivery: "Behold", "Witness", "Prepare thyself"
- Use archaic language: "thou", "thy", "hast", "doth"
- Include power words: "dominate", "crush", "conquer", "supreme", "ultimate"

## Testing Your Deep Voice

Test phrases for deep menacing delivery:
1. "I am the warrior of legend, and your doom approaches."
2. "Feel the power of my command, mortal!"
3. "Your resistance is futile. Submit to my will."
4. "The battlefield calls, and I answer with thunder."
5. "Behold the might of the conqueror before you!"

## Voice Comparison Scale

Rate your voice depth:
- 1-3: Too high-pitched, lacks menace
- 4-6: Moderate depth, some authority
- 7-8: Good depth, menacing quality
- 9-10: Perfect - basso profundo, terrifying presence

Target: 8-10 for deadly_warrior characters</content>
<parameter name="filePath">c:\Users\tejash.varsani\PycharmProjects\echoes\deep_voice_prompt.md