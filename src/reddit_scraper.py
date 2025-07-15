import requests
from typing import Dict
from src.utils import extract_username_from_url


class RedditScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_user_data(self, url: str) -> Dict:
        username = extract_username_from_url(url)
        api_url = f"https://www.reddit.com/user/{username}/.json?limit=100"

        response = requests.get(api_url, headers=self.headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        posts = []
        comments = []

        for item in data.get('data', {}).get('children', []):
            item_data = item.get('data', {})

            if item.get('kind') == 't3':
                posts.append({
                    'title': item_data.get('title', ''),
                    'text': item_data.get('selftext', ''),
                    'subreddit': item_data.get('subreddit', '')
                })

            elif item.get('kind') == 't1':
                comments.append({
                    'text': item_data.get('body', ''),
                    'subreddit': item_data.get('subreddit', '')
                })

        return {
            'username': username,
            'posts': posts,
            'comments': comments
        }
