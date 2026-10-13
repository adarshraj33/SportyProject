# Single Bet Placement — QA Automation

This project is my QA submission for the Single Bet Placement exercise.

I used **Python, Pytest, Selenium WebDriver, and Requests** to test the betting application. My main focus was checking that customers can place bets correctly and that the application handles money, balances, and bet confirmations safely.

## Project Deliverables

- [Test Plan](docs/test-plan.md) — six manual test scenarios covering important user journeys, validation, and boundary cases.
- [Test Results and Bugs](docs/execution-results.md) — test results and the bugs I found.
- [Automation Strategy](docs/automation-strategy.md) — what I automated, what I kept manual, and why.
- `tests/` — two automated tests: one UI test and one API test.

## Tools Used

- Python 3.10+
- Pytest
- Selenium WebDriver
- Requests
- Chrome
- uv (for installing dependencies)
- Allure (optional test reports)

## Setup

Clone the repository and open it in your terminal. Then install the project dependencies:

```bash
uv sync
```

Selenium Manager handles the ChromeDriver setup automatically if a compatible driver is not already available.

## Running the Tests

Run all tests:

```bash
uv run pytest
```

Run only the API test:

```bash
uv run pytest -m api
```

Run only the UI test:

```bash
uv run pytest -m ui
```

Run the UI test with Chrome visible:

```bash
UI_HEADLESS=false uv run pytest -m ui
```

## Test Environment

Application: https://qae-assignment-tau.vercel.app

API documentation: https://qae-assignment-tau.vercel.app/api/docs

Default test user:

```text
candidate-TFSLgcFZDB8D
```

This is a public test-user ID supplied for the exercise, not a password or API key. It is kept as the default so a reviewer can run the project without extra setup.

To use a different test user or environment:

```bash
export SPORTY_USER_ID='your-test-user'
export SPORTY_BASE_URL='https://qae-assignment-tau.vercel.app'
```

The tests use a balance reset fixture before and after tests that change account data. Because the reset API has a known issue, the tests also check the actual stored balance.

## Automated Tests

**1. UI Test — Place a Home-Win Bet**

Checks that a customer can select Home, enter a €10.00 stake, place a bet, and see the correct receipt and updated balance.

**2. API Test — Reject a Bet with Insufficient Balance**

Checks that the API rejects a bet when the stake is higher than the user's available balance.

## Current Test Results

The two automated tests currently fail because of bugs found in the application.

| Test | Result | Issue |
| --- | --- | --- |
| UI — Home-Win Bet | Failed | BET-003: The receipt shows the teams in the wrong order. |
| API — Insufficient Balance | Failed | BET-008: The API accepts a bet even when the balance is too low. |

These are application issues, not expected behaviour. I kept the assertions in place so the tests can help verify fixes later.

Other bugs and manual test results are documented in [Execution Results](docs/execution-results.md).

## Test Reports

The tests save Allure result data in `allure-results/`. If the Allure command-line tool is installed, you can view the report with:

```bash
allure serve allure-results
```

On macOS, install the command-line tool once with:

```bash
brew install allure
```

`allure-results/` and generated `allure-report/` files are ignored by Git.

## Project Structure

```text
docs/
  test-plan.md
  execution-results.md
  automation-strategy.md

tests/
  api/         # API tests
  ui/          # Selenium UI tests
  pages/       # Page Object Model
  fixtures/    # Test setup and cleanup
  support/     # API helper
  utils/       # Configuration
```

## Final Notes

I focused on automating the main betting journey and the API balance check because mistakes in these areas can directly affect customers and their money. I also used manual and exploratory testing to check other parts of the application.

The test plan, bug reports, and automation recommendations are in the `docs/` folder.
