#!/usr/bin/env python3
"""Simple CLI to generate historical stories with AI."""

import sys
import os
import asyncio

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from echoes.workflows.story_pipeline import generate_story_experience
from echoes.app.settings import MODEL
import json

def print_separator():
    """Print a nice separator line."""
    print("=" * 80)

def print_section(title):
    """Print a section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print('='*80)

def main():
    """Main function to run the story generator."""
    print_separator()
    print("🎭 ECHOES - AI Historical Story Generator")
    print_separator()
    print()
    
    # Get user input
    topic = input("📚 Enter a historical topic: ").strip()
    
    if not topic:
        print("❌ Error: Please enter a topic!")
        return
    
    print(f"\n🤖 Generating story about '{topic}' using {MODEL}...")
    print("⏳ This will take a moment as we call OpenAI API...\n")
    
    try:
        # Generate the story
        result = asyncio.run(generate_story_experience(topic, MODEL))
        
        # Display the results
        print_section("📋 RESEARCH BRIEF")
        print(result['brief'])
        
        print_section("📖 STORY")
        print(result['story'])
        
        print_section("❓ FREQUENTLY ASKED QUESTIONS")
        for i, qa in enumerate(result['faq'], 1):
            print(f"{i}. {qa}")
        
        print_section("🔗 MEDIA")
        print(f"🎵 Audio: {result['audio_url']}")
        print(f"🎬 Video: {result['video_url']}")
        
        print_separator()
        print("✅ Story generation complete!")
        print_separator()
        
        # Ask if user wants to save
        save = input("\n💾 Save story to file? (y/n): ").strip().lower()
        if save == 'y':
            filename = f"story_{topic.replace(' ', '_').lower()}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved to {filename}")
        
    except Exception as e:
        print(f"\n❌ Error generating story: {str(e)}")
        print("\n💡 Make sure:")
        print("   1. Your .env file has OPENAI_API_KEY set")
        print("   2. You have an active internet connection")
        print("   3. Your OpenAI API key is valid")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
        exit(0)
