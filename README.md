# RAG-Powered Data Engineering Assistant

## Project Overview

This project is a Retrieval-Augmented Generation (RAG) based Data Engineering Assistant built using Python, Sentence Transformers, ChromaDB, and Ollama.

The assistant helps users query data engineering documentation, pipeline information, operational runbooks, and governance policies using natural language.

Instead of relying solely on a Large Language Model (LLM), the system retrieves relevant information from a knowledge base and uses that context to generate responses.

---

## Features

* Semantic Search using Sentence Transformers
* Vector Storage using ChromaDB
* Document Chunking
* Metadata-Based Retrieval
* Source Attribution
* Local LLM Integration using Ollama
* Retrieval-Augmented Generation (RAG) Pipeline

---

## Tech Stack

* Python
* Sentence Transformers
* ChromaDB
* Ollama
* NumPy
* VS Code
* Git & GitHub

---

## Project Structure

```text
rag-data-engineering-assistant
│
├── data/
├── ingestion/
├── retrieval/
├── app.py
├── rag_chat.py
├── .gitignore
└── README.md
```

---

## RAG Architecture

User Question
↓
Embedding Generation
↓
Vector Search (ChromaDB)
↓
Relevant Document Retrieval
↓
Context Injection
↓
Local LLM (Ollama)
↓
Generated Answer

---

## Learning Objectives

This project was built to understand:

* Retrieval-Augmented Generation (RAG)
* Embeddings
* Vector Databases
* Semantic Search
* Document Chunking
* Local LLM Deployment
* Data Engineering Knowledge Retrieval

---

## Current Status

Completed:

* Document Ingestion
* Embedding Generation
* ChromaDB Integration
* Chunk-Based Retrieval
* Source Attribution
* Ollama Integration

Upcoming:

* Metadata Filtering
* Knowledge Base Expansion
* Streamlit UI
* Advanced Retrieval Techniques

---

## Author

Kanika Pitaliya
MSc Data Analytics
