import re
import pandas as pd
from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    def __init__(self):
        pass
    
    def process_user_data(self, user_data: Dict) -> Dict:
        logger.info(f"Processing data for user: {user_data['username']}")

        cleaned_posts = self._clean_posts(user_data['posts'])

        cleaned_comments = self._clean_comments(user_data['comments'])

        analytics = self._extract_analytics(cleaned_posts, cleaned_comments)
        
        return {
            'username': user_data['username'],
            'posts': cleaned_posts,
            'comments': cleaned_comments,
            'analytics': analytics,
            'raw_data': user_data
        }
    
    def _clean_posts(self, posts: List[Dict]) -> List[Dict]:
        cleaned_posts = []
        
        for post in posts:
            if not post.get('title') and not post.get('text'):
                continue
            
            cleaned_post = {
                'title': self._clean_text(post.get('title', '')),
                'text': self._clean_text(post.get('text', '')),
                'subreddit': post.get('subreddit', ''),
                'type': 'post',
                'word_count': len(post.get('text', '').split())
            }
            
            cleaned_posts.append(cleaned_post)
        
        return cleaned_posts
    
    def _clean_comments(self, comments: List[Dict]) -> List[Dict]:
        cleaned_comments = []
        
        for comment in comments:
            if not comment.get('text') or comment.get('text') in ['[deleted]', '[removed]']:
                continue
            
            cleaned_comment = {
                'text': self._clean_text(comment.get('text', '')),
                'subreddit': comment.get('subreddit', ''),
                'type': 'comment',
                'word_count': len(comment.get('text', '').split())
            }
            
            cleaned_comments.append(cleaned_comment)
        
        return cleaned_comments
    
    def _clean_text(self, text: str) -> str:
        if not text:
            return ""

        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*(.*?)\*', r'\1', text)      # Italic
        text = re.sub(r'~~(.*?)~~', r'\1', text)      # Strikethrough
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', text)  # Links

        text = re.sub(r'/u/\w+', '', text)  # Remove username mentions
        text = re.sub(r'/r/\w+', '', text)  # Remove subreddit mentions
        text = re.sub(r'&gt;.*?(?=\n|$)', '', text)  # Remove quotes

        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _extract_analytics(self, posts: List[Dict], comments: List[Dict]) -> Dict:
        all_content = posts + comments
        
        if not all_content:
            return self._empty_analytics()
        
        total_words = sum(item.get('word_count', 0) for item in all_content)
        
        subreddits = [item.get('subreddit', '') for item in all_content if item.get('subreddit')]
        subreddit_counts = pd.Series(subreddits).value_counts().to_dict()
        
        return {
            'total_posts': len(posts),
            'total_comments': len(comments),
            'total_content': len(all_content),
            'total_words': total_words,
            'avg_words_per_post': total_words / len(all_content) if all_content else 0,
            'top_subreddits': dict(list(subreddit_counts.items())[:10])
        }
    
    def _empty_analytics(self) -> Dict:
        return {
            'total_posts': 0,
            'total_comments': 0,
            'total_content': 0,
            'total_words': 0,
            'avg_words_per_post': 0,
            'top_subreddits': {}
        }
    
    def prepare_for_llm(self, processed_data: Dict) -> str:
        posts = processed_data['posts']
        comments = processed_data['comments']
        analytics = processed_data['analytics']
        
        all_texts = []
        
        for post in posts[:20]:
            if post['text'] or post['title']:
                text_entry = f"[POST in r/{post['subreddit']}] {post['title']} - {post['text']}"
                all_texts.append({
                    'text': text_entry,
                    'type': 'post',
                    'subreddit': post['subreddit']
                })
        
        for comment in comments[:30]:
            if comment['text']:
                text_entry = f"[COMMENT in r/{comment['subreddit']}] {comment['text']}"
                all_texts.append({
                    'text': text_entry,
                    'type': 'comment',
                    'subreddit': comment['subreddit']
                })
        
        summary = f"""
REDDIT USER DATA ANALYSIS FOR: {processed_data['username']}

ACTIVITY SUMMARY:
- Total Posts: {analytics['total_posts']}
- Total Comments: {analytics['total_comments']}
- Total Words: {analytics['total_words']}
- Average Words per Content: {analytics['avg_words_per_post']:.1f}

TOP SUBREDDITS:
{self._format_subreddits(analytics['top_subreddits'])}

CONTENT SAMPLES:
{self._format_content_samples(all_texts)}
"""
        
        return summary
    
    def _format_subreddits(self, subreddits: Dict) -> str:
        lines = []
        for subreddit, count in list(subreddits.items())[:5]:
            lines.append(f"- r/{subreddit}: {count} posts/comments")
        return '\n'.join(lines) if lines else "- No subreddit data available"
    
    def _format_content_samples(self, texts: List[Dict]) -> str:
        lines = []
        for i, item in enumerate(texts[:25], 1):
            lines.append(f"{i}. {item['text'][:200]}{'...' if len(item['text']) > 200 else ''}")
        return '\n'.join(lines) if lines else "No content available" 