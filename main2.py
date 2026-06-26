from openai.types import model
import truststore
import os
import truststore
#  must be called before making HTTPS requests

truststore.inject_into_ssl()


from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()


def main():
    print("Hello from langchain-course!")
    information:""" 
    Elon Reve Musk (born June 28, 1971) 
    is businessman, known for his leadership of Tesla, SpaceX, X (formerly Twitter), and xAI.
    He has also co-founded OpenAI and several other companies.
    """

    summary_template = """
    Given the following information about a person:

    {information}

    Please provide:
    1. A short summary
    2. Two interesting facts
    """

    prompt= PromptTemplate(
        input_variables=["information"],
        template=summary_template
    )

    llm=ChatOpenAI(
        model="openai/gbt-4.1-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
        max_tokens=300
        
    )

    chain=prompt|llm

