import sys
import os
import logging
from fastapi import FastAPI
from mangum import Mangum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Minimal app for infrastructure testing
mini_app = FastAPI()

@mini_app.get("/api/infra-test")
def infra_test():
    return {"status": "ok", "message": "Infra is working"}

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

backend_path = os.path.join(project_root, "Backend")
sys.path.insert(0, backend_path)

try:
    from Backend.main import app as fastapi_app
    # Combine with mini_app or just use the main one if it loads
    application = Mangum(fastapi_app, lifespan="off")
    logger.info("Vercel serverless function initialized successfully")
except Exception as e:
    logger.error(f"Initialization Failed: {e}")
    # Fallback to mini_app so we can at least see the logs via a route
    application = Mangum(mini_app, lifespan="off")

app = application
