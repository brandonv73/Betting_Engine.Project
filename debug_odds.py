# debug_odds.py
import json

RAW_LOG = "raw_365scores.jsonl"

# Carga la primera línea
entry   = json.loads(open(RAW_LOG, encoding="utf-8").readline())
payload = json.loads(entry["body"])

games = payload.get("games", [])
print(f"🔢 Total games: {len(games)}")

odd_list = games[0].get("odds")
print("🧩 Tipo de games[0]['odds']:", type(odd_list))
if isinstance(odd_list, list):
    print("🔑 keys de odds[0]:", list(odd_list[0].keys()))
    print("\n–– Ejemplo completo de odds[0] ––")
    print(json.dumps(odd_list[0], indent=2))
else:
    print("odds:", odd_list)