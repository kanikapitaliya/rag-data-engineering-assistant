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

print("\nTop Matches:\n")

for i in range(len(results["documents"][0])):

    print("-" * 50)

    print("SOURCE:")
    print(results["metadatas"][0][i]["source"])

    print()

    print(results["documents"][0][i])

    print()