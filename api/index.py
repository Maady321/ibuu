from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Diagnostic Minimal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Minimal App Live"}

@app.get("/api/infra-test")
def infra_test():
    return {
        "status": "ok",
        "env_keys": list(os.environ.keys()),
        "db_raw": os.getenv("DATABASE_URL", "NOT_SET")[:20] + "..."
    }

handler = app
