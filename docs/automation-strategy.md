# Automation Strategy and Recommendations

## The Two Tests I Chose to Automate

### 1. UI Test: Place a Home-Win Bet

I chose this test because placing a bet is the main feature of the application, and it is important to make sure everything works correctly.

The test selects Home for a match, enters a €10.00 stake, and places the bet. It then checks that the receipt shows the correct match, stake, odds, and payout. It also checks that the balance is updated correctly and the bet slip is cleared after closing the receipt.

I picked this test because even if a bet is placed successfully, the customer might still see the wrong information on the receipt or have the wrong amount taken from their balance.

### 2. API Test: Reject a Bet When the Balance Is Too Low

I chose this test because the application should never allow a customer to bet more money than they have.

The test first places a bet to reduce the user's balance. It then tries to place another bet with a stake higher than the remaining balance, but still below the €100 maximum stake.

The expected result is that the API rejects the bet and does not take any money.

I chose to automate this because checking the balance only in the browser is not enough. Someone could send a request directly to the API, so the API must also check that the user has enough money.

## What I Kept for Manual Testing and Why

I decided to keep some tests manual, such as changing or removing selections, trying different stake values, checking date and odds filters, and checking the page layout and loading messages.

These are still important tests, but I wanted to focus the automation on the areas where a problem could directly affect a customer's money or bet details.

I also kept the error message and Rebet feature as manual tests. This is because there is no reliable way to make a bet fail on purpose in the test environment. Automating this could cause the test to fail randomly.

Other API checks, such as sending invalid JSON, using incorrect match IDs, unsupported request methods, or placing multiple bets at the same time, can also be tested manually for now.

## Recommendations for the Future

If I had more time to work on this project, I would suggest the following improvements.

**1. Run automated tests regularly**

I would run the API test whenever new code is added and run the main UI test in Chrome regularly.

This would help catch important problems early. I would also make sure failed tests are reported properly rather than ignored.

**2. Improve the test environment**

I would recommend having a reliable way to reset the user's balance, separate test users, and matches that have not started yet.

It would also help to have a way to trigger a bet placement failure on purpose. This would make testing the error message and Rebet feature easier and more reliable.

**3. Make the requirements clearer**

Before adding more automated tests, I would clarify a few things in the requirements.

For example, the minimum stake is mentioned as both €1.00 and €1.01 in different places.

I would also confirm how payouts should be rounded, how invalid odds filters should behave, and exactly what information should appear on the bet receipt.

Having clear requirements would make it easier to write accurate tests and avoid confusion later.

## Final Thoughts

For this exercise, I focused on automating two important areas: making sure a normal bet is placed correctly and making sure the API does not accept bets when the user has insufficient funds.

I think these are good starting points because they cover the main customer journey and an important money-related validation rule.

The remaining tests can be done manually for now and added to automation later as the application and test environment improve.
