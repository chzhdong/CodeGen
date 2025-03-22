from langchain_chroma import Chroma
from flagembeddings import FlagEmbeddings

def reranked_documents(query, reranker_model, k = 10, n = 3):
    retriever = chroma_db.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)

    reranked_docs = [(query, doc) for doc in docs]
    scores = reranker_model.predict(reranked_docs)
    reranked_docs = [doc for _, doc in sorted(zip(scores, docs), reverse=True)][ : n]
    return reranked_docs
