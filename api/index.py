from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# 1. FIX PATHING FOR RECURSIVE IMPORTS
# index.py is in api/
# project_root is the parent of api/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
backend_dir = os.path.join(project_root, "Backend")

# Add root for 'from Backend.xxx'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add Backend root for 'from xxx' inside Backend
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Add api dir just in case
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

app = FastAPI(title="HomeBuddy", version="45.0-NAMESPACE")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Relative imports from Backend namespace
from Backend.routers import users, bookings, providers, reviews, services, supports

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
        "version": "45.0-NAMESPACE", 
        "project_root": project_root,
        "backend_dir": backend_dir,
        "sys_path": sys.path
    }

@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend restored and healthy"}

handler = app
