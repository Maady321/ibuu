import sys
import os
import logging
import traceback
from fastapi import FastAPI

# 1. PATHING FOR CONSOLIDATED STRUCTURE
# api/index.py
# api/Backend/...
api_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(api_dir, "Backend")

if api_dir not in sys.path:
    sys.path.insert(0, api_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 2. LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 3. FASTAPI BRIDGE
try:
    # Now it's a direct package import
    from Backend.main import app as fastapi_app
    app = fastapi_app
    
    @app.get("/api/infra-test")
    def infra_test():
        return {
            "status": "ok",
            "version": "33.0-CONSOLIDATED",
            "message": "Full Backend module is LIVE within the api/ dir",
            "sys_path": sys.path
        }
    
    logger.info("Vercel: Successfully loaded api.Backend.main app")
    
except Exception as e:
    error_trace = traceback.format_exc()
    logger.error(f"Consolidated Load Failed: {e}\n{error_trace}")
    
    app = FastAPI()
    @app.get("/api/infra-test")
    def infra_test():
        return {
            "status": "consolidate_error",
            "message": f"Module load failed: {str(e)}",
            "trace": error_trace
        }

# Vercel entry
handler = app
app_var = app
