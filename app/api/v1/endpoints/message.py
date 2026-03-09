
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db, Message
from logs.logger import logger
from config.config import REQUEST_COUNT, LATENCY_HISTOGRAM
import time


router = APIRouter()


@router.get("/message/{id}")
async def get_message(id: int, db: Session = Depends(get_db)):
    endpoint = "/message"
    method = "GET"
    start_time = time.time()
    status_code = "200"

    try:
        message = db.query(Message).filter(Message.id == id).first()

        if not message:
            status_code = "404"
            logger.error("message_not_found", message_id=id)
            raise HTTPException(status_code=404, detail="Message not found")

        return {"id": message.id, "text": message.text}

    except HTTPException as e:
        status_code = str(e.status_code)
        raise e
    except Exception as e:
        status_code = "500"
        logger.error("get_message_error", message_id=id, error=str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

    finally:
        duration = time.time() - start_time

        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=status_code
        ).inc()

        LATENCY_HISTOGRAM.labels(endpoint=endpoint).observe(duration)
