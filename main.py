import sys
import os
from src.reddit_scraper import RedditScraper
from src.data_processor import DataProcessor
from src.persona_generator import PersonaGenerator
from src.utils import save_persona_to_file

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <reddit_user_url>")
        sys.exit(1)

    url = sys.argv[1]

    try:
        scraper = RedditScraper()
        user_data = scraper.scrape_user_data(url)

        print(f"Generating persona for: {user_data['username']}")
        print(f"Found {len(user_data['posts'])} posts and "
              f"{len(user_data['comments'])} comments")

        processor = DataProcessor()
        processed_data = processor.process_user_data(user_data)

        llm_summary = processor.prepare_for_llm(processed_data)

        generator = PersonaGenerator()
        persona_data = generator.generate_persona(processed_data, llm_summary)

        if persona_data:
            formatted_persona = generator.format_persona(persona_data)

            filepath = save_persona_to_file(
                persona_data, formatted_persona, user_data['username']
            )
            print(f"Persona saved to: {filepath}")

        else:
            print("Failed to generate persona")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
