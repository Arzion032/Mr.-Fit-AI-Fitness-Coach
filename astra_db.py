from astrapy import DataAPIClient
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

ENDPOINT = os.getenv('ASTRA_ENDPOINT')
TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")

@st.cache_resource()
def get_db():
    client = DataAPIClient(TOKEN)
    db = client.get_database_by_api_endpoint(ENDPOINT)
    return db

db= get_db()
collection_names = ["user_profile", "notes"]

for collection in collection_names:
    
    try:  
        db.create_collection(collection)
        
    except:
        pass

user_profile = db.get_collection("user_profile")
notes = db.get_collection("notes")