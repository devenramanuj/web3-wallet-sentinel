import time
import requests

class RPCClient:
    """
    Multi-node failover wrapper for zero-dependency JSON-RPC calls.
    """
    def __init__(self, rpc_nodes, timeout=6):
        self.rpc_nodes = rpc_nodes
        self.timeout = timeout
        self.current_idx = 0

    def get_current_rpc(self):
        return self.rpc_nodes[self.current_idx]

    def rotate_rpc(self):
        self.current_idx = (self.current_idx + 1) % len(self.rpc_nodes)
        return self.get_current_rpc()

    def call(self, method, params=None):
        if params is None:
            params = []

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": int(time.time() * 1000)
        }
        headers = {"Content-Type": "application/json"}

        for _ in range(len(self.rpc_nodes)):
            rpc_url = self.get_current_rpc()
            try:
                res = requests.post(rpc_url, json=payload, headers=headers, timeout=self.timeout)
                if res.status_code == 200 and res.text:
                    data = res.json()
                    if "result" in data and data["result"] is not None:
                        return data["result"]
            except Exception:
                pass
            self.rotate_rpc()
            
        return None

    def get_native_balance(self, address):
        result = self.call("eth_getBalance", [address, "latest"])
        if result and result != "0x":
            return int(result, 16) / (10 ** 18)
        return 0.0

    def get_erc20_balance(self, wallet_address, token_contract, decimals):
        clean_addr = wallet_address.lower().replace("0x", "").zfill(64)
        data = "0x70a08231" + clean_addr
        result = self.call("eth_call", [{"to": token_contract, "data": data}, "latest"])
        if result and result != "0x":
            return int(result, 16) / (10 ** decimals)
        return 0.0
