from states.state import CodeState

def build_retrieve_node(reranker_model, chroma_db, k = 10, n = 3):
    def retrieve_rerank(state: CodeState) -> CodeState:
        retriever = chroma_db.as_retriever(search_kwargs={"k": k})
        docs = retriever.invoke(state["query"])

        reranked_docs = [[state["query"], doc.page_content] for doc in docs]
        scores = reranker_model.compute_score(reranked_docs)
        reranked_docs = [doc for _, doc in sorted(zip(scores, docs), reverse=True)][:n]
        state["docs"] = reranked_docs
        return state
    return retrieve_rerank
