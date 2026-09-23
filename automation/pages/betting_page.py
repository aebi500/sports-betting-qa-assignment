from decimal import Decimal
from urllib.parse import urlencode

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, USER_ID, WAIT_TIMEOUT


class BettingPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIMEOUT)

    def open(self):
        if not USER_ID:
            raise ValueError(
                "Set SPORTY_USER_ID before running the test."
            )

        query = urlencode(
            {
                "user-id": USER_ID
            }
        )

        self.driver.get(
            f"{BASE_URL}/?{query}"
        )

    def get_balance(self):
        element = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#header-balance > span:last-child"
                )
            )
        )

        return Decimal(
            element.text
            .split("€")[-1]
            .replace(",", "")
            .strip()
        )

    def select_upcoming_home(self):
        card = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[starts-with(@id, 'match-card-')]"
                    "[.//span[normalize-space()='UPCOMING']]"
                )
            )
        )

        teams = card.find_elements(
            By.CSS_SELECTOR,
            ".teamName"
        )

        home_team = teams[0].text.strip()
        away_team = teams[1].text.strip()

        button = card.find_element(
            By.CSS_SELECTOR,
            "button[id$='-home']"
        )

        odds = Decimal(
            button.find_element(
                By.CSS_SELECTOR,
                ".oddsButtonValue"
            ).text.strip()
        )

        self.wait.until(
            EC.element_to_be_clickable(button)
        ).click()

        return home_team, away_team, odds

    def enter_stake(self, amount):
        field = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "bet-slip-stake-input"
                )
            )
        )

        field.clear()

        field.send_keys(
            str(amount)
        )

    def get_potential_payout(self):
        element = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    "bet-slip-potential-payout"
                )
            )
        )

        return Decimal(
            element.text
            .replace("€", "")
            .replace(",", "")
            .strip()
        )

    def place_bet(self):
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "bet-slip-place-bet"
                )
            )
        ).click()

    def get_receipt(self):
        modal = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.ID,
                    "modal-success"
                )
            )
        )

        def read(element_id):
            return (
                modal.find_element(
                    By.ID,
                    element_id
                )
                .text
                .strip()
            )

        return {
            "bet_id": read(
                "modal-success-bet-id"
            ),

            "match": read(
                "modal-success-match"
            ),

            "stake": Decimal(
                read(
                    "modal-success-stake"
                )
                .replace("€", "")
                .replace(",", "")
            ),

            "odds": Decimal(
                read(
                    "modal-success-odds"
                )
            ),

            "payout": Decimal(
                read(
                    "modal-success-payout"
                )
                .replace("€", "")
                .replace(",", "")
            ),

            "placed_at": read(
                "modal-success-placed-at"
            ),
        }

    def close_receipt(self):
        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "modal-success-close"
                )
            )
        ).click()

        self.wait.until(
            EC.invisibility_of_element_located(
                (
                    By.ID,
                    "modal-success"
                )
            )
        )