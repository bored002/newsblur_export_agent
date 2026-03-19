from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub
from core.tools import fetch_all_saved_stories, search_saved_stories, generate_reading_stats

def create_news_agent():
    """
    Initializes the NewsBlur AI Agent with specific personality and tools.
    """
    # 1. Choose the Model
    # GPT-4o is recommended for complex tool-calling logic
    llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

    # 2. Define the System Prompt
    # This defines the "Soul" of your agent
    system_message = (
        "You are a sophisticated Personal Research Assistant. Your goal is to help the user "
        "manage and understand their NewsBlur 'Saved Stories'.\n\n"
        "GUIDELINES:\n"
        "- When summarizing, be concise but highlight key insights.\n"
        "- If the user asks for a 'digest', group stories by theme (e.g., Tech, Finance, Hobby).\n"
        "- Use the 'generate_reading_stats' tool to provide high-level overviews of habits.\n"
        "- If a story content is truncated, provide the link so the user can read more."
    )

    # 3. Pull the prompt template from LangChain Hub
    # We modify the base prompt to include our custom system message
    base_prompt = hub.pull("hwchase17/openai-functions-agent")
    prompt = base_prompt.partial(system_message=system_message)

    # 4. Assemble the Tools
    tools = [fetch_all_saved_stories, search_saved_stories, generate_reading_stats]

    # 5. Create the Agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    # The Executor is the runtime that manages the 'Think-Act-Observe' loop
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )