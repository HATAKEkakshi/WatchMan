from fastapi import FastAPI
from src.watchman import watchman


app = FastAPI()
app.include_router(watchman, prefix="/watchman", tags=["watchman"])

