import chromadb
import ollama

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="pipeline_docs"
)

# User Question
question = input("Ask a question: ")

# Retrieve context
results = collection.query(
    query_texts=[question],
    n_results=3
)

documents = results["documents"][0]

context = "\n\n".join(documents)

print("\nRetrieved Context:\n")
print(context)

# Prompt
prompt = f"""
You are a Data Engineering Assistant.

Rules:
1. Use ONLY the provided context.
2. If the answer is not present, say:
   "I cannot find that information in the provided documents."
3. Do not invent table names, pipelines, schemas, or fields.
4. Keep answers short.

Context:
{context}

Question:
{question}
"""

# Generate answer
response = ollama.chat(
    model="llama3.2:1b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nAnswer:\n")
print(response["message"]["content"])