"""Small client for the authenticated Sports Betting API."""

from __future__ import annotations

from typing import Any

import requests


class BettingApi:
    """Expose the few API operations this focused suite needs."""

    def __init__(self, base_url: str, user_id: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = {"x-user-id": user_id}

    def get_balance(self) -> dict[str, Any]:
        response = requests.get(
            f"{self.base_url}/api/balance", headers=self.headers, timeout=15
        )
        response.raise_for_status()
        return response.json()
    def get_matches(self) -> list[dict[str, Any]]:
        response = requests.get(
            f"{self.base_url}/api/matches", headers=self.headers, timeout=15
        )
        response.raise_for_status()
        return response.json()

    def place_bet(self, payload: dict[str, Any]) -> requests.Response:
        return requests.post(
            f"{self.base_url}/api/place-bet",
            headers={**self.headers, "Content-Type": "application/json"},
            json=payload,
            timeout=15,
        )

    def reset_balance(self) -> dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/reset-balance", headers=self.headers, timeout=15
        )
        response.raise_for_status()
        return response.json()
