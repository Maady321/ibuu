import sys
import os
import logging
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. IMMEDIATE DB URL FIX (FORCING PG8000)
db_url_raw = os.getenv("DATABASE_URL", "")
db_url_fixed = "N/A"

if db_url_raw:
    # Definitive Scheme Override (The most bulletproof way)
    if "://" in db_url_raw:
        _, rest = db_url_raw.split("://", 1)
        db_url_fixed = f"postgresql+pg8000://{rest}"
        # Override environment for all sub-modules
        os.environ["DATABASE_URL"] = db_url_fixed
    else:
        db_url_fixed = db_url_raw

# 2. PATHING
project_root = os.getcwd() 
api_dir = os.path.join(project_root, "api")
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

# 3. CORE APP
app = FastAPI(redirect_slashes=False, title="HomeBuddy API", version="4.0-BOMBSHELL-FIX")

# 4. DIAGNOSTICS HELPERS
init_status = "Not Started"
init_error = None

# LOAD LOGIC
try:
    from db.database import Base, engine
    from routers import users, bookings, providers, reviews, services, supports
    import models

    Base.metadata.create_all(bind=engine)
    
    app.include_router(users.router)
    app.include_router(bookings.router)
    app.include_router(providers.router)
    app.include_router(reviews.router)
    app.include_router(services.router)
    app.include_router(supports.router)
    
    init_status = "Success"
except Exception as e:
    init_status = "Failed"
    init_error = f"{str(e)}\n{traceback.format_exc()}"

# 5. ROUTES
@app.get("/api/infra-test")
def infra_test():
    return {
        "status": "ok",
        "version": "4.0-BOMBSHELL-FIX",
        "init_status": init_status,
        "init_error": init_error,
        "db": {
            "raw_prefix": db_url_raw.split("://")[0] if "://" in db_url_raw else "N/A",
            "fixed_prefix": db_url_fixed.split("://")[0] if "://" in db_url_fixed else "N/A",
            "env_now": os.getenv("DATABASE_URL", "").split("://")[0]
        },
        "sys": {
            "python": sys.version,
            "path": sys.path,
            "cwd": os.getcwd()
        }
    }

@app.get("/api/health")
def health():
    return {"status": "ok", "init": init_status}

@app.get("/api")
def root():
    return {"message": "HomeBuddy API v3.0 Live"}

# Vercel entry
handler = app
