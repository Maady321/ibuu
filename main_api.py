import sys
import os
import logging
import traceback
from fastapi import FastAPI

# 1. PATHING FOR ROOT STRUCTURE
# main_api.py
# Backend/...
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 2. LOGGING
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 3. FASTAPI BRIDGE
try:
    from Backend.main import app as fastapi_app
    app = fastapi_app
    
    @app.get("/api/infra-test")
    def infra_test():
        import sys
        return {
            "status": "ok",
            "version": "35.0-ROOT-RESTORED",
            "message": "Full Backend module is LIVE at root level",
            "sys_path": sys.path
        }
    
    logger.info("Vercel: Successfully loaded root-level main app")
    
except Exception as e:
    error_trace = traceback.format_exc()
    logger.error(f"Root Restore Failed: {e}\n{error_trace}")
    
    app = FastAPI()
    @app.get("/api/infra-test")
    def infra_test():
        return {
            "status": "root_restore_error",
            "message": str(e),
            "trace": error_trace
        }

# Vercel entry
handler = app
app_var = app
