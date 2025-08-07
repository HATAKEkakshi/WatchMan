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

# Collection will be created on first log insertion
print("Qdrant client initialized")