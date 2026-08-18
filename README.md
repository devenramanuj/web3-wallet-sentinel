# ⚡ Web3 Wallet Sentinel & Live Alert Engine

A lightweight, zero-dependency, multi-chain on-chain wallet and ERC-20 token tracking engine built with Python. Delivers instant, color-coded Discord Webhook alerts for wallet inflows, outflows, and balance shifts directly via native JSON-RPC without requiring third-party paid APIs.

---

## 🚀 Key Features

* **Multi-Chain Architecture:** Native support for **Ethereum Mainnet** and **Base Mainnet (Layer-2)**.
* **Zero Third-Party API Costs:** Direct low-level JSON-RPC calls (`eth_getBalance`, `eth_call`) with zero dependency on expensive indexed APIs.
* **Multi-Node Failover Engine:** High availability with automated round-robin failover across multiple public RPC nodes to bypass rate limits.
* **ERC-20 & Native Asset Support:** Real-time balance shift tracking for Native ETH, USDT, USDC, DAI, etc.
* **Instant Discord Webhooks:** Formatted Rich Embed alerts with automatic state-change detection (Inflow vs Outflow color coding).

---

## 📸 Live Alerts Preview

🚨 Web3 Alert: 📥 ફંડ જમા થયું (INFLOW)
વોલેટ: Binance Hot Wallet
0x28C6c06298d514Db089934071355E5743bf21d60
ચેઇન / નેટવર્ક: Ethereum Mainnet
ટોકન / એસેટ: ETH
ફેરફાર: +74.7160 ETH
નવું બેલેન્સ: 216,293.8480 ETH

---

## 🛠️ Project Structure

```text
├── LICENSE               # MIT License
├── README.md             # Project Documentation
├── config.py             # Networks, Tokens & Wallet Configuration
├── rpc_client.py         # Multi-Node Failover RPC Engine
├── notifier.py           # Discord Webhook Notification Module
└── tracker.py            # Main Engine Execution Loop

⚡ Quick Start & Installation
1. Clone the Repository
git clone [https://github.com/devenramanuj/web3-wallet-sentinel.git](https://github.com/devenramanuj/web3-wallet-sentinel.git)
cd web3-wallet-sentinel

2. Install Dependencies
pip install requests python-dotenv

3. Configure Webhook & Settings
​Create a .env file or configure directly in config.py:

DISCORD_WEBHOOK_URL="[https://discord.com/api/webhooks/your_webhook_url](https://discord.com/api/webhooks/your_webhook_url)"
CHECK_INTERVAL_SECONDS=30

4. Run the Engine
python tracker.py

🗺️ Roadmap & Milestones
​[x] Multi-node failover JSON-RPC engine
​[x] Ethereum & Base Mainnet native + ERC-20 tracking
​[x] Discord Webhook integration
​[ ] Telegram Bot API integration
​[ ] Web dashboard for dynamic wallet watchlist management
​[ ] Support for Arbitrum & Optimism L2 networks
​📄 License
​This project is licensed under the MIT License.
