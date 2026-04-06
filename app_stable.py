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
.room-card { background: #1e293b; border-radius: 8px; padding: 10px; margin: 5px; }
</style>
""", unsafe_allow_html=True)

# Data files
USERS_FILE = 'utilisateurs.json'
ROOMS_FILE = 'chambres.csv'
MAINTENANCE_FILE = 'maintenance_tasks.csv'

# Users
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

# Auth state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.nom = ""

# Login page
if not st.session_state.logged_in:
    st.title("🏨 Hotel Méditerranée")
    col1, col2 = st.columns([2,1])
    with col1:
        username = st.text_input("Utilisateur")
        password = st.text_input("Mot de passe", type="password")
    with col2:
        st.info("admin/admin123")
    if st.button("🔑 Connexion"):
        users = load_users()
        h = hashlib.sha256(password.encode()).hexdigest()
        if username in users and users[username]["password"] == h:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.session_state.nom = users[username]["nom"]
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects")
else:
    # Main dashboard
    st.title("🏨 Hotel Méditerranée Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"**👋 {st.session_state.nom}**")
        st.markdown(f"**Rôle:** {st.session_state.role.title()}")
        if st.button("🚪 Déconnexion"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Rooms
    @st.cache_data
    def load_rooms():
        if os.path.exists(ROOMS_FILE):
            df = pd.read_csv(ROOMS_FILE)
            df['numero'] = df['numero'].astype(str)
            return df
        # Default rooms
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
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total", len(rooms), delta=None)
    with col2:
        libres = len(rooms[rooms['statut'] == 'Libre'])
        st.metric("Libres", libres)
    with col3:
        occup = len(rooms[rooms['statut'] == 'Occupée'])
        st.metric("Occupées", occup)
    with col4:
        maint = len(rooms[rooms['statut'] == 'Maintenance'])
        st.metric("Maintenance", maint)
    
    # Room update
    st.subheader("🔄 Gérer une chambre")
    col_a, col_b = st.columns(2)
    with col_a:
        room_sel = st.selectbox("Chambre", rooms['numero'].tolist())
    with col_b:
        status_options = ['Libre', 'Occupée', 'Maintenance']
        new_status = st.selectbox("Nouveau statut", status_options)
    if st.button("✨ Mettre à jour", use_container_width=True):
        rooms.loc[rooms['numero'] == room_sel, 'statut'] = new_status
        save_rooms(rooms)
        st.success(f"✅ Chambre {room_sel} mise à jour: {new_status}")
        st.rerun()
    
    # Rooms grid
    st.subheader("🏠 Toutes les chambres")
    cols = st.columns(6)
    for idx, row in rooms.iterrows():
        with cols[idx % 6]:
            status_color = "green" if row['statut'] == 'Libre' else "orange" if row['statut'] == 'Occupée' else "red"
            st.markdown(f"""
            <div class="room-card">
                <h4 style="color: #CC6D3D;">{row['numero']}</h4>
                <p><strong>{row['type']}</strong></p>
                <span style="background: {status_color}; color: white; padding: 4px 8px; border-radius: 12px;">{row['statut']}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.dataframe(rooms)
    
    # Admin/Maintenance
    if st.session_state.role in ['admin', 'maintenance']:
        st.subheader("🔧 Maintenance")
        col_reset, col_fix = st.columns(2)
        with col_reset:
            if st.button("🔄 Reset toutes chambres Libre", type="secondary"):
                rooms['statut'] = 'Libre'
                save_rooms(rooms)
                st.success("✅ Toutes chambres libérées")
                st.rerun()
        with col_fix:
            if st.button("📊 Fix data (run fix.py)"):
                st.info("Run: python fix.py manually")

if __name__ == "__main__":
    pass

