# debug_payload.py
import json

RAW_LOG = "raw_365scores.jsonl"

with open(RAW_LOG, encoding="utf-8") as f:
    line = f.readline()           # leemos SOLO la primera línea
    if not line:
        raise SystemExit("⚠️ raw_365scores.jsonl está vacío")

    entry   = json.loads(line)    # parseamos el wrapper
    body_str = entry.get("body","")
    payload = json.loads(body_str)  # parseamos el JSON interno

print("📂 Claves top-level de payload:")
print(list(payload.keys()), "\n")

# Si hay "events"…
events = payload.get("events")
if isinstance(events, list) and events:
    ev0 = events[0]
    print("🔑 Claves de primer 'event':", list(ev0.keys()), "\n")

    # Si dentro hay 'markets'…
    mkts = ev0.get("markets")
    if isinstance(mkts, list) and mkts:
        m0 = mkts[0]
        print("🔑 Claves de markets[0]:", list(m0.keys()), "\n")

        # Si dentro de ese mercado hay 'selections'…
        sels = m0.get("selections")
        if isinstance(sels, list) and sels:
            print("🧩 Ejemplo de selection:")
            # Para no inundarte, sólo mostramos 1 selección con sus campos
            print(json.dumps(sels[0], indent=2))
        else:
            print("– No hay 'selections' en markets[0]")
    else:
        print("– No hay 'markets' en primer event")
else:
    print("– No hay 'events' en payload")