import sys
import os
import logging
from fastapi import FastAPI

# 1. PATHING
# We ensure the 'api' directory itself and its parent are in path
api_dir = os.path.dirname(os.path.abspath(__file__))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

# 2. APP INITIALIZATION WITH FALLBACK
try:
    from fastapi.middleware.cors import CORSMiddleware
    from db.database import engine, Base
    from routers import users, bookings, providers, reviews, services, supports

    app = FastAPI(title="HomeBuddy API", version="20.0-RECOVERY")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount routers
    app.include_router(users.router)
    app.include_router(bookings.router)
    app.include_router(providers.router)
    app.include_router(reviews.router)
    app.include_router(services.router)
    app.include_router(supports.router)

    @app.get("/api/infra-test")
    def infra_test():
        return {"status": "ok", "version": "20.0-RECOVERY", "message": "Full App Loaded Successfully"}

except Exception as e:
    import traceback
    error_trace = traceback.format_exc()
    
    # Create a minimal fallback app to report the error
    app = FastAPI()
    
    @app.get("/api/infra-test")
    def infra_test():
        return {
            "status": "error",
            "version": "20.0-RECOVERY-FALLBACK",
            "message": f"Initialization failed: {str(e)}",
            "trace": error_trace
        }

@app.get("/api/health")
def health():
    return {"status": "ok"}

# Vercel entry
handler = app
app_var = app # For multiple detection methods
