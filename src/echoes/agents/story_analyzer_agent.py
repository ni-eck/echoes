"""Story Analyzer Agent builder."""

from pathlib import Path
from agents import Agent

def _load_prompt(filename: str) -> str:
    """Load prompt from markdown file."""
    prompts_dir = Path(__file__).parent.parent / "prompts"
    return (prompts_dir / filename).read_text(encoding="utf-8")

def build_story_analyzer_agent(model: str) -> Agent:
    """
    Build the story analyzer agent that creates system prompts from completed stories.

    Args:
        model: OpenAI model name

    Returns:
        Configured Agent instance
    """
    return Agent(
        name="Story Analyzer Agent",
        model=model,
        instructions=_load_prompt("story_analyzer.md"),
    )