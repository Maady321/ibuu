import sys
import os
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/infra-test")
def infra_test():
    return {
        "status": "baseline",
        "cwd": os.getcwd(),
        "sys_path": sys.path,
        "files": os.listdir(".")
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}
