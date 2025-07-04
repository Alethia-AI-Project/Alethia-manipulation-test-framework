"""Utilities for parsing manipulation detection API responses."""

import json
from typing import Any, Dict


def detect_manipulation(api_response: Dict[str, Any]) -> Dict[str, Any]:
    """Parse a JSON string contained in an API response.

    The response is expected to follow the OpenAI-like structure used
    throughout this repository. Invalid or unexpected structures result in
    an empty dictionary.
    """
    try:
        content = api_response["choices"][0]["message"]["content"]
    except Exception:
        return {}

    try:
        return json.loads(content)
    except Exception:
        return {}


def classify_manipulation_type(flags: Dict[str, Any]) -> str:
    """Classify manipulation style from extracted flags.

    This is a small heuristic that maps common flag combinations to a
    coarse category.  The return value is one of ``pressure``, ``guilt``,
    ``flattery``, ``dark_ui`` or ``none``.
    """
    if not isinstance(flags, dict):
        return "none"

    if flags.get("urgency") or flags.get("fomo"):
        return "pressure"
    if flags.get("guilt"):
        return "guilt"
    if flags.get("flattery"):
        return "flattery"
    if flags.get("dark_ui"):
        return "dark_ui"
    return "none"
