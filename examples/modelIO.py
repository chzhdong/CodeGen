import os
import json
from pydantic import BaseModel, Field
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.utils.function_calling import convert_to_openai_tool
from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache

# Init the model
llm = OpenAI(api_key="123", base_url="http://localhost:8000/v1", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
chat_model = ChatOpenAI(api_key="123", base_url="http://localhost:8000/v1", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")

# Init the input
# text = "我想取一个英文名，我叫瓜皮"
# llm.invoke(text)

# Run the model with human messages
# messages = [HumanMessage(content=text)]
# chat_model.invoke(messages)

# Get all template prompts for models
# template = "你是专业的翻译负责将{input_language}翻译成{output_language}。"
# human_template = "{text}"
# chat_prompt = ChatPromptTemplate.from_messages([
#     ("system", template),
#     ("user", human_template)
# ])
# chat_prompt.format_messages(input_language="English", output_language="Chinese", text="I love you.")

# prompt_template = PromptTemplate.from_template("讲一个关于{name}的笑话。")
# prompt_template.format_template(name="瓜皮")

# Create a Pydantic model for the output
# class Joke(BaseModel):
#     setup: str = Field(description="问题")
#     punchline: str = Field(description="答案")

# joke_query = "说一个脑筋急转弯。"

# parser = JsonOutputParser(pydantic_model=Joke)
# prompt = PromptTemplate(
#     template="回答问题.\n{format_instructions}\n{query}",
#     input_variables=["query"],
#     partial_variables=["format_instructions": parser.format_instructions()],
# )

# chain = prompt | llm | parser
# chain.invoke({"query": joke_query})

# Stream the output
# message = [
#     SystemMessage(content="你是瓜皮，是一个专业的小丑演员。"),
#     HumanMessage(content="你是谁？")
# ]
# for chunk in chat_model.stream(message):
#     print(chunk.content, end="", flush=True)

# Binding tools to the model
# def multiply(a: int, b: int) -> int:
#     return a * b
# print(json.dumps(convert_to_openai_tool(multiply), indent=2))
# llm_with_tools = chat_model.bind_tools([multiply])
# llm_with_tools.invoke("3 * 12")

# Set the cache
set_llm_cache(InMemoryCache())

print(llm.invoke("写一首四言绝句。"))
