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
RECLAMATIONS_FILE = 'reclamations.csv'
PANNES_FILE = 'pannes.csv'
COMPOSANTS_FILE = 'composants_chambres.csv'

# Users
@st.cache_data
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    default_users = {
        "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "admin", "nom": "Admin"},
        "receptionniste": {"password": hashlib.sha256("reception123".encode()).hexdigest(), "role": "receptionniste", "nom": "Receptionniste"},
        "maintenance": {"password": hashlib.sha256("maintenance123".encode()).hexdigest(), "role": "maintenance", "nom": "Agent Maintenance"}
    }
    with open(USERS_FILE, 'w') as f:
        json.dump(default_users, f, indent=2)
    return default_users

# Auth state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.nom = ""

# Login
if not st.session_state.logged_in:
    st.title("🏨 Hotel Mediterranee")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    col1, col2 = st.columns(2)
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
    # Main app
    st.title("🏨 Hotel Mediterranee Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"**👋 {st.session_state.nom}**")
        st.markdown(f"**Rôle:** {st.session_state.role.title()}")
        if st.button("🚪 Déconnexion"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Load data safely
    @st.cache_data
    def load_df(filename, columns=None):
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            if columns:
                for col, default in columns.items():
                    if col not in df.columns:
                        df[col] = default
            return df
        return pd.DataFrame()
    
    rooms = load_df(ROOMS_FILE, {'numero': '', 'type': '', 'aile': '', 'statut': 'Libre', 'etage': 1})
    if rooms.empty:
        # Create default rooms
        data = []
        for i in range(101, 175):
            data.append({'numero': str(i), 'type': 'Standard', 'aile': 'A', 'statut': 'Libre', 'etage': 1})
        rooms = pd.DataFrame(data)
        rooms.to_csv(ROOMS_FILE, index=False)
    
    tasks = load_df(MAINTENANCE_FILE, {
        'priorite': 'Moyenne', 
        'duree_estimee_minutes': 0.0,
        'duree_reelle_minutes': 0.0,
        'type_panne': 'Autre'
    })
    reclamations = load_df(RECLAMATIONS_FILE)
    pannes = load_df(PANNES_FILE, {'priorite': 'Moyenne'})
    
    def save_df(df, filename):
        df.to_csv(filename, index=False)
    
    # Metrics - SAFE priorite handling
    total_rooms = len(rooms)
    free_rooms = len(rooms[rooms["statut"] == "Libre"])
    occupied_rooms = len(rooms[rooms["statut"] == "Occupée"])
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    
    total_tasks = len(tasks)
    tasks_pending = len(tasks[tasks["statut"] == "En attente"]) if len(tasks) > 0 else 0
    
    # SAFE pannes priorite
    pannes_haute = len(pannes[pannes.get('priorite', pd.Series()) == "Haute"]) if len(pannes) > 0 else 0
    pannes_moyenne = len(pannes[pannes.get('priorite', pd.Series()) == "Moyenne"]) if len(pannes) > 0 else 0
    pannes_basse = len(pannes[pannes.get('priorite', pd.Series()) == "Basse"]) if len(pannes) > 0 else 0
    
    # Dashboard
    st.markdown("### 🎯 Indicateurs Clés")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📈 Occupation", f"{occupancy_rate:.1f}%")
    with col2:
        st.metric("🛏️ Libres", free_rooms)
    with col3:
        st.metric("🔧 Tâches", total_tasks)
    
    # Maintenance tab with SAFE priorite sort
    st.subheader("🔧 Maintenance")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_statut = st.selectbox("Statut", ["Tous", "En attente", "En cours", "Terminé"])
    with col_f2:
        filter_priorite = st.selectbox("Priorité", ["Tous", "Haute", "Moyenne", "Basse"])
    
    filtered_tasks = tasks.copy()
    if filter_statut != "Tous":
        filtered_tasks = filtered_tasks[filtered_tasks["statut"] == filter_statut]
    if filter_priorite != "Tous":
        # SAFE priorite filter
        filtered_tasks = filtered_tasks[filtered_tasks.get('priorite', pd.Series()).fillna('Moyenne') == filter_priorite]
    
    # SAFE priority sort
    priority_order = {"Haute": 0, "Moyenne": 1, "Basse": 2}
    if len(filtered_tasks) > 0 and 'priorite' in filtered_tasks.columns:
        filtered_tasks = filtered_tasks.copy()
        filtered_tasks['priorite_sort'] = filtered_tasks['priorite'].map(priority_order).fillna(1)
        filtered_tasks = filtered_tasks.sort_values(['priorite_sort', 'date_creation'], ascending=[True, False]).drop('priorite_sort', axis=1)
    
    st.dataframe(filtered_tasks, use_container_width=True)
    
    # Room management
    st.subheader("🛏️ Chambres")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        room_sel = st.selectbox("Chambre", rooms['numero'].tolist())
    with col_r2:
        new_status = st.selectbox("Statut", ['Libre', 'Occupée', 'Maintenance'])
    if st.button("Mettre à jour"):
        rooms.loc[rooms['numero'] == room_sel, 'statut'] = new_status
        save_df(rooms, ROOMS_FILE)
        st.success(f"Chambre {room_sel} → {new_status}")
        st.rerun()
    
    st.dataframe(rooms)

**Fixed:**
- SyntaxError removed (clean code)
- KeyError 'priorite' fixed: `get('priorite', pd.Series()).fillna('Moyenne')`
- Safe sort/filter, empty DF handling

**Test:** `streamlit run app.py`

