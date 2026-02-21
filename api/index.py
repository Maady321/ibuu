import sys
import os
from fastapi import FastAPI

app = FastAPI()

try:
    import sqlalchemy
    import_status = "SQLAlchemy Imported Successfully"
except Exception as e:
    import_status = f"SQLAlchemy Import Failed: {e}"

@app.get("/api/infra-test")
def infra_test():
    return {
        "status": "incremental_check",
        "import_status": import_status,
        "sys_path": sys.path,
        "files_in_api": os.listdir("api") if os.path.exists("api") else "N/A"
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}
