import os
from langchain.llms import OpenAI
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def ask_with_search(prompt):
    search = GoogleSerperAPIWrapper()
    llm = OpenAI(temperature=0)
    search = GoogleSerperAPIWrapper()
    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="useful for when you need to ask with search"
        )
    ]

    self_ask_with_search = initialize_agent(tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)
    result = self_ask_with_search.run(prompt)
    return result
    
ask_with_search("")