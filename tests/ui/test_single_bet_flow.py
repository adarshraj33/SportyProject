"""UI check for placing one normal football bet."""

from decimal import Decimal

import allure
import pytest

from tests.pages.betting_page import BettingPage


@pytest.mark.ui
@pytest.mark.usefixtures("reset_balance_before_and_after")
@allure.title("Place a home-win bet and verify its receipt and balance")
@allure.severity(allure.severity_level.CRITICAL)
def test_home_win_receipt_and_balance_match_the_placed_bet(
    api, driver, settings
):
    """A normal home-win bet should show the right receipt and remaining balance."""
    matches = api.get_matches()
    assert matches, "The test needs at least one match"
    match = matches[0]
    stake = Decimal("10.00")
    expected_odds = Decimal(str(match["odds"]["home"]))
    starting_balance = Decimal(str(api.get_balance()["balance"]))
    expected_payout = stake * expected_odds
    expected_balance = starting_balance - stake

    expected_match = f'{match["homeTeam"]} vs {match["awayTeam"]}'
    expected_stake_text = f"€{stake:.2f}"
    expected_odds_text = f"{expected_odds:.2f}"
    expected_payout_text = f"€{expected_payout:.2f}"
    expected_header_balance = f"Balance: €{expected_balance:.2f}"

    page = BettingPage(driver)
    page.open(settings.base_url, settings.user_id)
    page.select_home_win(match["id"])
    page.enter_stake(stake)
    assert page.can_place_bet()
    page.submit_bet()

    placement_result = page.wait_for_placement_result()
    assert placement_result == "success"
    assert page.text(page.SUCCESS_MATCH) == expected_match
    assert page.text(page.SUCCESS_STAKE) == expected_stake_text
    assert page.text(page.SUCCESS_ODDS) == expected_odds_text
    assert page.text(page.SUCCESS_PAYOUT) == expected_payout_text
    assert page.text(page.HEADER_BALANCE) == expected_header_balance

    persisted_balance = Decimal(str(api.get_balance()["balance"]))
    assert persisted_balance == expected_balance

    page.close_success_receipt()
    assert page.selected_bet_count() == 0
    assert page.empty_slip_message() == "Select odds to place a bet"
