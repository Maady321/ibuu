from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/api/infra-test")
def infra_test():
    return {"status": "ok", "message": "Absolute bare minimum is working"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

# The Mangum handler
handler = Mangum(app, lifespan="off")

# Vercel looks for 'app' or 'handler'
application = app
