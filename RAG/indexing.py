import os
import glob
import json
from langchain_chroma import Chroma
from langchain_core.documents import Document

def build_database(embedding_model, working_dir, saving_dir):
    data_paths = glob.glob(os.path.join(working_dir, "*.json"))
    docs = []
    for data_path in data_paths:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            docs.extend([
                Document(
                    page_content=item["doc"],
                    metadata={"code": item["code"]}
                )
                for item in data
            ])
    chroma = Chroma.from_documents(
        documents=docs, 
        embedding=embedding_model, 
        collection_name="CodeGen", 
        persist_directory=saving_dir
    )
    print("Construct the Chroma vector database!")
    return chroma
