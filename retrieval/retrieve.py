import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="pipeline_docs"
)

query = input("Ask a question: ")

results = collection.query(
    query_texts=[query],
    n_results=1
)

print("\nBest Match:\n")

print(results["documents"][0][0])