# analysis.py
import pandas as pd
from sqlalchemy import create_engine
from math import isfinite

DB_URL = 'sqlite:///bets.db'
CUTOFF = 0.50

def load_odds():
    engine = create_engine(DB_URL, future=True)
    return pd.read_sql_table('odds', con=engine)

def compute_implied(df):
    df['p_impl'] = df['odd'].apply(lambda o: 1/o if isfinite(o) and o>0 else 0)
    df['group']  = df['match_id'] + "__" + df['market']
    over = df.groupby('group')['p_impl'].transform('sum')
    df['p_norm'] = df['p_impl'] / over
    return df

def find_value(df):
    return df[df['p_norm'] < CUTOFF]

def main():

    # 1) Carga y muestra un mini-resumen
    df = load_odds()
    print(f"⚙️ Total de odds cargadas: {len(df)}")
    print("Mercados disponibles:", df['market'].unique())
    print(df[['odd', 'match_id', 'market']].head(5).to_string(index=False))

    # 2) Computa p_norm
    df = compute_implied(df)

    # ———> Aquí insertamos el debug de rango de p_norm <———
    print(f"🔍 Rango de p_norm: {df['p_norm'].min():.4f}  –  {df['p_norm'].max():.4f}")
    # ——————————————————————————————————————————————

    # 3) Filtra value bets
    vb = find_value(df)
    print("\nValue Bets encontradas:\n",
          vb[['match_id', 'market', 'outcome', 'odd', 'p_norm']].to_string(index=False))

if __name__ == '__main__':
    main()