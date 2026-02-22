import os
import sys
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Pathing setup - Be extremely careful with relative paths on Vercel
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
backend_dir = os.path.join(project_root, "Backend")

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Initialize a base app
app = FastAPI(title="HomeBuddy Production")

# Global CORS - loosened for debug
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "HomeBuddy Bridge"}

try:
    from Backend.main import app as backend_app
    # If the import works, we use the backend app
    app = backend_app
except Exception as e:
    error_trace = traceback.format_exc()
    @app.get("/api/infra-test")
    def infra_test():
        return {
            "status": "error",
            "error": str(e),
            "trace": error_trace
        }

# Mangum for Netlify
try:
    from mangum import Mangum
    handler = Mangum(app)
except:
    pass
