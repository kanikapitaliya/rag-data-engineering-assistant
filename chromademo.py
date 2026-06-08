from pathlib import Path
import chromadb

# Create Chroma client
client = chromadb.PersistentClient(path="chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="pipeline_docs"
)

# Read documents
data_folder = Path("data")

documents = []
ids = []

for i, file in enumerate(data_folder.glob("*.md")):
    text = file.read_text(encoding="utf-8")

    documents.append(text)
    ids.append(f"doc_{i}")

# Store in ChromaDB
collection.add(
    documents=documents,
    ids=ids
)

# Ask a question
query = "Where does sales data come from?"

# Search
results = collection.query(
    query_texts=[query],
    n_results=1
)

print("\nQuestion:")
print(query)

print("\nBest Match:")
print(results["documents"][0][0])