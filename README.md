# Echoes 🎭

An AI-powered historical interactive learning platform that transforms user queries into multimodal experiences: research briefs, narrative stories, FAQs, audio, and video.

## 🌐 Live Demo

Try the live demo: **[https://talk-to-past.lovable.app/](https://talk-to-past.lovable.app/)**

## ✨ Features

- **🤖 Multi-Agent AI Pipeline**: Uses OpenAI Agents SDK with specialized agents for research, storytelling, and Q&A
- **🌐 Modern React Frontend**: Beautiful, responsive single-page application built with React 18, TypeScript, and Tailwind CSS
- **💻 Command Line Tool**: Simple CLI for programmatic use
- **🔌 REST API**: Full FastAPI backend with interactive documentation
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices
- **🎵 Media Generation**: Mocked TTS and video services (ready for real API integration)
- **🚀 Automated Launchers**: One-click startup scripts for development and production

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 18+** and npm (for frontend development)
- **OpenAI API Key** with access to GPT-4o

### 1. Environment Setup
```powershell
# Clone the repository
git clone https://github.com/ni-eck/echoes.git
cd echoes

# Create Python virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for frontend development)
cd frontend
npm install
cd ..
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

#### 🚀 Automated Launcher (Recommended)
```powershell
# Start both backend and frontend automatically
.\launch_echoes.ps1

# Or use Python directly
python start_with_browser.py
```
This will:
- Start the FastAPI backend on `http://127.0.0.1:8000`
- Start the React dev server on `http://localhost:3000`
- Open your browser to the React frontend automatically

#### Manual Startup

**Full-Stack Development:**
```powershell
# Terminal 1: Start FastAPI backend
cd src
python -m uvicorn echoes.app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Start React frontend
cd frontend
npm run dev
```
Then open **http://localhost:3000** in your browser!

**Backend Only:**
```powershell
cd src
python -m uvicorn echoes.app.main:app --reload --host 127.0.0.1 --port 8000
```
Then open **http://127.0.0.1:8000** in your browser (serves built React frontend).

**Command Line Tool:**
```powershell
python main.py
```

## 📖 Usage

### Web Interface
1. Open the application URL (automatically opened by launcher)
2. Enter any historical topic (e.g., "The moon landing", "Ancient Rome", "Cleopatra")
3. Click "🚀 Generate Story" or select from featured topics
4. Explore the interactive experience:
   - 📋 **Research Brief**: Historical facts and context
   - 📖 **Story**: Engaging narrative with scene descriptions
   - ❓ **FAQ**: Interactive Q&A about the topic
   - 🎵 **Audio**: Generated narration (currently mocked)
   - 🎬 **Video**: Historical animation (currently mocked)
   - 💬 **Chat**: Ask follow-up questions to AI agents

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
    "question": "What caused its fall?",
    "topic": "The Fall of the Berlin Wall"
  }'
```

**Response:**
```json
{
  "answer": "The fall was triggered by political reforms..."
}
```

### API Documentation
Visit **http://127.0.0.1:8000/docs** for interactive Swagger UI documentation.

## 🧪 Testing

```powershell
# Run from src/ directory (important!)
cd src
python -m pytest echoes/tests/ -v
```

All tests use mocked agents to avoid API costs and ensure deterministic results.

## 🏗️ Architecture

### Technology Stack

#### Backend
- **Framework**: FastAPI (async Python web framework)
- **AI**: OpenAI Agents SDK with GPT-4o
- **Configuration**: Pydantic v2 settings with environment variables
- **API**: RESTful endpoints with automatic OpenAPI documentation
- **Testing**: pytest with httpx for API testing

#### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development and optimized production builds
- **Styling**: Tailwind CSS with custom design system
- **UI Components**: shadcn/ui (Radix UI primitives)
- **Routing**: React Router for single-page application
- **State Management**: React Query for server state and TanStack Query for caching
- **Icons**: Lucide React icon library

#### Development Tools
- **Package Management**: pip (Python), npm (Node.js)
- **Environment**: Python virtual environments (.venv)
- **Version Control**: Git with GitHub
- **Code Quality**: ESLint (frontend), black/isort (Python)

### Multi-Agent Pipeline
1. **Researcher Agent** (temp=0.3) → Gathers historical facts and creates research briefs
2. **Storyteller Agent** (temp=0.7) → Crafts engaging 60-120s narratives with scene descriptions
3. **QA Agent** (temp=0.5) → Generates relevant questions and answers
4. **Services Layer** → Produces audio (TTS) and video (animation) - currently mocked

### Project Structure
```
echoes/
├── .github/                    # GitHub configuration
│   └── copilot-instructions.md # AI coding assistant guidelines
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/             # Route components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── lib/               # Utilities and API clients
│   │   └── assets/            # Static assets
│   ├── package.json           # Node.js dependencies
│   └── vite.config.ts         # Vite configuration
├── src/echoes/                # Main Python package
│   ├── app/                   # FastAPI application
│   │   ├── main.py            # App entry point & SPA serving
│   │   ├── routers/           # API endpoints
│   │   └── settings.py        # Configuration
│   ├── agents/                # OpenAI agent builders
│   ├── workflows/             # Multi-agent orchestration
│   ├── services/              # Mock TTS/video/storage services
│   ├── prompts/               # Agent system prompts (Markdown)
│   ├── schemas/               # Pydantic models
│   └── tests/                 # Test suite
├── static/                    # Built frontend assets (served by FastAPI)
├── templates/                 # Legacy Jinja2 templates
├── main.py                    # CLI tool
├── start_with_browser.py      # Automated launcher script
├── launch_echoes.ps1          # PowerShell launcher wrapper
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
└── README.md                  # This file
```

### Data Flow
```
User Query → React Frontend → FastAPI Backend → Multi-Agent Pipeline
    ↓
Researcher Agent → Storyteller Agent → QA Agent → Services
    ↓
JSON Response → Frontend → Interactive Experience
```

## 🔧 Development Workflows

### Frontend Development
```powershell
cd frontend
npm run dev          # Start dev server with hot reload
npm run build        # Production build to ../static
npm run preview      # Preview production build
```

### Backend Development
```powershell
cd src
python -m uvicorn echoes.app.main:app --reload --host 127.0.0.1 --port 8000
```

### Testing
```powershell
cd src
python -m pytest echoes/tests/ -v --cov=echoes
```

### Code Quality
```powershell
# Python
black src/ tests/
isort src/ tests/
flake8 src/ tests/

# JavaScript/TypeScript
cd frontend
npm run lint
npm run type-check
```

## 🔌 Integration Points

### External APIs
- **OpenAI Agents SDK**: Multi-agent orchestration with GPT-4o
- **ElevenLabs** (planned): Text-to-speech for audio narration
- **Runway ML/D-ID** (planned): AI video generation for historical animations

### Internal Services
- **TTS Service**: Mock implementation ready for ElevenLabs integration
- **Video Service**: Mock implementation ready for Runway ML integration
- **Storage Service**: Local file storage with URL generation

## 📝 Project Conventions

### Python
- **Imports**: Relative imports within package (`from ..agents import build_agent`)
- **Path Handling**: Always use `pathlib.Path` for cross-platform compatibility
- **Settings**: Pydantic v2 with `SettingsConfigDict` for environment configuration
- **Agent Pattern**: Builder functions return `Agent` instances, not classes
- **Mocking**: Patch at import location, not definition location

### JavaScript/TypeScript
- **Components**: Functional components with TypeScript interfaces
- **Styling**: Tailwind CSS classes with custom design tokens
- **API Calls**: React Query for server state management
- **Routing**: React Router with lazy-loaded components
- **Icons**: Lucide React for consistent iconography

### Testing
- **Location**: Tests run from `src/` directory only
- **Mocking**: `unittest.mock.patch` for agent builders
- **Coverage**: pytest-cov for coverage reporting

## 🚨 Common Pitfalls

1. **Directory Issues**: Always run tests from `src/` directory
2. **Import Errors**: Use `from agents import Agent`, not `from openai_agents import Agent`
3. **Path Resolution**: Frontend builds to `../static` relative to `frontend/` directory
4. **Environment Variables**: Required `.env` file with `OPENAI_API_KEY`
5. **Mock Patching**: Patch where imported (`echoes.workflows.*`), not where defined

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes with tests
4. Ensure all tests pass: `cd src && python -m pytest echoes/tests/ -v`
5. Submit a pull request with a clear description

### Development Setup
```powershell
# After cloning and basic setup
cd frontend && npm install
cd ..
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for the Agents SDK and GPT-4o
- FastAPI community for the excellent web framework
- React and Vite teams for modern frontend tooling
- shadcn/ui for beautiful component primitives