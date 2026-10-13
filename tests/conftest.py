"""Register shared fixtures and expose one settings fixture to every test."""

from __future__ import annotations

import pytest

from tests.utils.settings import Settings

pytest_plugins = (
    "tests.fixtures.api_fixtures",
    "tests.fixtures.browser_fixtures",
)


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.from_environment()
