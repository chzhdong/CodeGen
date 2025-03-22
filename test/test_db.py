import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection("CodeGen")

results = collection.get(include=["documents", "metadatas"], limit=5)

for i in range(len(results["documents"])):
    print(f"\nDocument {i+1}")
    print("Content:", results["documents"][i])
    print("Metadata:", results["metadatas"][i])
