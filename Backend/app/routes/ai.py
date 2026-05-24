from fastapi import APIRouter, HTTPException
import httpx

from app.schemas.ai import (
    GenerateRequest,
    DebugRequest,
    ExecuteRequest
)

router = APIRouter(prefix="/ai", tags=["AI"])


AI_BASE_URL = "http://localhost:9000/api/v1"


# Generate Code
@router.post("/generate")
async def generate_code(data: GenerateRequest):

    async with httpx.AsyncClient(timeout=120.0) as client:

        response = await client.post(
            f"{AI_BASE_URL}/inquiry",
            json=data.dict()
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="AI service error"
        )

    return response.json()


# Debugg
@router.post("/debug")
async def debug_code(data: DebugRequest):

    async with httpx.AsyncClient(timeout=120.0) as client:

        response = await client.post(
            f"{AI_BASE_URL}/debug",
            json=data.dict()
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="AI debug service error"
        )

    return response.json()

# Execute 
@router.post("/execute")
async def execute_code(data: ExecuteRequest):

    async with httpx.AsyncClient(timeout=120.0) as client:

        response = await client.post(
            f"{AI_BASE_URL}/execute",
            json=data.dict()
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="AI execute service error"
        )

    return response.json()