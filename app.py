import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import hashlib

st.set_page_config(page_title="Hotel Mediterranee", page_icon="🏨", layout="wide")

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

# ============================================
# FILES & CONSTANTS
# ============================================
DATA_DIR = os.getenv('DATA_DIR', '.')
USERS_FILE = os.path.join(DATA_DIR, 'utilisateurs.json')
ROOMS_FILE = os.path.join(DATA_DIR, 'chambres.csv')
MAINTENANCE_FILE = os.path.join(DATA_DIR, 'maintenance_tasks.csv')
RECLAMATIONS_FILE = os.path.join(DATA_DIR, 'reclamations.csv')
PANNES_FILE = os.path.join(DATA_DIR, 'pannes.csv')
COMPOSANTS_FILE = os.path.join(DATA_DIR, 'composants_chambres.csv')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.csv')
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, 'notifications.json')

# ============================================
# UTILS: Load/Save DataFrames & JSON
# ============================================
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

def save_df(df, filename):
    df.to_csv(filename, index=False)

@st.cache_data
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    # Defaults
    default_users = {
        "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "admin", "nom": "Admin"},
        "receptionniste": {"password": hashlib.sha256("reception123".encode()).hexdigest(), "role": "receptionniste", "nom": "Receptionniste"},
        "maintenance": {"password": hashlib.sha256("maintenance123".encode()).hexdigest(), "role": "maintenance", "nom": "Agent Maintenance"}
    }
    with open(USERS_FILE, 'w') as f:
        json.dump(default_users, f, indent=2)
    return default_users

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Auth helpers
def authenticate(username, password):
    users = load_users()
    hashed = hash_password(password)
    if username in users and users[username]["password"] == hashed:
        return users[username]
    return None

def is_admin():
    return st.session_state.get("user_role") == "admin"

def is_receptionniste():
    return st.session_state.get("user_role") == "receptionniste"

def is_maintenance():
    return st.session_state.get("user_role") == "maintenance"

# ============================================
# ROOMS MANAGEMENT
# ============================================
def load_rooms():
    df = load_df(ROOMS_FILE, {'numero': '', 'type': '', 'aile': '', 'statut': 'Libre', 'etage': 1})
    if df.empty:
        data = [{'numero': str(i), 'type': 'Standard', 'aile': 'A', 'statut': 'Libre', 'etage': 1} for i in range(101, 175)]
        df = pd.DataFrame(data)
        save_df(df, ROOMS_FILE)
    return df

def update_room_status(room_num, new_statut):
    rooms = load_rooms()
    rooms.loc[rooms["numero"] == str(room_num), "statut"] = new_statut
    save_df(rooms, ROOMS_FILE)
    return rooms

# ============================================
# RESERVATIONS (Merged from complete implementation)
# ============================================
def load_reservations():
    if os.path.exists(RESERVATIONS_FILE):
        df = pd.read_csv(RESERVATIONS_FILE)
        for col in ['date_arrivee', 'date_depart']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    return pd.DataFrame()

def check_availability(numero_chambre, date_debut, date_fin):
    reservations = load_reservations()
    rooms = load_rooms()
    room_row = rooms[rooms['numero'] == str(numero_chambre)]
    if len(room_row) == 0 or room_row.iloc[0]['statut'] == 'Maintenance':
        return False
    conflicting = reservations[
        (reservations['numero_chambre'] == str(numero_chambre)) &
        (reservations['statut'] != 'Annulée') &
        (
            (reservations['date_arrivee'] <= date_fin) &
            (reservations['date_depart'] >= date_debut)
        )
    ]
    return len(conflicting) == 0

def create_reservation(nom_client, numero_chambre, date_arrivee, date_depart, **kwargs):
    if not check_availability(numero_chambre, date_arrivee, date_depart):
        return False, "Chambre non disponible"
    reservations = load_reservations()
    prix_nuit = 120.0
    nbre_nuits = (date_depart - date_arrivee).days
    total_prix = prix_nuit * nbre_nuits
    new_id = reservations['id'].max() + 1 if len(reservations) > 0 else 1
    new_res = pd.DataFrame([{
        'id': new_id, 'nom_client': nom_client, 'numero_chambre': str(numero_chambre),
        'date_arrivee': date_arrivee, 'date_depart': date_depart, 'nbre_nuits': nbre_nuits,
        'prix_nuit': prix_nuit, 'total_prix': total_prix, 'statut': 'Confirmée', **kwargs
    }])
    reservations = pd.concat([reservations, new_res], ignore_index=True)
    save_df(reservations, RESERVATIONS_FILE)
    return True, f"Reservation #{new_id} created"

# ============================================
# MAINTENANCE & RECLAMATIONS (Core functions)
# ============================================
def load_maintenance_tasks():
    return load_df(MAINTENANCE_FILE, {'priorite': 'Moyenne', 'duree_estimee_minutes': 0.0})

def create_maintenance_task(chambre, description, assigned_to, created_by, **kwargs):
    tasks = load_maintenance_tasks()
    new_id = tasks["id"].max() + 1 if len(tasks) > 0 else 1
    new_task = pd.DataFrame([{
        "id": new_id, "chambre": chambre, "description": description,
        "assigned_to": assigned_to, "statut": "En attente",
        "date_creation": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "created_by": created_by, **kwargs
    }])
    tasks = pd.concat([tasks, new_task], ignore_index=True)
    save_df(tasks, MAINTENANCE_FILE)
    return tasks

def load_reclamations():
    return load_df(RECLAMATIONS_FILE)

def add_reclamation(chambre, type_panne, description, created_by):
    reclamations = load_reclamations()
    new_id = reclamations["id"].max() + 1 if len(reclamations) > 0 else 1
    new_rec = pd.DataFrame([{
        "id": new_id, "chambre": str(chambre), "type_panne": type_panne,
        "description": description, "date_declaration": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "statut": "Déclaré", "creé_par": created_by
    }])
    reclamations = pd.concat([reclamations, new_rec], ignore_index=True)
    save_df(reclamations, RECLAMATIONS_FILE)
    return reclamations

# ============================================
# NOTIFICATIONS (Simple)
# ============================================
def add_notification(title, message, type_notif="info"):
    st.toast(f"{title}: {message}")

# ============================================
# UI PAGES
# ============================================
def show_login():
    st.title("🏨 Hotel Mediterranee")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("🔑 Connexion"):
        user = authenticate(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_role = user["role"]
            st.session_state.user_nom = user["nom"]
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects")
    st.info("admin/admin123 | receptionniste/reception123 | maintenance/maintenance123")

def show_main_app():
    st.title("🏨 Hotel Mediterranee Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"**👋 {st.session_state.user_nom}**")
        st.markdown(f"**Rôle:** {st.session_state.user_role.title()}")
        if st.button("🚪 Déconnexion"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    rooms = load_rooms()
    reservations = load_reservations()
    tasks = load_maintenance_tasks()
    reclamations = load_reclamations()
    
    # Metrics
    total_rooms = len(rooms)
    free_rooms = len(rooms[rooms["statut"] == "Libre"])
    occupied_rooms = len(rooms[rooms["statut"] == "Occupée"])
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Libres", free_rooms)
    with col2: st.metric("Occupées", occupied_rooms)
    with col3: st.metric("Tâches", len(tasks))
    
    # Role-based tabs
    if is_maintenance():
        tab1, tab2 = st.tabs(["Dashboard", "Mes Tâches"])
        with tab1:
            st.dataframe(rooms)
        with tab2:
            st.dataframe(tasks[tasks["assigned_to"] == st.session_state.user_nom])
    
    elif is_receptionniste():
        tab1, tab2, tab3 = st.tabs(["Dashboard", "Réservations", "Pannes"])
        with tab1:
            st.dataframe(rooms)
            room_num = st.selectbox("Chambre", rooms["numero"])
            new_status = st.selectbox("Statut", ["Libre", "Occupée"])
            if st.button("Update"): update_room_status(room_num, new_status); st.rerun()
        with tab2:
            st.subheader("Réservations")
            st.dataframe(reservations)
        with tab3:
            st.subheader("Déclarer Panne")
            chambre = st.selectbox("Chambre", rooms["numero"])
            type_panne = st.selectbox("Type", ["Plomberie", "Électricité"])
            desc = st.text_area("Description")
            if st.button("Signaler"): add_reclamation(chambre, type_panne, desc, st.session_state.user_nom)
    
    else:  # Admin
        tabs = st.tabs(["Dashboard", "Chambres", "Réservations", "Maintenance", "Réclamations"])
        with tabs[0]: st.dataframe(rooms); st.dataframe(reservations.head())
        with tabs[1]: st.dataframe(rooms)
        with tabs[2]: st.dataframe(reservations)
        with tabs[3]: st.dataframe(tasks)
        with tabs[4]: st.dataframe(reclamations)

# ============================================
# MAIN
# ============================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login()
else:
    show_main_app()
