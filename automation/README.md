# QA Automation - Take-Home Assignment

This project contains automated UI and API tests created for the QA Engineer take-home assignment.

The automation focuses on two high-value areas:

1. End-to-end bet placement through the UI.
2. Balance consistency validation through the API.

---

## Tech Stack

- Python 3
- Pytest
- Selenium WebDriver
- Requests
- Google Chrome

---

## Project Structure

```text
automation/
├── config.py
├── conftest.py
├── requirements.txt
├── README.md
├── pages/
│   ├── __init__.py
│   └── betting_page.py
└── tests/
    ├── test_api_balance.py
    └── test_place_bet.py
```

### File Description

`config.py`  
Contains application URL, user ID configuration and wait timeout.

`conftest.py`  
Contains the Pytest WebDriver fixture used to launch and close Chrome.

`pages/betting_page.py`  
Contains the Page Object Model for the betting application.

`tests/test_place_bet.py`  
Contains the end-to-end UI automation test.

`tests/test_api_balance.py`  
Contains the API balance consistency test.

`requirements.txt`  
Contains the Python dependencies required to execute the automation.

---

# Automated Tests

## 1. End-to-End UI Test

File:

`tests/test_place_bet.py`

### Test Objective

Verify that a user can place a valid single bet and that the success receipt contains the correct bet information.

### Test Flow

The automation:

- Opens the betting application using the configured user ID.
- Finds the first available upcoming match.
- Selects the Home outcome.
- Captures the selected teams and odds.
- Enters a valid stake of €10.00.
- Calculates the expected potential payout.
- Validates the potential payout displayed in the bet slip.
- Places the bet.
- Reads the success receipt.
- Validates the match, stake, odds and potential payout.
- Closes the success receipt.

### Why This Test Was Selected

Bet placement is a critical user journey in a betting application.

Incorrect match information, odds, stake or payout displayed after bet placement could create a significant user trust and financial-impact risk.

### Current Result

The automation successfully completes the betting journey but detects issues in the success receipt.

Observed example:

Expected:

```text
Match: Leeds vs Norwich
Stake: €10.00
Odds: 2.05
Potential Payout: €20.50
```

Actual receipt:

```text
Match: Norwich vs Leeds
Stake: €10.00
Odds: 2.05
Potential Payout: €20.00
```

The automated test therefore fails with validation errors similar to:

```text
Incorrect match: expected 'Leeds vs Norwich', got 'Norwich vs Leeds'
Incorrect payout: expected €20.50, got €20.00
```

The match used by the test is selected dynamically, so the exact teams may differ in future executions.

---

## 2. API Balance Consistency Test

File:

`tests/test_api_balance.py`

### Test Objective

Verify that the balance returned by the reset-balance API matches the balance actually persisted by the application.

### APIs Used

```text
POST /api/reset-balance
GET /api/balance
```

### Test Flow

The automation:

- Sends a request to reset the user's balance.
- Validates that the reset request returns HTTP 200.
- Captures the balance and currency returned by the reset API.
- Calls the balance API for the same user.
- Validates that the balance request returns HTTP 200.
- Validates the currency.
- Compares the reset API balance with the subsequently persisted balance.

### Why This Test Was Selected

Balance consistency is a critical business rule in a betting application.

If an API reports that a balance has been reset to one value while another value is actually stored, the application can present incorrect financial information to the user.

### Current Result

Observed response from:

`POST /api/reset-balance`

```text
{
    "message": "Balance reset successfully",
    "balance": 125.5,
    "currency": "EUR"
}
```

Subsequent response from:

`GET /api/balance`

```text
{
    "balance": 120,
    "currency": "EUR"
}
```

The automated test therefore fails with:

```text
Balance inconsistency detected.
Reset API returned €125.5,
but GET /api/balance returned €120.
```

This indicates that the response returned by the reset API is inconsistent with the persisted account balance.

---

# Setup Instructions

## 1. Navigate to the Automation Directory

Example:

```powershell
cd "C:\Users\baner\Documents\Sporty Group\automation"
```

## 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

## 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should show:

```text
(.venv)
```

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# User ID Configuration

The application requires a user ID for both UI and API requests.

Set the environment variable before executing the tests.

Windows PowerShell:

```powershell
$env:SPORTY_USER_ID="<your-user-id>"
```

Example:

```powershell
$env:SPORTY_USER_ID="candidate-cyIa0M4Z55U4"
```

Verify the configured value:

```powershell
echo $env:SPORTY_USER_ID
```

---

# Running the Tests

## Run All Automated Tests

From the `automation` directory:

```powershell
python -m pytest tests -v -s
```

## Run Only the UI Test

```powershell
python -m pytest tests/test_place_bet.py -v -s
```

## Run Only the API Test

```powershell
python -m pytest tests/test_api_balance.py -v -s
```

---

# Current Test Execution Result

A complete execution currently collects two tests:

```text
collected 2 items
```

The current application behavior results in:

```text
test_api_balance.py::test_reset_balance_matches_persisted_balance FAILED

test_place_bet.py::test_place_valid_bet FAILED
```

These failures are caused by application behavior detected by the automated validations.

They are not expected-pass tests that have been modified to force a successful result.

The assertions intentionally validate the expected business behavior so that defects remain visible during execution.

---

# Notes

The UI automation uses explicit waits instead of fixed sleep statements wherever possible.

The Page Object Model is used to separate page interactions from test validations.

The user ID is provided through an environment variable rather than being hardcoded inside the automation code.

The UI test dynamically selects an upcoming match instead of depending on a specific match being permanently available.

The API test uses Python `requests` and validates both HTTP responses and business-data consistency.