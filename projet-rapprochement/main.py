# ================================================
# IMPORTS
# ================================================

import pandas as pd

# ================================================
# CHEMINS DES FICHIERS
# ================================================

#Chemins du grand livre et du releve bancaire
#chemin_gl = "data/grand_livre_assurvia.xlsx"
chemin_rb = "data/releve_bancaire_assurvia.xlsx"
chemin_gl_512 = "data/grand_livre_512_assurvia.xlsx"
chemin_export = "output/export-final.xlsx"
SEUIL_ECART = 50.0

# ================================================
# ÉTAPE 3 — CHARGEMENT ET EXPLORATION
# ================================================

#Chargement du grand livre en excluant la ligne d'en tete
#df_gl = pd.read_excel(chemin_gl, header=1)

#Chargement du releve bancaire en excluant la ligne d'en tete
df_rb = pd.read_excel(chemin_rb, header=1)

df_gl512 = pd.read_excel(chemin_gl_512, header=1)
"""
print("Fichiers chargés\n")
print("-"*7,end="\n"*2)
"""

"""
Lecture du grand livre  :

1. Utilisation de head() pour afficher les premieres lignes
2. Utilisation de dtypes pour afficher les types des colonnes
3. Utilisation de shape pour avoir le nombre de lignes et de colonnes
4. Combinaison de isnull() et sum() pour avoir le nombre de valeurs manquantes par colonne

"""
"""
print("1. Aperçu du Grand Livre : \n")
print(df_gl.head(7),end="\n"*2)
print("-"*7,end="\n"*2)

print("2. Colonnes et types de données (dtypes) : \n")
print(df_gl.dtypes)
print("-"*7,end="\n"*2)

print("3. Dimensions du tableau (Lignes, Colonnes) : \n")
print(df_gl.shape)
print("-"*7,end="\n"*2)

print("4. Nombre de valeurs manquantes par colonne : \n")
print(df_gl.isnull().sum())
print("-"*7,end="\n"*2)"""

"""
Lecture du releve bancaire  :

1. Utilisation de head() pour afficher les premieres lignes
2. Utilisation de dtypes pour afficher les types des colonnes
3. Utilisation de shape pour avoir le nombre de lignes et de colonnes
4. Combinaison de isnull() et sum() pour avoir le nombre de valeurs manquantes par colonne

"""

"""print("1b. Aperçu du Releve bancaire : \n")
print(df_rb.head(7),end="\n"*2)
print("-"*7,end="\n"*2)

print("2b. Colonnes et types de données (dtypes) : \n")
print(df_rb.dtypes)
print("-"*7,end="\n"*2)

print("3b. Dimensions du tableau (Lignes, Colonnes) : \n")
print(df_rb.shape)
print("-"*7,end="\n"*2)

print("4b. Nombre de valeurs manquantes par colonne : \n")
print(df_rb.isnull().sum())
print("-"*7,end="\n"*2)"""

# ================================================
# ÉTAPE 4 — NETTOYAGE ET NORMALISATION
# ================================================

# Filtre le tableau pour enlever la ligne TOTAL

#df_gl = df_gl[df_gl["id_ecriture"] != "TOTAL"]
df_rb = df_rb[df_rb["id_operation"] != "TOTAUX"]
df_gl512 = df_gl512[df_gl512["id_ecriture"] != "TOTAUX"]
df_gl512 = df_gl512[df_gl512["libelle"] != "Solde d'ouverture compte 512"]

# Creation colonne montants

df_gl512["montant"] = df_gl512["débit (€)"].fillna(0) + df_gl512["crédit (€)"].fillna(0)
df_rb["montant"] = df_rb["débit (€)"].fillna(0) + df_rb["crédit (€)"].fillna(0)

# Dictionnaires de nommage

En_TETE = {
    "id_ecriture":"id",
    "montant (€)":"montant",
    "id_operation":"id",
    "date_valeur":"date",
    "description":"libelle",    
    "solde (€)":"solde",
    "débit (€)":"debit",
    "crédit (€)":"credit",
    "solde cumulé (€)":"solde"
}


#df_gl = df_gl.rename(columns=En_TETE)
df_rb = df_rb.rename(columns=En_TETE)
df_gl512 = df_gl512.rename(columns=En_TETE)

#print(df_gl.columns)
#print(df_rb.columns)

#df_gl["date"] = pd.to_datetime(df_gl["date"])
df_rb["date"] = pd.to_datetime(df_rb["date"])
df_gl512["date"] = pd.to_datetime(df_gl512["date"])

#print(df_gl.dtypes)
#print(df_rb.dtypes)

"""df_gl["sens"] = (df_gl["sens"].str.lower()
                 .str.strip()
                 .str.replace("ébit","ebit")
                 .str.replace("édit","edit"))"""

df_rb["sens"] = (df_rb["sens"].str.lower()
                 .str.strip()
                 .str.replace("ébit","ebit")
                 .str.replace("édit","edit"))

df_gl512["sens"] = (df_gl512["sens"].str.lower()
                 .str.strip()
                 .str.replace("ébit","ebit")
                 .str.replace("édit","edit"))

#print(df_gl["sens"].unique())
#print(df_rb["sens"].unique())

#df_gl = df_gl.drop(columns="compte")

df_gl512 = df_gl512.drop(columns=["debit","credit","solde"])
df_rb = df_rb.drop(columns=["debit","credit","solde"])

# print(df_gl512.columns)
# print(df_rb.columns)

# Rajout du signe math pour que les montants dans le GL aient le meme sens que ceux dans le releve

df_gl512.loc[df_gl512["sens"]=="credit","montant"] = df_gl512.loc[df_gl512["sens"]=="credit","montant"] * -1
df_rb.loc[df_rb["sens"]=="debit", "montant"] = df_rb.loc[df_rb["sens"]=="debit", "montant"]  * - 1

# Fusion des tableaux

df_final = pd.merge(df_gl512, df_rb,how="outer",on="montant",indicator=True)

# DataFrame pour les ecritures rapprochees

df_rappro = df_final[df_final["_merge"] =="both"]
df_suspens_gl = df_final[df_final["_merge"] =="left_only"]
df_suspens_rb = df_final[df_final["_merge"] =="right_only"]

NOUVELLE_ENTETE = {
    "id_x":"id_GL",
    "id_GL_x":"id_GL",
    "date_x":"date_GL",
    "date_GL_x":"date_GL",
    "libelle_x":"libelle_GL",
    "libelle_GL_x":"libelle_GL",
    "sens_x":"sens_GL",
    "sens_GL_x":"sens_GL",
    "montant_x":"montant_GL",
    "id_y":"id_RB",
    "id_RB_y":"id_RB",
    "date_y":"date_RB",
    "date_RB_y":"date_RB",
    "libelle_y":"libelle_RB",
    "libelle_RB_y":"libelle_RB",
    "sens_y":"sens_RB",
    "sens_RB_y":"sens_RB",
    "montant_y":"montant_RB",
    "_merge":"Match",
    "Match_x":"match_GL",
    "Match_y":"match_RB"
}

df_rappro = df_rappro.rename(columns=NOUVELLE_ENTETE)

df_suspens_gl = df_suspens_gl.rename(columns=NOUVELLE_ENTETE)
df_suspens_gl = df_suspens_gl.dropna(axis=1,how="all")

df_suspens_rb = df_suspens_rb.rename(columns=NOUVELLE_ENTETE)
df_suspens_rb = df_suspens_rb.dropna(axis=1,how="all")

# Creation d'un tableau de rapprochement de potetiels suspens

df_ecarts_potentiels = df_suspens_gl.merge(df_suspens_rb,how="cross")
df_ecarts_potentiels["ecart"] = abs(df_ecarts_potentiels["montant_x"]-df_ecarts_potentiels["montant_y"])
df_ecarts_potentiels = df_ecarts_potentiels[(df_ecarts_potentiels["ecart"] <= SEUIL_ECART) & (df_ecarts_potentiels["ecart"] > 0)]

df_ecarts_potentiels = df_ecarts_potentiels.dropna(axis=1,how="all")
df_ecarts_potentiels = df_ecarts_potentiels.rename(columns=NOUVELLE_ENTETE)

# Reset des index

df_rappro.reset_index(drop=True, inplace=True)
df_suspens_gl.reset_index(drop=True,inplace=True)
df_suspens_rb.reset_index(drop=True, inplace=True)
df_ecarts_potentiels.reset_index(drop=True, inplace=True)

# Creation du tableau de synthese : Liste des donnees

data_synthese = [
    {"Catégorie": "Rapprochées", "Nombre": len(df_rappro), "Montant Total": df_rappro["montant"].sum()},
    {"Catégorie": "Suspens GL", "Nombre": len(df_suspens_gl), "Montant Total": df_suspens_gl["montant"].sum()},
    {"Catégorie": "Suspens RB", "Nombre": len(df_suspens_rb), "Montant Total": df_suspens_rb["montant"].sum()},
    {"Catégorie": "Écarts Potentiels", "Nombre": len(df_ecarts_potentiels), "Montant Total": df_ecarts_potentiels["ecart"].sum()}
]

# Creation du tableau de synthese : Transformation de la liste des donnees en tableau
df_synthese = pd.DataFrame(data_synthese)

# Creation de l'output

with pd.ExcelWriter(chemin_export) as writer :
    df_synthese.to_excel(writer, sheet_name="SYNTHESE",index=False)
    df_rappro.to_excel(writer,sheet_name="Rapprochees",index=False)
    df_suspens_gl.to_excel(writer,sheet_name="Suspens GL",index=False)
    df_suspens_rb.to_excel(writer,sheet_name="Suspens RB",index=False)
    df_ecarts_potentiels.to_excel(writer,sheet_name="Ecarts potentiels",index=False)

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

print("=== RÉSULTATS DU RAPPROCHEMENT ASSURVIA — JANVIER 2025 ===")
print(f"✓ Lignes rapprochées   : {len(df_rappro)}")
print(f"✓ Suspens GL           : {len(df_suspens_gl)}")
print(f"✓ Suspens RB           : {len(df_suspens_rb)}")
print(f"✓ Écarts potentiels    : {len(df_ecarts_potentiels)}",f"(écart max : {df_ecarts_potentiels["ecart"].sum()}€)")
print(f"✓ Fichier exporté      : {chemin_export}")