import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import hashlib

# Page config
st.set_page_config(page_title="Hotel Mediterranee", page_icon="🏨", layout="wide")

# Dark theme
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; }
h1, h2 { color: #CC6D3D; }
.stTextInput > div > div > input { background-color: #1e293b; color: white; }
.stSelectbox > div > div > select { background-color: #1e293b; color: white; }
.stButton > button { background: #CC6D3D; color: white; border-radius: 10px; }
.sidebar .stMarkdown { color: white; }
</style>
""", unsafe_allow_html=True)

# Data files
USERS_FILE = 'utilisateurs.json'
ROOMS_FILE = 'chambres.csv'
MAINTENANCE_FILE = 'maintenance_tasks.csv'

# Load users
@st.cache_data
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    default_users = {
        "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "admin", "nom": "Admin"},
        "reception": {"password": hashlib.sha256("recept123".encode()).hexdigest(), "role": "reception", "nom": "Reception"},
        "maint": {"password": hashlib.sha256("maint123".encode()).hexdigest(), "role": "maintenance", "nom": "Maintenance"}
    }
    with open(USERS_FILE, 'w') as f:
        json.dump(default_users, f, indent=2)
    return default_users

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

# Auth
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.nom = ""

if not st.session_state.logged_in:
    st.title("🏨 Hotel Mediterranée")
    username = st.text_input("Utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Connexion"):
        users = load_users()
        h = hashlib.sha256(password.encode()).hexdigest()
        if username in users and users[username]["password"] == h:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.session_state.nom = users[username]["nom"]
            st.rerun()
        else:
            st.error("Erreur de connexion")
else:
    # Main app
    st.title("🏨 Hotel Méditerranee - Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.write(f"👋 {st.session_state.nom}")
        st.write(f"Rôle: {st.session_state.role}")
        if st.button("Déconnexion"):
            for k in st.session_state.keys():
                del st.session_state[k]
            st.rerun()
    
    # Load rooms
    @st.cache_data
    def load_rooms():
        if os.path.exists(ROOMS_FILE):
            df = pd.read_csv(ROOMS_FILE)
            df['numero'] = df['numero'].astype(str)
            return df
        # Create default rooms
        data = []
        for i in range(101, 175):
            data.append({'numero': str(i), 'type': 'Standard', 'aile': 'A', 'statut': 'Libre', 'etage': 1})
        df = pd.DataFrame(data)
        df.to_csv(ROOMS_FILE, index=False)
        return df

    def save_rooms(df):
        df.to_csv(ROOMS_FILE, index=False)

    rooms = load_rooms()
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total", len(rooms))
    with col2:
        st.metric("Libres", len(rooms[rooms.statut == 'Libre']))
    with col3:
        st.metric("Maintenance", len(rooms[rooms.statut == 'Maintenance']))
    
    # Room status update
    st.subheader("Gestion Chambres")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        room_sel = st.selectbox("Chambre", rooms.numero.tolist())
    with col_b:
        new_status = st.selectbox("Statut", ['Libre', 'Occupée', 'Maintenance'])
    if st.button("Mettre à jour"):
        rooms.loc[rooms.numero == room_sel, 'statut'] = new_status
        save_rooms(rooms)
        st.success(f"Chambre {room_sel} → {new_status}")
        st.rerun()
    
    st.dataframe(rooms)
    
    # Maintenance
    if st.session_state.role in ['admin', 'maintenance']:
        st.subheader("Maintenance")
        if st.button("Reset all rooms Libre"):
            rooms['statut'] = 'Libre'
            save_rooms(rooms)
            st.success("Reset OK")
            st.rerun()

Reverted to basic stable version: simple login, room management, metrics, no JS complexity.
Use `streamlit run app.py` to test.
Original advanced version backed up as app_advanced.py.
Data reset available via fix.py if needed.

