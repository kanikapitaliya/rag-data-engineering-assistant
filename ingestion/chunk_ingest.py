from pathlib import Path
import chromadb

client = chromadb.PersistentClient(path="chroma_db")

try:
    client.delete_collection("pipeline_chunks")
except:
    pass

collection = client.get_or_create_collection(
    name="pipeline_chunks"
)

data_folder = Path("data")

chunk_id = 0

for file in data_folder.glob("*.md"):

    text = file.read_text(encoding="utf-8")

    chunks = text.split("\n\n")

    for chunk in chunks:

        chunk = chunk.strip()

        if len(chunk) < 20:
            continue

        collection.add(
            documents=[chunk],
            ids=[f"chunk_{chunk_id}"],
            metadatas=[
                {
                    "source": file.name
                }
            ]
        )

        chunk_id += 1

print(f"Stored {chunk_id} chunks.")