# Single Bet Placement — Test Plan

**Scope:** Desktop web, upcoming football matches, single bets only.

I’ve focused on six scenarios that cover the main betting journey, stake validation, changing selections, failed placements, filters, and API checks. My main concern is making sure customers are charged the correct amount, know whether their bet went through, and cannot place a bet with invalid details.

## SBP-01 — Place a single bet successfully

**Priority:** Critical

**Risk Rationale:** This is the main flow customers will use. Even if the bet appears to go through, an incorrect deduction or receipt could cause a serious problem.

**Steps:**
1. Open the app using the provided user ID and check the starting balance.
2. Choose **1 (Home)** for Manchester Utd vs Chelsea at odds of **2.45**.
3. Enter a **€10.00** stake and check the potential payout shown in the bet slip.
4. Click **Place Bet** and wait for the result.
5. Check the receipt, close it, and look at the updated balance and bet slip.

**Expected Result:** Only one selection is in the slip. The button displays **Placing...** while the request is being processed. The receipt shows the correct match, Home selection, €10.00 stake, 2.45 odds, and €24.50 potential payout. The balance is reduced by exactly €10.00, and the bet slip is empty after the receipt is closed.

## SBP-02 — Check stake validation and limit boundaries

**Priority:** Critical

**Risk Rationale:** Stake validation directly affects customers' money. The app and API should both prevent stakes that are too small, too large, incorrectly formatted, or higher than the available balance.

**Steps:**
1. Add an outcome to the bet slip.
2. Leave the stake blank. Attempt to enter `abc` and `10.999`, and note whether the input blocks or trims invalid characters. Then test `0.99`, `1.00`, `1.01`, `100.00`, and `100.01`.
3. To test insufficient balance, first lower the balance with a valid bet, then enter an amount above the remaining balance but no more than €100.00.
4. For each value, check the validation message and whether **Place Bet** is enabled.
5. Send a few invalid stake values directly to `POST /api/place-bet` to confirm the backend also validates them.
6. Check that the balance has not changed after rejected requests.

**Expected Result:** Only valid numeric stakes with no more than two decimal places, within the agreed minimum and maximum limits, and within the customer's available balance can be placed. Invalid values show a useful message and cannot be submitted. The API also rejects invalid stakes without deducting money.

**Clarification needed:** The specification appears to mention both **€1.00** and **€1.01** as the minimum stake. This should be confirmed before deciding which boundary value should pass.

## SBP-03 — Change or remove a selection

**Priority:** High

**Risk Rationale:** The feature only supports one selection at a time. If a previous selection remains in the slip, a customer could accidentally place a bet on the wrong outcome.

**Steps:**
1. Select **1** for one match.
2. Select **X** for a different match, then **2** for another match.
3. Check the bet slip after each selection.
4. Remove the current selection using the small **x** beside it.
5. Add another selection, enter a stake, and use **Remove All**.

**Expected Result:** Each new selection replaces the previous one, so the bet slip never contains more than one outcome. The match, outcome, odds, and payout update to match the latest selection. Both removal options clear the selection and stake, and the customer cannot place a bet with an empty slip.

## SBP-04 — Handle a failed bet placement

**Priority:** High

**Risk Rationale:** A failed request can leave customers unsure whether their money was taken. The error flow should be clear and should not create duplicate bets or leave old details in the slip.

**Steps:**
1. Add a valid selection and stake.
2. Use the test environment to trigger a placement failure.
3. Check the error message and available actions: **Rebet**, **Close**, and the top-right **x**.
4. Select **Rebet** and check what happens.
5. Repeat the failure and close the error using **Close**, then repeat it again using the top-right **x**.
6. Check the balance and bet slip after each attempt.

**Expected Result:** The customer sees a clear error and knows what they can do next. **Rebet** retries the same valid selection and stake. **Close** and **x** dismiss the error and clear the bet slip. A failed bet should not deduct money, and retrying must not result in duplicate bets. If the original request's outcome is uncertain, the app must confirm its status before retrying rather than risk placing it twice.

## SBP-05 — Check date and odds filter boundaries

**Priority:** Medium

**Risk Rationale:** Incorrect filters may hide matches that should be available or show matches outside the customer's chosen range. Boundary values are especially easy to get wrong.

**Steps:**
1. Filter matches to a single kickoff date and check the results.
2. Set a date range with known matches on both the start and end dates.
3. Set minimum and maximum odds to values that exactly match odds shown on available outcomes.
4. Check whether outcomes at both limits are included.
5. Try setting the minimum odds higher than the maximum, and then try non-numeric values.

**Expected Result:** Matches on the selected date and both endpoints of a date range are included. Odds exactly equal to the minimum or maximum are also included. Invalid odds ranges are not applied, and the customer receives a clear validation message.

## SBP-06 — Validate API requests and user isolation

**Priority:** Medium

**Risk Rationale:** Frontend validation alone is not enough because requests can be sent directly to the API. The backend must reject malformed or unauthorized requests without changing account data.

**Steps:**
1. Call the relevant endpoints with a missing `x-user-id` header, a blank header, and a valid user ID.
2. Try malformed JSON, a JSON array instead of the expected object, unknown or blank match IDs, an invalid selection, and a stake with too many decimal places.
3. Try an unsupported HTTP method.
4. Check the response status and error message for each invalid request.
5. Reset the test user's balance and immediately read it back using the same user ID.
6. Where separate test users are available, verify that one user's requests do not affect another user's balance.

**Expected Result:** Missing or invalid authentication information and unsupported methods return the status codes defined by the API contract. Invalid bet details return **422** with a useful error code or message. Rejected requests do not change balances or create bets. After a reset, the returned balance matches the balance retrieved for that same user, and one user's actions do not affect another user's account.
