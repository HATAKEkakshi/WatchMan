import os
import glob
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity


def generate_log_embeddings(log_directory, output_file="log_embeddings.npy"):
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
    log_files = glob.glob(os.path.join(log_directory, "*.log"))

    if not log_files:
        return None, None

    all_log_lines = []
    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            all_log_lines.extend(cleaned_lines)
        except Exception:
            continue

    if not all_log_lines:
        return None, None

    embeddings = embeddings_model.embed_documents(all_log_lines)
    embeddings_array = np.array(embeddings)
    np.save(output_file, embeddings_array)
    return embeddings_array, all_log_lines

def find_similar_logs(query_text, embeddings_array, log_lines, top_k=5):
    embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")
    query_embedding = embeddings_model.embed_query(query_text)
    query_embedding = np.array(query_embedding).reshape(1, -1)

    similarities = cosine_similarity(query_embedding, embeddings_array)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            'log_line': log_lines[idx],
            'similarity': float(similarities[idx]),
            'index': int(idx)
        })

    return results
