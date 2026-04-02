import pandas as pd

def transform_clients(df:pd.DataFrame) -> tuple[pd.DataFrame,dict]:
    stat = {}

    stat['nbr doublons'] = df.duplicated(subset='id_client').sum()
    df = df.drop_duplicates(subset='id_client')

    masque_email = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,5}$'
    masque_valide = df['email'].str.contains(masque_email,
                                             regex=True,
                                             na=False)
    
    df.loc[~masque_valide,'email'] = pd.NA

    df['date_naissance'] = pd.to_datetime(df['date_naissance'],
                                          errors='coerce')
    
    stat['nbr dates invalides'] = df['date_naissance'].isna().sum()
    
    stat['nbr emails invalides'] = df['email'].isna().sum()
    
    df['telephone'] = df['telephone'].fillna('Inconnu')

    df = df.dropna(subset='date_naissance')
    
    print(f'Clients : {stat['nbr doublons']} doublons, {stat['nbr emails invalides']} emails invalides, {stat['nbr dates invalides']} dates invalides')
    return (df,stat)


def transform_contrats(df:pd.DataFrame, df_clients_clean:pd.DataFrame) -> tuple[pd.DataFrame,dict]:
    stat = {}

    df['prime_annuelle'] = (df['prime_annuelle'].astype(str)
                            .str.replace(r'[^\d.,]',"",regex=True)
                            .str.replace(r'(\d),(\d{3})', r'\1\2', regex=True)
                            .str.replace(',','.'))
    
    df['prime_annuelle'] = pd.to_numeric(df['prime_annuelle'],errors='coerce')

    stat['nbr primes invalides'] = df['prime_annuelle'].isna().sum()

    df['date_souscription'] = pd.to_datetime(df['date_souscription'],errors='coerce')
    
    stat['nbr dates incoherentes'] = ((df['date_souscription'] > pd.Timestamp.now()).sum() +
                                         df['date_souscription'].isna().sum())
    
    df = df[df['date_souscription'] <= pd.Timestamp.now()]
    
    df = df.dropna(subset=['prime_annuelle','date_souscription'])

    mapping_status = {
        'actif'    : 'Actif',
        'résilié'  : 'Résilié',
        'resilie'  : 'Résilié',
        'résilie'  : 'Résilié',
        'suspendu' : 'Suspendu'
    }

    df['statut'] = (df['statut'].str.lower()
                                .str.strip()
                                .map(mapping_status))
    
    stat['nbr statut non reconnu'] = df['statut'].isna().sum()
    
    df['statut'] = df['statut'].fillna('Inconnu')

    identifiant_clean = df_clients_clean['id_client']

    df['client_orphelin'] = (~df['id_client'].isin(identifiant_clean))

    stat['nbr client orphelin'] = df['client_orphelin'].sum()

    print(f'Contrats : {stat['nbr primes invalides']} primes invalides, {stat['nbr statut non reconnu']} status non reconnus, {stat['nbr client orphelin']} clients sans iD, {stat['nbr dates incoherentes']} dates incohérentes' )

    return (df,stat)


def transform_sinistres(df:pd.DataFrame, df_contrats_clean:pd.DataFrame) -> tuple[pd.DataFrame,dict]:
    stat = {}

    df['date_sinistre'] = pd.to_datetime(df['date_sinistre'], errors='coerce')
    stat['Dates incoherentes'] = (df['date_sinistre'].isna().sum() + 
                                  (df['date_sinistre'] > pd.Timestamp.now()).sum())
    
    df = df.dropna(subset='date_sinistre')
    df = df[df['date_sinistre'] <= pd.Timestamp.now()]

    # Nettoyage défensif — utile si les montants viennent d'un export ERP avec symboles
    df['montant_sinistre'] = (df['montant_sinistre'].astype(str)
                                                    .str.replace(r'[^\d.,]',"",regex=True)
                                                    .str.replace(r'(\d),(\d{3})', r'\1\2', regex=True)
                                                    .str.replace(',','.'))
    
    df['montant_sinistre'] = pd.to_numeric(df['montant_sinistre'], errors='coerce')
    stat['nbr montants incoherents'] = (df['montant_sinistre'] <= 0).sum()

    df = df[df['montant_sinistre'] > 0]

    df['sinistres_orphelin'] = (~df['id_contrat'].isin(df_contrats_clean['id_contrat']))

    stat['nbr sinistres orphelins'] = df['sinistres_orphelin'].sum()

    df['description'] = df['description'].fillna('Non renseigné')

    print(f'Sinistres : {stat['Dates incoherentes']} dates invalides, {stat['nbr montants incoherents']} montants invalides, {stat['nbr sinistres orphelins']} sinistres orphelins')
    
    return (df,stat)

def transform_all(data:dict[str,pd.DataFrame]) -> tuple[dict[str, pd.DataFrame], dict[str, dict]]:
    data_clean = {}
    stat_clean = {}

    df_clients = data.get('clients')

    if df_clients is not None:
        df_clients_clean, stat_client = transform_clients(df_clients)
        data_clean['clients'] = df_clients_clean
        stat_clean['clients'] = stat_client
    else:
        data_clean['clients'] = pd.DataFrame(columns=['id_client'])
        stat_clean['clients'] = {'error': 'Fichier manquant'}
    
    df_contrats = data.get('contrats')

    if df_contrats is not None and not data_clean['clients'].empty:
        df_contrats_clean, stat_contrat = transform_contrats(df_contrats,data_clean['clients'])
        data_clean['contrats'] = df_contrats_clean
        stat_clean['contrats'] = stat_contrat
    else:
        data_clean['contrats'] = pd.DataFrame(columns=['id_contrat'])
        stat_clean['contrats'] = {'error': 'Fichier manquant'}
    
    df_sinistres = data.get('sinistres')

    if df_sinistres is not None and not data_clean['contrats'].empty:
        df_sinistres_clean, stat_sinistres = transform_sinistres(df_sinistres,data_clean['contrats'])
        data_clean['sinistres'] = df_sinistres_clean
        stat_clean['sinistres'] = stat_sinistres
    else:
        data_clean['sinistres'] = pd.DataFrame(columns=['id_sinistre'])
        stat_clean['sinistres'] = {'error':'Fichier manquant'}
    
    return (data_clean,stat_clean)