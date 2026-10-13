"""Centralised environment settings for local and CI runs."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    base_url: str
    user_id: str
    headless: bool

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            base_url=os.getenv(
                "SPORTY_BASE_URL", "https://qae-assignment-tau.vercel.app"
            ).rstrip("/"),
            user_id=os.getenv("SPORTY_USER_ID", "candidate-TFSLgcFZDB8D"),
            headless=os.getenv("UI_HEADLESS", "true").lower() == "true",
        )
