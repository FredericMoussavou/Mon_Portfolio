import pandas as pd
import os

# Création du dossier s'il n'existe pas
os.makedirs("sources", exist_ok=True)

regions = ["Nord", "Sud", "Est", "Ouest"]
mois_liste = ["Janvier", "Fevrier", "Mars"]

for i, mois in enumerate(mois_liste):
    data = {
        "Date": [f"2024-0{i+1}-15"] * 4,
        "Region": regions,
        "Ventes": [1000 + (i*100), 1200 - (i*50), 800 + (i*200), 1500 - (i*100)],
        "Contrats_Signes": [10 + i, 12, 8 + i*2, 15 - i]
    }
    df = pd.DataFrame(data)
    df.to_excel(f"sources/ventes_{mois.lower()}.xlsx", index=False)

print("✅ Les 3 fichiers (janvier, fevrier, mars) ont été créés dans /sources")