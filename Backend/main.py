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
    version="55.0-RECOVERY"
)
app.router.redirect_slashes = False # Crucial for Vercel/Netlify to prevent POST -> GET 307 redirects

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
    allow_origin_regex=r"https://.*\.vercel\.app|https://.*\.netlify\.app|http://localhost:.*|http://127\.0\.0\.1:.*",
    allow_credentials=True,
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
    logger.info("Startup: Syncing database...")
    try:
        # Only sync if using real DB, SQLite in-memory doesn't need this
        if "sqlite" not in str(engine.url):
            Base.metadata.create_all(bind=engine)
            logger.info("Database synchronized.")
    except Exception as e:
        logger.error(f"Post-startup DB sync failed: {e}")

@app.get("/api/infra-test")
def infra_test():
    return {
        "status": "ok", 
        "message": "Backend Is Live", 
        "db": str(engine.url).split("@")[-1] if "@" in str(engine.url) else "local"
    }

app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(providers.router)
app.include_router(reviews.router)
app.include_router(services.router)
app.include_router(supports.router)

@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend package is healthy"}
