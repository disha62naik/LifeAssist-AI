# modules/__init__.py
# Makes 'modules' a Python package so imports like
# "from modules.decision import evaluate_decision" work correctly.

from .decision import evaluate_decision
from .planner import generate_plan
from .productivity import calculate_productivity
from .suggestions import get_suggestions

__all__ = [
    "evaluate_decision",
    "generate_plan",
    "calculate_productivity",
    "get_suggestions",
]