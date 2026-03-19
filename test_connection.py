import os
from dotenv import load_dotenv
from core.client import NewsBlurClient

def test_newsblur():
    print("--- 🔍 Starting NewsBlur Connection Test ---")
    
    # 1. Load .env
    if not load_dotenv():
        print("❌ Error: .env file not found!")
        return

    # 2. Check Credentials
    user = os.getenv("NEWSBLUR_USERNAME")
    if not user:
        print("❌ Error: NEWSBLUR_USERNAME is missing in .env")
        return
    print(f"✅ Credentials found for user: {user}")

    # 3. Attempt Login and Hash Fetch
    try:
        print("📡 Attempting to login and fetch story hashes...")
        client = NewsBlurClient()
        hashes = client.get_all_starred_hashes()
        
        if hashes:
            print(f"✅ Success! Found {len(hashes)} saved stories.")
            
            # 4. Attempt Detailed Fetch (First 3 stories)
            print("📑 Testing detailed content fetch for the first 3 stories...")
            sample_stories = client.fetch_story_details(hashes[:3])
            
            for i, story in enumerate(sample_stories, 1):
                print(f"   {i}. [{story.title[:40]}...] - Tags: {story.tags}")
            
            print("\n🚀 Everything is working! You are ready to run main.py.")
        else:
            print("⚠️ Login successful, but no saved stories were found in this account.")

    except Exception as e:
        print(f"❌ Connection Failed: {str(e)}")

if __name__ == "__main__":
    test_newsblur()