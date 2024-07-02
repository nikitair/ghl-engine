from config.logging_config import logger
from fastapi import APIRouter

router = APIRouter(prefix="/ghl", tags=["GHL"])

@router.get("/")
async def ghl_index():
    return {"router": "GHL"}
