# extractor.py
import json
from models import Odds  # asume tu clase Odd tiene campos (match_id, market, outcome, odd, source)

class OddsExtractor:

    def extract(self, url: str, body_bytes: bytes):
        """
        Extrae las odds de una respuesta raw de 365scores:
        - payload["games"] → cada juego
        - game["odds"] → dict con lineType + options
        - options → lista con rate.decimal
        """
        results = []
        try:
            payload = json.loads(body_bytes)
        except Exception:
            return results

        for game in payload.get("games", []):
            match_id = game.get("id")
            odds_block = game.get("odds", {})
            # Nombre del mercado
            lt = odds_block.get("lineType", {})
            market = lt.get("name") or lt.get("shortName") or f"line_{lt.get('id')}"

            for opt in odds_block.get("options", []):
                # Nombre del resultado (1, X, 2, etc.)
                outcome = opt.get("name")
                # Valor decimal de la cuota
                rate = opt.get("rate", {}).get("decimal")
                try:
                    odd_val = float(rate)
                except Exception:
                    continue

                results.append(
                    Odds(
                        match_id = str(match_id),
                        market   = market,
                        outcome  = outcome,
                        odd      = odd_val,
                        source   = url
                    )
                )

        return results