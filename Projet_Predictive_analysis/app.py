import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from modules import cleaning, errors

st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 24px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

BASE = Path(__file__).parent
dossier_fichier = BASE/"data"

@st.cache_data
def load_and_clean_data(chemin : Path) -> pd.DataFrame:
    liste_fichier = []

    for fichier in chemin.glob("*.csv"):
        df = pd.read_csv(fichier)
        liste_fichier.append(df)
    
    if liste_fichier:
        df_global = pd.concat(liste_fichier,ignore_index=True)
        df_global = cleaning.clean_data(df_global)
    else:
        raise errors.DossierVideError("Le dossier data est vide ou ne contient pas de fichier .csv")
    
    return df_global

try:
    df = load_and_clean_data(dossier_fichier)
except errors.DossierVideError as e:
    st.error(e)
    st.stop()

st.title("Assurvia Insight")
st.subheader("Dashboard Analytics 360°")

st.sidebar.header("Filtres")

choix_contrat = st.sidebar.multiselect("Type de contrats",
                                       df["Contrat"].unique(),
                                       default=df["Contrat"].unique())

choix_canal = st.sidebar.multiselect("Type de canal",
                                       df["Canal"].unique(),
                                       default=df["Canal"].unique())

filter_contrat_and_canal = (
    (df["Contrat"].isin(choix_contrat)) &
    (df["Canal"].isin(choix_canal))
)



df_selected = df[filter_contrat_and_canal]
corr_age_prix =df_selected["Age_Client"].corr(df_selected["Prix"])

if not df_selected.empty:


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("CA annuel",value= cleaning.format_fr(df_selected["Prix"].sum(),"€"))
    with col2:
        st.metric("Prix moyen",value= cleaning.format_fr(df_selected["Prix"].mean(),"€"))
    with col3:
        st.metric("Nbr Transactions",value=len(df_selected))
    with col4:
        st.metric("Corr Age/Prix", value= cleaning.format_fr(corr_age_prix))
    

    st.divider()
    st.dataframe(df_selected,
                hide_index=True,
                column_config={
                    "Prix":st.column_config.NumberColumn("Prix",format="%.2f €")
                })
    st.sidebar.header("Reglages")
    nb_tranches = st.sidebar.slider("Précision de l'analyse (Nombre de barres)", 5, 100, 30)

    st.subheader("Analyse de la Distribution des Ages")
    age_col1, age_col2 = st.columns(2)

    with age_col1:
        figure = px.histogram(df_selected,x="Age_Client",
                            color="Canal",
                            nbins=nb_tranches,
                            barmode="group",
                            title="Distrib. des Canaux de Souscription/Tranche d'Âge")
        st.plotly_chart(figure)

    with age_col2:
        # Le Violin Plot pour voir la "densité" (où se concentrent la majorité des ventes)
        fig_violin = px.violin(
            df_selected, 
            x="Canal", 
            y="Age_Client", 
            color="Canal", 
            box=True, # Ajoute la mini-boîte à l'intérieur pour le meilleur des deux mondes
            title="Densité des Ages par Canal",
            points="all" # Affiche tous les points pour voir le volume réel
        )
        st.plotly_chart(fig_violin, use_container_width=True)
    st.divider() # Une petite ligne de séparation pour la lisibilité
    
    # Création de deux colonnes pour les graphiques
    st.subheader("Analyse de la Distribution des Prix")
    plot_col1, plot_col2 = st.columns(2)

    with plot_col1:
        # Le Box Plot pour voir les outliers et les quartiles par type de contrat
        fig_box = px.box(
            df_selected, 
            x="Contrat", 
            y="Prix", 
            color="Contrat",
            title="Dispersion des Prix par Contrat",
            points="outliers" # Affiche uniquement les points très éloignés
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with plot_col2:
        # Le Violin Plot pour voir la "densité" (où se concentrent la majorité des ventes)
        fig_violin = px.violin(
            df_selected, 
            x="Canal", 
            y="Prix", 
            color="Canal", 
            box=True, # Ajoute la mini-boîte à l'intérieur pour le meilleur des deux mondes
            title="Densité des Prix par Canal",
            points="all" # Affiche tous les points pour voir le volume réel
        )
        st.plotly_chart(fig_violin, use_container_width=True)
else:
    st.warning("⚠️ Veuillez sélectionner au moins une région pour afficher les données.")

