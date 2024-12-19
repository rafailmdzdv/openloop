# OpenLoop 自动注册与挖矿脚本

使用此基于 Python 的脚本在 VPS 上实现 OpenLoop 去中心化挖矿的自动化操作，可同时管理多个设备和 IP 地址，确保 24/7 不间断运行并最大化收益。非常适合需要通过 HTTP 协议高效处理 WebSocket 连接的用户。

## 功能特性

- OpenLoop 自动化注册脚本。
- OpenLoop 多账号 24/7 不间断运行脚本。
- 通过 HTTP 代理连接到 WebSocket 服务器。
- 同时处理多个 OpenLoop 账号！每个账号对应一个独立代理。
- OpenLoop 项目近期融资 1500 万美金 - [https://substack.com/home/post/p-153030845](https://substack.com/home/post/p-153030845)

# 创建 Accounts.txt 文件

1. 格式 => email:password
2. 你也可以使用 Gmail + 标记或自定义域名邮箱，以及 Gmail 点号技巧来生成账号。

# 获取代理 IP (Socks5/HTTP)

1. 在此注册账户：https://app.proxies.fo/signup?referral=662d5a3a775a945a8de790ba
2. 前往 https://app.proxies.fo/plans 购买对应套餐
3. ![image](https://github.com/user-attachments/assets/5453eabd-0a09-49f7-b004-1ca4617b9f8a)
4. **推荐** - 你可以使用加密货币 (Binance) 来支付。
5. 购买后进入仪表盘，点击 `Go to Generator` 按钮。
6. 在生成页面中，将代理格式设为 `USER:PASS@HOST:PORT` 并选择 `HTTP`，然后在 proxy count 中填写数量（如 200）。
7. 点击保存生成代理列表。
8. ![image](https://github.com/user-attachments/assets/010753b5-1112-48c0-9a40-6b00189abd10)
9. 你可以使用任意数量的代理，代理池最大可达 25,000 个。

## 环境要求

- OpenLoop 邀请链接 ( [https://openloop.so/ ](https://openloop.so/) )
- Python (安装 Python: https://www.python.org/downloads/ [Windows/Mac]或使用 Ubuntu Server：`sudo apt install python3`)
- VPS 服务器 (可使用 AWS 免费层、Google 免费层或任意 ~2-5$/月的在线服务器)
- 代理服务器：购买 ISP Residential Proxies 才能获得 $GRASS 收益，如果使用数据中心或免费劣质代理将无收益。
- 推荐代理提供商：Proxies.fo - [https://app.proxies.fo/signup?referral=662d5a3a775a945a8de790ba](https://app.proxies.fo/signup?referral=662d5a3a775a945a8de790ba) [购买 1GB 套餐足以支撑 1-6 个月并提供无限账号或代理]
- Light Node (适用于 VPS) - [https://www.lightnode.com/?inviteCode=OUMJXM&promoteWay=LINK](https://www.lightnode.com/?inviteCode=OUMJXM&promoteWay=LINK)

## 运行步骤

在运行脚本前，请确保已安装 Python。然后使用以下命令安装必要的 Python 包：

1. ``` git clone https://github.com/Solana0x/openloop.git ```
2. ``` cd openloop ```
3. ``` pip install -r requirements.txt ```
4. 在 `reg.py` 文件的第 11 行替换 `Invite code`。
6. 不要忘记在 proxy.txt 文件中添加多个代理，你可以添加多达 10000+ 条代理！！每个账号对应一个代理！格式为：`http://username:pass@ip:port`
7. 你可从 Proxies.fo 网站获取多个代理 IP 地址。
8. 注册账号时请修改 `reg.py` 文件中的相关信息，然后运行命令 `python reg.py` 来创建账号。
9. 挖矿启动方式：运行 `python mine.py`，确保你的 `tokens.txt` 文件中包含从 openloop 网站获得的访问令牌。
10. 如果你已有注册好的账号，但需要新的访问令牌列表，只需在 accounts.txt 文件中加入 `email:pass` 格式的账号数据，然后运行 `python get_token.py`。

![image](https://github.com/user-attachments/assets/a2350548-f56a-4905-a7a9-b83484b1a8d1)

## 寻求帮助

如需帮助请联系：`0xphatom` (Discord) https://discord.com/users/979641024215416842

# 社交平台

- **Telegram** - [https://t.me/phantomoalpha](https://t.me/phantomoalpha)
- **Discord** - [https://discord.gg/pGJSPtp9zz](https://discord.gg/pGJSPtp9zz)
