from fastapi import APIRouter

system_router = APIRouter()

@system_router.get("/health")
async def health():
    return {"status": "healthy"}