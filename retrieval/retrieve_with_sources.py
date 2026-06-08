import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="pipeline_chunks"
)

question = input("Ask a question: ")

results = collection.query(
    query_texts=[question],
    n_results=3
)

print("\nTOP SOURCES:\n")

for i in range(len(results["documents"][0])):

    source = results["metadatas"][0][i]["source"]

    chunk = results["documents"][0][i]

    print(f"[{i+1}] {source}")
    print(chunk)
    print()