from dataclasses import dataclass
from datetime import datetime

@dataclass
class Odds:
    timestamp: datetime  # cuándo capturaste la cuota
    match_id: str  # identificador único del partido
    market: str  # nombre del mercado ("1X2", "Over/Under")
    outcome: str  # resultado ("Home", "Draw", "Away")
    odd: float  # valor numérico de la cuota
