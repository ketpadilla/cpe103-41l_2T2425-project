from utils import prompt_continue, print_header, print_bank_name, clear_screen
from typing import Final, List, Dict
from time import sleep
from cli import BANK_NAME, DB_PATH
import csv
import re
import random


class User:
    """Represents a user in the banking system."""

    def __init__(self):
        """Initializes a User instance with default values."""
        self.account_id: str = None
        self.name: str = ""
        self.balance: float = 0.0

    def login(self) -> None:
        """Handles the user login process.

        Prompts the user for an account ID and PIN. Validates the credentials and logs the user in if valid.
        """
        PROMPT_STR: Final[str] = 'Login'
        STR_LEN, PADDING = print_bank_name(BANK_NAME)
        TOTAL_WIDTH: Final[int] = (2 * PADDING) + max(STR_LEN, len(PROMPT_STR))
        print_header(PROMPT_STR, TOTAL_WIDTH)

        attempts_id = 3
        while attempts_id > 0:
            account_id = input("Enter Account ID: ")

            if not self.is_valid_account_id_format(account_id):
                print("Invalid Account ID. Please try again.")
            else:
                found = False
                with open(DB_PATH, mode='r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row['account_id'] == account_id:
                            found = True
                            attempts_pin = 3
                            while attempts_pin > 0:
                                if row['pin'] == self.get_pin():
                                    self.account_id = row['account_id']
                                    return
                                print("Incorrect PIN. Please try again.")
                                attempts_pin -= 1
                                print(f"\nAttempts Left: {attempts_pin}")
                            print("\nToo many attempts.")
                            return

                if not found:
                    print("Account ID not found. Please try again.")

            attempts_id -= 1
            print(f"\nAttempts Left: {attempts_id}")
        print("\nToo many attempts.")

    def is_valid_account_id_format(self, account_id: str) -> bool:
        """Validates the format of the account ID.

        Args:
            account_id (str): The account ID to validate.

        Returns:
            bool: True if the account ID is in the format 'XXXX-XXXX-XXXX', False otherwise.
        """
        return re.fullmatch(r"\d{4}-\d{4}-\d{4}", account_id) is not None

    def get_pin(self) -> str:
        """Prompts the user to enter a PIN and validates its format.

        Returns:
            str: The valid PIN entered by the user, or None if invalid.
        """
        pin = input("Enter PIN: ")
        if self.is_valid_pin(pin):
            return pin
        else:
            print("Invalid PIN Format. Please try again")
            return None

    def is_valid_pin(self, pin: str) -> bool:
        """Validates the format of the PIN.

        Args:
            pin (str): The PIN to validate.

        Returns:
            bool: True if the PIN is a 4-digit number, False otherwise.
        """
        return pin.isdigit() and len(pin) == 4

    def create_account(self) -> None:
        """Handles the creation of a new user account.

        Prompts the user for a name and PIN, generates a unique account ID, and saves the account to the database.
        """
        PROMPT_STR: Final[str] = 'Create Account'
        STR_LEN, PADDING = print_bank_name(BANK_NAME)
        TOTAL_WIDTH: Final[int] = (2 * PADDING) + max(STR_LEN, len(PROMPT_STR))
        print_header(PROMPT_STR, TOTAL_WIDTH)

        attempts_name = 3
        while attempts_name > 0:
            name: str = input("Enter Name: ")
            if not self.validate_name(name):
                print("Name must contain only letters and spaces")
            else:
                attempts_pin = 3
                while attempts_pin > 0:
                    pin = self.get_pin()
                    if pin is not None:
                        # Generate a unique account ID
                        self.account_id: str = self.generate_unique_account_id()
                        self.name: str = name
                        self.balance: float = 0.00

                        # Calculate entry_id by counting the number of rows in the CSV file
                        with open(DB_PATH, mode='r', newline='') as file:
                            reader = csv.reader(file)
                            rows = list(reader)
                            entry_id = len(rows)  # Assign the next available ID

                        # Append the new account to the CSV file
                        with open(DB_PATH, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([entry_id, self.account_id, self.name, self.balance, pin])

                        print(f"\nAccount successfully created\nYour Account ID is {self.account_id}")
                        sleep(2)
                        prompt_continue()
                        return

                    attempts_pin -= 1
                    print(f"\nAttempts Left: {attempts_pin}")
                print("\nToo many attempts.")
                return

            attempts_name -= 1
            print(f"\nAttempts Left: {attempts_name}")
        print("\nToo many attempts.")

    def validate_name(self, name: str) -> bool:
        """Validates the format of the user's name.

        Args:
            name (str): The name to validate.

        Returns:
            bool: True if the name contains only letters and spaces, False otherwise.
        """
        return bool(re.match("^[a-zA-Z ]*$", name))

    def generate_unique_account_id(self) -> str:
        """Generates a unique account ID in the format 'XXXX-XXXX-XXXX'.

        Returns:
            str: A unique account ID.
        """
        while True:
            account_id = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            if not self.account_id_exists(account_id):
                return account_id

    def account_id_exists(self, account_id: str) -> bool:
        """Checks if an account ID already exists in the database.

        Args:
            account_id (str): The account ID to check.

        Returns:
            bool: True if the account ID exists, False otherwise.
        """
        with open(DB_PATH, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == account_id:
                    return True
        return False

    def load_account_details(self) -> None:
        """Loads the account details from the database.

        Updates the user's name and balance based on the account ID.
        """
        if self.account_id is None:
            print("Error: Account ID is not set.")
            prompt_continue()
            return

        with open(DB_PATH, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['account_id'] == self.account_id:
                    self.name = row['name']
                    self.balance = float(row['balance'])
                    break

    def check_balance(self) -> None:
        """Displays the current balance of the user's account."""
        if self.account_id is None:
            print("Error: No account loaded.")
            prompt_continue()
            return

        HEADER_STR: Final[str] = 'Check Balance'
        DETAILS: List[str] = [
            f'Account #: {self.account_id}',
            f'Account Name: {self.name}',
            f'Balance: {self.balance:.2f}'
        ]

        STR_LEN, PADDING = print_bank_name(BANK_NAME)
        MAX_LEN: Final[int] = max(len(line) for line in DETAILS)
        TOTAL_WIDTH: Final[int] = (2 * PADDING) + max(STR_LEN, MAX_LEN)
        print_header(HEADER_STR, TOTAL_WIDTH)

        print('-' * TOTAL_WIDTH)
        for line in DETAILS:
            print(f'| {line.ljust(TOTAL_WIDTH - 3)}|')
        print('-' * TOTAL_WIDTH)

        prompt_continue()

    def withdraw(self) -> None:
        """Handles the withdrawal of funds from the user's account."""
        if self.account_id is None:
            print("Error: No account loaded.")
            prompt_continue()
            return

        if self.balance == 0:
            print("Account is empty.")
            prompt_continue()
            return

        HEADER_STR: str = 'Withdraw'
        STR_LEN, PADDING = print_bank_name(BANK_NAME)
        TOTAL_WIDTH: int = (2 * PADDING) + max(STR_LEN, len(HEADER_STR))
        print_header(HEADER_STR, TOTAL_WIDTH)

        amt: int = self.get_amount('withdraw', TOTAL_WIDTH)
        self.balance -= amt

        print(f"\nWithdrawing {amt:.2f} from {self.account_id}...")
        self.update_balance()
        sleep(2)

        clear_screen()
        self.show_new_balance(amt, TOTAL_WIDTH, 'Withdrawn')
        prompt_continue()

    def deposit(self) -> None:
        """Handles the deposit of funds into the user's account."""
        if self.account_id is None:
            print("Error: No account loaded.")
            prompt_continue()
            return

        HEADER_STR: str = 'Deposit'
        STR_LEN, PADDING = print_bank_name(BANK_NAME)
        TOTAL_WIDTH: int = (2 * PADDING) + max(STR_LEN, len(HEADER_STR))
        print_header(HEADER_STR, TOTAL_WIDTH)

        amt: int = self.get_amount('deposit', TOTAL_WIDTH)
        self.balance += amt

        print(f"\nDepositing {amt:.2f} to {self.account_id}...")
        self.update_balance()
        sleep(2)

        clear_screen()
        self.show_new_balance(amt, TOTAL_WIDTH, 'Deposited')
        prompt_continue()

    def get_amount(self, transaction_type: str, total_width: int) -> float:
        """Prompts the user to enter an amount for a transaction.

        Args:
            transaction_type (str): The type of transaction ('withdraw' or 'deposit').
            total_width (int): The width of the display for formatting.

        Returns:
            float: The valid amount entered by the user.
        """
        print_header(f"Enter amount to {transaction_type}", total_width)
        while True:
            amt: str = input(": ")

            try:
                amt = float(amt)
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
                continue

            if amt <= 0:
                print("Amount must be greater than zero. Please try again.")
                continue

            if transaction_type == 'withdraw' and amt > self.balance:
                print(f"Insufficient funds. Your balance is ${self.balance:.2f}. Please enter a valid amount.")
                continue
            else:
                return amt

    def show_new_balance(self, amt: int, total_width: int, action: str) -> None:
        """Displays the updated balance after a transaction.

        Args:
            amt (int): The amount involved in the transaction.
            total_width (int): The width of the display for formatting.
            action (str): The type of transaction ('Withdrawn' or 'Deposited').
        """
        HEADER_STR = f'Transaction Completed'
        print_bank_name(BANK_NAME)
        print_header(HEADER_STR, total_width)

        if action == 'Withdrawn':
            prev_balance = self.balance + amt
        elif action == 'Deposited':
            prev_balance = self.balance - amt
        else:
            prev_balance = self.balance

        DETAILS: List[str] = [
            f'Original Balance: {prev_balance:.2f}',
            f'{action} Amount: {amt:.2f}',
            f'New Balance: {self.balance:.2f}'
        ]

        sleep(1)
        print('-' * total_width)
        for line in DETAILS:
            print(f'| {line.ljust(total_width - 3)}|')
        print('-' * total_width)

        sleep(1)

    def update_balance(self) -> None:
        """Updates the user's balance in the database."""
        if self.account_id is None:
            print("Error: No account loaded.")
            return

        rows = []
        with open(DB_PATH, mode='r') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['account_id'] == self.account_id:
                    row['balance'] = f"{self.balance:.2f}"
                rows.append(row)

        with open(DB_PATH, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def get_account_id(self) -> str:
        """Returns the user's account ID.

        Returns:
            str: The account ID of the user.
        """
        return self.account_id


class Admin(User):
    """Represents an admin user in the banking system."""
    pass