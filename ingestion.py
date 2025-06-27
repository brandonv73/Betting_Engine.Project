import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_models import Base, RawRequest, Odds
from extractor import OddsExtractor

def ingest(
    raw_file: str = 'raw_365scores.jsonl',
    db_url: str = 'sqlite:///bets.db'
):
    # 1) Crear motor y tablas
    engine = create_engine(db_url, echo=False, future=True)
    Base.metadata.create_all(engine)

    # 2) Sesiones
    Session = sessionmaker(bind=engine, future=True)
    extractor = OddsExtractor()

    # 3) Leer raw JSONL e insertar en BD
    with Session() as session, open(raw_file, 'r', encoding='utf-8') as f:
        for line in f:
            entry = json.loads(line)

            # Guarda la petición cruda
            raw = RawRequest(
                timestamp = datetime.utcnow(),
                url       = entry['url'],
                status    = entry.get('status'),
                body      = entry.get('body')
            )
            session.add(raw)
            session.flush()  # para obtener raw.id

            # Extrae y guarda las Odds relacionadas
            body_bytes = entry.get('body', '').encode()
            for o in extractor.extract(entry['url'], body_bytes):
                odd = Odds(
                    timestamp      = o.timestamp,
                    match_id       = o.match_id,
                    market         = o.market,
                    outcome        = o.outcome,
                    odd            = o.odd,
                    raw_request_id = raw.id
                )
                session.add(odd)

        # Confirma la transacción
        session.commit()

    print(f"[+] Ingestión completa en {db_url}")

if __name__ == '__main__':
    ingest()