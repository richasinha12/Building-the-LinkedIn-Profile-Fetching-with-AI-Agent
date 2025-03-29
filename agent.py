Step--1 :- Getting the python environment ready


langchain
langchain_ollama # optional if we use free LLM API's
langchain_groq # Mandatory - we would be using free API's from groq
langchain_core
langchain_tools
langchain_community
dotenv # to manage our API Keys as environment variables
phidata # We would leverage Google search Tool from Phidata
googlesearch-python


Step — 2:- Getting the API Keys ready

TAVILY_API_KEY=*************************************************
GROQ_API_KEY=***************************************************


Step — 3:- Setting up Tool functions required for the Agent

from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv() # This function would read the .env file and creates environmental variables for all API keys present in that file

def search_profile_url_using_tavily(name):
    search = TavilySearchResults()
    return search.run(name)

from phi.tools.googlesearch import GoogleSearch

Step — 4:- Creating the agent

# All langchain imports
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults

# importing dotenv
from dotenv import load_dotenv
load_dotenv()

# Importing google search agent from Phidata
from phi.tools.googlesearch import GoogleSearch

# function that acts as Tool for our AI Agent
def search_profile_url_using_tavily(name):
    search = TavilySearchResults()
    return search.run(name)

def get_linkedin_url(name:str) -> str:
    groq_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
    template = """Given the full name {name_of_person} I want you to get me a link to their linkin profile page. Your answer should only contain the URL"""
    
    prompt_template = PromptTemplate(input_variables=["name_of_person"], template=template)
    
    tools_for_agent = [
        Tool(
            name="Crawl google for linkedin profile page",
            func=search_profile_url_using_tavily,
            description="Tool to get linkedin profile page from google"
            ),
        Tool(
            name = "Google search tool",
            func = GoogleSearch().google_search,
            description="Tool to perform a google search"
        )
        ]
    
    react_prompt = hub.pull("hwchase17/react")
    
    agent = create_react_agent(llm=groq_llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True,
                                handle_parsing_errors=True)
    
    result = agent_executor.invoke(input={"input":prompt_template.format_prompt(name_of_person=name)},
                                ) 
    return result["output"]    



