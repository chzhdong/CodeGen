from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Init the model
llm = ChatOpenAI(api_key="123", base_url="http://localhost:8000/v1", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
# print(llm.invoke("Hello, how are you?"))

# Create a prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是瓜皮，是一个专业的小丑演员。"),
    ("user", "{input}")
])
chain = prompt | llm
# print(chain.invoke({"input": "你是谁？"}))

# Get the output with output parser
output_parser = StrOutputParser()
chain = prompt | llm | output_parser
print(chain.invoke({"input": "你是谁？"}))
