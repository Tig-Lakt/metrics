import time
import asyncio
from fastapi import APIRouter


router = APIRouter()


@router.post("/process")
async def process_data(data: dict):

   return {"echo": data.get("data")}