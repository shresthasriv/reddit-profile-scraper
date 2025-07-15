import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'deepseek').lower()

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_BASE_URL = 'https://api.deepseek.com'
DEEPSEEK_MODEL = 'deepseek-chat'

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = 'gpt-4o'

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
ANTHROPIC_MODEL = 'claude-3-5-sonnet'

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = 'gemini-2.5-flash'

OUTPUT_DIR = 'outputs'
PERSONA_TEMPLATE = """
USER PERSONA ANALYSIS

=== BASIC INFORMATION ===
Age Range: {age_range}
Location: {location}
Occupation/Field: {occupation}

=== PERSONALITY TRAITS ===
{personality_traits}

=== INTERESTS & HOBBIES ===
{interests}

=== COMMUNICATION STYLE ===
{communication_style}

=== VALUES & BELIEFS ===
{values}

=== BEHAVIORAL PATTERNS ===
{behavior_patterns}

=== GOALS & MOTIVATIONS ===
{goals}

=== CITATIONS ===
{citations}
"""
