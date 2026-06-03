"""Token masking utilities for safe config logging.

Mirrors the qase-javascript-commons `token-masker.ts` contract so leaked
debug logs cannot expose customer API tokens. The only secret we currently
need to mask sits at ``config.testops.api.token``.
"""

import json
from typing import Any


def mask_token(token: str) -> str:
    """Return a masked representation of an API token.

    Tokens of 7 chars or fewer are fully replaced with asterisks.
    Longer tokens keep the first 3 and last 4 characters: ``abc****wxyz``.
    """
    if not isinstance(token, str):
        return token
    if len(token) <= 7:
        return "*" * len(token)
    return f"{token[:3]}****{token[-4:]}"


def sanitize_config_for_log(config: Any) -> str:
    """Return a JSON string of ``config`` with the API token masked.

    Accepts any object with a JSON-serialisable ``__str__`` (e.g. ``BaseModel``)
    or a dict. Falls back to ``str(config)`` if the serialised form cannot be
    parsed as JSON, so callers never lose log output to a masking bug.
    """
    try:
        raw = config if isinstance(config, str) else str(config)
        parsed = json.loads(raw)
    except (TypeError, ValueError):
        return str(config)

    token = (
        parsed.get("testops", {}).get("api", {}).get("token")
        if isinstance(parsed, dict)
        else None
    )
    if token:
        parsed["testops"]["api"]["token"] = mask_token(token)

    return json.dumps(parsed, indent=4, sort_keys=True)
