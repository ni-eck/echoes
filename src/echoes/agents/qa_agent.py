"""QA agent for questions and answers."""

from pathlib import Path
from agents import Agent

def _load_prompt(filename: str) -> str:
    """Load prompt template from prompts directory."""
    prompts_dir = Path(__file__).parent.parent / "prompts"
    prompt_path = prompts_dir / filename
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def build_qa_agent(model: str) -> Agent:
    """
    Build a QA Agent that generates questions and answers.
    
    Args:
        model: OpenAI model name (e.g., "gpt-4o")
    
    Returns:
        Agent configured for Q&A generation
    """
    system_prompt = _load_prompt("qa.md")
    
    agent = Agent(
        name="QA",
        model=model,
        instructions=system_prompt,
        tools=[],
    )
    
    return agent