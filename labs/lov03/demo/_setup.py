"""Plumbing: puts the shared kit (labs/_shared/lovkit) and this folder on the import path. Ignore this file."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_shared"))
sys.path.insert(0, str(HERE))
