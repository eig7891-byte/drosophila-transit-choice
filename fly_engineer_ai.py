"""
Legacy alias forwarding to src.ai for backward compatibility.
"""
from src.ai import (
    get_avatar_b64,
    get_gemini_client,
    generate_ai_response,
    inject_fly_engineer_floating_widget,
)

__all__ = [
    "get_avatar_b64",
    "get_gemini_client",
    "generate_ai_response",
    "inject_fly_engineer_floating_widget",
]
