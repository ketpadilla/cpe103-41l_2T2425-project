from utils import prompt_continue, print_header, print_bank_name, clear_screen
from typing import Final, List, Dict
from time import sleep
from cli import BANK_NAME, DB_PATH
import csv
import re
import random

class User:
  def __init__(self):
    self.account_id: str = None 
    self.name: str = ""
    self.balance: float = 0.0

  def login(self) -> None:
    PROMPT_STR: Final[str] = 'Login'
    STR_LEN, PADDING = print_bank_name(BANK_NAME) 
    TOTAL_WIDTH: Final[int] = (2 * PADDING) + max(STR_LEN, len(PROMPT_STR))
    print_header(PROMPT_STR, TOTAL_WIDTH)

    attempts_id = attempts_pin = 3
    while attempts_id > 0:
      account_id = input("Enter Account ID: ")

      if not (self.is_valid_account_id_format(account_id)):
        print("Invalid Account ID. Please try again")
      
      else:
        with open(DB_PATH, mode='r') as file:
          reader = csv.DictReader(file)
          for row in reader:
            if row['account_id'] == account_id:

              while attempts_pin > 0:
                if row['pin'] == self.get_pin():
                  self.account_id = row['account_id']
                  return
                
                print("Incorrect PIN. Please try again")

                attempts_pin -= 1
                print(f"\nAttempts Left: {attempts_pin}")
              print("\nToo many attempts.")
      
          print("Account ID not found. Please try again.")
      
      attempts_id -= 1
      print(f"\nAttempts Left: {attempts_id}")
    print("\nToo many attempts.")

  def is_valid_account_id_format(self, account_id: str) -> None:
    return bool(account_id) and len(account_id) == 14 and all(part.isdigit() for part in account_id.split('-'))

  def get_pin(self) -> str:
    pin = input("Enter PIN: ")

    if (self.is_valid_pin(pin)):
      return pin
    else:
      print("Invalid PIN Format. Please try again")
      return None

  def is_valid_pin(self, pin: str) -> bool:
    return pin.isdigit() and len(pin) == 4 

  def create_account(self) -> None:
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
            self.account_id = self.generate_unique_account_id()
            self.name = name
            self.balance = 0.00

            with open(DB_PATH, mode='a', newline='') as file:
              writer = csv.writer(file)
              writer.writerow([self.account_id, self.name, pin, self.balance])
            
            print(f"\nAccount successfully created\n Your Account ID is {self.account_id}")
            
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
    return bool(re.match("^[a-zA-Z ]*$", name)) 

  def generate_unique_account_id(self) -> str:
    while True:
      account_id = f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
      if not self.account_id_exists(account_id):
        return account_id

  def account_id_exists(self, account_id: str) -> bool:
    with open(DB_PATH, mode='r') as file:
      reader = csv.reader(file)
      for row in reader:
        if row and row[0] == account_id:
          return True
    return False

  def load_account_details(self) -> None:
    if self.account_id is None:
      print("Error: Account ID is not set.")
      return
    
    with open(DB_PATH, mode='r') as file:
      reader = csv.DictReader(file)
      for row in reader:
        if row['account_id'] == self.account_id:
          self.name = row['name']
          self.balance = float(row['balance'])
          break

  def check_balance(self) -> None:
    if self.account_id is None:
      print("Error: No account loaded.")
      return
    
    HEADER_STR: Final[str] = 'Check Balance'

  def generate_new_account_id(self) -> int:
    try:
      with open(DB_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        account_ids = [int(row['account_id']) for row in reader]
        return max(account_ids, default=1000) + 1
    except FileNotFoundError:
      return 1001

  def load_account_details(self) -> None:
    if self.account_id is None:
      print("Error: Account ID is not set.")
      return
    
    with open(DB_PATH, mode='r') as file:
      reader = csv.DictReader(file)

      for row in reader:
        if row['account_id'] == str(self.account_id):
          self.name = row['name']
          self.balance = float(row['balance'])
          break

  def check_balance(self) -> None:
    if self.account_id is None:
      print("Error: No account loaded.")
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
    if self.account_id is None:
      print("Error: No account loaded.")
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
    if self.account_id is None:
      print("Error: No account loaded.")
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
    if self.account_id is None:
      print("Error: No account loaded.")
      return
    
    accounts: List[Dict[str, str]] = []
    with open(DB_PATH, mode='r') as file:
      reader = csv.DictReader(file)
      fieldnames = reader.fieldnames 

      for row in reader:
        if row['account_id'] == str(self.account_id):  
          row['balance'] = f"{self.balance:.2f}"  
        accounts.append(row)

    with open(DB_PATH, mode='w', newline='') as file:
      writer = csv.DictWriter(file, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(accounts)

  def get_account_id(self) -> str:
    return self.account_id

class Admin(User):
  pass