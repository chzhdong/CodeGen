from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import JSONLoader

loader_1 = JSONLoader(
    file_path="./dataset/webquery.json",
    jq_schema=".[] | {description: .doc, program: .code}",
    text_content=False
)
docs_1 = loader_1.load()
loader_2 = JSONLoader(
    file_path="./dataset/cosqa.json",
    jq_schema=".[] | {description: .doc, program: .code}",
    text_content=False
)
docs_2 = loader_2.load()
docs = docs_1 + docs_2

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    collection_name="CodeGen",
    persist_directory="./chroma_db"
)
