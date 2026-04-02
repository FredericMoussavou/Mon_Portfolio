import pandas as pd
from pathlib import Path
import sqlite3
from sqlalchemy import create_engine


def load(data_clean: dict[str, pd.DataFrame], chemin_db: Path) -> dict[str, int]:
    stats_loads = {}
    engine = create_engine(f"sqlite:///{chemin_db}")
    
    with engine.connect() as conn:
        for nom_table, df in data_clean.items():
            if not df.empty:
                df.to_sql(
                    name=nom_table,
                    con=conn,
                    if_exists="replace",
                    index=False
                )
                stats_loads[nom_table] = len(df)
                print(f"✓ Table '{nom_table}' chargée — {len(df)} lignes")
            else:
                stats_loads[nom_table] = 0

    print(f"✓ Base de données : {chemin_db}")

    return stats_loads