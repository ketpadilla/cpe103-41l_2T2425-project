import os
from typing import Final, Dict, Tuple
from time import sleep

def start_transaction(bank_name: str) -> bool:
    HEADER_STR = "Welcome"
    STR_LEN, PADDING = print_bank_name(bank_name) 
    TOTAL_WIDTH: Final[int] = (2 * PADDING) + max(STR_LEN, len(HEADER_STR))
    print_header(HEADER_STR, TOTAL_WIDTH)

    START_OPTIONS: Final[List[str]] = [
      'Start',
      'Create Account',
      'Quit'
    ]

    ascii_num: int = ord('A')

    print('-' * TOTAL_WIDTH)
    for incr in range(len(START_OPTIONS)):
      option_text = f"{chr(ascii_num)}. {START_OPTIONS[incr]}"
      print(f"| {option_text.ljust(TOTAL_WIDTH - 3)}|") 
      ascii_num += 1
    print('-' * TOTAL_WIDTH)

    option: int = ask_option(START_OPTIONS)
    return option 

def clear_screen() -> None:
  """Clears the console screen based on the operating system."""
  os.system('cls' if os.name == 'nt' else 'clear')

def print_bank_name(bank_name: str, prefix: str = "", suffix: str = "") -> Tuple[int, int]:
  """Prints the bank name and returns the length of the printed string and padding."""
  PADDING: Final[int] = 5
  PRINT_STR: Final[str] = f"{prefix} {bank_name} {suffix}".strip()
  STR_LEN: Final[int] = len(PRINT_STR)
  TOTAL_WIDTH: Final[int] = (2 * PADDING) + STR_LEN

  print('-' * (TOTAL_WIDTH), end="\n|")
  print(PRINT_STR.center(TOTAL_WIDTH - 2), end="|\n")
  print('-' * (TOTAL_WIDTH))

  return STR_LEN, PADDING

def print_header(header: str, TOTAL_WIDTH: Final[int]) -> None:
  """Print Screen Header and adjust to total width of contents"""
  print('-' * TOTAL_WIDTH)
  print(f"| {header.center(TOTAL_WIDTH - 3)}|") 
  print('-' * TOTAL_WIDTH)

def print_menu(bank_name: str, options: list[str]) -> None:
  """Prints a menu with options and adjusts to bank name length."""
  STR_LEN, PADDING = print_bank_name(bank_name) 

  MAX_LEN: Final[int] = max(len(option) for option in options)
  TOTAL_WIDTH: Final[int] = (2 * PADDING) + max(STR_LEN, MAX_LEN)
  print_header('Start Transaction', TOTAL_WIDTH)

  ascii_num: int = ord('A')

  print('-' * TOTAL_WIDTH)
  for incr in range(len(options)):
    option_text = f"{chr(ascii_num)}. {options[incr]}"
    print(f"| {option_text.ljust(TOTAL_WIDTH - 3)}|") 
    ascii_num += 1
  print('-' * TOTAL_WIDTH)

def ask_option(options: list[str]) -> int:
  """Prompts the user to select an option from a list and returns the chosen option."""
  
  NUM_OPTIONS: int = len(options)

  while True:
    usr_op: str = input("Enter the letter of your choice: ").strip().upper()
      
    if len(usr_op) == 1 and ord('A') <= ord(usr_op) <= ord('A') + NUM_OPTIONS - 1:
      return ord(usr_op.upper()) - ord('A')
    else:
      print(f"Invalid choice. Please try again.")

def exit_program() -> None:
  print("Terminating Transaction...")
  sleep(1.5)
  exit(0)

def prompt_new_transaction(bank_name: str) -> bool:
  clear_screen()
  
  PROMPT_STR: Final[str] = 'Would you like to make another transaction?'
  STR_LEN, PADDING = print_bank_name(bank_name) 
  TOTAL_WIDTH: Final[int] = (2 * PADDING) + max(STR_LEN, len(PROMPT_STR))
  print_header(PROMPT_STR, TOTAL_WIDTH)

  while True:
    usr_op: str = input("(Y/N): ")

    if usr_op.upper() in ['Y', 'N']:
      return usr_op.upper() == 'Y'
    else:
      print(f"Invalid choice. Please try again.")

def prompt_continue() -> None:
  input("\nPress any key to continue.")