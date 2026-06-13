from pathlib import Path
import chromadb

client = chromadb.PersistentClient(path="chroma_db")

try:
    client.delete_collection("knowledge_base")
except:
    pass

collection = client.get_or_create_collection(
    name="knowledge_base"
)

kb_path = Path("knowledge_base")

chunk_id = 0

for category_folder in kb_path.iterdir():

    if not category_folder.is_dir():
        continue

    document_type = category_folder.name

    for file in category_folder.iterdir():

        if not file.is_file():
            continue

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
                        "source": file.name,
                        "document_type": document_type
                    }
                ]
            )

            chunk_id += 1

print(f"Stored {chunk_id} chunks.")