import pandas as pd

chemin_data = "data/data_qualite.xlsx"
chemin_output = "output/data_cleaned.xlsx"

# Chargement des donnees

df_donnees = pd.read_excel(chemin_data)
lignes_total = len(df_donnees)

"""print(pd.isnull(df_donnees).sum())
print("\n","-"*10,"\n")
print(df_donnees.duplicated().sum())
print("\n","-"*10,"\n")
print(df_donnees.dtypes)"""

# Conversion de la colonne date et creation d'une image avec les dates futures

df_donnees["Date_Transaction"] = pd.to_datetime(df_donnees["Date_Transaction"],errors="coerce")
df_dates_futures = df_donnees[df_donnees["Date_Transaction"] > pd.Timestamp.now()]
df_donnees = df_donnees[df_donnees["Date_Transaction"] <= pd.Timestamp.now()]

# Conversion de la colonne montant en numeric

df_donnees["Montant"] = pd.to_numeric(df_donnees["Montant"],errors="coerce")

# DaraFrames des donnees vides et des doublons

df_vides = df_donnees[df_donnees.isnull().any(axis=1)]

print("\n","-"*10,"\n")
df_doublons = df_donnees[df_donnees.duplicated()]

# Nouveau Df pour fichier final

df_clean = df_donnees.drop_duplicates().dropna(how="any")

# Le petit défi de calcul (KPI)

lignes_propres = len(df_clean)
kpi_sante = (lignes_propres/lignes_total) * 100

# Creation de la synthese
data_synthese = [
    {"Categorie":"Doublons","Nombre":len(df_doublons)},
    {"Categorie":"Lignes vides","Nombre":len(df_vides)},
    {"Categorie":"Dates future","Nombre":len(df_dates_futures)},
    {"Categorie":"Lignes supprimees","Nombre":lignes_total - lignes_propres},
    {"Categorie":"KPI Sante_fichier","Nombre": f"{kpi_sante:.2f}%"}
]

df_audit = pd.DataFrame(data_synthese)

# Ecriture dans le fichier final

with pd.ExcelWriter(chemin_output) as writer :
    df_clean.to_excel(writer,sheet_name="Data_Clean",index=False)
    df_audit.to_excel(writer, sheet_name="Audit_Log",index=False)
    df_dates_futures.to_excel(writer, sheet_name="Dates_futures", index=False)

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


print("=== RAPPORT QUALITÉ DES DONNÉES ===")
print(f"✓ Lignes chargées       : {lignes_total}")
print(f"✓ Doublons détectés     : {len(df_doublons)}")
print(f"✓ Lignes vides          : {len(df_vides)}")
print(f"✓ Dates futures         : {len(df_dates_futures)}")
print(f"✓ KPI santé fichier     : {kpi_sante:.2f}%")
print("✓ Fichier exporté       : output/data_cleaned.xlsx")


    