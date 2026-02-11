"""
Main entry point for Vercel deployment
Routes all API requests to the FastAPI backend
"""
import sys
import os

# Set up path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

backend_path = os.path.join(project_root, "Backend")
sys.path.insert(0, backend_path)

# Mark as production environment
os.environ['ENVIRONMENT'] = 'production'

try:
    # Import and wrap the FastAPI app for Vercel
    from Backend.main import app as fastapi_app
    from mangum import Mangum
    
    # Create Mangum handler for Vercel's Python runtime
    app = Mangum(fastapi_app, lifespan="off")
    
    # Export as both app and application for compatibility
    application = app
    
    print("✓ Vercel serverless function initialized successfully", flush=True)
    
except ImportError as e:
    print(f"✗ Import Error: Missing dependency - {e}", flush=True)
    raise
except Exception as e:
    print(f"✗ Fatal Error during initialization: {e}", flush=True)
    import traceback
    traceback.print_exc()
    raise
