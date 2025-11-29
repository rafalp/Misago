from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Optional

AvatarEntry = Mapping[str, Any]


def _normalize_size(size: Any) -> int:
    try:
        return int(size)
    except (TypeError, ValueError):
        return 0


def _coerce_avatar_sequence(raw: Any) -> Sequence[AvatarEntry]:
    if isinstance(raw, list):
        return raw
    if isinstance(raw, tuple):
        return list(raw)
    return []


def resolve_avatar_for_size(raw: Any, size: Any) -> Optional[AvatarEntry]:
    """Return avatar entry closest to requested size or None when unavailable."""

    avatars = _coerce_avatar_sequence(raw)
    if not avatars:
        return None

    requested_size = _normalize_size(size)
    selected: Optional[AvatarEntry] = None

    for avatar in avatars:
        if not isinstance(avatar, Mapping):
            continue

        url = avatar.get("url")
        if not url:
            continue

        if selected is None:
            selected = avatar

        avatar_size = avatar.get("size")
        if isinstance(avatar_size, int) and avatar_size >= requested_size:
            selected = avatar

    return selected
