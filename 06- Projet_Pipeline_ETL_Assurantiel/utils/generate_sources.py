import pandas as pd
import numpy as np
from faker import Faker
import random
from pathlib import Path

# Initialisation
fake = Faker('fr_FR')
BASE_DIR = Path(__file__).parent.parent
SOURCE_DIR = BASE_DIR / "sources"
SOURCE_DIR.mkdir(exist_ok=True)

def generate_data(n_clients=1000, n_contrats=1500, n_sinistres=500):
    print(f"🚀 Initialisation de la génération : {n_clients} clients, {n_contrats} contrats, {n_sinistres} sinistres.")

    # --- 1. GÉNÉRATION DES CLIENTS ---
    clients = []
    for i in range(1, n_clients + 1):
        clients.append({
            "id_client": i,
            "nom": fake.last_name(),
            "prenom": fake.first_name(),
            "date_naissance": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),
            "ville": fake.city(),
            "code_postal": fake.postcode(),
            "email": fake.ascii_free_email(),
            "telephone": fake.phone_number()
        })
    df_clients = pd.DataFrame(clients)

    # Injection Anomalies Clients
    nb_doublons = 20
    nb_emails_inv = 10
    nb_dates_inv = 5
    nb_tel_nan = 15

    # Doublons (même id_client)
    df_clients = pd.concat([df_clients, df_clients.sample(nb_doublons)], ignore_index=True)
    # Emails invalides
    idx_email = df_clients.sample(nb_emails_inv).index
    df_clients.loc[idx_email, 'email'] = "error_at_domain.com"
    # Dates invalides (format impossible)
    idx_date = df_clients.sample(nb_dates_inv).index
    df_clients.loc[idx_date, 'date_naissance'] = "1990-31-02"
    # Téléphones manquants
    idx_tel = df_clients.sample(nb_tel_nan).index
    df_clients.loc[idx_tel, 'telephone'] = np.nan

    # --- 2. GÉNÉRATION DES CONTRATS ---
    types_contrat = ["Auto", "Habitation", "Santé", "Prévoyance"]
    statuts = ["actif", "Actif", "ACTIF", "Résilié", "REsilie", "Suspendu"]
    contrats = []
    nb_clients_fantomes = 10
    
    # IDs existants + IDs fantômes (9999)
    client_ids = list(df_clients['id_client'].unique()) + [9999] * nb_clients_fantomes
    
    for i in range(1, n_contrats + 1):
        prix_base = random.uniform(300, 2500)
        format_prix = random.choice([
            f"{prix_base:.2f}", 
            f"{int(prix_base)} €", 
            f"{str(prix_base).replace('.', ',')}", 
            f"  {prix_base:.1f}  "
        ])

        contrats.append({
            "id_contrat": i,
            "id_client": random.choice(client_ids),
            "type_contrat": random.choice(types_contrat),
            "date_souscription": fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
            "prime_annuelle": format_prix,
            "statut": random.choice(statuts)
        })
    df_contrats = pd.DataFrame(contrats)

    # --- 3. GÉNÉRATION DES SINISTRES ---
    sinistres = []
    nb_contrats_fantomes = 5
    nb_dates_futures = 4
    
    contrat_ids = list(df_contrats['id_contrat'].unique()) + [8888] * nb_contrats_fantomes
    
    for i in range(1, n_sinistres + 1):
        sinistres.append({
            "id_sinistre": 5000 + i,
            "id_contrat": random.choice(contrat_ids),
            "date_sinistre": fake.date_between(start_date='-3y', end_date='today').strftime('%Y-%m-%d'),
            "montant_sinistre": round(random.uniform(-100, 5000), 2),
            "statut_sinistre": random.choice(["Ouvert", "Clôturé", "Expertise", "Rejeté"]),
            "description": random.choice([fake.sentence(), np.nan])
        })
    df_sinistres = pd.DataFrame(sinistres)

    # Injection Dates futures (aléatoires)
    idx_futures = df_sinistres.sample(nb_dates_futures).index
    df_sinistres.loc[idx_futures, 'date_sinistre'] = "2030-12-25"
    # Calcul des montants négatifs pour le rapport
    nb_negatifs = len(df_sinistres[df_sinistres['montant_sinistre'] < 0])

    # SAUVEGARDE
    df_clients.to_csv(SOURCE_DIR / "clients.csv", index=False)
    df_contrats.to_csv(SOURCE_DIR / "contrats.csv", index=False)
    df_sinistres.to_csv(SOURCE_DIR / "sinistres.csv", index=False)

    # --- RÉSUMÉ DES ANOMALIES (Le Référentiel) ---
    print("\n" + "="*30)
    print("📋 RÉSUMÉ DES ANOMALIES INJECTÉES")
    print("="*30)
    print(f"✓ Clients doublons (ID identiques) : {nb_doublons}")
    print(f"✓ Emails invalides                 : {nb_emails_inv}")
    print(f"✓ Dates de naissance impossibles   : {nb_dates_inv}")
    print(f"✓ Téléphones manquants             : {nb_tel_nan}")
    print(f"✓ IDs clients fantômes (dans ctr)  : {nb_clients_fantomes} (ID=9999)")
    print(f"✓ IDs contrats fantômes (dans sin) : {nb_contrats_fantomes} (ID=8888)")
    print(f"✓ Montants sinistres négatifs      : ~{nb_negatifs}")
    print(f"✓ Dates sinistres dans le futur    : {nb_dates_futures}")
    print("="*30)
    print(f"\n✅ Fichiers prêts dans : {SOURCE_DIR}\n")

if __name__ == "__main__":
    generate_data()