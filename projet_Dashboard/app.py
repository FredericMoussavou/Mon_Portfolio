import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px

st.markdown("""
<style>
div[data-testid="stMetricValue"] > div {
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

BASE = Path(__file__).parent
fichier_data = BASE/"data"


st.title("Dashboard Assurvia")
st.subheader("KPIs Ventes")

class DossierVideError(Exception):
    pass

@st.cache_data
def regrouper_fichier(chemin : Path):
    liste_fichiers = []
    for fichier in chemin.glob("*.xlsx"):
        df_temp = pd.read_excel(fichier)
        liste_fichiers.append(df_temp)
    if liste_fichiers:
        df_global = pd.concat(liste_fichiers, ignore_index=True)
        df_global["Date"] = pd.to_datetime(df_global["Date"])
    else:
        raise DossierVideError("Le dossier data est vide ou ne contient pas de fichier .xlsx")

    return df_global

st.sidebar.header("Filtre")

try:
    df_test = regrouper_fichier(fichier_data)
except DossierVideError as e:
    st.error(e)
    st.stop()

region_choisie = st.sidebar.multiselect("Regions",df_test["Region"].unique(),default=df_test["Region"].unique())
df_selectionne = df_test[df_test["Region"].isin(region_choisie)]

if not df_selectionne.empty:
    

    ca_par_region = df_selectionne.groupby("Region")["Ventes"].sum()

    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:
        st.metric(label="CA Total",value=f"{df_selectionne["Ventes"].sum():,.2f} $")
    with col2:
        st.metric(label="CA min",value=f"{df_selectionne["Ventes"].min():,.2f} $")
    with col3:
        st.metric(label="CA max",value=f"{df_selectionne["Ventes"].max():,.2f} $")
    with col4:
        st.metric(label="Nombre de ventes",value=len(df_selectionne))
    with col5:
        st.metric(label="Panier moyen",value=f"{df_selectionne["Ventes"].sum()/len(df_selectionne):,.2f} $")

    st.dataframe(df_selectionne.head(10))

    st.subheader("Répartition du CA par Région")
    
    # Graphique CA par region

    df_bar = ca_par_region.reset_index()
    figure_bar = px.bar(df_bar,x='Region',
                        y='Ventes',
                        color='Region'
                        ,title='CA par Région')
    
    st.plotly_chart(figure_bar)

    # Camembert repartition CA par region
    df_pie = ca_par_region.reset_index()
    figure = px.pie(df_pie, values='Ventes', names='Region', title='Répartition par CA')
    st.plotly_chart(figure)

    # Bouton de telechargement donnees en CSV
    csv = df_selectionne.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
    label="Télécharger les données (CSV)",
    data=csv,
    file_name='export_assurvia.csv',
    mime='text/csv',
    )
else:
    st.warning("⚠️ Veuillez sélectionner au moins une région pour afficher les données.")

