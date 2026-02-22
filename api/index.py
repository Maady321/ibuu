# Vercel Entry Point
import os
import sys
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Pathing setup
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if os.path.join(project_root, "Backend") not in sys.path:
    sys.path.insert(0, os.path.join(project_root, "Backend"))

try:
    from Backend.main import app
except Exception as e:
    error_trace = traceback.format_exc()
    app = FastAPI(title="Error Recovery App")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    
    @app.get("/api/infra-test")
    def error_report():
        return {"status": "error", "error": str(e), "trace": error_trace}
    
    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    def catch_all(path: str):
        return {"detail": "Backend failed to load", "error": str(e)}

# Export handler for Netlify/AWS if needed
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    pass
