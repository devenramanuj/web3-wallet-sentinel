import time
import requests
from datetime import datetime

# ================= કન્ફિગરેશન =================
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

CHECK_INTERVAL_SECONDS = 30  # દર ૩૦ સેકન્ડે ચેક કરશે

# સ્ટેબલ અને ઝડપી RPC એન્ડપોઇન્ટ્સ
RPC_NODES = [
    "https://eth.merkle.io",
    "https://1rpc.io/eth",
    "https://ethereum-rpc.publicnode.com"
]

# ટ્રેક કરવા માટેના વોલેટ્સ
TRACKED_WALLETS = {
    "Vitalik Buterin": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "Binance Hot Wallet": "0x28C6c06298d514Db089934071355E5743bf21d60"
}

# સપોર્ટેડ ટોકન્સ
TOKENS = {
    "USDT": {
        "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "decimals": 6
    },
    "USDC": {
        "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "decimals": 6
    }
}

# છેલ્લું જાણીતું બેલેન્સ સ્ટોર કરવા માટે (ઇન-મેમરી સ્ટેટ)
state = {}

# ================= RPC કોમ્યુનિકેશન =================
def call_rpc(method, params):
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
    headers = {"Content-Type": "application/json"}
    
    for rpc in RPC_NODES:
        try:
            res = requests.post(rpc, json=payload, headers=headers, timeout=6)
            if res.status_code == 200 and res.text:
                json_data = res.json()
                if "result" in json_data:
                    return json_data["result"]
        except Exception:
            continue
    return None

def fetch_eth_balance(address):
    result = call_rpc("eth_getBalance", [address, "latest"])
    return int(result, 16) / (10 ** 18) if result else 0.0

def fetch_token_balance(wallet_address, token_contract, decimals):
    clean_addr = wallet_address.lower().replace("0x", "").zfill(64)
    data = "0x70a08231" + clean_addr
    result = call_rpc("eth_call", [{"to": token_contract, "data": data}, "latest"])
    if result and result != "0x":
        return int(result, 16) / (10 ** decimals)
    return 0.0

# ================= DISCORD નોટિફિકેશન =================
def send_discord_alert(wallet_name, address, asset_name, old_bal, new_bal):
    diff = new_bal - old_bal
    action = "📥 ફંડ જમા થયું (INFLOW)" if diff > 0 else "📤 ફંડ ટ્રાન્સફર થયું (OUTFLOW)"
    color = 3066993 if diff > 0 else 15158332 # લીલો અથવા લાલ

    embed = {
        "title": f"🚨 Web3 Alert: {action}",
        "description": f"**વોલેટ:** `{wallet_name}`\n`{address}`",
        "color": color,
        "fields": [
            {"name": "ટોકન / એસેટ", "value": f"**{asset_name}**", "inline": True},
            {"name": "ફેરફાર", "value": f"`{diff:+.4f} {asset_name}`", "inline": True},
            {"name": "નવું બેલેન્સ", "value": f"**{new_bal:,.4f} {asset_name}**", "inline": False}
        ],
        "footer": {"text": f"Ethereum Mainnet • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
    }
    
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]}, timeout=5)
    except Exception as e:
        print(f"Discord Alert મોકલવામાં ભૂલ: {e}")

# ================= મોનિટરિંગ લૂપ =================
def start_engine():
    print("🚀 Web3 Wallet Tracker Engine શરૂ થયું...")
    
    # શરૂઆતનું બેઝલાઇન બેલેન્સ સેટ કરવું
    for name, addr in TRACKED_WALLETS.items():
        print(f"[{name}] નું બેલેન્સ લોડ થઈ રહ્યું છે...")
        state[(addr, "ETH")] = fetch_eth_balance(addr)
        for t_name, t_info in TOKENS.items():
            state[(addr, t_name)] = fetch_token_balance(addr, t_info["address"], t_info["decimals"])
    
    print("✅ બેઝલાઇન લોડ થઈ ગયું. લાઈવ મોનિટરિંગ ચાલુ છે...\n")

    while True:
        try:
            for name, addr in TRACKED_WALLETS.items():
                # ETH ચેક
                curr_eth = fetch_eth_balance(addr)
                prev_eth = state.get((addr, "ETH"), curr_eth)
                if abs(curr_eth - prev_eth) > 0.0001:  # માઈક્રો ફેરફારો ઇગ્નોર
                    send_discord_alert(name, addr, "ETH", prev_eth, curr_eth)
                    state[(addr, "ETH")] = curr_eth

                # ટોકન્સ ચેક
                for t_name, t_info in TOKENS.items():
                    curr_tok = fetch_token_balance(addr, t_info["address"], t_info["decimals"])
                    prev_tok = state.get((addr, t_name), curr_tok)
                    if abs(curr_tok - prev_tok) > 0.01:
                        send_discord_alert(name, addr, t_name, prev_tok, curr_tok)
                        state[(addr, t_name)] = curr_tok

            time.sleep(CHECK_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\nટ્રેકર બંધ કરવામાં આવ્યું.")
            break
        except Exception as err:
            print(f"લૂપ એરર: {err}")
            time.sleep(5)

if __name__ == "__main__":
    start_engine()
