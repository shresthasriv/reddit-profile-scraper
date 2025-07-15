import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.reddit_scraper import RedditScraper
from src.data_processor import DataProcessor
from src.persona_generator import PersonaGenerator
from src.utils import extract_username_from_url, save_persona_to_file


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <reddit_user_url>")
        print("Example: python main.py https://www.reddit.com/user/kojied/")
        return 1
    
    url = sys.argv[1]
    
    try:
        username = extract_username_from_url(url)
        print(f"Generating persona for: {username}")

        scraper = RedditScraper()
        user_data = scraper.scrape_user_data(url)
        
        if not user_data['posts'] and not user_data['comments']:
            print("No data found for this user")
            return 1
        
        print(f"Found {len(user_data['posts'])} posts and {len(user_data['comments'])} comments")
        
        processor = DataProcessor()
        processed_data = processor.process_user_data(user_data)
        llm_summary = processor.prepare_for_llm(processed_data)
        
        generator = PersonaGenerator()
        persona_data = generator.generate_persona(processed_data, llm_summary)
        formatted_persona = generator.format_persona(persona_data)
        
        output_file = save_persona_to_file(persona_data, formatted_persona, username)
        print(f"Persona saved to: {output_file}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 