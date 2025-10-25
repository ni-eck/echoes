"""Director agent to coordinate other agents."""

from pathlib import Path
from agents import Agent
from typing import Optional

def build_director_agent(model: str) -> Agent:
    """
    Build a Director Agent that coordinates other agents (optional).
    
    This agent can orchestrate complex multi-agent workflows by delegating
    tasks to specialized agents and synthesizing their outputs.
    
    Args:
        model: OpenAI model name (e.g., "gpt-4o")
    
    Returns:
        Agent configured for coordination
    
    Example:
        director = build_director_agent("gpt-4o")
        result = director.coordinate_research_and_storytelling(topic="WWII")
    """
    agent = Agent(
        name="Director",
        model=model,
        instructions="""You are a Director Agent that coordinates multiple specialized agents.
        Your role is to:
        1. Break down complex requests into subtasks
        2. Delegate to appropriate specialist agents
        3. Synthesize results into coherent outputs
        4. Ensure quality and consistency across agent outputs""",
        tools=[],
    )
    
    return agent

class DirectorCoordinator:
    """
    Optional coordinator class for future complex orchestration.
    
    This can be extended to manage stateful multi-agent conversations
    and more sophisticated delegation patterns.
    """
    
    def __init__(self, model: str):
        self.director = build_director_agent(model)
        self.model = model
    
    def coordinate_agents(self, task: str, agents: list) -> str:
        """
        Coordinate multiple agents to complete a complex task.
        
        Args:
            task: The task description
            agents: List of agent builders to coordinate
        
        Returns:
            Synthesized result from all agents
        """
        # Future implementation: orchestrate agents based on director's plan
        return f"Director coordinating task: {task}"