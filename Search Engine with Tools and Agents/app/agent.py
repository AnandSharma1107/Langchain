from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun,DuckDuckGoSearchRun
from langchain.agents import initialize_agent,AgentType
from dotenv import load_dotenv
from langchain_groq import ChatGroq

def get_tools():
    ## Arxiv, wikipedia wrapper and tools
    arxiv_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)
    arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)

    api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)
    wiki=WikipediaQueryRun(api_wrapper=api_wrapper)

    # Using DuckDuckGo for searching the queries
    search=DuckDuckGoSearchRun(name="Search")

    return [search, arxiv, wiki]

def create_agent(api_key : str):
    llm=ChatGroq(groq_api_key=api_key,model_name="meta-llama/llama-4-scout-17b-16e-instruct",streaming=True)
    tools=get_tools()
    search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)
    return search_agent