from fastapi import FastAPI
app = FastAPI()
@app.get("/api/infra-test")
def test():
    return {"status": "MINIMAL_WORKS"}
