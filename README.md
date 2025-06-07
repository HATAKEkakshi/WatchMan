# 🕵️‍♂️ Watchman - Log Intelligence API

**Watchman** is a powerful FastAPI-based backend application designed to semantically process and analyze logs using embedding models and LLMs. It can ingest logs from multiple files, generate vector embeddings, perform semantic search, and provide intelligent responses using LLaMA 3 via Groq.

---

## 📦 Features

- ✅ **Multi-file Log Ingestion** - Handles `.log` and rotated files like `Watchman.log.1`.
- 🔢 **Embeddings Storage** - Embeds logs using `sentence-transformers/all-MiniLM-L12-v2` and stores them in FAISS.
- 🔍 **Semantic Search** - Returns top-k log lines based on semantic similarity.
- 💬 **LLM Chat Interface** - Uses LLaMA-3-70B via Groq for intelligent log conversations.
- 📜 **Custom Logging** - Rotating file logger included.
- 🌱 **Easily Extensible** - Modular codebase.

---

## 🛠️ Tech Stack

| Tool              | Purpose                          |
|-------------------|----------------------------------|
| FastAPI           | Web framework                    |
| LangChain         | Retrieval chain & doc handling   |
| HuggingFace       | Embedding model                  |
| FAISS             | Vector storage                   |
| Groq + LLaMA 3    | LLM-based QA                     |
| NumPy / Scikit-learn | Embedding similarity           |
| dotenv            | Environment config               |
| Uvicorn           | ASGI server                      |

---

## 📁 Project Structure

```
watchman/
│
├── main.py # FastAPI app with all routes
├── .env # Environment variables
├── logs/
│ └── Watchman.log # Auto-generated log file
├── Log/
│ └── log.py # Custom logger (rotating)
├── embeddings/
│ └── embedding.py # Embedding generation, search logic
└── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/HATAKEkakshi/WatchMan.git
cd WatchMan
```
### 2.Create virtual environment
```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4.Create Env
```
GROQ_API_KEY=your_groq_api_key_here

```
###5.🚀 Run the App
```
uvicorn app:app --reload
```
