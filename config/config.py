import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '')
DEEPSEEK_BASE_URL = 'https://api.deepseek.com'
DEEPSEEK_MODEL = 'deepseek-chat'

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
