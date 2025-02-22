"""  
ATM SIMULATION SYSTEM
Made By : Akshat Bhardwaj
Date : 12 / 11 / 2024
Version : 1.4

Author's Message : Hi reader , I am Akshat Bhardwaj the coder , tester and developer of this mini-project , this is 
my first project as I recently started coding. It took me about 12 days to make it to how it looks now, not that it is 
anything outstanding but I must say it still is efficient in it's own way as it is implemented on real world principles.
This is the 4TH version all the previous versions were all without a database system , but in this we can actually store data
and can also overwrite it ,pretty amazing is'nt it. I am really looking forward to the future enhancements but I have to 
study more as exams are near but I will try to get as closer to the Final Launching Software as soon as possible. Mail me 
on the email provided to let me know of how this project can be improvised.

Thanks for reading 
AKSHAT BHARDWAJ
akshatbhardwaj872@gmail.com
SGT UNIVERSITY

FEATURES :
    
    1 USER AUTHENTICATION 
    2 CHECK BALANCE 
    3 DEPOSIT MONEY 
    4 WITHDRAW MONEY 
    5 ACCOUNT TYPE 
    6 ERROR HANDLING (INVALID PIN, INSUFFICIENT FUNDS etc.)
    
FUTURE ENHANCEMENTS :
    
    1 IMPLEMENTING GUI USING tkinter or Flask
    2 USE HASHING FOR SECURE PIN STORAGE 
    3 INTEGRATE SMS / EMAIL NOTIFICATION 
    4 MULTITHREADING FOR CONCURRENT TRANSACTIONS 


OOPS CONCEPT IMPLEMENTED : 
    
    1. Encapsulation: Private variables for sensitive data (password, balance)
    2. Abstraction: ATM class hides implementation details
    3. Inheritance: SavingsAccount and CurrentAccount inherit from Account
    4. Polymorphism: Different withdrawal limits for Savings and Current account
    
SOFTWARE REQUIREMENTS :
    Use any python dependencies as long as it has a dedicated terminal example : spyder etc."""


import json
import os
from getpass import getpass

class Account:
    """Base class for different types of accounts."""
    def __init__(self, account_number, name, password, balance=0.0):
        self.account_number = account_number
        self.name = name
        self.__password = str(password)  
        self.__balance = balance  

    def authenticate(self, password):
        """Checks if the entered password is correct."""
        return str(password) == self.__password  
    
    def get_balance(self):
        """Returns the current balance."""
        return self.__balance
    
    def deposit(self, amount):
        """Deposits money into the account."""
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        """Method to be overridden in subclasses."""
        raise NotImplementedError("Withdraw method must be defined in subclasses")
    
    def _update_balance(self, amount):
        """Protected method to update balance."""
        self.__balance = amount

    def to_dict(self):
        """Converts account details to a dictionary for storage."""
        return {
            "account_number": self.account_number,
            "name": self.name,
            "password": self.__password,  
            "balance": self.__balance
        }

class SavingsAccount(Account):
    """Derived class for savings account with withdrawal limit."""
    def withdraw(self, amount):
        if 0 < amount <= self.get_balance() and amount <= 100000:  
            self._update_balance(self.get_balance() - amount)
            return True
        return False

class CurrentAccount(Account):
    """Derived class for current account with a higher withdrawal limit."""
    def withdraw(self, amount):
        if 0 < amount <= self.get_balance() and amount <= 50000:  
            self._update_balance(self.get_balance() - amount)
            return True
        return False

class ATM:
    """ATM system for user interactions."""
    DATA_FILE = "accounts.json"

    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):
        """Loads accounts from a file."""
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r") as file:
                return {acc["account_number"]: self.create_account_object(acc) for acc in json.load(file)}
        return {}
    
    def create_account_object(self, acc_data):
        """Creates an Account object from stored data."""
        if "account_type" in acc_data and acc_data["account_type"] == "current":
            return CurrentAccount(acc_data["account_number"], acc_data["name"], acc_data["password"], acc_data["balance"])
        return SavingsAccount(acc_data["account_number"], acc_data["name"], acc_data["password"], acc_data["balance"])

    def save_accounts(self):
        """Saves accounts to a file."""
        with open(self.DATA_FILE, "w") as file:
            json.dump([acc.to_dict() for acc in self.accounts.values()], file, indent=4)

    def create_account(self):
        """Allows user to create a new account."""
        acc_num = input("Enter Account Number: ")
        if acc_num in self.accounts:
            print("Account already exists!")
            return
        name = input("Enter Name: ")
        try:
            password = str(getpass("Set Password: "))
        except Exception:
            print("getpass not supported, using input instead.")
            password = input("Set Password: ") 
        acc_type = input("Account Type (savings/current): ").lower()
        if acc_type == "current":
            self.accounts[acc_num] = CurrentAccount(acc_num, name, password)
        else:
            self.accounts[acc_num] = SavingsAccount(acc_num, name, password)
        self.save_accounts()
        print("Account created successfully!")

    def login(self):
        """Authenticates user and provides access to ATM functions."""
        acc_num = input("Enter Account Number: ")
        try:
            password = str(getpass("Enter Password: "))
        except Exception:
            print("getpass not supported, using input instead.")
            password = input("Enter Password: ")  
        account = self.accounts.get(acc_num)
        if account and account.authenticate(password):
            print(f"\nWelcome, {account.name}!")
            self.account_menu(account)
        else:
            print("Invalid credentials!")

    def account_menu(self, account):
        """Displays account options after login."""
        while True:
            print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Logout")
            choice = input("Choose an option: ")
            if choice == "1":
                print(f"Current Balance: ${account.get_balance()}")
            elif choice == "2":
                amount = float(input("Enter amount to deposit: "))
                if account.deposit(amount):
                    self.save_accounts()
                    print("Deposit successful!")
                else:
                    print("Invalid amount!")
            elif choice == "3":
                amount = float(input("Enter amount to withdraw: "))
                if account.withdraw(amount):
                    self.save_accounts()
                    print("Withdrawal successful!")
                else:
                    print("Invalid amount or exceeds limit!")
            elif choice == "4":
                print("Logging out...")
                break
            else:
                print("Invalid option!")

    def run(self):
        """Main menu for ATM system."""
        while True:
            print("\n==== ATM SYSTEM ====")
            print("1. Create Account\n2. Login\n3. Exit")
            choice = input("Enter choice: ")
            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.login()
            elif choice == "3":
                print("Thank you for using our ATM!")
                break
            else:
                print("Invalid choice! Try again.")

if __name__ == "__main__":
    atm = ATM()
    atm.run()
