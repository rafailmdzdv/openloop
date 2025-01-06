
# OpenLoop Automated Reg + Mining

Developed by [Solana0x](https://github.com/Solana0x/openloop). Added wallet linking on signing up.

## Features

- openloop Automated Reg Script.
- OpenLoop Automated Multiple Account 24/7 Up time Script.
- Connects to a WebSocket server using HTTP proxies.
- Handles Multiple Get OpenLoop Accounts at once !! 1 Account => mapped with 1 Proxy
- 15M$ by [themself](https://cryptorank.io/drophunting/open-loop-activity591) :D
- Wallet linking by [rafailmdzdv](https://github.com/rafailmdzdv)

## accounts.txt

Format: `email:password:solana_private_key`

## proxy.txt

Format: `http://username:password@ip:port`

## Requirements

- Python 3.12
  
## Steps

Before running the script, ensure you have Python installed on your machine. Then, install the necessary Python packages using:

```shell
git clone https://github.com/Solana0x/openloop.git && \
cd openloop && \
python3.12 -m venv .venv && \
. ./.venv/bin/activate && \
pip install -r requirements.txt
```
1. Replace `Invite code` in `reg.py` File Line ```12```.
2. To create / reg account run -> `python reg.py`
3. To start Mining Run `python mine.py` make sure your `tokens.txt` file have the access token of the openloop website.
4. If you have already reg accounts and wanted new access tokens list just add your accounts data in accounts.txt file  `email:pass:solana_private_key` format and run `python get_token.py`

## Support

```
# Solana
3q87zLdFVGBh7cSUQavhK5AkdNzXyD2U7xCmB27PSBdX

# TRC20
TTHJgyn3NC69UXSzEYAvZzBbRRps9vtuZf

# EVM
0xc0fa4dcd208c7e45e2a324784526eed0fc4ef8cb
```

[![](./assets/telegram.svg "Channel")](https://t.me/glistdao)
