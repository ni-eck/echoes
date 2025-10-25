"""Tests for story pipeline."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# Import the FastAPI app
from echoes.app.main import app

client = TestClient(app)

# Mock agent response class
class MockAgent:
    """Mock Agent that returns deterministic responses."""
    
    def __init__(self, response: str):
        self.response = response
    
    async def run(self, prompt: str) -> str:
        """Return mock response."""
        return self.response

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

@pytest.fixture
def mock_agents():
    """Fixture to patch all agent builders."""
    with patch('echoes.workflows.story_pipeline.build_researcher_agent', mock_researcher_agent), \
         patch('echoes.workflows.story_pipeline.build_storyteller_agent', mock_storyteller_agent), \
         patch('echoes.workflows.story_pipeline.build_qa_agent', mock_qa_agent), \
         patch('echoes.app.routers.chat.build_qa_agent', mock_qa_agent):
        yield

def test_root_endpoint():
    """Test the root health check endpoint."""
    response = client.get("/")
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