from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# 1. PATHING FOR FLATTENED STRUCTURE
# Since index.py is alongside auth.py, etc., we add the current dir to sys.path
api_dir = os.path.dirname(os.path.abspath(__file__))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

app = FastAPI(title="HomeBuddy", version="46.0-MONOLITH")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TOP-LEVEL SIBLING IMPORTS
from routers import users, bookings, providers, reviews, services, supports

app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(providers.router)
app.include_router(reviews.router)
app.include_router(services.router)
app.include_router(supports.router)

@app.get("/api/infra-test")
def infra_test():
    return {
        "status": "ok", 
        "version": "46.0-MONOLITH", 
        "api_dir": api_dir,
        "sys_path": sys.path
    }

@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend monolith is healthy"}

handler = app
