# Pipeline ETL Assurantiel — Python

## Contexte métier

Une compagnie d'assurance reçoit chaque mois des fichiers de données brutes
depuis plusieurs sources — CRM, système de gestion des sinistres, outil de
facturation. Ces fichiers arrivent dans des formats différents, avec des
qualités variables, et doivent être consolidés dans une base de données
centrale pour alimenter les reportings. Réalisé manuellement, ce travail
est chronophage et source d'erreurs. Ce pipeline l'automatise entièrement.

---

## Résultats sur le jeu de données de démonstration

| Étape | Entrée | Sortie | Anomalies détectées |
|---|---|---|---|
| Clients | 1 020 lignes | 995 lignes propres | 20 doublons, 9 emails invalides, 5 dates invalides |
| Contrats | 1 500 lignes | 1 500 lignes propres | 21 clients orphelins |
| Sinistres | 500 lignes | 496 lignes propres | 4 dates incohérentes, 1 sinistre orphelin |

**3 020 lignes traitées — 2 991 lignes propres chargées en base SQLite en quelques secondes.**

---

## Architecture du pipeline

```
Extract → Transform → Load
```

### Extract
Lecture de tous les fichiers CSV présents dans le dossier `sources/`.
Chaque fichier est chargé dans un DataFrame pandas et retourné dans un
dictionnaire. Les erreurs de lecture sont gérées fichier par fichier
sans interrompre le pipeline.

### Transform
Nettoyage et normalisation des données selon des règles métier définies
par source. Les anomalies sont détectées, comptabilisées et signalées
sans bloquer le pipeline.

Règles appliquées par source :

**Clients**
- Suppression des doublons sur `id_client`
- Validation des emails par expression régulière
- Conversion et validation des dates de naissance
- Normalisation des téléphones manquants

**Contrats**
- Nettoyage des primes (symboles, séparateurs décimaux multiples)
- Normalisation des statuts (actif/Actif/ACTIF → Actif)
- Détection des contrats avec `id_client` inexistant (orphelins)
- Suppression des dates de souscription futures ou invalides

**Sinistres**
- Suppression des montants négatifs ou nuls
- Suppression des dates futures ou invalides
- Détection des sinistres avec `id_contrat` inexistant (orphelins)
- Remplacement des descriptions manquantes

### Load
Chargement des trois DataFrames propres dans une base SQLite locale.
Chaque exécution recrée les tables proprement (`if_exists="replace"`).

---

## Structure du projet

```
pipeline-etl-assurvia/
│
├── sources/              # Fichiers CSV bruts (non versionnés — voir utils/)
├── database/             # Base SQLite générée (non versionnée)
├── output/               # Rapports d'exécution horodatés (non versionnés)
│
├── modules/
│   ├── __init__.py
│   ├── extract.py        # Étape Extract — lecture des fichiers CSV
│   ├── transform.py      # Étape Transform — nettoyage et validation
│   ├── load.py           # Étape Load — écriture en base SQLite
│   └── errors.py         # Exceptions personnalisées
│
├── utils/
│   └── generate_data.py  # Générateur de données fictives (Faker)
│
├── main.py               # Orchestrateur du pipeline
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/votre-nom/pipeline-etl-assurvia.git
cd pipeline-etl-assurvia
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

---

## Utilisation

### 1 — Générer les données sources

```bash
python utils/generate_data.py
```

Cette commande génère trois fichiers CSV dans le dossier `sources/` :
- `clients.csv` — 1 000 clients avec anomalies volontaires
- `contrats.csv` — 1 500 contrats avec formats de prix hétérogènes
- `sinistres.csv` — 500 sinistres avec dates et montants invalides

### 2 — Lancer le pipeline

```bash
python main.py
```

Le pipeline extrait, nettoie et charge les données en base SQLite.
Un rapport d'exécution horodaté est généré dans `output/`.

---

## Rapport d'exécution

Chaque exécution génère un fichier `output/rapport_YYYYMMDD_HHMMSS.txt`
avec le détail de toutes les anomalies détectées et le nombre de lignes
chargées par table.

Exemple de sortie terminal :

```
✓ clients.csv chargé  — 1020 lignes, 8 colonnes
✓ contrats.csv chargé — 1500 lignes, 6 colonnes
✓ sinistres.csv chargé — 500 lignes, 6 colonnes
Clients  : 20 doublons, 9 emails invalides, 5 dates invalides
Contrats : 0 primes invalides, 0 statuts non reconnus, 21 clients orphelins
Sinistres: 4 dates incohérentes, 0 montants invalides, 1 sinistre orphelin
✓ Table 'clients'   chargée — 995 lignes
✓ Table 'contrats'  chargée — 1500 lignes
✓ Table 'sinistres' chargée — 496 lignes
```

---

## Technologies

| Bibliothèque | Rôle |
|---|---|
| pandas | Manipulation et transformation des DataFrames |
| sqlalchemy | Connexion pandas → SQLite |
| faker | Génération de données fictives réalistes |
| numpy | Injection de valeurs manquantes dans les données de test |
| pathlib | Gestion des chemins indépendante de l'OS |

---

## Limites connues

- Le pipeline traite uniquement des fichiers CSV — une évolution naturelle
  serait de supporter des fichiers Excel ou des appels API
- Le mode `if_exists="replace"` recrée les tables à chaque exécution —
  un mode `append` avec gestion des doublons serait plus adapté en production
- Les règles de transformation sont codées en dur dans `transform.py` —
  une évolution serait de les externaliser dans un fichier de configuration YAML

---

## Compétences démontrées

- Architecture modulaire ETL avec séparation des responsabilités
- Gestion défensive des erreurs avec exceptions personnalisées
- Nettoyage de données réelles — regex, normalisation, validation métier
- Persistance en base de données relationnelle avec SQLAlchemy
- Génération de données fictives réalistes avec Faker
- Rapport d'exécution horodaté et archivé automatiquement