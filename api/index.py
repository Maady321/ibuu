import sys
import os
import logging
from fastapi import FastAPI
from mangum import Mangum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

backend_path = os.path.join(project_root, "Backend")
sys.path.insert(0, backend_path)

try:
    from Backend.main import app as fastapi_app
    app = fastapi_app
    handler = Mangum(app, lifespan="off")
    @app.get("/api/infra-test")
    def infra_test():
        return {"status": "ok", "message": "Full Backend package Loaded successfully on Pydantic V1 stack"}
    logger.info("Vercel serverless function initialized successfully with Backend package")
except Exception as e:
    import traceback
    error_trace = traceback.format_exc()
    logger.error(f"Backend Initialization Failed: {e}\n{error_trace}")
    
    app = FastAPI()
    @app.get("/api/infra-test")
    def infra_test():
        return {
            "status": "error", 
            "message": f"Backend failed to load: {str(e)}",
            "trace": error_trace
        }
    handler = Mangum(app, lifespan="off")

application = app
