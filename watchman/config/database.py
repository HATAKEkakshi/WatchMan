from motor.motor_asyncio import AsyncIOMotorClient
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from watchman.config.model import model_settings

# MongoDB setup
client = AsyncIOMotorClient(model_settings.MONGODB_URL)
db = client.watchman
logs_collection = db.logs

# Qdrant setup
qdrant_client = QdrantClient(host=model_settings.QDRANT_HOST, port=model_settings.QDRANT_PORT)

try:
    # Check if collection exists first
    collections = qdrant_client.get_collections()
    collection_names = [col.name for col in collections.collections]
    
    if "logs" not in collection_names:
        qdrant_client.create_collection(
            collection_name="logs",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print("Created 'logs' collection in Qdrant")
    else:
        print("'logs' collection already exists")
except Exception as e:
    print(f"Error with Qdrant collection: {e}")
    # Create collection anyway if it doesn't exist
    try:
        qdrant_client.create_collection(
            collection_name="logs",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
        print("Successfully created 'logs' collection")
    except Exception as create_error:
        print(f"Failed to create collection: {create_error}")