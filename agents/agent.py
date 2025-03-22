import os
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from FlagEmbedding import FlagReranker
from langgraph.graph import StateGraph, END
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatZhipuAI

from states.state import CodeState
from RAG.indexing import build_database
from RAG.retrieve import build_retrieve_node
from RAG.augment import build_prompt, build_feedback
from tools.interpreter import interpret
from agents.infer import build_generate_node
from agents.rectify import build_correct_node

def evaluation(state: CodeState):
        if state['passed']:
            return END
        elif state['rounds'] < 3:
            return "return"
        else:
            return END

def core(query: str) -> None:
    initial_state = {
        "query": f"{query}",
        "docs": [],
        "code": "",
        "passed": False,
        "error": "",
        "prompt": [],
        "feedback": [],
        "rounds": 0
    }

    llm_model = ChatZhipuAI(
        temperature=0.5,
        api_key="ceeea9054cb94631b53e5831f6d55e7a.b9ZhGmJ3K5JWm5lW",
        model="glm-4"
    )

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    reranker_model = FlagReranker(
        "BAAI/bge-reranker-base", 
        use_fp16=True
    )

    if os.path.exists("./chroma_db"):
        chroma_db = Chroma(collection_name="CodeGen", persist_directory="./chroma_db", embedding_function=embedding_model)
    else:
        chroma_db = build_database(embedding_model, './dataset', './chroma_db')

    graph_builder = StateGraph(CodeState)
    rerank_node = build_retrieve_node(reranker_model, chroma_db, 10, 3)
    infer_node = build_generate_node(llm_model)
    correct_node = build_correct_node(llm_model)

    graph_builder.add_node("retrieve", rerank_node)
    graph_builder.add_node("augment", build_prompt)
    graph_builder.add_node("inference", infer_node)
    graph_builder.add_node("evaluate", interpret)
    graph_builder.add_node("return", build_feedback)
    graph_builder.add_node("rectify", correct_node)

    graph_builder.set_entry_point("retrieve")
    graph_builder.add_edge("retrieve", "augment")
    graph_builder.add_edge("augment", "inference")
    graph_builder.add_edge("inference", "evaluate")
    graph_builder.add_edge("evaluate", "return")
    graph_builder.add_edge("return", "rectify")
    graph_builder.add_edge("rectify", "evaluate")
    graph_builder.add_conditional_edges("evaluate", evaluation)
    graph = graph_builder.compile()

    final_state = graph.invoke(initial_state)

    print("生成的代码:\n", final_state['code'])
    print("是否通过评估：", final_state['passed'])

# llm_model = ChatOpenAI(
    #     api_key="123", 
    #     model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", 
    #     base_url="http://localhost:8000/v1"
    # )
