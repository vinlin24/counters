"""
Executes the package to add the counters package to the Windows Task
Scheduler.
"""

from pathlib import Path

from .parser import parser

ns = parser.parse_args()

path = Path(ns.path)
if not path.is_dir():
    print(f"Could not resolve '{path}' as a path to a directory.")
    raise SystemExit
