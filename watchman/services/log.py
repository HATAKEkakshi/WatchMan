from datetime import datetime
from typing import List
from bson import ObjectId
import uuid
from qdrant_client.http.models import PointStruct
from watchman.config.database import logs_collection, qdrant_client
from watchman.config.model import model_settings
from watchman.config.redis import cache_query_result, get_cached_query_result, cache_embeddings, get_cached_embeddings
from watchman.model.log_model import LogRequest, LogResponse, QueryRequest

class LogService:
    def __init__(self):
        self.embedding_model = model_settings.get_huggingface_embeddings()
        self.llm = model_settings.get_groq_model()
    
    async def create_log(self, log_request: LogRequest) -> LogResponse:
        log_data = {
            "service": log_request.service,
            "level": log_request.level,
            "message": log_request.message,
            "metadata": log_request.metadata,
            "timestamp": datetime.utcnow()
        }
        
        result = await logs_collection.insert_one(log_data)
        mongo_id = str(result.inserted_id)
        qdrant_id = str(uuid.uuid4())
        
        # Generate embedding and store in Qdrant
        embedding = self.embedding_model.embed_query(log_request.message)
        await cache_embeddings(mongo_id, embedding)
        
        # Prepare payload for Qdrant (convert non-serializable types)
        qdrant_payload = {
            "mongo_id": mongo_id,
            "service": log_request.service,
            "level": log_request.level,
            "message": log_request.message,
            "metadata": log_request.metadata,
            "timestamp": log_data["timestamp"].isoformat()
        }
        
        # Create collection if it doesn't exist
        try:
            qdrant_client.upsert(
                collection_name="logs",
                points=[PointStruct(
                    id=qdrant_id,
                    vector=embedding,
                    payload=qdrant_payload
                )]
            )
        except Exception as e:
            if "doesn't exist" in str(e):
                from qdrant_client.http.models import Distance, VectorParams
                qdrant_client.create_collection(
                    collection_name="logs",
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
                qdrant_client.upsert(
                    collection_name="logs",
                    points=[PointStruct(
                        id=qdrant_id,
                        vector=embedding,
                        payload=qdrant_payload
                    )]
                )
            else:
                raise e
        
        return LogResponse(
            id=mongo_id,
            service=log_request.service,
            level=log_request.level,
            message=log_request.message,
            metadata=log_request.metadata,
            timestamp=log_data["timestamp"]
        )
    
    async def query_logs(self, query_request: QueryRequest) -> dict:
        # Check cache first
        cached_result = await get_cached_query_result(query_request.query, query_request.service or "all")
        if cached_result:
            return cached_result
        
        query_embedding = self.embedding_model.embed_query(query_request.query)
        
        search_results = qdrant_client.search(
            collection_name="logs",
            query_vector=query_embedding,
            limit=query_request.limit
        )
        
        context = "\n".join([point.payload["message"] for point in search_results])
        
        response = self.llm.invoke(
            model_settings.log_prompt_template.format(
                context=context,
                query=query_request.query
            )
        )
        
        result = {
            "answer": response.content,
            "relevant_logs": [
                {
                    "id": point.payload["mongo_id"],
                    "message": point.payload["message"],
                    "service": point.payload["service"],
                    "score": point.score
                } for point in search_results
            ]
        }
        
        # Cache the result
        await cache_query_result(query_request.query, query_request.service or "all", result)
        return result

log_service = LogService()