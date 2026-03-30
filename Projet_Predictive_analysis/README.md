Projet Assurvia : Système d'Analyse Décisionnelle et Traitement de Données

Présentation du projet

Ce projet consiste en une application de Business Intelligence conçue pour la société Assurvia. L'objectif est de centraliser, nettoyer et analyser des flux de données hétérogènes provenant de multiples fichiers CSV pour fournir une vision à 360 degrés de l'activité commerciale et des comportements clients.

Le système automatise le pipeline ETL (Extract, Transform, Load) : de la lecture des fichiers bruts sur le disque jusqu'à la visualisation des corrélations statistiques.

Architecture Technique
L'application est découpée en modules spécialisés pour garantir la maintenabilité et la robustesse du code :

app.py : Point d'entrée principal. Gère l'interface utilisateur Streamlit, le routage des données et l'interaction avec l'utilisateur.

modules/cleaning.py : Moteur de traitement de données. Contient les fonctions de normalisation, de nettoyage par expressions régulières (Regex) et de formatage localisé.

modules/errors.py : Gestionnaire d'exceptions personnalisées pour une remontée d'erreurs précise en cas d'anomalie dans le dossier de données.

data/ : Répertoire source destiné à recevoir les fichiers CSV bruts.

Fonctionnalités Principales
1. Traitement et Nettoyage (Pipeline ETL)
Le processus de nettoyage assure l'intégrité des analyses grâce aux étapes suivantes :

Fusion de sources : Concaténation dynamique de tous les fichiers CSV présents dans le répertoire source.

Normalisation monétaire : Utilisation de Regex pour transformer des chaînes de caractères complexes (symboles, séparateurs de milliers variables) en types numériques exploitables.

Gestion des types : Conversion stricte des colonnes temporelles et numériques avec gestion des erreurs via l'argument coerce.

Traitement des valeurs manquantes : Suppression des lignes critiques sans date ou prix, et imputation par la valeur "Inconnu" pour les variables catégorielles (Nom, Adresse, etc.).

2. Analyse Statistique et Corrélation
L'application calcule en temps réel des indicateurs de performance et des mesures statistiques :

Calcul de Corrélation de Pearson : Mesure de la relation linéaire entre l'âge des clients et le montant des contrats.

Agrégations financières : Calcul dynamique du Chiffre d'Affaires total, du panier moyen et du volume de transactions en fonction des filtres appliqués.

3. Visualisations Multidimensionnelles
Le dashboard propose quatre types de visualisations complémentaires via Plotly :

Histogrammes groupés : Analyse de la répartition des canaux de vente par tranche d'âge avec réglage de la précision (bins).

Violin Plots : Visualisation de la densité de population pour identifier les segments clients dominants par canal.

Box Plots : Analyse de la dispersion des prix et identification des valeurs aberrantes (outliers) par type de contrat.

Installation et Déploiement
Prérequis
Python 3.8 ou supérieur

Gestionnaire de paquets pip

Procédure d'installation
Cloner le dépôt :

Bash
git clone https://github.com/votre-compte/assurvia-insight.git
Créer et activer un environnement virtuel :

Bash
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
Installer les dépendances :

Bash
pip install -r requirements.txt
Lancement de l'application
Bash
streamlit run app.py
Spécifications de Formatage
L'application respecte les standards de présentation français pour les rapports financiers :

Séparateur de milliers : Espace.

Séparateur décimal : Virgule.

Unité monétaire : Symbole Euro (€) en suffixe.

Interface : Thème optimisé via injection CSS personnalisée pour une meilleure lisibilité des métriques.

Auteur : [Frederic Moussavou]

Version : 1.0.0