#  By vicvenpet (nano. && ovra.)
#  This script collects coins from your accounts.json to a blog.
#  https://github.com/vicvenpet/amino/blob/main/scripts/collect/lib/tools.py

import json
import os
from time import sleep
from aminofixfix import Client, SubClient

class AminoCollector:
    def __init__(self):
        os.system("clear")
        print("Coin collector for blog\n\n")
        self.url_blog = input("Enter the blog link: ")
        self.client = Client()

    def select_account(self, accounts: list) -> dict:
        """Select an account from the accounts.json file."""
        print("\nSelect an account:")
        for i, account in enumerate(accounts):
            print(f"{i + 1}. {account['email']}")

        choice = int(input("\nEnter the account number (Collector would start from there): "))
        if 1 <= choice <= len(accounts):
            return accounts[choice - 1]
        else:
            print("Invalid choice. Please try again.")
            return self.select_account(accounts)

    def get_accounts(self) -> list:
        """Get accounts from accounts.json file."""
        try:
            with open("accounts.json", "r") as file:
                accounts = json.load(file)
            return accounts
        except Exception as error:
            print(error)
            return []

    def get_coins(self, account: dict) -> None:
        """Log in to an account, get the total amount of amino coins in the wallet and transfer everything to a blog."""
        email = account["email"]
        password = account["password"]
        device = account["device"]
        print(f"\n[+] {email[:10]}...{email[-12:]}")
        self.client = Client(device)
        try:
            self.client.login(email, password)
            print("[+] Login - OK")
            data = self.client.get_from_code(self.url_blog)
            blog_id = data.objectId
            com_id = data.comId
            self.client.join_community(com_id)
            print("[+] Community Joined - OK")
            total_wallet = int(self.client.get_wallet_info().totalCoins)
            print(f"[+] Wallet Balance: {total_wallet} coins")

            sub_client = SubClient(self.client, comId=com_id, profile=self.client.profile)

            coins_sent = 0
            if total_wallet >= 500:
                for _ in range(total_wallet // 500):
                    sub_client.send_coins(coins=500, blogId=blog_id)
                    total_wallet -= 500
                    coins_sent += 500

            if total_wallet > 0:
                sub_client.send_coins(coins=total_wallet, blogId=blog_id)
                coins_sent += total_wallet

            print(f"[+] Coins Sent: {coins_sent}")

        except Exception as error:
            print(error)

    def start(self) -> None:
        """Start the coin collector."""
        accounts = self.get_accounts()
        if not accounts:
            print("No accounts found in accounts.json. Please add accounts and try again.")
            return

        selected_account = self.select_account(accounts)
        self.get_coins(selected_account)
        print("\n[+] Script finished")

if __name__ == "__main__":
    collector = AminoCollector()
    collector.start()
