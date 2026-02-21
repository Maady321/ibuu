from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/api/infra-test")
def infra_test():
    return {"status": "ok", "message": "FastAPI + Mangum (Minimal) is working"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

handler = Mangum(app, lifespan="off")
application = app
