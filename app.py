from sentence_transformers import SentenceTransformer
from pathlib import Path
import numpy as np

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read documents
data_folder = Path("data")

documents = []
file_names = []

for file in data_folder.glob("*.md"):
    text = file.read_text(encoding="utf-8")

    documents.append(text)
    file_names.append(file.name)

# Create embeddings
doc_embeddings = model.encode(documents)

# User question
query = "Where does sales data come from?"

# Create query embedding
query_embedding = model.encode(query)

# Similarity calculation
scores = np.dot(doc_embeddings, query_embedding)

best_match_index = np.argmax(scores)

print("\nQuestion:")
print(query)

print("\nBest Matching File:")
print(file_names[best_match_index])

print("\nDocument Content:")
print(documents[best_match_index])