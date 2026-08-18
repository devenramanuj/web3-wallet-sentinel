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

