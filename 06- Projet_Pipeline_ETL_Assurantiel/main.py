from modules import errors, extract, transform, load
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
SOURCES = BASE/"sources"
DATABASE = BASE/"database"/"assurvia.db"
OUTPUT = BASE/"output"

if __name__ == "__main__":
    try:
        #========================================
        #ÉTAPE 1 — EXTRACTION
        #========================================

        data,stat_extract = extract.extract_all(SOURCES)

        #========================================
        #ÉTAPE 2 — TRANSFORMATION
        #========================================

        data_clean, stat_transform = transform.transform_all(data)

        #========================================
        #ÉTAPE 3 — LOAD
        #========================================

        stat_load = load.load(data_clean,DATABASE)

        #========================================
        #ÉTAPE 4 — REPORT
        #========================================

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_fichier = f"rapport_{timestamp}.txt"
        chemin_rapport = OUTPUT/nom_fichier

        rapport = f"""
        ========================================
        RAPPORT D'EXÉCUTION — PIPELINE ASSURVIA
        ========================================
        EXTRACTION
        ✓ clients   : {stat_extract.get('clients', {}).get('Nbr ligne',0)} lignes extraites
        ✓ contrats  : {stat_extract.get('contrats', {}).get('Nbr ligne',0)} lignes extraites
        ✓ sinistres : {stat_extract.get('sinistres', {}).get('Nbr ligne',0)} lignes extraites

        TRANSFORMATION
        Clients
            → {stat_transform['clients'].get('nbr doublons', 0)} doublons supprimés
            → {stat_transform['clients'].get('nbr emails invalides', 0)} emails invalides
            → {stat_transform['clients'].get('nbr dates invalides', 0)} dates invalides
        
        Contrats
            → {stat_transform['contrats'].get('nbr primes invalides', 0)} primes invalides
            → {stat_transform['contrats'].get('nbr statut non reconnu', 0)} statuts non reconnus
            → {stat_transform['contrats'].get('nbr client orphelin', 0)} clients orphelins
        
        Sinistres
            → {stat_transform['sinistres'].get('Dates incoherentes', 0)} dates incohérentes
            → {stat_transform['sinistres'].get('nbr montants incoherents', 0)} montants invalides
            → {stat_transform['sinistres'].get('nbr sinistres orphelins', 0)} sinistres orphelins

        CHARGEMENT EN BASE
        ✓ clients   : {stat_load.get('clients', 0)} lignes chargées
        ✓ contrats  : {stat_load.get('contrats', 0)} lignes chargées
        ✓ sinistres : {stat_load.get('sinistres', 0)} lignes chargées

        BASE DE DONNÉES : {DATABASE.relative_to(BASE)}
        ========================================
        """

        print(rapport)

        with open(chemin_rapport, 'w', encoding="utf-8") as f:
            f.write(rapport)

        print(f"Rapport archivé sous : {chemin_rapport.relative_to(BASE)}")
    except Exception as e:
        print(f"✗ Pipeline interrompu : {e}")