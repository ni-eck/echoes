"""Storyteller agent for creating narratives."""

from pathlib import Path
from agents import Agent

def _load_prompt(filename: str) -> str:
    """Load prompt template from prompts directory."""
    prompts_dir = Path(__file__).parent.parent / "prompts"
    prompt_path = prompts_dir / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def build_storyteller_agent(model: str) -> Agent:
    """
    Build a Storyteller Agent that transforms facts into engaging narratives.
    
    Args:
        model: OpenAI model name (e.g., "gpt-4o")
    
    Returns:
        Agent configured for storytelling
    """
    system_prompt = _load_prompt("storyteller.md")
    
    agent = Agent(
        name="Storyteller",
        model=model,
        instructions=system_prompt,
        tools=[],
    )
    
    return agent