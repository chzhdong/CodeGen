from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

chroma_db = Chroma(collection_name="CodeGen", persist_directory="./chroma_db", embedding_function=embedding_model)

retriever = chroma_db.as_retriever(search_kwargs={"k": 3})

query = "读取 CSV 文件"
docs = retriever.invoke(query)

for doc in docs:
    print(doc.page_content)
