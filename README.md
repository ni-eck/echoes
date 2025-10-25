# Echoes

An AI-powered historical interactive learning platform that turns user questions about history into animated, narrated, and conversational video experiences.

## Overview

Echoes uses a multi-agent pipeline powered by the OpenAI Agents SDK to transform any historical topic into:
- **Research Brief**: Verified facts and timeline
- **Narrative Story**: Engaging 60-120 second script with scene beats
- **FAQ**: Related questions and answers
- **Audio**: Text-to-speech narration (mocked)
- **Video**: AI-generated visualization (mocked)

## Setup

### 1. Create Virtual Environment
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Configure Environment
```powershell
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 4. Run the Application
```powershell
uvicorn src.echoes.app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the runner script:
```powershell
python src/run.py
```

### 5. Access Interactive Docs
Open `http://localhost:8000/docs` in your browser

## API Usage

### Generate a Story
```bash
curl -X POST http://localhost:8000/api/story \
  -H "Content-Type: application/json" \
  -d '{"topic": "The Fall of the Berlin Wall"}'
```

Response:
```json
{
  "topic": "The Fall of the Berlin Wall",
  "brief": "Research facts and timeline...",
  "story": "Narrative script...",
  "faq": ["Q: When did the wall fall?", "A: November 9, 1989", ...],
  "audio_url": "/static/audio_abc123.txt",
  "video_url": "/static/video_abc123.txt"
}
```

### Interactive Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "story_context": "The Berlin Wall fell in 1989...",
    "question": "What led to the fall of the wall?"
  }'
```

Response:
```json
{
  "answer": "The fall was triggered by..."
}
```

## Testing

```powershell
pytest src/echoes/tests/
```

## Project Structure

```
src/echoes/
├── app/              # FastAPI application
├── agents/           # OpenAI agent implementations
├── workflows/        # Multi-agent orchestration
├── services/         # TTS, video, storage services
├── prompts/          # Agent system prompts
├── schemas/          # Pydantic models
└── tests/            # Test suite
```

## Architecture

The system follows a multi-agent pipeline:
1. **Researcher Agent** → Gathers facts
2. **Storyteller Agent** → Creates narrative
3. **QA Agent** → Generates FAQ
4. **Services** → Produce media (mocked)

See `.github/copilot-instructions.md` for detailed architecture notes.