"""API check for the balance-protection business rule."""

from decimal import Decimal

import allure
import pytest


@pytest.mark.api
@pytest.mark.usefixtures("reset_balance_before_and_after")
@allure.title("Reject a bet that costs more than the available balance")
@allure.severity(allure.severity_level.CRITICAL)
def test_api_rejects_a_bet_above_the_available_balance(api):
    """The API must stop a customer from betting money they do not have.

    This is the chosen API test because browser validation can be bypassed. The service
    itself must protect the customer's available funds.
    """
    matches = api.get_matches()
    assert matches, "The test needs at least one match"
    match = matches[0]

    # The reset balance is above the €100 stake cap. Place €50 first so a valid-format
    # stake can be greater than the remaining balance without exceeding that cap.
    setup_stake = Decimal("50.00")
    balance_before_setup = Decimal(str(api.get_balance()["balance"]))
    assert balance_before_setup >= setup_stake

    setup_response = api.place_bet(
        {"matchId": match["id"], "selection": "HOME", "stake": float(setup_stake)}
    )
    assert setup_response.status_code == 200

    remaining_balance = Decimal(str(api.get_balance()["balance"]))
    rejected_stake = remaining_balance + Decimal("1.00")
    assert rejected_stake <= Decimal("100.00")

    response = api.place_bet(
        {
            "matchId": match["id"],
            "selection": "HOME",
            "stake": float(rejected_stake),
        }
    )

    assert response.status_code == 422
    assert response.json()["error"] == "insufficient_balance"
    assert Decimal(str(api.get_balance()["balance"])) == remaining_balance
