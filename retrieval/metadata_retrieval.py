import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="knowledge_base"
)

question = input("Ask a question: ")

# Simple intent routing
document_type = None

question_lower = question.lower()

if any(word in question_lower for word in
       ["fail", "failure", "error", "recover", "restart", "outage"]):

    document_type = "runbooks"

elif any(word in question_lower for word in
         ["query", "sql"]):

    document_type = "sql"

elif any(word in question_lower for word in
         ["policy", "pii", "security"]):

    document_type = "policies"

elif any(word in question_lower for word in
         ["table", "column", "schema"]):

    document_type = "catalog"

elif "pipeline" in question_lower:

    document_type = "pipelines"

print(f"\nSearching document type: {document_type}")

if document_type:

    results = collection.query(
        query_texts=[question],
        n_results=3,
        where={"document_type": document_type}
    )

else:

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

print("\nResults:\n")

for i in range(len(results["documents"][0])):

    metadata = results["metadatas"][0][i]

    print("-" * 50)

    print(metadata)

    print()

    print(results["documents"][0][i])

    print()