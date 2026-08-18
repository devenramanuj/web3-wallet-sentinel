import requests
from datetime import datetime
from config import DISCORD_WEBHOOK_URL

def send_discord_alert(network_name, wallet_name, address, asset_name, old_bal, new_bal):
    if not DISCORD_WEBHOOK_URL:
        print("[Warning] Discord Webhook URL સેટ નથી.")
        return

    diff = new_bal - old_bal
    action = "📥 ફંડ જમા થયું (INFLOW)" if diff > 0 else "📤 ફંડ ટ્રાન્સફર થયું (OUTFLOW)"
    color = 3066993 if diff > 0 else 15158332  # લીલો અથવા લાલ

    embed = {
        "title": f"🚨 Web3 Alert: {action}",
        "description": f"**વોલેટ:** `{wallet_name}`\n`{address}`",
        "color": color,
        "fields": [
            {"name": "ચેઇન / નેટવર્ક", "value": f"**{network_name}**", "inline": True},
            {"name": "ટોકન / એસેટ", "value": f"**{asset_name}**", "inline": True},
            {"name": "ફેરફાર", "value": f"`{diff:+.4f} {asset_name}`", "inline": True},
            {"name": "નવું બેલેન્સ", "value": f"**{new_bal:,.4f} {asset_name}**", "inline": False}
        ],
        "footer": {"text": f"{network_name} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
    }

    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]}, timeout=5)
    except Exception as e:
        print(f"[Error] Discord Alert મોકલવામાં ભૂલ: {e}")
