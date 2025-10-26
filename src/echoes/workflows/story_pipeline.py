"""Workflow for the story generation pipeline."""

import asyncio
from agents import Runner
from ..agents.researcher_agent import build_researcher_agent
from ..agents.storyteller_agent import build_storyteller_agent
from ..agents.qa_agent import build_qa_agent
from ..agents.narrative_styler_agent import build_narrative_styler_agent
from ..agents.story_analyzer_agent import build_story_analyzer_agent
from ..services.tts_service import synthesize_voice
from ..services.video_service import generate_video_from_script

async def generate_story_experience(topic: str, model: str) -> dict:
    """
    Generate a complete story experience from a historical topic.
    
    This orchestrates the multi-agent pipeline:
    1. Research brief (facts, timeline, citations)
    2. Narrative Style Guide (dynamic system prompt creation)
    3. Story narrative (60-120s script with scene beats)
    4. Story Analysis (generate system prompt from completed story)
    5. FAQ list (5 Q&As)
    6. Audio URL (TTS synthesis)
    7. Video URL (video generation)
    
    Args:
        topic: Historical topic to explore
        model: OpenAI model name (e.g., "gpt-4o")
    
    Returns:
        Dictionary with keys: topic, brief, story, system_prompt, faq, audio_url, video_url
    """
    # Step 1: Research Agent - Gather factual information
    researcher = build_researcher_agent(model)
    research_prompt = f"""Topic: {topic}

Return a factual brief with:
- 3-5 key bullet points about this topic
- A short timeline of major events
- Brief citations or sources (can be general historical knowledge)

Format as a structured brief."""
    
    research = str((await Runner.run(researcher, research_prompt)).final_output)
    
    # Step 2: Narrative Styler Agent - Create dynamic system prompt
    styler = build_narrative_styler_agent(model)
    style_prompt = f"""Topic: {topic}

Analyze this historical topic and create a dynamic system prompt for storytelling.
Consider the optimal narrative perspective and style for this specific topic."""

    dynamic_system_prompt = str((await Runner.run(styler, style_prompt)).final_output)
    
    # Step 3: Storyteller Agent - Create engaging narrative using dynamic prompt
    storyteller = build_storyteller_agent(model)
    story_prompt = f"""{dynamic_system_prompt}

Brief:
{research}
---
Create a 60-120 second narrative script with scene beats.
Make it engaging, educational, and appropriate for all ages.
Include visual scene descriptions for animation."""
    
    story = str((await Runner.run(storyteller, story_prompt)).final_output)
    
    # Step 4.5: Story Analyzer Agent - Generate system prompt from completed story
    analyzer = build_story_analyzer_agent(model)
    analysis_prompt = f"""Completed Story:
{story}
---
Analyze this story and generate a comprehensive system prompt that captures its narrative style, themes, and structure. This prompt should enable creating similar stories or continuing this narrative."""
    
    system_prompt = str((await Runner.run(analyzer, analysis_prompt)).final_output)
    
    # Step 5: QA Agent - Generate FAQ
    qa = build_qa_agent(model)
    faq_prompt = f"""Story:
{story}
---
Return 5 likely follow-up questions with concise answers as a plain list.
Format: One Q&A per line, like:
Q: [question]
A: [answer]"""
    
    faq_raw = (await Runner.run(qa, faq_prompt)).final_output
    
    # Normalize FAQ into a list of strings
    faq_lines = str(faq_raw).splitlines()
    faq_list = [line.strip("- • ").strip() for line in faq_lines if line.strip()]
    
    # Step 6: Generate Audio (TTS)
    audio_url = synthesize_voice(story, topic)
    
    # Step 7: Generate Video
    video_url = generate_video_from_script(story)
    
    return {
        "topic": topic,
        "brief": research,
        "story": story,
        "system_prompt": system_prompt,
        "faq": faq_list,
        "audio_url": audio_url,
        "video_url": video_url,
    }