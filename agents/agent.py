import os
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from FlagEmbedding import FlagAutoModel
from langgraph.graph import StateGraph, END
from langchain_huggingface import HuggingFaceEmbeddings

from prompts.prompt import get_prompt, get_feedback
from loader.data import vector_database
from executor.runner import py_checker
from parser.markdown import MarkdownOutputParser
from retriever.docs import build_retrieve_node
from classes.state import CodeState
from generator.codegen import build_generate_node
from debug.refine import build_refine_node

def py_agent(query: str) -> None:
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

    DeepSeek = ChatOpenAI(api_key="123", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", base_url="http://localhost:8000/v1")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    reranker_model = FlagAutoModel("BAAI/bge-reranker-base", use_fp16=True)

    if os.path.exists("./chroma_db"):
        chroma_db = Chroma(collection_name="CodeGen", persist_directory="./chroma_db", embedding_function=embedding_model)
    else:
        chroma_db = vector_database(embedding_model, './dataset', './chroma_db')

    graph_builder = StateGraph(CodeState)

    rerank_node = build_retrieve_node(reranker_model, 10, 3)
    generate_node = build_generate_node(DeepSeek)
    refine_node = build_refine_node(DeepSeek)

    graph_builder.add_node("retrieve", rerank_node)
    graph_builder.add_node("prompt", get_prompt)
    graph_builder.add_node("generate", generate_node)
    graph_builder.add_node("check", py_checker)
    graph_builder.add_node("feedback", get_feedback)
    graph_builder.add_node("refine", refine_node)

    graph_builder.set_entry_point("retrieve")
    graph_builder.add_edge("retrieve", "prompt")
    graph_builder.add_edge("prompt", "generate")
    graph_builder.add_edge("generate", "check")
    graph_builder.add_edge("check", "feedback")
    graph_builder.add_edge("feedback", "refine")
    graph_builder.add_edge("refine", "check")

    def evaluation_decision(state: CodeState):
        if state.passed:
            return END
        elif state.rounds < 3:
            return "refine"
        else:
            return END

    graph_builder.add_conditional_edge("check", evaluation_decision)
    graph = graph_builder.compile()

    final_state = graph.invoke(initial_state)

    print("\n🚀 最终结果：")
    print("生成的代码:\n", final_state.code)
    print("是否通过评估：", final_state.passed)
