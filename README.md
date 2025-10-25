# Echoes 🎭

An AI-powered historical interactive learning platform that transforms user queries into multimodal experiences: research briefs, narrative stories, FAQs, audio, and video.

## ✨ Features

- **🤖 Multi-Agent AI Pipeline**: Uses OpenAI Agents SDK with specialized agents for research, storytelling, and Q&A
- **🌐 Web Interface**: Beautiful, responsive web UI for easy story generation
- **💻 Command Line Tool**: Simple CLI for programmatic use
- **🔌 REST API**: Full FastAPI backend with interactive documentation
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🎵 Media Generation**: Mocked TTS and video services (ready for real API integration)

## 🚀 Quick Start

### 1. Environment Setup
```powershell
# Clone the repository
git clone https://github.com/ni-eck/echoes.git
cd echoes

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Key
```powershell
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
```

### 3. Run the Application

#### Web Interface (Recommended)
```powershell
uvicorn src.echoes.app.main:app --reload
```
Then open **http://127.0.0.1:8000** in your browser!

#### Command Line Tool
```powershell
python generate_story.py
```

#### API Server Only
```powershell
uvicorn src.echoes.app.main:app --reload --host 127.0.0.1 --port 8000
```

## 📖 Usage

### Web Interface
1. Open http://127.0.0.1:8000
2. Enter any historical topic (e.g., "The moon landing", "Ancient Rome")
3. Click "🚀 Generate Story"
4. View research brief, narrative, FAQ, and media links
5. Download results as JSON

### API Endpoints

#### Generate Story
```bash
curl -X POST "http://127.0.0.1:8000/api/story" \
  -H "Content-Type: application/json" \
  -d '{"topic": "The Fall of the Berlin Wall"}'
```

**Response:**
```json
{
  "topic": "The Fall of the Berlin Wall",
  "brief": "Research facts and timeline...",
  "story": "Engaging narrative script...",
  "faq": ["Q: When did it fall?", "A: November 9, 1989"],
  "audio_url": "/static/audio_abc123.mp3",
  "video_url": "/static/video_abc123.mp4"
}
```

#### Interactive Chat
```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "story_context": "The Berlin Wall divided East and West Berlin...",
    "question": "What caused its fall?"
  }'
```

**Response:**
```json
{
  "answer": "The fall was triggered by political reforms..."
}
```

### API Documentation
Visit **http://127.0.0.1:8000/docs** for interactive Swagger UI.

## 🧪 Testing

```powershell
cd src
python -m pytest echoes/tests/ -v
```

## 🏗️ Architecture

### Multi-Agent Pipeline
1. **Researcher Agent** → Gathers historical facts and creates briefs
2. **Storyteller Agent** → Crafts engaging narratives with scene descriptions
3. **QA Agent** → Generates relevant questions and answers
4. **Services** → Produces audio (TTS) and video (animation) - currently mocked

### Project Structure
```
src/echoes/
├── app/              # FastAPI application & settings
│   ├── main.py       # App entry point with web interface
│   ├── routers/      # API endpoints (story.py, chat.py)
│   └── settings.py   # Pydantic configuration
├── agents/           # OpenAI agent builders
├── workflows/        # Multi-agent orchestration
├── services/         # Mock TTS/video/storage services
├── prompts/          # Agent system prompts (Markdown)
├── schemas/          # Request/response models
└── tests/            # Comprehensive test suite

templates/            # Jinja2 HTML templates
static/              # Static assets (CSS, JS, media)
generate_story.py    # CLI tool
```

## 🔧 Development

- **Framework**: FastAPI with async support
- **AI**: OpenAI Agents SDK with GPT-4o
- **Frontend**: Bootstrap 5 + Vanilla JavaScript
- **Testing**: pytest with httpx
- **Configuration**: Pydantic settings with dotenv

## 📝 Notes

- Services are currently mocked but follow production-ready patterns
- Ready for integration with real TTS (ElevenLabs) and video (Runway ML) APIs
- All agents use temperature settings optimized for their roles
- Comprehensive error handling and logging included

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.