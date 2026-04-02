import pandas as pd
from pathlib import Path
from modules import errors


def extract_csv(chemin:Path) -> pd.DataFrame:
    try :
        df:pd.DataFrame = pd.read_csv(chemin)
        if df.empty:
            raise errors.FichierVideError(f"Le fichier {chemin.name} est vide")
        return df
    except FileNotFoundError:
        print(f"Fichier '{chemin.name}' non trouvé")
        return pd.DataFrame()
    except (errors.FichierVideError) as e:
        print(f"Erreur lors de la lecture de {chemin.name}: {e}")
        return pd.DataFrame()

def extract_all(dossier:Path) -> tuple[dict[str,pd.DataFrame],dict[str,dict]]:
    data = {}
    stat = {}    

    for fichier in dossier.glob("*.csv"):
        df= extract_csv(fichier)
        if not df.empty:
            data[fichier.stem]= df
            stat[fichier.stem]= {"Nbr ligne":len(df),
                                "Nbr colonnes":len(df.columns),
                                "Colonnes":df.columns.tolist()}
            print(f"✓ {fichier.name} chargé — {len(df)} lignes, {len(df.columns)} colonnes")
                              
    return (data,stat)



