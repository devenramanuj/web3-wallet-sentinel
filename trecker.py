import time
from config import NETWORKS, TRACKED_WALLETS, CHECK_INTERVAL_SECONDS
from rpc_client import RPCClient
from notifier import send_discord_alert

# દરેક નેટવર્ક માટે RPC ક્લાયન્ટ શરૂ કરવા
clients = {chain_key: RPCClient(info["rpc_nodes"]) for chain_key, info in NETWORKS.items()}

# છેલ્લું જાણીતું સ્ટેટ: (chain_key, address, asset) -> balance
state = {}

def start_engine():
    print("=" * 60)
    print("🚀 Web3 Wallet Sentinel & Live Alert Engine શરૂ થયું...")
    print("=" * 60)

    # ૧. પ્રારંભિક બેઝલાઇન લોડ કરવું
    for chain_key, net_info in NETWORKS.items():
        print(f"\n🌐 [{net_info['name']}] માટે બેઝલાઇન લોડ થઈ રહ્યું છે...")
        client = clients[chain_key]
        native_sym = net_info["native_currency"]

        for name, addr in TRACKED_WALLETS.items():
            # નેટિવ બેલેન્સ
            state[(chain_key, addr, native_sym)] = client.get_native_balance(addr)
            
            # ERC-20 ટોકન બેલેન્સ
            for t_name, t_info in net_info["tokens"].items():
                state[(chain_key, addr, t_name)] = client.get_erc20_balance(
                    addr, t_info["address"], t_info["decimals"]
                )
            print(f"  └── [{name}] ડેટા સિંક થયો.")

    print("\n✅ તમામ નેટવર્ક્સનું બેઝલાઇન સિંક થઈ ગયું. લાઈવ મોનિટરિંગ એક્ટિવ છે...\n")

    # ૨. લાઇવ મોનિટરિંગ લૂપ
    while True:
        try:
            for chain_key, net_info in NETWORKS.items():
                client = clients[chain_key]
                native_sym = net_info["native_currency"]
                net_name = net_info["name"]

                for name, addr in TRACKED_WALLETS.items():
                    # નેટિવ એસેટ ચેકિંગ
                    curr_native = client.get_native_balance(addr)
                    prev_native = state.get((chain_key, addr, native_sym), curr_native)
                    if abs(curr_native - prev_native) > 0.0001:
                        send_discord_alert(net_name, name, addr, native_sym, prev_native, curr_native)
                        state[(chain_key, addr, native_sym)] = curr_native

                    # ERC-20 ટોકન ચેકિંગ
                    for t_name, t_info in net_info["tokens"].items():
                        curr_tok = client.get_erc20_balance(addr, t_info["address"], t_info["decimals"])
                        prev_tok = state.get((chain_key, addr, t_name), curr_tok)
                        if abs(curr_tok - prev_tok) > 0.01:
                            send_discord_alert(net_name, name, addr, t_name, prev_tok, curr_tok)
                            state[(chain_key, addr, t_name)] = curr_tok

            time.sleep(CHECK_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            print("\n🛑 ટ્રેકર સુરક્ષિત રીતે બંધ કરવામાં આવ્યું.")
            break
        except Exception as err:
            print(f"⚠️ મોનિટરિંગ લૂપ એરર: {err}")
            time.sleep(5)

if __name__ == "__main__":
    start_engine()
