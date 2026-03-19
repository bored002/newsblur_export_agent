import os
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

# 1. Define a clean Data Model for the AI
class SavedStory(BaseModel):
    id: str
    title: str
    link: str
    content: str
    feed_id: Optional[int] = None
    tags: List[str] = []

class NewsBlurClient:
    def __init__(self):
        self.base_url = "https://www.newsblur.com"
        self.session = requests.Session()
        self.username = os.getenv("NEWSBLUR_USERNAME")
        self.password = os.getenv("NEWSBLUR_PASSWORD")
        self._login()

    def _login(self):
        """Authenticates with NewsBlur and maintains a session."""
        login_url = f"{self.base_url}/api/login"
        response = self.session.post(
            login_url, 
            data={'username': self.username, 'password': self.password}
        )
        if not response.json().get('authenticated'):
            raise ConnectionError("Failed to login to NewsBlur. Check your .env file.")

    def _clean_html(self, html_content: str) -> str:
        """Strips HTML tags to save tokens for the AI Agent."""
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator=' ', strip=True)

    def get_all_starred_hashes(self) -> List[str]:
        """Step 1: Get unique IDs for all saved stories."""
        url = f"{self.base_url}/reader/starred_story_hashes"
        response = self.session.get(url)
        return response.json().get('starred_story_hashes', [])

    def fetch_story_details(self, hashes: List[str]) -> List[SavedStory]:
        """Step 2: Fetch full content in batches of 100."""
        stories = []
        # NewsBlur API allows max 100 hashes per request
        for i in range(0, len(hashes), 100):
            batch = hashes[i : i + 100]
            url = f"{self.base_url}/reader/river_stories"
            params = {'h': batch}
            response = self.session.get(url, params=params)
            
            raw_stories = response.json().get('stories', [])
            for s in raw_stories:
                stories.append(SavedStory(
                    id=s.get('story_hash'),
                    title=s.get('story_title', 'No Title'),
                    link=s.get('story_permalink'),
                    # Clean the content so the AI doesn't see <div> tags
                    content=self._clean_html(s.get('story_content', '')),
                    tags=s.get('story_tags', [])
                ))
        return stories
