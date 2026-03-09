import os
import sys

from dotenv import load_dotenv

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_PATH)

from prometheus_client import Counter, Histogram

dotenv_path = os.path.join(PROJECT_PATH, ".env") 
load_dotenv(dotenv_path, override=True) 


host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
database = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# Метрики
REQUEST_COUNT = Counter("http_requests_total", "Total requests", ["method", "endpoint", "status"])
LATENCY_HISTOGRAM = Histogram("http_request_duration_seconds", "Latency", ["endpoint"])

ENDPOINT_PROCESS = "/process"