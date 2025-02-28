import os
from utils import clear_screen, print_menu, ask_option, prompt_new_transaction, start_transaction, exit_program
from models import *
from typing import Final, Callable, List

# Constants for the bank name and database path
BANK_NAME: Final[str] = 'Filipinas Incorporated'
DB_PATH: Final[str] = 'data/users.csv'


def main():
    """Main function to run the banking application.

    This function handles the main flow of the banking application, including user login,
    account creation, and transaction management.
    """
    clear_screen()
    usr_op: int = start_transaction(BANK_NAME)

    if usr_op == 2:
        exit_program()

    clear_screen()
    user: User = User()

    if usr_op == 0:
        # Attempt to log in the user
        user.login()
        user.load_account_details()
    elif usr_op == 1:
        # Create a new account for the user
        user.create_account()
    else:
        print("Error. Please Restart.")

    # Check if the account ID is set
    if user.get_account_id() is None:
        print("\nNo Account ID set. Please Try Again")
        exit_program()

    clear_screen()

    # Define transaction options and their corresponding functions
    TX_OPTIONS: Final[List[str]] = [
        'Check Balance',
        'Withdraw',
        'Deposit',
        'Cancel Transaction'
    ]

    TX_FUNCTIONS: Final[List[Callable[[], None]]] = [
        user.check_balance,
        user.withdraw,
        user.deposit,
        exit_program,
    ]

    while True:
        # Display the transaction menu and get the user's choice
        print_menu(BANK_NAME, TX_OPTIONS)
        option: int = ask_option(TX_OPTIONS)

        clear_screen()
        # Execute the selected transaction function
        TX_FUNCTIONS[option]()

        # Prompt the user for a new transaction
        if prompt_new_transaction(BANK_NAME):
            clear_screen()
            continue
        else:
            print(f'\nThank you for using {BANK_NAME}. See you next time!')
            TX_FUNCTIONS[3]()


if __name__ == '__main__':
    main()