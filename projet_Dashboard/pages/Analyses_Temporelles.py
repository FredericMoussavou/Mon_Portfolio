from app import regrouper_fichier, DossierVideError
import pandas as pd
import streamlit as st
from pathlib import Path
import plotly.express as px

st.markdown("""
<style>
div[data-testid="stMetricValue"] > div {
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

BASE = Path(__file__).parent.parent
fichier_data = BASE/"data"


st.title("Dashboard Assurvia")
st.header("Evolution du CA")

st.sidebar.header("Filtres temporels")


try:
    df_test = regrouper_fichier(fichier_data)
    df_test["Date"] = pd.to_datetime(df_test["Date"])
except DossierVideError as e:
    st.error(e)
    st.stop()


region_choisie = st.sidebar.multiselect("Regions",
                                        options=df_test["Region"].unique(),
                                        default=df_test["Region"].unique())

annee_choisie = st.sidebar.multiselect("Annee",
                                       options=sorted(df_test["Date"].dt.year.unique()),
                                       default=df_test["Date"].dt.year.unique())

dict_mois = {
    1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 
    5: "Mai", 6: "Juin", 7: "Juillet", 8: "Août", 
    9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
}

df_test["Mois_Nom"] = df_test["Date"].dt.month.map(dict_mois)

mois_choisi = st.sidebar.multiselect("Mois",
                                     options=dict_mois.values(),
                                     default=dict_mois.values())

filter_period = (
    (df_test["Region"].isin(region_choisie)) & 
    (df_test["Date"].dt.year.isin(annee_choisie)) & 
    (df_test["Mois_Nom"].isin(mois_choisi))
)

#periode_choisie=st.sidebar.multiselect("Periodes",df_test["Date"].unique(),default=df_test["Date"].unique())


df_selectionne = df_test[filter_period]


if not df_selectionne.empty:
    st.subheader("Meilleur CA")
    ca_par_region=df_selectionne.groupby("Region")["Ventes"].sum()
    
    st.metric(label=ca_par_region.idxmax(),value=f"{ca_par_region.max()} $")

    ca_par_temps = df_selectionne.groupby("Date")["Ventes"].sum().sort_index()
    st.line_chart(ca_par_temps)