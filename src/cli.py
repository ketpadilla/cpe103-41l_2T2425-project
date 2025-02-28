import os
from utils import clear_screen, print_menu, ask_option, prompt_new_transaction, start_transaction, exit_program
from models import *
from typing import Final, Callable, List

BANK_NAME: Final[str] = 'Filipinas Incorporated'
DB_PATH: Final[str] = 'data/users.csv'
  
def main():
  clear_screen()
  usr_op: int = start_transaction(BANK_NAME)
  
  if usr_op == 2:
    exit_program()

  clear_screen()
  user: User = User()

  if usr_op == 0:
    status: bool = user.login()

  elif usr_op == 1:
    user.create_account()

  else:
    print("Error. Please Restart.")

  if (user.get_account_id() == None):
    print("\nNo Account ID set. Please Try Again")
    exit_program()

  clear_screen()
  
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
    print_menu(BANK_NAME, TX_OPTIONS)
    option: int = ask_option(TX_OPTIONS)

    clear_screen()
    TX_FUNCTIONS[option]()

    if (prompt_new_transaction(BANK_NAME)):
      clear_screen()
      continue
    else:
      print(f'\nThank you for using {BANK_NAME}. See you next time!')
      TX_FUNCTIONS[3]()

if __name__ == '__main__':
  main()