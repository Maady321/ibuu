from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Ensure Backend directory parts are in path
backend_root = os.path.dirname(os.path.abspath(__file__))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

app = FastAPI(
    title="HomeBuddy", 
    version="55.0-RECOVERY",
    redirect_slashes=False  # Crucial for Vercel/Netlify to prevent POST -> GET 307 redirects
)

@app.api_route("/api/debug-path", methods=["GET", "POST"])
async def debug_path(request: Request):
    return {
        "url": str(request.url),
        "method": request.method,
        "headers": dict(request.headers)
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ibuuuuu.netlify.app",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "https://full-stack-project-iota-five.vercel.app"
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",  # Support for Vercel Branch/Preview deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Relative imports from Backend namespace
from routers import users, bookings, providers, reviews, services, supports

# Initialize Database Tables
from db.database import engine, Base
import models.users, models.providers, models.services, models.bookings, models.reviews, models.supports

try:
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing database: {e}")
    # Don't crash here, might be a transient connection issue

app.include_router(users.router)
app.include_router(bookings.router)
app.include_router(providers.router)
app.include_router(reviews.router)
app.include_router(services.router)
app.include_router(supports.router)

@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend package is healthy"}
