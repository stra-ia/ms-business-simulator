from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/message")
async def send_message():
    return {
        "message": "Hello World"
    }