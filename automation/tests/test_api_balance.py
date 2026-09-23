import requests

from config import BASE_URL, USER_ID


def test_reset_balance_matches_persisted_balance():
    """
    High-value API test.

    Verify that the balance returned by POST /api/reset-balance
    matches the balance actually persisted and returned by
    GET /api/balance.
    """

    assert USER_ID, (
        "SPORTY_USER_ID is not set."
    )

    headers = {
        "x-user-id": USER_ID
    }

    # Step 1: Reset balance
    reset_response = requests.post(
        f"{BASE_URL}/api/reset-balance",
        headers=headers,
        timeout=10
    )

    assert reset_response.status_code == 200, (
        f"Reset balance API failed. "
        f"Expected status 200, "
        f"got {reset_response.status_code}."
    )

    reset_body = reset_response.json()

    # Step 2: Get persisted balance
    balance_response = requests.get(
        f"{BASE_URL}/api/balance",
        headers=headers,
        timeout=10
    )

    assert balance_response.status_code == 200, (
        f"Get balance API failed. "
        f"Expected status 200, "
        f"got {balance_response.status_code}."
    )

    balance_body = balance_response.json()

    # Print values for evidence
    print(
        "\nReset API response:",
        reset_body
    )

    print(
        "GET balance response:",
        balance_body
    )

    # Step 3: Validate currency
    assert reset_body["currency"] == "EUR"

    assert balance_body["currency"] == "EUR"

    # Step 4: Validate persisted balance
    assert reset_body["balance"] == balance_body["balance"], (
        f"Balance inconsistency detected. "
        f"Reset API returned EUR {reset_body['balance']}, "
        f"but GET /api/balance returned "
        f"EUR {balance_body['balance']}."
    )