import openai
import json
import logging
from typing import Dict, List
import google.generativeai as genai
import anthropic
from config.config import (LLM_PROVIDER, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL,
                           DEEPSEEK_MODEL, OPENAI_API_KEY, OPENAI_MODEL,
                           ANTHROPIC_API_KEY, ANTHROPIC_MODEL,
                           GEMINI_API_KEY, GEMINI_MODEL, PERSONA_TEMPLATE)

logger = logging.getLogger(__name__)


class PersonaGenerator:

    def __init__(self):
        self.client = None
        self.provider = LLM_PROVIDER
        self._initialize_llm()

    def _initialize_llm(self):
        if self.provider == 'openai':
            self._initialize_openai()
        elif self.provider == 'anthropic':
            self._initialize_anthropic()
        elif self.provider == 'gemini':
            self._initialize_gemini()
        else:
            self._initialize_deepseek()

    def _initialize_openai(self):
        if not OPENAI_API_KEY:
            logger.error("OpenAI API key not found. Please set "
                         "OPENAI_API_KEY environment variable.")
            return

        try:
            self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")

    def _initialize_anthropic(self):
        if not ANTHROPIC_API_KEY:
            logger.error("Anthropic API key not found. Please set "
                         "ANTHROPIC_API_KEY environment variable.")
            return

        try:
            self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            logger.info("Anthropic client initialized successfully")
        except ImportError:
            logger.error("Anthropic library not installed. "
                         "Run: pip install anthropic")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")

    def _initialize_gemini(self):
        if not GEMINI_API_KEY:
            logger.error("Gemini API key not found. Please set "
                         "GEMINI_API_KEY environment variable.")
            return

        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.client = genai.GenerativeModel(GEMINI_MODEL)
            logger.info("Gemini client initialized successfully")
        except ImportError:
            logger.error("Google Generative AI library not installed. "
                         "Run: pip install google-generativeai")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")

    def _initialize_deepseek(self):
        if not DEEPSEEK_API_KEY:
            logger.error("DeepSeek API key not found. Please set "
                         "DEEPSEEK_API_KEY environment variable.")
            return

        try:
            self.client = openai.OpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url=DEEPSEEK_BASE_URL
            )
            logger.info("DeepSeek client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize DeepSeek client: {e}")

    def generate_persona(self, processed_data: Dict, llm_summary: str) -> Dict:
        logger.info(f"Generating persona for user: {processed_data['username']}")

        try:
            prompt = self._create_persona_prompt(llm_summary, processed_data)

            if self.provider == 'anthropic':
                response_text = self._call_anthropic(prompt)
            elif self.provider == 'gemini':
                response_text = self._call_gemini(prompt)
            else:
                response_text = self._call_openai_compatible(prompt)

            return self._parse_persona_response(response_text, processed_data)

        except Exception as e:
            logger.error(f"{self.provider.title()} failed: {e}")

    def _call_openai_compatible(self, prompt: str) -> str:
        model = OPENAI_MODEL if self.provider == 'openai' else DEEPSEEK_MODEL

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": self._get_system_prompt()
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000,
            stream=False
        )

        return response.choices[0].message.content

    def _call_anthropic(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=2000,
            temperature=0.7,
            system=self._get_system_prompt(),
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text

    def _call_gemini(self, prompt: str) -> str:
        full_prompt = f"{self._get_system_prompt()}\n\n{prompt}"

        response = self.client.generate_content(
            full_prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 2000,
            }
        )

        return response.text

    def _get_system_prompt(self) -> str:
        return """You are an expert user researcher and psychologist """ \
               """specializing in digital behavior analysis.
        Your task is to create detailed user personas based on Reddit activity data.

        Analyze the provided Reddit posts and comments to extract insights about:
        1. Demographics (age range, location hints, occupation/field)
        2. Personality traits (Big Five personality dimensions, """ \
               """communication style)
        3. Interests and hobbies
        4. Values and beliefs
        5. Behavioral patterns
        6. Goals and motivations

        For each characteristic you identify, provide specific citations to """ \
               """the posts or comments that support your analysis.
        Be objective and evidence-based in your analysis. If certain """ \
               """information cannot be determined from the data, state that clearly.

        Format your response as a structured json analysis that can be """ \
               """easily parsed."""

    def _create_persona_prompt(self, llm_summary: str,
                               processed_data: Dict) -> str:
        return f"""
        Please analyze the following Reddit user data and create a """ \
               f"""comprehensive user persona.

        {llm_summary}

        Return your analysis as a JSON object with this exact structure:
        {{
            "age_range": "estimated age range with reasoning",
            "location": "any location hints found or 'Unknown'",
            "occupation": "profession or field of interest or 'Unknown'",
            "personality_traits": "key personality characteristics """ \
               f"""with explanations",
            "interests": "main interests, hobbies, and topics of engagement",
            "communication_style": "description of how they communicate online",
            "values": "core values and belief systems",
            "behavior_patterns": "posting habits, engagement patterns, etc",
            "goals": "what drives this user's online behavior",
            "citations": [
                {{
                    "characteristic": "what this supports",
                    "type": "post or comment",
                    "subreddit": "subreddit name",
                    "quote": "brief quote from their content"
                }}
            ]
        }}

        Only include information that can be supported by the provided data.
        If something cannot be determined, use """ \
               f""""Unable to determine from available data".

        IMPORTANT: Return only valid JSON, no additional text or formatting.
        """

    def _parse_persona_response(self, persona_text: str,
                                processed_data: Dict) -> Dict:
        try:
            response_text = persona_text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]

            response_text = response_text.strip()

            persona_data = json.loads(response_text)

            return {
                'username': processed_data['username'],
                'age_range': persona_data.get('age_range', 'Unknown'),
                'location': persona_data.get('location', 'Unknown'),
                'occupation': persona_data.get('occupation', 'Unknown'),
                'personality_traits': persona_data.get(
                    'personality_traits', 'Unable to determine'),
                'interests': persona_data.get(
                    'interests', 'Unable to determine'),
                'communication_style': persona_data.get(
                    'communication_style', 'Unable to determine'),
                'values': persona_data.get('values', 'Unable to determine'),
                'behavior_patterns': persona_data.get(
                    'behavior_patterns', 'Unable to determine'),
                'goals': persona_data.get('goals', 'Unable to determine'),
                'citations': persona_data.get('citations', []),
                'raw_analysis': persona_text,
                'analytics': processed_data['analytics']
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Raw response: {persona_text}")

    def format_persona(self, persona_data: Dict) -> str:

        citations_text = self._format_citations(persona_data['citations'])

        formatted_persona = PERSONA_TEMPLATE.format(
            age_range=persona_data['age_range'],
            location=persona_data['location'],
            occupation=persona_data['occupation'],
            personality_traits=persona_data['personality_traits'],
            interests=persona_data['interests'],
            communication_style=persona_data['communication_style'],
            values=persona_data['values'],
            behavior_patterns=persona_data['behavior_patterns'],
            goals=persona_data['goals'],
            citations=citations_text
        )

        analytics = persona_data['analytics']
        top_subreddits = ', '.join(list(analytics['top_subreddits'].keys())[:5])
        analytics_summary = f"""
=== ACTIVITY STATISTICS ===
Total Posts: {analytics['total_posts']}
Total Comments: {analytics['total_comments']}
Total Words: {analytics['total_words']}
Average Words per Content: {analytics['avg_words_per_post']:.1f}
Top Subreddits: {top_subreddits}
"""

        return formatted_persona + analytics_summary

    def _format_citations(self, citations: List[Dict]) -> str:
        if not citations:
            return "No specific citations available."

        formatted_citations = []
        for i, citation in enumerate(citations, 1):
            if isinstance(citation, dict):
                characteristic = citation.get('characteristic', 'General')
                cite_type = citation.get('type', 'unknown').upper()
                subreddit = citation.get('subreddit', 'unknown')
                quote = citation.get('quote', 'No quote available')

                citation_text = (f"{i}. [{characteristic}] - {cite_type} "
                                 f"in r/{subreddit}: \"{quote}\"")
            else:
                citation_text = f"{i}. {citation}"

            formatted_citations.append(citation_text)

        return '\n'.join(formatted_citations)
