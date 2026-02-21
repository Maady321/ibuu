from fastapi import FastAPI
from mangum import Mangum
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/api/infra-test")
def infra_test():
    return {
        "status": "ok", 
        "message": "FastAPI + Mangum is working",
        "env": os.getenv("ENVIRONMENT", "not-set")
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}

handler = Mangum(app, lifespan="off")
application = app
