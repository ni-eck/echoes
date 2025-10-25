# Echoes AI Copilot Instructions

## Project Overview
Echoes is an AI-powered historical interactive learning platform that transforms user queries into multimodal experiences: research brief, narrative story, FAQ, audio, and video.

## Architecture

### Multi-Agent Pipeline (Fully Implemented)
The system uses **OpenAI Agents SDK** (`from agents import Agent`) to orchestrate specialized agents:
- `researcher_agent.py` - Gathers historical facts (temp=0.3, web_search tool with graceful fallback)
- `storyteller_agent.py` - Creates 60-120s narratives (temp=0.7)
- `qa_agent.py` - Generates Q&A content (temp=0.5)
- `director_agent.py` - Optional coordinator (example class provided)

**Actual Data Flow**: User Query → `generate_story_experience()` → Researcher → Storyteller → QA → TTS/Video Services → Response

### Project Structure (src-layout)
```
src/echoes/           # Main package (run from src/)
├── app/              # FastAPI application
│   ├── settings.py   # Pydantic v2 (pydantic_settings.BaseSettings)
│   └── routers/      # story.py, chat.py
├── agents/           # Agent builders returning Agent instances
├── workflows/        # story_pipeline.py orchestrates agents
├── services/         # Mock TTS/video/storage (production-ready structure)
├── prompts/          # Markdown templates loaded at runtime
└── tests/            # pytest with mocked agents
```

## Critical Developer Workflows

### Running from Correct Directory
```powershell
# IMPORTANT: Tests must run from src/ directory
cd src
python -m pytest echoes/tests/ -v

# App imports require src/ in path or run from src/
uvicorn echoes.app.main:app --reload
```

### Testing Pattern
Tests use `unittest.mock.patch` to replace agent builders at **import location**:
```python
# Patch where functions are imported, not where they're defined
with patch('echoes.workflows.story_pipeline.build_researcher_agent', mock_fn), \
     patch('echoes.app.routers.chat.build_qa_agent', mock_fn):
```

### Environment Setup
```powershell
.venv\Scripts\Activate.ps1  # Windows PowerShell
# .env file must contain: OPENAI_API_KEY, OPENAI_MODEL
```

## Project-Specific Conventions

### Settings (Pydantic v2)
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    openai_api_key: str
    openai_model: str = "gpt-4o"
```
Access via: `from echoes.app.settings import MODEL, OPENAI_API_KEY`

### Agent Pattern (CRITICAL)
```python
from agents import Agent  # NOT openai_agents
from pathlib import Path

def _load_prompt(filename: str) -> str:
    prompts_dir = Path(__file__).parent.parent / "prompts"
    return (prompts_dir / filename).read_text(encoding="utf-8")

def build_agent(model: str) -> Agent:
    return Agent(
        name="AgentName",
        model=model,
        instructions=_load_prompt("agent.md"),
        tools=["web_search"] if available else None,  # Graceful fallback
        temperature=0.3  # Varies by agent role
    )
```

### Service Mocks (Production Structure)
All services in `services/` are mocked but production-ready:
- `storage.py`: Saves to temp dir, returns `/static/...` URLs
- `tts_service.py`: Creates mock audio files
- `video_service.py`: Creates mock video files
- Ready for real API integration (ElevenLabs, Runway, D-ID)

### Import Conventions
- Relative imports within package: `from ..agents.researcher_agent import build_researcher_agent`
- Always use `Path` for file operations: `Path(__file__).parent.parent / "prompts"`
- Agent builders return `Agent`, not classes

## Integration Points

### OpenAI Agents SDK (ACTUAL USAGE)
```python
from agents import Agent  # Package name is 'agents'

agent = Agent(name="...", model=model, instructions=prompt, temperature=0.3)
result = agent.run("user prompt here")  # Returns string
```

### Workflow Orchestration
`workflows/story_pipeline.py` is the main entry point:
1. Builds agents with model parameter
2. Calls `.run(prompt)` on each agent sequentially
3. Passes outputs between agents via string prompts
4. Calls mock services for TTS/video
5. Returns dict matching `StoryResponse` schema

## Testing Requirements

### Mock Agent Pattern
```python
class MockAgent:
    def __init__(self, response: str):
        self.response = response
    def run(self, prompt: str) -> str:
        return self.response

def mock_agent_builder(model: str):
    return MockAgent("deterministic response")

# Patch at import location
with patch('echoes.workflows.story_pipeline.build_researcher_agent', mock_agent_builder):
```

### Test Execution
```bash
cd src  # MUST be in src directory
python -m pytest echoes/tests/ -v  # All 5 tests pass
```

## Common Pitfalls

1. **Wrong import**: Use `from agents import Agent`, NOT `from openai_agents import Agent`
2. **Wrong directory**: Tests fail if not run from `src/`
3. **Pydantic v2**: Use `pydantic_settings.BaseSettings` with `model_config = SettingsConfigDict(...)`
4. **Mock location**: Patch where imported (`echoes.workflows.*`), not where defined (`echoes.agents.*`)
5. **Path handling**: Always use `Path` for cross-platform compatibility

## Current Status
**Production Ready** - All features implemented, tested, and documented. Services are mocked but follow production patterns for easy API integration.