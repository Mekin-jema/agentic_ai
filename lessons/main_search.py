from dotenv import load_dotenv
import os
import truststore

# Must be called before making HTTPS requests
load_dotenv()
truststore.inject_into_ssl()


from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import  ChatOpenAI
from tavily import TavilyClient

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search(query:str)->str:
    """
    Tool that searches over internet
    Args:
        query:The query to search for 
    Returns:
        The result of the search
    """
    print(f"Searching for {query}")
    return tavily.search(query=query)
llm=ChatOpenAI(
        model="openai/gpt-4.1-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
        max_tokens=300,
)
tools=[search]
agent=create_agent( model=llm,tools=tools
    
)


def main():
    print("Hello from langchain-course!")


    result = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content="""
                Search LinkedIn for the top AI Engineering job openings.
                Focus on roles such as:
                - AI Engineer
                - Generative AI Engineer
                - LLM Engineer
                - Machine Learning Engineer
                - Agentic AI Engineer
                - AI Platform Engineer

                Return the top 10 jobs with:
                1. Job title
                2. Company
                3. Location
                4. Experience level
                5. Brief job description
                6. Job URL
                """
            )
        ]
    }
)
    print(result)

if __name__ == "__main__":
    main()