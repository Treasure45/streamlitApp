import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Fonction pour se connecter à la base de données
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        if connection.is_connected():
            st.success("Connexion à la base de données réussie")
    except Error as e:
        st.error(f"Erreur lors de la connexion à la base de données : {e}")
    return connection

# Fonction pour exécuter une requête de recherche
def execute_search_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# Fonction pour ajouter un champ à une table
def add_column_to_table(connection, table_name, column_name, column_type):
    cursor = connection.cursor()
    query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
    cursor.execute(query)
    connection.commit()

# Interface utilisateur Streamlit
st.title("Application de Recherche et de Gestion MySQL")

# Informations de connexion
st.sidebar.header("Informations de Connexion à la Base de Données")
host_name = st.sidebar.text_input("Hôte", "localhost")
user_name = st.sidebar.text_input("Utilisateur", "root")
user_password = st.sidebar.text_input("Mot de passe", type="password")
db_name = st.sidebar.text_input("Nom de la Base de Données", "mydatabase")

# Connexion à la base de données
if st.sidebar.button("Se Connecter"):
    st.session_state.connection = create_connection(host_name, user_name, user_password, db_name)

# Initialiser connection dans session_state s'il n'existe pas
if 'connection' not in st.session_state:
    st.session_state.connection = None

# Recherches interactives
st.header("Recherche de Commandes")
queryDb = st.selectbox("Sélectionnez le statut de la commande", ["37445", "37190"])
query = f"SELECT * FROM atl_renf_acc WHERE lot = '{queryDb}'"
if st.button("Rechercher"):
    if st.session_state.connection and st.session_state.connection.is_connected():
        results = execute_search_query(st.session_state.connection, query)
        df = pd.DataFrame(results)
        st.write(df)
    else:
        st.error("Veuillez vous connecter à la base de données.")

# Ajout d'un champ à une table
st.header("Ajouter un Champ à une Table")
table_name = st.text_input("Nom de la Table")
column_name = st.text_input("Nom du Champ")
column_type = st.text_input("Type du Champ")
if st.button("Ajouter Champ"):
    if st.session_state.connection and st.session_state.connection.is_connected():
        add_column_to_table(st.session_state.connection, table_name, column_name, column_type)
        st.success(f"Champ {column_name} ajouté à la table {table_name}")
    else:
        st.error("Veuillez vous connecter à la base de données.")

# Fermeture de la connexion à la base de données
if st.sidebar.button("Déconnecter"):
    if st.session_state.connection and st.session_state.connection.is_connected():
        st.session_state.connection.close()
        st.session_state.connection = None
        st.success("Connexion à la base de données fermée")
