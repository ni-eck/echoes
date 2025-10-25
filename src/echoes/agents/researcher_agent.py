"""Researcher agent for gathering historical facts."""

import os
from pathlib import Path
from agents import Agent

def _load_prompt(filename: str) -> str:
    """Load prompt template from prompts directory."""
    prompts_dir = Path(__file__).parent.parent / "prompts"
    prompt_path = prompts_dir / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def build_researcher_agent(model: str) -> Agent:
    """
    Build a Researcher Agent that gathers verified historical facts.
    
    Args:
        model: OpenAI model name (e.g., "gpt-4o")
    
    Returns:
        Agent configured for historical research
    """
    system_prompt = _load_prompt("researcher.md")
    
    # Try to enable web_search tool if available
    tools = []  # No tools for now
    # try:
    #     tools = ["web_search"]
    # except Exception:
    #     # Gracefully fall back to no tools if web_search is unavailable
    #     pass
    
    agent = Agent(
        name="Researcher",
        model=model,
        instructions=system_prompt,
        tools=tools,
    )
    
    return agent