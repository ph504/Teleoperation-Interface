# File: main/utils/path_setup.py

import sys
import os

def extend_path_to_root():
    """
    Adds the project root (src/test/src/) to sys.path
    so you can import from `main.*` no matter where the script is run from.
    """
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if root_path not in sys.path:
        sys.path.insert(0, root_path)
