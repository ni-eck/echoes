"""Narrative Style Guide Agent builder."""

from pathlib import Path
from agents import Agent

def _load_prompt(filename: str) -> str:
    """Load prompt from markdown file."""
    prompts_dir = Path(__file__).parent.parent / "prompts"
    return (prompts_dir / filename).read_text(encoding="utf-8")

def build_narrative_styler_agent(model: str) -> Agent:
    """
    Build the narrative styler agent that creates dynamic system prompts.

    Args:
        model: OpenAI model name

    Returns:
        Configured Agent instance
    """
    return Agent(
        name="Narrative Style Guide Agent",
        model=model,
        instructions=_load_prompt("narrative_styler.md"),
    )