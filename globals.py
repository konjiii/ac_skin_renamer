import sys
from pathlib import Path

# Determine root directory based on whether the app is frozen (packaged) or not
ROOT_DIR = (
    Path(sys.executable).parent
    if getattr(sys, "frozen", False)
    else Path(__file__).parent
)