from decimal import Decimal

from pages.betting_page import BettingPage


def test_place_valid_bet(driver):
    """
    Critical E2E test.

    Verify that a valid single bet can be placed
    and that the success receipt displays the
    correct match, stake, odds and potential payout.
    """

    betting_page = BettingPage(driver)

    # Open application
    betting_page.open()

    # Select Home for the first upcoming match
    home_team, away_team, odds = (
        betting_page.select_upcoming_home()
    )

    # Get balance after the page has loaded
    starting_balance = betting_page.get_balance()

    stake = Decimal("10.00")

    expected_match = (
        f"{home_team} vs {away_team}"
    )

    expected_payout = (
        stake * odds
    ).quantize(Decimal("0.01"))

    # Enter stake
    betting_page.enter_stake(stake)

    # Validate payout shown in bet slip
    displayed_payout = (
        betting_page.get_potential_payout()
    )

    assert displayed_payout == expected_payout, (
        f"Bet slip payout is incorrect. "
        f"Expected EUR {expected_payout}, "
        f"but got EUR {displayed_payout}."
    )

    # Place bet
    betting_page.place_bet()

    # Get success receipt
    receipt = betting_page.get_receipt()

    print(
        "\nStarting balance:",
        starting_balance
    )

    print(
        "Match:",
        expected_match
    )

    print(
        "Odds:",
        odds
    )

    print(
        "Stake:",
        stake
    )

    print(
        "Expected payout:",
        expected_payout
    )

    print(
        "Receipt:",
        receipt
    )

    # Collect all receipt validation failures
    errors = []

    if receipt["match"] != expected_match:
        errors.append(
            f"Incorrect match: expected '{expected_match}', "
            f"got '{receipt['match']}'"
        )

    if receipt["stake"] != stake:
        errors.append(
            f"Incorrect stake: expected EUR {stake}, "
            f"got EUR {receipt['stake']}"
        )

    if receipt["odds"] != odds:
        errors.append(
            f"Incorrect odds: expected {odds}, "
            f"got {receipt['odds']}"
        )

    if receipt["payout"] != expected_payout:
        errors.append(
            f"Incorrect payout: expected EUR {expected_payout}, "
            f"got EUR {receipt['payout']}"
        )

    # Close receipt
    betting_page.close_receipt()

    # Fail once with all detected receipt problems
    assert not errors, "\n".join(errors)