import chromadb
import ollama

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="knowledge_base"
)

question = input("Ask a question: ")

question_lower = question.lower()

document_type = None

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

context = "\n\n".join(
    results["documents"][0]
)

prompt = f"""
Answer the question using the context below.

Be concise.

Context:

{context}

Question:

{question}
"""

response = ollama.chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nContext Used:\n")
print(context)

print("\nAnswer:\n")
print(response["message"]["content"])