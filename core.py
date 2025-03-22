import os
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

os.environ['LANGSMITH_TRACING']=True
os.environ['LANGSMITH_API_KEY']='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'

DeepSeek = ChatOpenAI(api_key="123", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", base_url="http://localhost:8000/v1")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

chroma_db = Chroma(collection_name="CodeGen", persist_directory="./chroma_db", embedding_function=embedding_model)
retriever = chroma_db.as_retriever(search_kwargs={"k": 3})

query = "读取 CSV 文件"
docs = retriever.invoke(query)

messages = [
    SystemMessage(content="You are a professional programmer. Generate clean Python code based on human instructions.")
]
for doc in docs:
    messages.append(HumanMessage(content=f"Instruction: {doc.page_content}"))
    messages.append(AIMessage(content=doc.metadata["code"]))
messages.append(HumanMessage(content=f"Instruction: {query}"))

try:
    for token in DeepSeek.stream(messages):
        print(token.content, end="", flush=True)
except Exception as e:
    print("❌ 出错了:", str(e))
