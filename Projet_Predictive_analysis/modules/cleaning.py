import pandas as pd

def clean_data(df:pd.DataFrame) -> pd.DataFrame:
    # Creation d'une copie du df reçu
    df_cleaned : pd.DataFrame = df.copy()
    
    # Conversion de la colonne date en date
    df_cleaned["Date"] = pd.to_datetime(df_cleaned["Date"], errors="coerce")

    # Conversion de ma colonne prix en numerique avec suppression d'eventuel symbole
    df_cleaned["Prix"] = (df_cleaned["Prix"].astype(str)
                  .str.replace(r'[^\d,.]',"",regex=True)
                  .str.replace(r'(\d),(\d{3})'," ",regex=True)
                  .str.replace(",","."))
    df_cleaned["Prix"] = pd.to_numeric(df_cleaned["Prix"],errors="coerce")

    # Suppression des lignes dont les dates et prix sont vides
    df_cleaned = df_cleaned.dropna(subset=["Date","Prix"])
    
    # Remplacement des données NA par Inconnu
    df_cleaned[["Nom","Prenom","Telephone","Adresse"]] = df_cleaned[["Nom","Prenom","Telephone","Adresse"]].fillna("Inconnu")

    return df_cleaned

def format_fr(valeur, symbole=""):
    # Formatage de base avec virgule pour les milliers : 1,250.50
    s = f"{valeur:,.2f}"
    # On remplace la virgule par un espace (milliers) 
    # et le point par une virgule (décimales)
    s = s.replace(",", " ").replace(".", ",")
    return f"{s} {symbole}"
