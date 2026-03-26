import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent
liste_fichiers = []

dossier = BASE/"sources"
dossier_output = BASE/"output"/"rapport_final.xlsx"

for chemin in dossier.glob("*.xlsx"):
    df_temp = pd.read_excel(chemin)
    liste_fichiers.append(df_temp)

if len(liste_fichiers):
    df_final = pd.concat(liste_fichiers,ignore_index=True)

    # Conversion de la date
    df_final["Date"] = pd.to_datetime(df_final["Date"])

    #Extraction de la periode dans la colonne Mois
    df_final["Mois"] = df_final["Date"].dt.to_period('M')

    #Regroupement des ventes par periode (CA/M)
    df_mensuel = df_final.groupby("Mois")["Ventes"].sum().reset_index()

    #Regroupemet des ventes par regions (CA/R)
    df_region = df_final.groupby("Region")["Ventes"].sum().reset_index().sort_values(by="Ventes",ascending=False)
    meilleure_region = df_region.iloc[0]["Region"]

    # TCD

    df_pivot = df_final.pivot_table(
        index= "Region",
        columns="Mois",
        values="Ventes",
        aggfunc="sum"
    ).reset_index()

    df_pivot.columns = [str(col) for col in df_pivot.columns]

    with pd.ExcelWriter(dossier_output) as writer:
        df_mensuel.to_excel(writer,sheet_name="CA par mois",index=False)
        df_region.to_excel(writer,sheet_name="CA par Region",index=False)
        df_pivot.to_excel(writer,sheet_name="TCD mensuel par region",index=False)
    

        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for col in worksheet.columns:
                max_length = 0
                column_letter = col[0].column_letter # Récupère la lettre (A, B, C...)
                
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                # On ajuste la largeur avec une petite marge (+2)
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    print("=== RAPPORT CONSOLIDÉ DES VENTES ===")
    print(f"✓ Fichiers chargés      : {len(liste_fichiers)}")
    print(f"✓ Lignes consolidées    : {len(df_final)}")
    print(f"✓ Période couverte      : du {df_final["Mois"].min()} au {df_final["Mois"].max()}")
    print(f"✓ Meilleure région      : {meilleure_region}")
    print("✓ Fichier exporté       : output/rapport_final.xlsx")
else :
    print('Le dossier "sources/" est vide ou ne contient aucun fichier .xlsx')
