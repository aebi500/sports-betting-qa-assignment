# Single Bet Placement — Manual Test Plan

## Test Plan Overview

### Objective
Validate the critical single-bet placement workflow, stake validations,
selection behavior, balance handling, receipt accuracy, and persistence.

### Scope
- Single football bet placement
- Bet-slip selection and replacement
- Stake validation and boundary testing
- Balance validation
- Success receipt validation
- Selection removal
- Balance persistence after refresh

### Test Environment
- Desktop Google Chrome
- Assigned candidate User ID
- QA assignment web application
- API endpoints used where required for test setup and balance verification

### Test Approach
Risk-based manual testing covering critical user journeys, business rules,
boundary conditions, negative scenarios, and state consistency.

## TC-01: Verify successful placement of a valid single bet

Priority: Critical

Risk rationale: Bet placement is the core user journey. A failure prevents
users from placing valid bets, while incorrect balance deductions or
receipt values can cause financial discrepancies and loss of trust.

### Preconditions
- The application is open in desktop Chrome using the assigned User ID.
- An upcoming football match is available with selectable odds.
- The user has at least €10.00 available balance.
- The bet slip is empty and no bet placement is in progress.

### Steps

1. Record the starting balance in the header and bet slip.
2. Select the home-win outcome (1) for an upcoming football match.
3. Record the match name, selected outcome, and odds.
4. Enter a stake of €10.00 and check the potential payout.
5. Click Place Bet once and observe the loading state.
6. Check the success receipt and updated balance.
7. Close the receipt and check the bet slip.
8. Refresh the page and check that the updated balance persists.

### Expected Results

- The bet slip shows the selected match, home-win outcome, and correct odds.
- Potential payout equals €10.00 multiplied by the selected odds.
- The Place Bet button shows "Placing..." while processing.
- Placement completes with one success receipt.
- The receipt includes a non-empty Bet ID, correct match and selection,
  €10.00 stake, selected odds, correct potential payout, and placement timestamp.
- The header and bet-slip balances both equal the starting balance minus €10.00.
- Closing the receipt leaves no active selection.
- Refreshing the page retains the updated balance.

## TC-02: Verify bet placement is blocked when the stake exceeds the available balance

Priority: Critical

Risk rationale: Accepting a stake greater than the available balance
allows users to place bets they cannot fund. This can create negative
balances and expose the business to financial loss.

### Preconditions

- The application is open in desktop Chrome using the assigned User ID.
- An upcoming football match is available with selectable odds.
- Establish an available balance lower than the stake being tested.
- Record the actual available balance before entering the stake.
- The bet slip is empty and no bet placement is in progress.

### Test Data

- Stake: Any value greater than the recorded available balance.

### Steps

1. Record the actual available balance shown in the header and bet slip.
2. Select an outcome for an upcoming football match.
3. Enter a stake greater than the recorded available balance.
4. Check the validation message and Place Bet button.
5. If Place Bet is enabled, click it once and observe the result.
6. Check the balance, then refresh the page and check it again.

### Expected Results

- The message "Insufficient balance" is displayed.
- Bet placement is blocked or rejected.
- No success receipt is shown.
- No stake is deducted.
- The header and bet-slip balances remain unchanged from the recorded starting balance, including after refresh.

## TC-03: Verify the maximum stake boundary

Priority: High

Risk rationale: Accepting stakes above €100.00 violates the per-bet limit
and increases the business's financial exposure. Rejecting valid stakes
at or just below €100.00 prevents users from placing permitted bets.

### Preconditions

- The application is open in desktop Chrome using the assigned User ID.
- An upcoming football match is available with selectable odds.
- Ensure sufficient balance is available before each boundary test.
- Record the actual starting balance before placement.
- The bet slip is empty and no bet placement is in progress.

### Test Data

| Stake | Expected outcome |
| --- | --- |
| €99.99 | Bet accepted |
| €100.00 | Bet accepted |
| €100.01 | Bet rejected with "Maximum stake is €100.00" |

### Steps

1. Record the actual starting balance.
2. Select an outcome for an upcoming football match.
3. Enter the stake value from the test-data table.
4. Observe any validation message.
5. If Place Bet is enabled, click it once.
6. Check the placement result and balance.
7. For successful placement, verify the receipt's stake, odds,
   and potential payout, then close the receipt.
8. Refresh the page and verify the balance.
9. Restore sufficient balance and clear any active selection
   before repeating with the next stake value.

### Expected Results

- €99.99: Placement succeeds and the receipt shows a €99.99 stake.
- €100.00: Placement succeeds and the receipt shows a €100.00 stake.
- For successful bets, the remaining balance equals the recorded starting balance minus the accepted stake.
- For successful bets, potential payout equals stake multiplied
  by the selected odds, displayed to currency precision.
- €100.01: "Maximum stake is €100.00" is displayed,
  placement is blocked or rejected, and no success receipt appears.
- The rejected bet leaves the balance unchanged from the recorded starting balance.
- Header and bet-slip balances agree and persist after refresh.

## TC-04: Verify a new selection replaces the previous selection

Priority: High

Risk rationale: If a new selection does not replace the previous one,
the user could place a bet on an unintended outcome. Multiple active
selections would also violate the single-bet requirement.

### Preconditions

- The application is open in desktop Chrome using the assigned User ID.
- At least two upcoming football matches have selectable odds.
- The available balance is at least €10.00.
- The bet slip is empty and no bet placement is in progress.

### Test Data

- Stake: €10.00
- First selection: Home win (1) on match A.
- Second selection: Draw (X) on match A.
- Third selection: Away win (2) on match B.

### Steps

1. Record the starting balance.
2. Select Home win (1) on match A and enter a €10.00 stake.
3. Check the bet-slip selection, odds, and potential payout.
4. Select Draw (X) on the same match.
5. Check that only the Draw selection remains with its correct odds.
6. If the stake was cleared, re-enter €10.00. Check the potential payout.
7. Select Away win (2) on match B.
8. Check that only match B's Away selection remains with its correct odds.
9. If the stake was cleared, re-enter €10.00. Check the potential payout.
10. Verify that the balance has not changed. Do not place the bet.

### Expected Results

- The bet slip contains exactly one selection after each selection change.
- Each new selection replaces the previous selection.
- Match details, outcome, and odds match the latest selected odds button.
- With a €10.00 stake entered, potential payout equals €10.00
  multiplied by the latest selected odds.
- No previous match or outcome remains as an active bet-slip selection.
- The balance remains unchanged because no bet has been placed.

## TC-05: Verify invalid stake inputs cannot be used to place a bet

Priority: High

Risk rationale: Accepting missing, non-numeric, or over-precision stakes
can create invalid bets and incorrect financial calculations.

### Preconditions

- The application is open in desktop Chrome using the assigned User ID.
- An upcoming football match has been selected.
- Sufficient available balance is present and the starting balance is recorded.
- No bet placement is in progress.

### Test Data

| Input | Rule being checked |
| --- | --- |
| Empty field | Stake is required |
| abc | Stake must be numeric |
| 10.001 | Stake must have no more than two decimal places |

### Steps

1. Record the starting balance.
2. Clear the stake field completely.
3. Enter or paste the test input, leaving the field empty for the empty-input case.
4. Record the value actually retained in the field and any validation message.
5. Check the Place Bet button. If enabled while the field contains
   an invalid value or is empty, click it once.
6. Verify that no successful placement occurs and the balance is unchanged.
7. Repeat for each input, clearing the field between cases.
8. Refresh the page and verify that the balance remains unchanged.

### Expected Results

- An empty stake cannot be submitted successfully.
- Non-numeric text is prevented from entering the field or rejected.
- A third decimal digit is prevented, or the over-precision value
  is rejected before successful placement.
- Invalid values retained in the field receive clear validation feedback.
- No success receipt appears for an invalid or empty stake.
- No money is deducted; the balance remains unchanged after refresh.

## TC-06: Verify selection removal using X and Remove All

Priority: Medium

Risk rationale: A selection that remains active after removal could
cause an unintended bet. Removing an unplaced selection must not
deduct money from the user's balance.

### Preconditions

- The application is open in desktop Chrome using the assigned User ID.
- An upcoming football match has selectable odds.
- The available balance is at least €10.00.
- No bet placement is in progress.

### Steps

1. Record the starting balance.
2. Select an outcome and enter a €10.00 stake.
3. Click the per-selection remove button (X) in the bet slip.
4. Check that the bet slip has no active selection.
5. Check that placement cannot proceed without a selection.
6. Select an outcome again and enter a €10.00 stake.
7. Click Remove All.
8. Check that the bet slip has no active selection and placement
   cannot proceed.
9. Verify that the balance remains unchanged.

### Expected Results

- Both removal controls clear the active selection.
- The bet-slip selection count returns to zero.
- Removed match details and odds are no longer shown as an active selection.
- Bet placement is blocked without a selection.
- No success receipt appears and no stake is deducted.