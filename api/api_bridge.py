import sys
import os
import logging
import traceback
from fastapi import FastAPI

# 1. PATHING FOR RESTORED STRUCTURE
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

backend_path = os.path.join(project_root, "Backend")
sys.path.insert(0, backend_path)

# 2. LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 3. FASTAPI BRIDGE
try:
    # Import the main app from the restored Backend folder
    from Backend.main import app as fastapi_app
    app = fastapi_app
    
    @app.get("/api/infra-test")
    def infra_test():
        return {
            "status": "ok",
            "version": "28.0-RESTRUCTURED",
            "message": "Full Backend package is LIVE on restored V1 stack",
            "sys_path": sys.path
        }
    
    logger.info("Vercel: Successfully loaded Backend.main app")
    
except Exception as e:
    error_trace = traceback.format_exc()
    logger.error(f"Backend Restore Failed: {e}\n{error_trace}")
    
    app = FastAPI()
    @app.get("/api/infra-test")
    def infra_test():
        return {
            "status": "restore_error",
            "message": str(e),
            "trace": error_trace
        }

# Vercel entry
handler = app
