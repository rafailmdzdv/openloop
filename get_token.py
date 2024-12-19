import requests
import json
import time
import random
from itertools import cycle

ACCOUNTS_FILE = "accounts.txt"
PROXIES_FILE = "proxy.txt"
TOKENS_FILE = "tokens.txt"

def read_accounts(file_path):
    """
    Reads accounts from the accounts.txt file.
    Each line should be formatted as email:password.
    """
    accounts = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                email, password = line.split(":", 1)
                accounts.append({"email": email, "password": password})
    return accounts

def read_proxies(file_path):
    """
    Reads proxies from the proxy.txt file.
    Each line should be formatted as http://username:password@ip:port.
    """
    proxies = []
    with open(file_path, "r") as file:
        proxies = [line.strip() for line in file if line.strip()]
    return cycle(proxies)

def save_token(token, file_path):
    """
    Saves a token to the tokens.txt file.
    """
    with open(file_path, "a") as file:
        file.write(token + "\n")

def get_token_for_account(account, proxy):
    """
    Logs in to get a token for a given account using an HTTP proxy.
    """
    url = "https://api.openloop.so/users/login"
    headers = {"Content-Type": "application/json"}
    payload = {"username": account["email"], "password": account["password"]}
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), proxies=proxies, timeout=10)
        if response.status_code != 200:
            print(f"[ERROR] Login failed for {account['email']}. Status Code: {response.status_code}")
            return None
        
        data = response.json()
        access_token = data.get("data", {}).get("accessToken")
        if access_token:
            print(f"[SUCCESS] Token fetched for {account['email']}")
            return access_token
        else:
            print(f"[ERROR] No token returned for {account['email']}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Proxy or network error for {account['email']}: {str(e)}")
    return None

def main():
    accounts = read_accounts(ACCOUNTS_FILE)
    proxies = read_proxies(PROXIES_FILE)
    open(TOKENS_FILE, "w").close()
    for account in accounts:
        proxy = next(proxies)
        print(f"[INFO] Using proxy: {proxy} for account: {account['email']}")
        token = get_token_for_account(account, proxy)
        if token:
            save_token(token, TOKENS_FILE)
        time.sleep(random.uniform(5, 15))

if __name__ == "__main__":
    main()
