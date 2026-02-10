import sys
import os

# Ensure the Backend directory is in the path so we can import main.py
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Backend")
sys.path.insert(0, backend_path)

# Import the FastAPI app instance from Backend/main.py
try:
    from main import app
except ImportError:
    # Fallback if the path structure is slightly different in the build env
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from Backend.main import app

# Vercel will discover this 'app' and treat it as the entry point
