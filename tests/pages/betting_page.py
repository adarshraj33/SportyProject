"""Page object for the single-bet flow."""

from __future__ import annotations

from decimal import Decimal

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as conditions

from tests.pages.base_page import BasePage


class BettingPage(BasePage):
    """Keep selectors and betting actions out of the test itself."""

    MATCH_LIST = (By.ID, "match-list")
    BET_SLIP_COUNT = (By.ID, "bet-slip-count")
    EMPTY_SLIP_MESSAGE = (By.CSS_SELECTOR, ".betSlipBodyEmpty")
    STAKE_INPUT = (By.ID, "bet-slip-stake-input")
    PLACE_BET = (By.ID, "bet-slip-place-bet")
    SUCCESS_MODAL = (By.ID, "modal-success")
    SUCCESS_CLOSE = (By.ID, "modal-success-close")
    ERROR_MODAL = (By.ID, "modal-error")
    SUCCESS_MATCH = (By.ID, "modal-success-match")
    SUCCESS_STAKE = (By.ID, "modal-success-stake")
    SUCCESS_ODDS = (By.ID, "modal-success-odds")
    SUCCESS_PAYOUT = (By.ID, "modal-success-payout")
    HEADER_BALANCE = (By.ID, "header-balance")

    def open(self, base_url: str, user_id: str) -> None:
        self.driver.get(f"{base_url}/?user-id={user_id}")
        self.wait.until(conditions.presence_of_element_located(self.MATCH_LIST))

    def select_home_win(self, match_id: str) -> None:
        self.click((By.ID, f"odds-{match_id}-home"))

    def selected_bet_count(self) -> int:
        return int(self.text(self.BET_SLIP_COUNT))

    def empty_slip_message(self) -> str:
        return self.text(self.EMPTY_SLIP_MESSAGE)

    def enter_stake(self, stake: Decimal) -> None:
        self.fill(self.STAKE_INPUT, f"{stake:.2f}")

    def submit_bet(self) -> None:
        self.click(self.PLACE_BET)

    def can_place_bet(self) -> bool:
        button = self.wait.until(conditions.visibility_of_element_located(self.PLACE_BET))
        return button.is_enabled()

    def wait_for_placement_result(self) -> str:
        """Wait for either final state and return the state that the user sees."""
        self.wait.until(
            conditions.any_of(
                conditions.visibility_of_element_located(self.SUCCESS_MODAL),
                conditions.visibility_of_element_located(self.ERROR_MODAL),
            )
        )
        success_modals = self.driver.find_elements(*self.SUCCESS_MODAL)
        if success_modals and success_modals[0].is_displayed():
            return "success"
        return "error"

    def close_success_receipt(self) -> None:
        self.click(self.SUCCESS_CLOSE)
        self.wait.until(conditions.invisibility_of_element_located(self.SUCCESS_MODAL))
