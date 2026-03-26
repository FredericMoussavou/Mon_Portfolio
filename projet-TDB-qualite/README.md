Data Quality Dashboard and Automated Cleansing
Objectif du Projet
Ce projet automatise l'audit et le nettoyage de fichiers de transactions financières. Dans un contexte de clôture comptable ou d'analyse de données bancaires et assurantielles, l'intégrité des informations est critique. Ce script identifie les anomalies, génère des indicateurs de performance (KPI) sur la fiabilité des données et produit un jeu de données sain pour l'exploitation métier.

Stack Technique
Langage : Python 3.13

Bibliothèques :

pandas : Ingestion, filtrage et transformation de données (Data Wrangling).

openpyxl : Moteur de lecture et d'écriture des fichiers Excel.

Fonctionnalités de Diagnostic
Le moteur de contrôle audite quatre dimensions fondamentales de la qualité de données :

Complétude : Détection des valeurs manquantes (NaN) sur les champs critiques (ID Client, Montant).

Unicité : Identification des doublons parfaits et des redondances métiers.

Typage (Sanity Check) : Conversion forcée des montants via to_numeric pour isoler et traiter les erreurs de saisie textuelle.

Calcul de KPI : Détermination automatique du score de santé global du fichier source.

Structure du Projet
Plaintext
PROJET-TDB-QUALITE/
├── data/               # Fichiers sources (Excel contenant des anomalies)
├── output/             # Rapports de sortie (Données nettoyées et logs d'audit)
├── venv/               # Environnement virtuel Python
├── main.py             # Script principal de traitement
├── requirements.txt    # Liste des dépendances
└── README.md           # Documentation technique
Utilisation
Installation des dépendances :

Bash
pip install -r requirements.txt
Exécution du script :

Bash
python main.py
Livrables
Le script génère un fichier data_cleaned.xlsx structuré en deux onglets distincts :

Data_Clean : Le dataset final, dédoublonné et typé, prêt pour l'intégration en base de données ou en outil de BI.

Audit_Log : Un tableau de synthèse récapitulant la volumétrie des erreurs par catégorie et le taux de fiabilité final du fichier traité.