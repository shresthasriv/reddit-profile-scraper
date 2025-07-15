import os
from datetime import datetime
from typing import Dict
from config.config import OUTPUT_DIR


def extract_username_from_url(url: str) -> str:
    url = url.rstrip('/')

    if '/user/' in url:
        return url.split('/user/')[-1].split('/')[0]
    else:
        raise ValueError("Invalid Reddit user URL format")


def save_persona_to_file(persona_data: Dict, formatted_persona: str,
                         username: str) -> str:
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{username}_persona_{timestamp}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("REDDIT USER PERSONA ANALYSIS\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Username: {username}\n")
        f.write("=" * 80 + "\n\n")
        f.write(formatted_persona)

    return filepath
