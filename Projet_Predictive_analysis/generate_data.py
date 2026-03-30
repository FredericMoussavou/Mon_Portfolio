import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

fake = Faker(['fr_FR']) # Pour avoir des noms et adresses bien français

def generer_donnees_assurvia_complexe(n_lignes=1000):
    np.random.seed(42)
    
    # --- Données de base (reprise du script précédent) ---
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=np.random.randint(0, 366)) for _ in range(n_lignes)]
    contrats_base = {"Auto": 450, "Habitation": 250, "Santé": 800, "Loisirs": 120}
    types = np.random.choice(list(contrats_base.keys()), n_lignes)
    prix = [contrats_base[t] * np.random.uniform(0.8, 1.2) for t in types]
    ages = np.random.randint(18, 85, n_lignes)
    canaux = np.random.choice(["Web", "Téléphone", "Agence"], n_lignes)
    regions = np.random.choice(["Nord", "Sud", "Est", "Ouest", "IDF"], n_lignes)
    csat = np.random.randint(1, 6, n_lignes)

    # --- Nouvelles Données Personnelles avec Faker ---
    noms = [fake.last_name() for _ in range(n_lignes)]
    prenoms = [fake.first_name() for _ in range(n_lignes)]
    adresses = [fake.address().replace('\n', ', ') for _ in range(n_lignes)]
    telephones = [fake.phone_number() for _ in range(n_lignes)]

    # Création du DataFrame
    df = pd.DataFrame({
        "Date": dates,
        "Nom": noms,
        "Prenom": prenoms,
        "Telephone": telephones,
        "Adresse": adresses,
        "Contrat": types,
        "Prix": prix,
        "Age_Client": ages,
        "Canal": canaux,
        "Region": regions,
        "Satisfaction": csat
    })

    # --- Introduction volontaire de données manquantes (NaN) ---
    # On choisit environ 15% des lignes pour supprimer des infos
    for col in ["Telephone", "Adresse", "Prenom"]:
        mask = np.random.random(n_lignes) < 0.15 # 15% de chance d'être vide
        df.loc[mask, col] = np.nan

    return df.sort_values("Date")

# Génération
df_final = generer_donnees_assurvia_complexe(2000)
df_final.to_csv("assurvia_data_science_v2.csv", index=False)
print("✅ Fichier généré avec succès (incluant des données manquantes) !")