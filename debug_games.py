# debug_games.py
import json

RAW_LOG = "raw_365scores.jsonl"

# Leer primera línea
entry = json.loads(open(RAW_LOG, encoding="utf-8").readline())
payload = json.loads(entry["body"])

# 1) Mostrar qué claves hay en 'games'
games = payload.get("games", [])
print(f"Total games: {len(games)}")
if not games:
    raise SystemExit("No hay juegos en payload['games']")

print("\n🔑 Claves de games[0]:")
print(list(games[0].keys()))

# 2) Si existe 'bookmakers', ver sus claves
bms = games[0].get("bookmakers", [])
print(f"\n– Bookmakers en games[0]: {len(bms)}")
if bms:
    print("🔑 Claves de bookmakers[0]:", list(bms[0].keys()))

    # 3) Si dentro de un bookmaker hay mercados, ver sus claves
    mkts = bms[0].get("markets") or bms[0].get("events") or bms[0].get("oddsGroups")
    if isinstance(mkts, list) and mkts:
        print("\n🔑 Claves de markets[0]:", list(mkts[0].keys()))
        # 4) Ejemplo de selección/price si existe
        sels = mkts[0].get("selections") or mkts[0].get("prices") or mkts[0].get("odds")
        if isinstance(sels, list) and sels:
            print("\n🧩 Ejemplo de selección/price:")
            print(json.dumps(sels[0], indent=2))
        else:
            print("– No hay lista de selecciones en markets[0]")
    else:
        print("– No hay mercados en bookmakers[0]")
else:
    print("– No hay bookmakers en games[0]")