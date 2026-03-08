
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db, Message


router = APIRouter()


@router.get("/message/{id}")
async def get_message(id: int, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"id": message.id, "text": message.text}