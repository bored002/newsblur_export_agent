from agents.news_agent import create_news_agent
from dotenv import load_dotenv

load_dotenv()
agent = create_news_agent()
agent.invoke({"input": "What have I been reading about lately?"})