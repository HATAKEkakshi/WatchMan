from fastapi import APIRouter, Header, HTTPException
from watchman.model.log_model import LogRequest, LogResponse, QueryRequest
from watchman.services.log import log_service

router = APIRouter(prefix="/api/logs", tags=["logs"])

@router.post("/", response_model=LogResponse)
async def create_log(
    log_request: LogRequest,
    service: str = Header(..., description="Service name (backend/auth)")
):
    log_request.service = service
    return await log_service.create_log(log_request)

@router.post("/query")
async def query_logs(query_request: QueryRequest):
    return await log_service.query_logs(query_request)