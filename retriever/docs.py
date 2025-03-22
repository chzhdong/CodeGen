from langchain_chroma import Chroma
from classes.state import CodeState

def build_retrieve_node(reranker_model, k = 10, n = 3):
    def reranked_documents(state: CodeState) -> CodeState:
        retriever = chroma_db.as_retriever(search_kwargs={"k": k})
        docs = retriever.invoke(state.query)

        reranked_docs = [(query, doc) for doc in docs]
        scores = reranker_model.predict(reranked_docs)
        reranked_docs = [doc for _, doc in sorted(zip(scores, docs), reverse=True)][:n]
        state.docs = reranked_docs
        return state
    return reranked_documents
