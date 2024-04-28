#  By vicvenpet (nano. && ovra.)
#  This script allows user verify up to (without proxys) 5 accounts.
#  https://github.com/vicvenpet/amino/blob/main/scripts/verify/main.py

from k_amino import Client
import getpass
import json

def load_accounts(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def save_accounts(accounts, filepath):
    with open(filepath, 'w') as file:
        json.dump(accounts, file, indent=4)

def login_and_verify(accounts_filepath, start_index=0):
    accounts = load_accounts(accounts_filepath)
    
    for i in range(start_index, len(accounts)):
        account = accounts[i]
        print(f"Logging in with account: {account['email']}")
        client = Client()
        try:
            client.login(email=account['email'], password=account['password'])
            print("Login successful.")
            # Perform verification here if needed
            # Example: Verify email confirmation, mobile number, etc.
            # If verification successful, you can break the loop and move to the next account
            # Otherwise, continue with the next account.
        except Exception as e:
            print(f"Login failed: {str(e)}. Skipping to the next account.")
            continue
        
        # Prompt the user to decide whether to move to the next account or not
        move_next = input("Press Enter to move to the next account (or type 'skip' to skip)...")
        if move_next.lower() == "skip":
            print("Skipping to the next account.")
            client.logout()
            continue
        
        client.logout()
        
        # Update the index of the last processed account
        start_index = i + 1
        save_accounts(accounts, accounts_filepath)
    
    print("All accounts processed.")

if __name__ == "__main__":
    accounts_filepath = "accounts.json"
    
    # You can specify the index from where you want to start processing accounts
    start_index = 0
    login_and_verify(accounts_filepath, start_index)
