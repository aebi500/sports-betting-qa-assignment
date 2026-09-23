# Strategy & Recommendations

## Why These Two Tests Were Selected for Automation

### 1. End-to-End UI Bet Placement Test

The valid single-bet placement flow was selected because it represents the most critical user journey in the application.

The automated test covers the flow from selecting an upcoming match through entering a stake, validating the calculated payout, placing the bet, and validating the success receipt.

This test provides high value because it validates several important areas in one journey:

- Match and selection handling
- Odds used for the bet
- Stake entry
- Potential payout calculation
- Successful bet placement
- Receipt accuracy

During execution, the test detected product issues where the match order in the receipt was reversed and the potential payout shown in the receipt was incorrect.

### 2. API Balance Consistency Test

The balance reset and balance retrieval APIs were selected because balance integrity is a critical business rule in a betting application.

The automated test compares the balance returned by:

`POST /api/reset-balance`

with the balance subsequently returned by:

`GET /api/balance`

This test is fast, deterministic, and validates backend state directly without relying on the UI.

It also detected a real consistency issue: the reset API reported a balance of EUR 125.50 while the persisted balance returned by `GET /api/balance` was EUR 120.00.

These two tests were chosen together because they provide coverage at two different layers:

- UI level: critical end-to-end customer journey
- API level: critical backend financial-data consistency

---

## What Was Intentionally Left as Manual Only

The remaining scenarios were kept manual for this take-home exercise because the requirement was to automate only two high-value tests.

Manual testing was used for areas where exploratory observation, visual behavior, unusual interaction patterns, or multiple input variations provided more value within the available scope.

Examples include:

- Maximum stake boundary checks
- Insufficient balance validation
- Invalid stake input behavior
- Switching between selections
- Removing selections using individual remove and Remove All controls
- Odds filtering and displayed match count
- Betting interaction with past matches
- Extremely large numeric stake values
- Rapid repeated clicks on the receipt Close button
- Repeated clicks while bet placement is in progress

Some of these scenarios would be good future automation candidates, especially boundary-value and validation tests. However, they were intentionally left manual here to keep the automation focused on the two highest-risk areas and to avoid adding unnecessary framework complexity for the assignment.

---

## Recommendations if the Project Scales

### 1. Add Automated Tests to CI/CD

The automation suite should run automatically as part of the CI/CD pipeline.

A recommended approach would be:

- Run API and fast validation tests on every pull request.
- Run critical UI smoke tests on every deployment to a QA environment.
- Run a broader regression suite on scheduled builds or before production releases.
- Publish test reports, screenshots, logs, and failure evidence as pipeline artifacts.

This would provide fast feedback to developers and reduce the risk of regressions reaching later environments.

### 2. Expand Test Layers and Improve Test Data Management

The test suite should be expanded beyond a small number of end-to-end tests.

Recommended layers include:

- API tests for balance, bet placement, validation rules, and error responses
- UI smoke tests for critical customer journeys
- Boundary and negative tests for stake rules
- Integration tests for UI/API state consistency
- Focused regression tests for previously discovered defects

Test data should also be isolated and predictable.

Instead of relying on a shared account state, each automated run should use a dedicated test user or a reliable setup mechanism that establishes the required balance and account state before execution.

Tests should be independent so that the result of one test does not affect another.

### 3. Clarify Business Rules and Expected Behaviour in the Specification

Several behaviours should be explicitly documented to avoid ambiguity between development and QA.

Examples include:

- Exact balance value expected after a reset
- Whether stake should be retained or cleared when a user changes selection
- Whether past matches must always be non-interactive
- Expected behaviour for extremely large numeric inputs
- Required fields in the success receipt
- Expected rounding rules for potential payout
- Expected handling of repeated clicks while a bet request is processing
- Expected behaviour of the displayed match count after filters are applied

Clear acceptance criteria for these rules would improve both manual and automated test coverage and reduce interpretation differences.

---

## Summary

The automation strategy focused on one critical end-to-end UI flow and one critical API business-rule validation.

The remaining scenarios were covered manually to maximize exploratory coverage within the scope of the assignment.

If the application grows, the next priorities should be CI/CD integration, broader layered automation with reliable test data, and clearer business-rule specifications.
