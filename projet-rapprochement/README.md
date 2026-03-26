Projet : Rapprochement Bancaire Automatisé (Python)

Quel problème ce projet résout-il ?
Ce script permet de comparer automatiquement un Grand Livre comptable et un Relevé Bancaire pour identifier les opérations qui correspondent et celles qui sont en "suspens" (erreurs ou oublis). Il transforme un travail manuel de plusieurs heures en un clic de quelques secondes.

Technologies utilisées
Python 3 : Le langage de programmation.

Pandas : La bibliothèque pour manipuler les tableaux de données (DataFrames).

Openpyxl : Pour lire et écrire les fichiers Excel (.xlsx).

Comment lancer le script ?
Préparer l'environnement :
Installe les bibliothèques nécessaires avec cette commande :

Bash
pip install pandas openpyxl
Organiser les données :
Place tes fichiers Excel dans le dossier data/ :

grand_livre_512_assurvia.xlsx

releve_bancaire_assurvia.xlsx

Exécuter le robot :
Lance le script principal :

Bash
python main.py
À quoi ressemble le résultat ?
Le script génère un fichier export-final.xlsx dans le dossier output/. Ce fichier contient 3 onglets :

Rapprochees : Les lignes qui matchent parfaitement (Compta = Banque).

Suspens GL : Les écritures présentes uniquement en comptabilité.

Suspens RB : Les opérations présentes uniquement sur le relevé bancaire.