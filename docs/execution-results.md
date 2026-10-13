# Single Bet Placement — Test Results

**Test date:** 13 October 2026
**Test setup:** Vercel test app, user ID `candidate-TFSLgcFZDB8D`, desktop Chrome, and API requests using the `x-user-id` header.

I tested the main bet flow and checked a few API responses. I also opened the app in Chrome to make sure the matches and bet slip loaded. I reset the balance after tests that changed it when possible.

I ran the main bet test using Selenium in headless Chrome. It was able to choose a match, enter a stake, place the bet, and open the success receipt. The test then failed because the teams were shown in the wrong order on the receipt.

## Tests I ran

### SBP-01 — Place a €10 home-win bet

**Result: Failed**

I reset the balance and got a response showing €125.50. A separate balance check, recorded in SBP-03, showed that the service had actually stored €120.00. I then placed a €10.00 Home bet on Manchester Utd vs Chelsea. The API accepted the bet (HTTP 200) and returned the correct possible payout of €24.50.

But there were problems with the response. It showed a balance of `110` and the currency as `USD`. When I checked `/api/balance`, it showed `110` again, but this time in `EUR`.

The €110 balance is consistent with deducting €10.00 from the actual stored balance of €120.00. The confirmed placement problem is the `USD` currency; the specification requires EUR in all responses.

The Selenium test found another problem: the receipt showed **Chelsea vs Manchester Utd** instead of **Manchester Utd vs Chelsea**. The test stopped there, so I did not mark the remaining receipt checks as passed.

### SBP-02 — Reject an invalid selection

**Result: Passed**

I sent a request to `POST /api/place-bet` with a valid match ID and a €10.00 stake, but used `INVALID` as the selection.

The API returned HTTP 422 with this message:

```json
{"error":"invalid_selection","message":"Selection must be one of: HOME, DRAW, AWAY."}
```

The bet was not placed. This is the correct result because the API should reject a selection that is not Home, Draw, or Away.

### SBP-03 — Check the balance after a reset

**Result: Failed**

I called `POST /api/reset-balance`. The response said the balance was €125.50. Right after that, I called `GET /api/balance` with the same user ID, but it showed €120.00.

The two values should match. The reset API said it worked, but the balance check showed a different amount.

## Other things I noticed

- The app loaded in desktop Chrome and showed 103 matches, including Manchester Utd vs Chelsea. The balance shown on the page was €125.50.
- For Selenium, I used the element IDs already in the page, such as the odds buttons and stake field. This is more reliable than choosing elements by their position.
- The minimum stake is not clear in the specification. One part says €1.01, while the error message and API documentation say €1.00.
- When I used a date filter for a past date, the app still let me place a bet on a match from that date. I logged this as BET-004.

## Bugs found during testing


### BET-001 — Balance does not reset correctly

**Severity: High**

**Steps to reproduce:**

1. Send `POST /api/reset-balance` with the user ID in the `x-user-id` header.
2. Check the balance in the response.
3. Call `GET /api/balance` with the same user ID.

**Expected result:** Both responses should show €125.50.

**Actual result:** The reset response showed €125.50, but the balance check showed €120.00.

**Why it matters:** The app says the balance was reset, but the money available to the user is different. This also makes repeated tests harder.

**Evidence:** API responses recorded.

### BET-002 — Bet API returns the wrong currency

**Severity: High**

**Steps to reproduce:**

1. Send a valid €10.00 bet to `POST /api/place-bet`.
2. Check the `currency` field in the response.

**Expected result:** The currency should be `EUR`.

**Actual result:** The bet response showed `USD`, even though the balance API showed `EUR`.

**Why it matters:** Another part of the app using this response could show the bet in the wrong currency.

**Evidence:** Direct API response captured during SBP-01 on 13 October 2026.

### BET-003 — Receipt shows the teams in the wrong order

**Severity: High**

**Steps to reproduce:**

1. Open the app using the test user ID.
2. Choose Home (`1`) for Manchester Utd vs Chelsea.
3. Enter €10.00 and place the bet.
4. Check the success receipt.

**Expected result:** The receipt should say `Manchester Utd vs Chelsea`.

**Actual result:** It said `Chelsea vs Manchester Utd`.

**Why it matters:** This can confuse the user, especially when they bet on Home or Away.

**Evidence:** Selenium test `test_home_win_receipt_and_balance_match_the_placed_bet`.

### BET-004 — App allows bets on past matches

**Severity: High**

**Steps to reproduce:**

1. Open the app with the test user ID.
2. Set the date filter to a date that has already passed.
3. Pick a match shown for that date.
4. Enter a valid stake and place the bet.

**Expected result:** The app should not let users bet on matches that have already started or finished.

**Actual result:** I was able to select a past match and place the bet. The app showed a success receipt.

**Why it matters:** Someone might be able to bet after a match has already happened and the result is known.

**Evidence:** [Past match in the bet slip](Evidence/past_event_active_bet_slip.png) and [successful bet receipt](Evidence/past_event_success_bet.png). The match was dated 25 September 2026 and marked `PAST`.

### BET-005 — Receipt shows the wrong possible payout

**Severity: Critical**

**Steps to reproduce:**

1. Choose an outcome with odds other than 2.00.
2. Enter a valid stake and place the bet.
3. Compare the payout on the receipt with stake × odds.
4. Try another stake or different odds.

**Expected result:** The payout should match the stake multiplied by the odds. For example, €1.00 at odds of 2.05 should show €2.05.

**Actual result:** The receipt showed €2.00 for every bet I checked manually. In one example, €1.00 at odds of 2.05 still showed €2.00.

**Why it matters:** Users are being shown the wrong amount they could win. This is a serious issue because it involves money.

**Evidence:** [Receipt showing €2.00 instead of €2.05](Evidence/past_event_success_bet.png).

### BET-006 — Receipt does not show which outcome was chosen

**Severity: High**

**Steps to reproduce:**

1. Choose an outcome, such as Home (`1`).
2. Enter a stake and place the bet.
3. Look at the success receipt.

**Expected result:** The receipt should show whether the user picked Home, Draw, or Away.

**Actual result:** It showed the match, stake, odds, payout, and time, but not the selected outcome.

**Why it matters:** Users cannot clearly check what they bet on. This is even more confusing when the teams are also shown in the wrong order.

**Evidence:** [Success receipt](Evidence/past_event_success_bet.png). The bet slip showed `Match Winner: Home`, but the receipt did not.

### BET-007 — Available balance is missing from the bet slip

**Severity: Medium**

**Steps to reproduce:**

1. Open the app and choose an outcome.
2. Look at the bet slip before placing the bet.

**Expected result:** The bet slip should show the available balance along with the stake and possible payout.

**Actual result:** The balance was only shown at the top of the page, not inside the active bet slip.

**Why it matters:** Users have to look somewhere else to check how much money they have before placing a bet.

**Evidence:** [Active bet slip](Evidence/active_bet_slip_missing_balance.png). The page header showed €120.00.

### BET-008 — API accepts a bet even when there is not enough balance

**Severity: Critical**

**Steps to reproduce:**

1. Reset the test user and check the balance using `GET /api/balance`.
2. Place a valid €50.00 bet to lower the balance.
3. Check the new balance.
4. Send another bet with a stake €1.00 higher than the remaining balance, keeping the stake at €100.00 or less.

**Expected result:** The API should reject the bet with HTTP 422 and `insufficient_balance`. The balance should stay the same.

**Actual result:** The API accepted the bet and returned HTTP 200.

**Why it matters:** A user can place a bet without enough money in their account. This is a serious financial issue.

**Evidence:** Automated API test `test_api_rejects_a_bet_above_the_available_balance`.

## Final automated test results

I included two tests in the final automated run. Both found bugs:

- **API test:** Failed because the API accepted a bet with a stake higher than the available balance (BET-008).
- **UI test:** Reached the success receipt, then failed because the team names were in the wrong order (BET-003).

The other bugs came from the manual tests and extra checks described above.
