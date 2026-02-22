from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure Backend directory parts are in path
backend_root = os.path.dirname(os.path.abspath(__file__))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

app = FastAPI(
    title="HomeBuddy", 
    version="55.0-RECOVERY",
    redirect_slashes=False  # Crucial for Vercel/Netlify to prevent POST -> GET 307 redirects
)

@app.get("/")
def read_root():
    return {"message": "HomeBuddy API is running", "version": "55.0-RECOVERY"}

@app.api_route("/api/debug-path", methods=["GET", "POST"])
async def debug_path(request: Request):
    return {
        "url": str(request.url),
        "method": request.method,
        "headers": dict(request.headers)
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Relative imports handled by index.py pathing
from routers import users, bookings, providers, reviews, services, supports

# Initialize Database on Startup
from db.database import engine, Base
import models.users, models.providers, models.services, models.bookings, models.reviews, models.supports

@app.on_event("startup")
def startup_event():
    try:
        logger.info("Initial check of database connection...")
        # We don't necessarily want to create_all on every serverless hit, 
        # but for this project it ensures the DB matches the schema
        Base.metadata.create_all(bind=engine)
        logger.info("Database synchronized.")
    except Exception as e:
        logger.warning(f"Database sync skipped/failed: {e}")

@app.get("/api/infra-test")
def infra_test():
    return {"status": "ok", "message": "Backend Is Live", "source": "Backend.main"}

app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(providers.router)
app.include_router(reviews.router)
app.include_router(services.router)
app.include_router(supports.router)

@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend package is healthy"}
