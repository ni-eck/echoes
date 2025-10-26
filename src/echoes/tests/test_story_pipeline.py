"""Tests for story pipeline."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# Import the FastAPI app
from echoes.app.main import app

client = TestClient(app)

# Mock result class
class MockResult:
    """Mock result from Runner.run."""
    def __init__(self, output: str):
        self.final_output = output

# Mock agent builders
def mock_researcher_agent(model: str):
    """Mock researcher agent with deterministic output."""
    return MockAgent(
        """Research Brief: The Fall of the Berlin Wall

Key Points:
- The Berlin Wall stood from 1961 to 1989
- Divided East and West Berlin during the Cold War
- Symbol of the Iron Curtain between Soviet and Western blocs
- Peaceful protests and political changes led to its fall

Timeline:
- August 13, 1961: Construction begins
- November 9, 1989: Border crossing announcement
- November 10-12, 1989: Wall breached and dismantled

Sources: Historical records and Cold War documentation"""
    )

def mock_storyteller_agent(model: str):
    """Mock storyteller agent with deterministic output."""
    return MockAgent(
        """It was November 9, 1989. The city of Berlin held its breath.

SCENE 1: A crowd gathers at Checkpoint Charlie as rumors spread of border changes.

For 28 years, the concrete barrier had divided families, friends, and a nation. But tonight was different.

SCENE 2: Guards at the wall look at each other uncertainly, overwhelmed by thousands approaching.

When the announcement came, it was unclear and hurried. But the people understood: the wall was opening.

SCENE 3: Hammers and picks appear. People climb the wall, celebrating together.

By dawn, the symbol of division was becoming a symbol of unity. The Berlin Wall was falling, and with it, an era was ending."""
    )

def mock_qa_agent(model: str):
    """Mock QA agent with deterministic output."""
    return MockAgent(
        """Q: When did the Berlin Wall fall?
A: November 9, 1989

Q: How long did the Berlin Wall stand?
A: 28 years, from 1961 to 1989

Q: What caused the fall of the Berlin Wall?
A: Peaceful protests, political reforms in Eastern Europe, and mounting pressure for freedom

Q: What did the Berlin Wall symbolize?
A: The division between communist East and democratic West during the Cold War

Q: How did people react when the wall came down?
A: With celebration, joy, and emotional reunions of families separated for decades"""
    )

def mock_narrative_styler_agent(model: str):
    """Mock narrative styler agent with deterministic output."""
    return MockAgent(
        """You are a historical storyteller specializing in dramatic political events. Create narratives that:

- Use third-person limited perspective with dramatic tension and emotional depth
- Explore themes of division, unity, freedom, and human resilience
- Develop characters through their reactions to historical forces
- Structure stories with clear scene beats and emotional arcs
- Maintain historical accuracy while focusing on human elements

Key guidelines:
- Build suspense through political uncertainty and personal stakes
- Include sensory details of crowds, sounds, and atmosphere
- Show transformation from division to unity
- End with hope and reflection on human potential"""
    )

def mock_story_analyzer_agent(model: str):
    """Mock story analyzer agent with deterministic output."""
    return MockAgent(
        """You are a historical storyteller specializing in dramatic political transformations. Create narratives that:

- Use third-person dramatic perspective with building tension and emotional release
- Explore themes of division overcome, freedom achieved, and human resilience
- Develop characters through their personal reactions to world-changing events
- Structure stories with scene progression: setup, confrontation, climax, resolution
- Maintain atmospheric tension throughout with sensory details and emotional stakes

Key guidelines:
- Focus on the human element within larger historical forces
- Build emotional investment through personal stories and relationships
- Include vivid scene descriptions for visual impact
- Balance educational content with engaging narrative flow
- End with reflection on the broader implications of the event"""
    )

async def mock_runner_run(agent, prompt):
    """Mock Runner.run that returns appropriate MockResult based on agent."""
    # Determine which agent this is based on the prompt or agent attributes
    if "research" in prompt.lower() or "brief" in prompt.lower():
        response = """Research Brief: The Fall of the Berlin Wall

Key Points:
- The Berlin Wall stood from 1961 to 1989
- Divided East and West Berlin during the Cold War
- Symbol of the Iron Curtain between Soviet and Western blocs
- Peaceful protests and political changes led to its fall

Timeline:
- August 13, 1961: Construction begins
- November 9, 1989: Border crossing announcement
- November 10-12, 1989: Wall breached and dismantled

Sources: Historical records and Cold War documentation"""
    elif "narrative" in prompt.lower() and "style" in prompt.lower():
        response = """You are a historical storyteller specializing in dramatic political events. Create narratives that:

- Use third-person limited perspective with dramatic tension and emotional depth
- Explore themes of division, unity, freedom, and human resilience
- Develop characters through their reactions to historical forces
- Structure stories with clear scene beats and emotional arcs
- Maintain historical accuracy while focusing on human elements

Key guidelines:
- Build suspense through political uncertainty and personal stakes
- Include sensory details of crowds, sounds, and atmosphere
- Show transformation from division to unity
- End with hope and reflection on human potential"""
    elif "scene beats" in prompt.lower() or "narrative script" in prompt.lower():
        response = """It was November 9, 1989. The city of Berlin held its breath.

SCENE 1: A crowd gathers at Checkpoint Charlie as rumors spread of border changes.

For 28 years, the concrete barrier had divided families, friends, and a nation. But tonight was different.

SCENE 2: Guards at the wall look at each other uncertainly, overwhelmed by thousands approaching.

When the announcement came, it was unclear and hurried. But the people understood: the wall was opening.

SCENE 3: Hammers and picks appear. People climb the wall, celebrating together.

By dawn, the symbol of division was becoming a symbol of unity. The Berlin Wall was falling, and with it, an era was ending."""
    elif "analyze this story" in prompt.lower() or "system prompt" in prompt.lower():
        response = """You are a historical storyteller specializing in dramatic political transformations. Create narratives that:

- Use third-person dramatic perspective with building tension and emotional release
- Explore themes of division overcome, freedom achieved, and human resilience
- Develop characters through their personal reactions to world-changing events
- Structure stories with scene progression: setup, confrontation, climax, resolution
- Maintain atmospheric tension throughout with sensory details and emotional stakes

Key guidelines:
- Focus on the human element within larger historical forces
- Build emotional investment through personal stories and relationships
- Include vivid scene descriptions for visual impact
- Balance educational content with engaging narrative flow
- End with reflection on the broader implications of the event"""
    else:  # QA agent
        response = """Q: When did the Berlin Wall fall?
A: November 9, 1989

Q: How long did the Berlin Wall stand?
A: 28 years, from 1961 to 1989

Q: What caused the fall of the Berlin Wall?
A: Peaceful protests, political reforms in Eastern Europe, and mounting pressure for freedom

Q: What did the Berlin Wall symbolize?
A: The division between communist East and democratic West during the Cold War

Q: How did people react when the wall came down?
A: With celebration, joy, and emotional reunions of families separated for decades"""
    
    return MockResult(response)

@pytest.fixture
def mock_agents():
    """Fixture to patch Runner.run to return mock results."""
    with patch('agents.Runner.run', side_effect=mock_runner_run):
        yield

def test_root_endpoint():
    """Test the root health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Echoes"
    assert data["status"] == "ok"
    assert "version" in data

def test_story_endpoint(mock_agents):
    """Test /api/story endpoint with mocked agents."""
    response = client.post(
        "/api/story",
        json={"topic": "The Fall of the Berlin Wall"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check all required fields are present
    assert "topic" in data
    assert "brief" in data
    assert "story" in data
    assert "system_prompt" in data
    assert "faq" in data
    assert "audio_url" in data
    assert "video_url" in data
    
    # Verify content
    assert data["topic"] == "The Fall of the Berlin Wall"
    assert "Berlin Wall" in data["brief"]
    assert "November 9, 1989" in data["story"]
    assert isinstance(data["faq"], list)
    assert len(data["faq"]) > 0
    assert "/static/" in data["audio_url"]
    assert "/static/" in data["video_url"]

def test_chat_endpoint(mock_agents):
    """Test /api/chat endpoint with mocked QA agent."""
    response = client.post(
        "/api/chat",
        json={
            "story_context": "The Berlin Wall fell on November 9, 1989 after 28 years of division.",
            "question": "When did the wall fall?"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Check response structure
    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0

def test_story_endpoint_missing_topic():
    """Test /api/story with missing topic field."""
    response = client.post("/api/story", json={})
    assert response.status_code == 422  # Validation error

def test_chat_endpoint_missing_fields():
    """Test /api/chat with missing required fields."""
    response = client.post("/api/chat", json={"question": "test"})
    assert response.status_code == 422  # Validation error