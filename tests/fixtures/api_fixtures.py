"""Fixtures for authenticated API access and resettable account state."""

from __future__ import annotations

import pytest

from tests.support.api_client import BettingApi
from tests.utils.settings import Settings


@pytest.fixture(scope="session")
def api(settings: Settings) -> BettingApi:
    return BettingApi(settings.base_url, settings.user_id)


@pytest.fixture
def reset_balance_before_and_after(api: BettingApi):
    """Test setup and cleanup for any check that can place a bet.

    Pytest runs the first reset before the test body, pauses at ``yield`` while the test
    runs, then attempts a second reset as cleanup. The test still reads the balance back
    before using it because the hosted reset response is currently inconsistent.
    """
    api.reset_balance()
    yield
    api.reset_balance()
