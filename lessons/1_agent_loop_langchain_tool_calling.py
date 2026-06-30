from langsmith import traceable
import os
from langchain_core.language_models import BaseChatModel
from dotenv import load_dotenv
import truststore

# Must be called before making HTTPS requests
load_dotenv()
truststore.inject_into_ssl()
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage,SystemMessage,ToolMessage

''' init_chat_model(
    # model: str | None = None,
    # *,
    # model_provider: str | None = None,
    # configurable_fields: Literal['any'] | list[str] | tuple[str, ...] | None = None,
    # config_prefix: str | None = None,
    # **kwargs: Any = {}
    # ) -> BaseChatModel | _ConfigurableModel'''

MAX_ITERATION = 10
MODEL="openai/gpt-5.1-nano"

@tool
def get_product_price(product_name:str)->float:
    """Get the price of a product by name"""
    print(f">>Executing get_product_price(product='{product_name}')")
    prices={
        "Laptop":1200,
        "Mouse":25,
        "Keyboard":75,
    }
    return prices.get(product_name,0)

@tool 
def apply_discount(price:float,discount_tier:str)->float:
    """Apply discount to a price based on the discount tier"""
    
    print(f">>Executing apply_discount(price={price},discount_tier='{discount_tier}')")
    discounts={
        "regular":0.0,
        "silver":0.10,
        "gold":0.15,
        "platinum":0.20,
    }
    discount_rate=discounts.get(discount_tier,0.0)
    return price*(1-discount_rate) 

#  ---  Tools (Langchain @tool decorator)


@traceable(name="LangChain Agent Loop ")
def run_agent(question:str):
    """Run the agent with a question and print the result"""
    tools=[get_product_price,apply_discount] 
    tools_dict={t.name:t for t in tools}
    
    llm=init_chat_model(
        
        model_provider="openai",
        model="openai/gpt-4.1-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
        max_tokens=300,
    #     model=MODEL, 
    #     temperature=0.2, 
    #     # max_tokens=1000,  # Optional, let the model decide
    #     # top_p=0.9,  # Optional, let the model decide
    #     # presence_penalty=0.5,  # Optional, let the model decide
    #     # frequency_penalty=0.5,  # Optional, let the model decide
    #     tools=tools 
    )
    llm_with_tools=llm.bind_tools(tools) 
    print(f"Question:{question}\n")
    print("="*60)

    messages=[
    SystemMessage(
        content=[
            "You are a helpful shopping assistant",
            "You have access to a product catalog tool",
            "and a discount tool .\n\n",
            "STRICT RULES-You must follow these exactly:\n",
            "1. NEVER guess or assume any product price."
            "YOU MUST call get_product_price first to get the real price .\n"
            "2. Ony call apply_discount after you have received  a price from  "
            "get_product_price tool pass the exact price"
            " returned by get_product_price - do NOT pass a made-up number "
            "3. Never calculate  discounts yourself using math,ALWAYS use the apply_discount tool \n"
            "4. if the user does not specify  a discount tier "
            "ask them which tier to use - do Not assume one. "
        ]
      
    ),
    HumanMessage(content=question)
    ]
    
    for iteration in range(MAX_ITERATION+1):
        print(f"ITERATION {iteration + 1}".center(60,"="))
        ai_message=llm_with_tools.invoke(messages)
        tool_calls=ai_message.tool_calls
        
        if not tool_calls:
            print(f"\nFinal Answer:{ai_message.content}")
            return ai_message.content
        # process only the FIRST  tool call - force one tool per iteration 
        tool_call= tool_calls[0]
        tool_name=tool_call.get("name")
        tool_args=tool_call.get("args",{})
        tool_call_id=tool_call.get("id")
        print(f" [Tool Selected {tool_name} with args:{tool_args} ]")
        tool_to_use=tools_dict.get(tool_name)
        if tool_to_use is None:

            raise ValueError(f" Tool '{tool_name}' not found in tools dict" )
        obeservation=tool_to_use.invoke(tool_args)

        print(f"[Tool Response : {obeservation}")
        
        messages.append(ai_message)
        messages.append(ToolMessage(content=str(obeservation),tool_call_id=tool_call_id))
  

# write the main funcion
if __name__ == "__main__":
    print("Hello LangChain Agent (.bind_tools)!")
    print()
    result = run_agent("What is the price of a Keyboard after applying a gold discount?")