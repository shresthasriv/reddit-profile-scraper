# Reddit User Persona Generator

A Python tool that generates detailed user personas from Reddit profiles using AI analysis.

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/shresthasriv/reddit-profile-scraper.git
```

### 2. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure API Keys
Create a `.env` file in the project root with your preferred LLM provider:

#### Option 1: DeepSeek (Default)
```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

#### Option 2: OpenAI
```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
```

#### Option 3: Anthropic
```bash
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

#### Option 4: Google Gemini
```bash
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
```

### API Key Sources
- DeepSeek: https://platform.deepseek.com/
- OpenAI: https://platform.openai.com/
- Anthropic: https://console.anthropic.com/
- Google Gemini: https://aistudio.google.com/

## Execution

### Generate Persona for a Reddit User
```bash
python main.py <reddit_username>
```

### Example
```bash
python main.py kojied
```

## Output

The tool will:
1. Fetch the user's 100 Reddit posts and comments
2. Process and analyze the content using LLM
3. Generate a detailed user persona
4. Save the results to `outputs/<username>_persona.txt`

## Generated Persona Includes

- Age range and location estimates
- Occupation/field of interest
- Personality traits and communication style
- Interests and hobbies
- Values and behavioral patterns
- Goals and motivations
- Supporting citations from their content
- Activity statistics

## Requirements

- Python 3.7+
- API key for one of: DeepSeek, OpenAI, Anthropic, or Google Gemini
- Internet connection
