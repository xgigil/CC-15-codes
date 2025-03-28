from abc import ABC, abstractmethod

class BankAccount(ABC):
    def __init__(self, account_number, owner, balance):
        self.account_number = account_number
        self.owner = owner
        self._balance = 0  # Protected variable
        self.balance = balance  # Use setter to validate

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount >= 0:
            self._balance = amount
        else:
            print("Error: Balance cannot be negative.")

    @abstractmethod
    def calculate_interest(self):
        pass

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"Deposited ${amount} into {self.owner}'s account. New balance: ${self._balance}")
        else:
            print("Error: Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self._balance:
            self._balance -= amount
            print(f"Withdrawn ${amount} from {self.owner}'s account. Remaining balance: ${self._balance}")
        elif amount <= 0:
            print("Error: Withdrawal amount must be positive.")
        else:
            print("Error: Insufficient funds.")

    def display_info(self):
        print(f"Account Number: {self.account_number}, Owner: {self.owner}, Balance: ${self._balance}")

class SavingsAccount(BankAccount):
    def __init__(self, account_number, owner, balance, interest_rate):
        super().__init__(account_number, owner, balance)
        self.interest_rate = interest_rate  # Example: 0.02 for 2%

    def calculate_interest(self):
        interest = self._balance * self.interest_rate
        print(f"Interest for {self.owner}: ${interest}")
        return interest


class CheckingAccount(BankAccount):
    def __init__(self, account_number, owner, balance, overdraft_limit):
        super().__init__(account_number, owner, balance)
        self.overdraft_limit = overdraft_limit

    def calculate_interest(self):
        print("Checking accounts do not earn interest.")

    def withdraw(self, amount):
        if amount > 0 and amount <= (self._balance + self.overdraft_limit):
            self._balance -= amount
            print(f"Withdrawn ${amount} from {self.owner}'s account. Remaining balance: ${self._balance}")
        else:
            print("Error: Overdraft limit exceeded.")

def show_account_details(account):
    account.display_info()

# 🔹 Test Cases
savings = SavingsAccount("1001", "Alice", 5000, 0.03)
checking = CheckingAccount("2001", "Bob", 1000, 500)

print("\n--- Account Details ---")
show_account_details(savings)
show_account_details(checking)

# Perform transactions
savings.deposit(200)
checking.withdraw(1200)
savings.withdraw(6000)

print("\n--- Interest Calculation ---")
savings.calculate_interest()
checking.calculate_interest()