import sys
import os

# Simulate Vercel pathing
current_dir = os.getcwd()
# Assuming we are in the project root
api_dir = os.path.join(current_dir, "api")
project_root = current_dir
backend_dir = os.path.join(project_root, "Backend")

sys.path.insert(0, project_root)
sys.path.insert(0, backend_dir)

print(f"Path: {sys.path[:3]}")

try:
    from Backend.main import app
    print("SUCCESS: Imported Backend.main.app")
except Exception as e:
    print(f"FAILURE: {e}")
    import traceback
    traceback.print_exc()
