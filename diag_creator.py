import streamlit as st
import requests

#post to database
DATABASE_URL = st.secrets["DATABASE_URL"]
DATABASE_API_KEY = st.secrets["DATABASE_API_KEY"]

def get_organizations_from_database():
    url = f"{DATABASE_URL}/rest/v1/organizations"
    headers = {
        "apikey": DATABASE_API_KEY,
        "Authorization": f"Bearer {DATABASE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            orgs = response.json()
            
            if not orgs:
                st.warning("No organizations found in database")
                return []
            
            names = [org['name'] for org in orgs if org.get("status") == "ongoing"]
            return names
        else:
            st.warning(f"Failed to fetch organizations: {response.status_code}")
            return []
    except Exception as e:
        st.warning(f"Error fetching organizations: {e}")
        return []


def post_orga_to_database(orga_name, description):
    url = f"{DATABASE_URL}/rest/v1/organizations"
    headers = {
        "apikey": DATABASE_API_KEY,
        "Authorization": f"Bearer {DATABASE_API_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    data = {
        "name": orga_name,
        "description": description,
    }
    response = requests.post(url, headers=headers, json=data)
    return response

# User Interface
st.title("Générateur pour e-diag personnality")

st.header("Renseignez les informations suivantes:")
orga_name = st.text_input("id de l'e-diag")
st.write(f"e-diag id (tel que ça va apparaite dans la base de données): {orga_name}")

description = st.text_input("description de l'e-diag (contexte & personne référante)")
st.write(f"description de l'e-diag: {description}")

# fetch organization list from database
list_of_orga = get_organizations_from_database()

if orga_name in list_of_orga:
    st.error("cet id existe déjà :pensive:")

submit_button = st.button("Générer l'e-diag")
if submit_button:
    if orga_name not in list_of_orga:
        st.write(f"e-diag id: {orga_name}")
        st.write(f"description: {description}")

        response = post_orga_to_database(orga_name, description)
        if response.status_code == 201 or response.status_code == 204:
            st.success("id a été créé avec succes! :smiley:")
        else:
            st.error(f"Failed to create id: {response.status_code} - {response.text}")
            response = post_orga_to_database(orga_name, description)
    else:
        st.error("id existe déjà dans la base de données :confounded:")
    








