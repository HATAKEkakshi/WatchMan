from typing import ClassVar
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts.chat import ChatPromptTemplate
from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file="./.env",
    env_ignore_empty=True,
    extra="ignore"
)

def get_log_prompt_template() -> ChatPromptTemplate:
    template = """You are a DevOps Log Intelligence Assistant. Analyze the provided log context and answer the user's query clearly and concisely.

Context: {context}
Query: {query}

Provide a helpful response based on the log information."""
    return ChatPromptTemplate.from_template(template)

class ModelSettings(BaseSettings):
    GROQ_API_KEY: str
    MONGODB_URL: str = "mongodb://mongodb:27017"
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    
    model_config = _base_config
    log_prompt_template: ClassVar[ChatPromptTemplate] = get_log_prompt_template()

    def get_groq_model(self):
        return ChatGroq(
            groq_api_key=self.GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile"
        )

    def get_huggingface_embeddings(self):
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

model_settings = ModelSettings()
