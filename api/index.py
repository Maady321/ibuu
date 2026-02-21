import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fallback basic app if EVERYTHING else fails
from http.server import BaseHTTPRequestHandler
class fallback_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        import json
        self.wfile.write(json.dumps({"status": "critical_error", "message": "Failed to load FastAPI/Mangum libraries"}).encode('utf-8'))

try:
    from fastapi import FastAPI
    from mangum import Mangum

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)
    backend_path = os.path.join(project_root, "Backend")
    sys.path.insert(0, backend_path)

    try:
        from Backend.main import app as fastapi_app
        app = fastapi_app
        logger.info("Backend Loaded Successfully")
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Backend Import Failed: {e}\n{error_trace}")
        app = FastAPI()
        @app.get("/api/infra-test")
        def infra_test():
            return {"status": "error", "message": f"Backend package failed: {str(e)}", "trace": error_trace}
    
    handler = Mangum(app, lifespan="off")
    application = app

except Exception as e:
    import traceback
    logger.error(f"Framework Load Failed: {e}\n{traceback.format_exc()}")
    # Vercel looks for 'app' or 'handler'
    # Since FastAPI failed, we use the fallback handler
    handler = fallback_handler

# For Vercel zero-config
app = application if 'application' in locals() else None
