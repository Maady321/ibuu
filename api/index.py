import sys
import os

# Root of the project is the current directory's parent
# This file is project_root/api/index.py
# Backend is project_root/Backend
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_path = os.path.join(root_path, "Backend")

if backend_path not in sys.path:
    sys.path.append(backend_path)

# Import the FastAPI app from Backend/main.py
try:
    from main import app
except ImportError as e:
    # Fallback for different environments
    print(f"Import Error: {e}")
    # Try adding root path too
    if root_path not in sys.path:
        sys.path.append(root_path)
    from Backend.main import app

# Vercel will discover 'app' and run it
