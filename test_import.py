import sys
import traceback

try:
    print("Attempting to import diet_planner...")
    import diet_planner
    print("Import successful!")
except Exception:
    print("Import failed!")
    traceback.print_exc()
