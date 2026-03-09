import time
import asyncio
from fastapi import APIRouter, HTTPException
from logs.logger import logger
from config.config import REQUEST_COUNT, LATENCY_HISTOGRAM, ENDPOINT_PROCESS


router = APIRouter()


@router.post("/process")
async def process_data(data: dict):
	method = "POST"
	start_time = time.time()
	status_code = "200"
    
	try:
		# Симуляция обработки
		await asyncio.sleep(0.7)

		if not data.get("data"):
			status_code = "400"
			raise HTTPException(status_code=400, detail="Missing data")

		result = {"echo": data.get("data")}
		return result

	except HTTPException as e:
		status_code = str(e.status_code)
		raise e
	except Exception as e:
		status_code = "500"
		logger.error("process_data_failed", error=str(e))
		raise HTTPException(status_code=500, detail="Internal Server Error")

	finally:
		duration = time.time() - start_time

		# Запись метрик
		REQUEST_COUNT.labels(
			method=method,
			endpoint=ENDPOINT_PROCESS,
			status=status_code
		).inc()

		LATENCY_HISTOGRAM.labels(endpoint=ENDPOINT_PROCESS).observe(duration)

		logger.info("data_processed", status=status_code, duration=duration)
