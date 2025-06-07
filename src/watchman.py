# main.py
from fastapi import APIRouter, Query
from Log.log import WatchmanLogger
from embeddings.embedding import generate_log_embeddings, find_similar_logs
import os
import glob
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")

watchman = APIRouter()
logger = WatchmanLogger()

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question based on the context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Question:{input}
    """
)

# Global vectorstore and embeddings model
vectorstore = None
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")


def store_embeddings(log_dir: str = "logs/"):
    logger.info(f"Storing embeddings for logs in directory: {log_dir}")

    # Get all relevant log files (including rotated logs)
    log_files = glob.glob(os.path.join(log_dir, "*.log")) + glob.glob(os.path.join(log_dir, "Watchman.log*"))
    logger.info(f"Found {len(log_files)} log files: {log_files}")

    all_log_lines = []
    total_lines = 0
    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = [line.strip() for line in f if line.strip()]
            logger.info(f"Read {len(lines)} lines from {log_file}")
            all_log_lines.extend(lines)
            total_lines += len(lines)
        except Exception as e:
            logger.error(f"Failed to read {log_file}: {e}")

    if total_lines == 0:
        logger.error("No log lines found in any files.")
        return {"error": "No log lines found."}

    logger.info(f"Total lines aggregated from all files: {total_lines}")

    global vectorstore
    vectorstore = FAISS.from_texts(all_log_lines, embeddings_model)

    save_path = os.path.join(os.getcwd(), "log_vector_store")
    vectorstore.save_local(save_path)
    logger.info(f"Embeddings stored successfully at {save_path}")

    return {"message": "Embeddings stored successfully.", "total_lines": total_lines}


@watchman.get("/healthz")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


@watchman.get("/embeddings")
async def get_embeddings(log_dir: str = Query("logs/", description="Path to log directory")):
    logger.info("Embeddings endpoint called")
    embeddings, log_lines = generate_log_embeddings(log_dir)
    if embeddings is None:
        return {"error": "No embeddings generated"}
    return {"embeddings": embeddings.tolist(), "total_logs": len(log_lines)}


@watchman.get("/store")
async def store_logs_embeddings(log_dir: str = Query("logs/", description="Path to log directory")):
    logger.info("Store embeddings endpoint called")
    return store_embeddings(log_dir)


@watchman.get("/search")
async def search_logs(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(5, description="Number of similar logs to return"),
    log_dir: str = Query("logs/", description="Path to log directory")
):
    logger.info(f"Search requested with query: {query}")
    embeddings, log_lines = generate_log_embeddings(log_dir)
    if embeddings is None:
        return {"error": "No logs to search in."}

    results = find_similar_logs(query, embeddings, log_lines, top_k=top_k)
    return {"results": results}


@watchman.get("/chat")
async def chat_with_logs(query: str):
    global vectorstore
    if vectorstore is None:
        try:
            load_path = os.path.join(os.getcwd(), "log_vector_store")
            vectorstore = FAISS.load_local(load_path, embeddings_model)
            logger.info("Vector store loaded successfully.")
        except Exception as e:
            logger.error(f"Vector store not found or failed to load. Error: {str(e)}")
            return {"error": "Vector store not found. Please run /store to initialize it."}

    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectorstore.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": query})

    answer = response.get("answer")
    if not answer:
        return {"error": "No answer generated."}
    return {"response": answer}
