import os
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from prompts.prompt import get_prompt, get_feedback
from loader.data import vector_database
from executor.runner import py_checker
from parser.markdown import MarkdownOutputParser

def py_agent(query: str) -> None:
    DeepSeek = ChatOpenAI(api_key="123", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", base_url="http://localhost:8000/v1")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if os.path.exists("./chroma_db"):
        chroma_db = Chroma(collection_name="CodeGen", persist_directory="./chroma_db", embedding_function=embedding_model)
    else:
        chroma_db = vector_database(embedding_model, './dataset', './chroma_db')

    retriever = chroma_db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)

    prompt = get_prompt(docs, query)
    parser = MarkdownOutputParser()
    ok = False

    while (not ok):
        output = DeepSeek.invoke(prompt)
        code = parser.parse(output)

        ok, msg = py_checker(code)
        print(ok, "\n", msg)
        prompt = get_feedback(docs, query, code, msg)

    print("Generated Code for instruction: \n", code)
