from langchain.tools import tool
from core.client import NewsBlurClient
import pandas as pd
from typing import List, Optional

# Initialize the client once to be used by all tools
nb_client = NewsBlurClient()

@tool
def fetch_all_saved_stories(limit: Optional[int] = 50) -> str:
    """
    Fetches the most recent saved (starred) stories from NewsBlur.
    Use this when the user wants to see their latest bookmarks or needs a general summary.
    'limit' specifies how many stories to retrieve (default 50).
    """
    try:
        hashes = nb_client.get_all_starred_hashes()
        # Only take the most recent 'limit' hashes to save time/tokens
        recent_hashes = hashes[:limit]
        
        stories = nb_client.fetch_story_details(recent_hashes)
        
        # Convert to a list of strings for the AI to read easily
        formatted_output = ""
        for s in stories:
            formatted_output += f"Title: {s.title}\nLink: {s.link}\nContent: {s.content[:200]}...\n---\n"
        
        return formatted_output if formatted_output else "No saved stories found."
    except Exception as e:
        return f"Error fetching stories: {str(e)}"

@tool
def search_saved_stories(query: str) -> str:
    """
    Searches through the user's saved stories for a specific keyword or topic.
    Use this when the user asks a specific question like 'What did I save about Python?'
    """
    hashes = nb_client.get_all_starred_hashes()
    # For a simple search, we fetch the last 100 and filter locally
    stories = nb_client.fetch_story_details(hashes[:100])
    
    results = [s for s in stories if query.lower() in s.title.lower() or query.lower() in s.content.lower()]
    
    if not results:
        return f"No stories found matching '{query}'."
    
    output = f"Found {len(results)} stories matching '{query}':\n"
    for r in results:
        output += f"- {r.title} ({r.link})\n"
    return output

@tool
def generate_reading_stats() -> str:
    """
    Analyzes saved stories to provide statistics on tags and sources.
    Use this when the user asks 'What are my reading habits?' or 'What tags do I use most?'
    """
    hashes = nb_client.get_all_starred_hashes()
    stories = nb_client.fetch_story_details(hashes[:100])
    
    if not stories:
        return "Not enough data to generate stats."

    # Use Pandas for quick analysis (as seen in the original repo)
    df = pd.DataFrame([{'tags': s.tags} for s in stories])
    
    # Flatten tags list and count occurrences
    all_tags = df.explode('tags')['tags'].value_counts().head(5)
    
    stats_msg = "Your top 5 most used tags are:\n"
    for tag, count in all_tags.items():
        stats_msg += f"- {tag}: {count} stories\n"
        
    return stats_msg