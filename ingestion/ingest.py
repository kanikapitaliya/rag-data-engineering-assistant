from pathlib import Path
import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="pipeline_docs"
)

data_folder = Path("data")

documents = []
ids = []

for i, file in enumerate(data_folder.glob("*.md")):
    text = file.read_text(encoding="utf-8")

    documents.append(text)
    ids.append(file.stem)

# clear old data
try:
    collection.delete(ids=collection.get()["ids"])
except:
    pass

collection.add(
    documents=documents,
    ids=ids
)

print(f"Ingested {len(documents)} documents.")