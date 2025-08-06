"""
Backend package initialization
"""
from pathlib import Path
import sys

# Add backend directory to Python path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
