import requests
import random
import time
import json
from itertools import cycle

from solders.keypair import Keypair

TOKENS_FILE = "tokens.txt"
PROXIES_FILE = "proxy.txt"
BANDWIDTH_SHARE_URL = "https://api.openloop.so/bandwidth/share"
MISSIONS_URL = "https://api.openloop.so/missions"
INFO_URL = "https://api.openloop.so/users/profile"
LINK_WALLET_URL = "https://api.openloop.so/users/link-wallet"
MISSION_COMPLETE_URL = "https://api.openloop.so/missions/{mission_id}/complete"
MESSAGE = "Please sign this message to connect your wallet to OpenLoop and verifying your ownership only."
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

def get_random_quality():
    """Returns a random quality score between 60 and 99."""
    return random.randint(60, 99)

def get_proxies():
    """Reads proxies from proxy.txt and creates a cycle."""
    with open(PROXIES_FILE, "r") as file:
        proxies = [line.strip() for line in file if line.strip()]
    if not proxies:
        raise ValueError("No proxies found in proxy.txt.")
    return cycle(proxies)

def get_tokens():
    """Reads tokens from tokens.txt."""
    with open(TOKENS_FILE, "r") as file:
        tokens_with_privates = [line.strip().split(":") for line in file if line.strip()]
    if not tokens_with_privates:
        raise ValueError("No tokens found in tokens.txt.")
    return tokens_with_privates

def share_bandwidth(token, proxy):
    """Shares bandwidth using the specified token and proxy."""
    quality = get_random_quality()
    max_retries = 1

    for attempt in range(max_retries):
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "user-agent": USER_AGENT,
            }
            payload = json.dumps({"quality": quality})

            response = requests.post(
                BANDWIDTH_SHARE_URL,
                headers=headers,
                data=payload,
                proxies={"http": proxy, "https": proxy},
                timeout=40
            )

            if not response.ok:
                raise Exception(f"Failed to share bandwidth. Status: {response.status_code}, Response: {response.text}")
            data = response.json()
            balance = data.get("data", {}).get("balances", {}).get("POINT", "N/A")
            print(f"[SUCCESS] Bandwidth shared. Quality: {quality}, Total Earnings: {balance}")
            return
        except Exception as e:
            print(f"[ERROR] Attempt {attempt + 1} failed. Error: {e}")
            if "locked" in str(e):
                print(f"[ERROR] Locked status detected. Skipping token: {token}")
                return
            time.sleep(1)

    print("[ERROR] Max retries reached. Skipping.")

def check_missions_once(tokens, proxies):
    """Checks for available missions for all tokens once."""
    for token, _ in tokens:
        proxy = next(proxies)
        try:
            response = requests.get(
                MISSIONS_URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "user-agent": USER_AGENT,
                },
                proxies={"http": proxy, "https": proxy},
                timeout=10
            )

            if not response.ok:
                print(f"[ERROR] Failed to fetch missions for token {token}. Status: {response.status_code}")
                continue

            missions_data = response.json().get("data", {})
            available_missions = [
                mission["missionId"]
                for mission in missions_data.get("missions", [])
                if mission["status"] == "available"
            ]

            print(f"[INFO] {len(available_missions)} available missions found.")
            for mission_id in available_missions:
                complete_mission(mission_id, token, proxy)
        except Exception as e:
            print(f"[ERROR] Error fetching missions: {e}")
            continue

def complete_mission(mission_id, token, proxy):
    """Completes a mission."""
    try:
        response = requests.get(
            MISSION_COMPLETE_URL.format(mission_id=mission_id),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "user-agent": USER_AGENT,
            },
            proxies={"http": proxy, "https": proxy},
            timeout=10
        )

        if not response.ok:
            raise Exception(f"Failed to complete mission {mission_id}. Status: {response.status_code}")

        data = response.json()
        print(f"[SUCCESS] Mission {mission_id} completed.")
        return data
    except Exception as e:
        print(f"[ERROR] Error completing mission {mission_id}: {e}")


def has_address(access_token: str, proxy: str) -> bool:
    response = requests.get(
        INFO_URL,
        headers={
            "user-agent": USER_AGENT,
            "authorization": "Bearer {0}".format(access_token),
        },
        proxies={"http": proxy, "https": proxy},
    )
    if response.status_code != 200:
        return False
    json_response = response.json()
    print("[{0}] wallet address: {1}".format(
        json_response["data"].get("username"),
        json_response["data"].get("address"),
    ))
    return bool(json_response["data"].get("address"))


def link_wallet(
    access_token: str,
    private_key: str,
    proxy: str,
) -> tuple[bool, str]:
    keypair = Keypair.from_base58_string(private_key)
    signature = str(keypair.sign_message(MESSAGE.encode("utf-8")))
    pub_key = str(keypair.pubkey())
    response = requests.post(
        LINK_WALLET_URL,
        headers={
            "user-agent": USER_AGENT,
            "authorization": "Bearer {0}".format(access_token),
        },
        json={
            "message": MESSAGE,
            "signature": signature,
            "wallet": pub_key,
        },
        proxies={"http": proxy, "https": proxy},
    )
    print("Response from API to link wallet -> {0}".format(response.text))
    if response.status_code == 200:
        return True, pub_key
    return False, pub_key

def main():
    print("[INFO] Starting bandwidth sharing...")

    tokens = get_tokens()
    proxies = get_proxies()
    check_missions_once(tokens, proxies)
    while True:
        for token, private_key in tokens:
            proxy = next(proxies)
            if not has_address(token, proxy):
                link_wallet(token, private_key, proxy)
            print(f"[INFO] Using proxy: {proxy} for token: {token}")
            share_bandwidth(token, proxy)
        print("[INFO] Waiting for the next interval...")
        time.sleep(60)

if __name__ == "__main__":
    main()
