import requests
import json
import random
import time
from itertools import cycle

ACCOUNTS_FILE = "accounts.txt"
PROXIES_FILE = "proxy.txt"
TOKEN_FILE = "tokens.txt"

INVITE_CODE = "ol41fe134b"
REGISTER_URL = "https://api.openloop.so/users/register"
LOGIN_URL = "https://api.openloop.so/users/login"


def read_accounts(file_path):
    """Reads accounts from accounts.txt (email:password)."""
    accounts = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                email, password = line.split(":", 1)
                accounts.append({"email": email, "password": password})
    return accounts


def read_proxies(file_path):
    """Reads proxies from proxy.txt."""
    proxies = []
    with open(file_path, "r") as file:
        proxies = [line.strip() for line in file if line.strip()]
    return cycle(proxies)


def save_token(token, file_path):
    """Saves token to tokens.txt."""
    with open(file_path, "a") as file:
        file.write(token + "\n")


def generate_name(email):
    """Generates a random name based on the email username."""
    base_name = email.split("@")[0]
    random_number = random.randint(10, 99)
    return f"{base_name}{random_number}"


def login_user(email, password, proxy):
    """Logs in the user to fetch the access token."""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            login_payload = {"username": email, "password": password}
            response = requests.post(
                LOGIN_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps(login_payload),
                proxies={"http": proxy, "https": proxy},
                timeout=10,
            )

            if not response.ok:
                print(f"[ERROR] Login failed for {email}. Status: {response.status_code}")
                continue

            data = response.json()
            access_token = data.get("data", {}).get("accessToken")
            if access_token:
                print(f"[SUCCESS] Token fetched for {email}")
                save_token(access_token, TOKEN_FILE)
                return access_token
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Login attempt failed for {email}: {str(e)}")
        time.sleep(1)

    print(f"[ERROR] Max retries reached for login: {email}")
    return None


def register_user(email, password, proxy):
    """Registers a user and handles login if registration fails."""
    max_retries = 5
    for attempt in range(max_retries):
        try:
            name = generate_name(email)
            registration_payload = {
                "name": name,
                "username": email,
                "password": password,
                "inviteCode": INVITE_CODE,
            }
            response = requests.post(
                REGISTER_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps(registration_payload),
                proxies={"http": proxy, "https": proxy},
                timeout=10,
            )

            if response.status_code == 401:
                print(f"[INFO] Email {email} already exists. Logging in...")
                return login_user(email, password, proxy)

            if not response.ok:
                print(f"[ERROR] Registration failed for {email}. Status: {response.status_code}")
                continue

            print(f"[SUCCESS] Registration successful for {email}")
            return login_user(email, password, proxy)
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Registration attempt failed for {email}: {str(e)}")
        time.sleep(1)

    print(f"[ERROR] Max retries reached for registration: {email}")
    return None


def main():
    accounts = read_accounts(ACCOUNTS_FILE)
    proxies = read_proxies(PROXIES_FILE)
    open(TOKEN_FILE, "w").close()

    for account in accounts:
        proxy = next(proxies)
        email = account["email"]
        password = account["password"]
        print(f"[INFO] Registering account {email} using proxy {proxy}")
        register_user(email, password, proxy)
        time.sleep(random.uniform(5, 15))


if __name__ == "__main__":
    main()
