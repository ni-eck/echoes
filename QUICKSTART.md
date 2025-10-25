# Echoes - Quick Start Guide

## Prerequisites
✅ Python 3.10+ installed
✅ Virtual environment created (`.venv`)
✅ Dependencies installed
✅ OpenAI API key

## 30-Second Setup

### 1. Activate Virtual Environment
```powershell
.venv\Scripts\Activate.ps1
```

### 2. Add Your API Key
Edit `.env` file:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL=gpt-4o
```

### 3. Start the Server
```powershell
uvicorn src.echoes.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open Browser
Go to: http://localhost:8000/docs

## Test the API

### Generate a Story (via Swagger UI)
1. Open http://localhost:8000/docs
2. Click on `/api/story` POST endpoint
3. Click "Try it out"
4. Enter a topic:
   ```json
   {
     "topic": "The Moon Landing"
   }
   ```
5. Click "Execute"

### Or Use curl
```bash
curl -X POST http://localhost:8000/api/story \
  -H "Content-Type: application/json" \
  -d '{"topic": "The Fall of the Berlin Wall"}'
```

### Expected Response
```json
{
  "topic": "The Fall of the Berlin Wall",
  "brief": "Research brief with facts and timeline...",
  "story": "Narrative script with scene beats...",
  "faq": [
    "Q: When did the wall fall?",
    "A: November 9, 1989",
    ...
  ],
  "audio_url": "/static/audio_20251025_143022_abc123.mp3",
  "video_url": "/static/video_20251025_143025_def456.mp4"
}
```

## Run Tests

```powershell
cd src
python -m pytest echoes/tests/ -v
```

Expected output:
```
============================================== 5 passed in 2.29s ===============================================
```

## Project Structure

```
src/echoes/
├── app/              # FastAPI application
│   ├── main.py       # Entry point
│   ├── settings.py   # Configuration
│   └── routers/      # API endpoints
├── agents/           # AI agents (OpenAI SDK)
├── workflows/        # Multi-agent orchestration
├── services/         # TTS, video, storage
├── prompts/          # Agent system prompts
├── schemas/          # Pydantic models
└── tests/            # Test suite
```

## Common Commands

### Development
```powershell
# Start with auto-reload
uvicorn src.echoes.app.main:app --reload

# Run tests
pytest src/echoes/tests/ -v

# Check for errors
python -c "import sys; sys.path.insert(0, 'src'); from echoes.app.main import app; print('✅ OK')"
```

### Production
```powershell
# Start without reload
uvicorn src.echoes.app.main:app --host 0.0.0.0 --port 8000

# Or use the runner
python src/run.py
```

## Troubleshooting

### Import Errors
```powershell
# Ensure you're in the project root
cd c:\Users\tejash.varsani\PycharmProjects\echoes

# Activate venv
.venv\Scripts\Activate.ps1
```

### Missing Dependencies
```powershell
pip install -r requirements.txt
```

### API Key Not Found
Make sure `.env` exists with:
```
OPENAI_API_KEY=sk-...
```

## Next Steps

1. **Try Different Topics**: Experiment with various historical events
2. **Use the Chat Endpoint**: Ask follow-up questions about generated stories
3. **Integrate Real Services**: Replace mock TTS/video with real APIs
4. **Add Frontend**: Build a React/Vue interface

## Support

- API Documentation: http://localhost:8000/docs
- Project Instructions: `.github/copilot-instructions.md`
- Implementation Details: `IMPLEMENTATION.md`
- Full Status: `PROJECT_STATUS.md`

---

**Happy Storytelling!** 🎭📚✨