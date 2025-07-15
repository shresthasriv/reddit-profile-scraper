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

### 3. Configure API Key
Create a `.env` file in the project root:
```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

Get your DeepSeek API key from: https://platform.deepseek.com/

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
- DeepSeek API key
- Internet connection
