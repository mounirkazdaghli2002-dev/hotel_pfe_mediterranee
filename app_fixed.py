import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import hashlib
import base64

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

DATA_DIR = os.getenv('DATA_DIR', '.')
USERS_FILE = os.path.join(DATA_DIR, 'utilisateurs.json')
ROOMS_FILE = os.path.join(DATA_DIR, 'chambres.csv')
MAINTENANCE_FILE = os.path.join(DATA_DIR, 'maintenance_tasks.csv')
RECLAMATIONS_FILE = os.path.join(DATA_DIR, 'reclamations.csv')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.csv')
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, 'notifications.json')

def load_df(filename, columns=None):
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            if columns:
                for col, default in columns.items():
                    if col not in df.columns:
                        df[col] = default
            return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def save_df(df, filename):
    try:
        df.to_csv(filename, index=False)
    except Exception as e:
        st.error(f"Erreur sauvegarde {filename}: {e}")

@st.cache_data
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    default_users = {
        "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "admin", "nom": "Admin"},
        "receptionniste": {"password": hashlib.sha256("reception123".encode()).hexdigest(), "role": "receptionniste", "nom": "Receptionniste"},
        "maintenance": {"password": hashlib.sha256("maintenance123".encode()).hexdigest(), "role": "maintenance", "nom": "Agent Maintenance"}
    }
    with open(USERS_FILE, 'w') as f:
        json.dump(default_users, f, indent=2)
    return default_users

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
    st.rerun()

def load_reservations():
    df = load_df(RESERVATIONS_FILE)
    return df

def load_maintenance_tasks():
    return load_df(MAINTENANCE_FILE, {'priorite': 'Moyenne', 'duree_estimee_minutes': 0.0})

def load_reclamations():
    return load_df(RECLAMATIONS_FILE)

def add_notification(title, message, type_notif="info"):
    st.toast(f"{title}: {message}")

def check_and_restore_session():
    session_str = st.query_params.get("session", None)
    if session_str:
        try:
            data = json.loads(base64.b64decode(session_str).decode())
            if (datetime.now().timestamp() - data["timestamp"]) < 604800:  # 7 days
                st.session_state.logged_in = True
                st.session_state.username = data["username"]
                st.session_state.user_role = data["role"]
                st.session_state.user_nom = data["nom"]
                return True
        except:
            pass
    return False

def show_login():
    st.title("🏨 Hotel Mediterranee")
    if check_and_restore_session():
        st.rerun()
    
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    remember_me = st.checkbox("Se souvenir de moi")
    
    if st.button("🔑 Se connecter"):
        user = authenticate(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_role = user["role"]
            st.session_state.user_nom = user["nom"]
            if remember_me:
                session_data = {
                    "username": username,
                    "role": user["role"],
                    "nom": user["nom"],
                    "timestamp": int(datetime.now().timestamp())
                }
                encoded = base64.b64encode(json.dumps(session_data).encode()).decode()
                st.query_params["session"] = encoded
            st.success("Connecté!")
            st.rerun()
        else:
            st.error("Identifiants incorrects")
    
    st.info("admin/admin123 | receptionniste/reception123 | maintenance/maintenance123")

def show_main_app():
    st.title("🏨 Hotel Mediterranee Dashboard")
    
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
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Libres", len(rooms[rooms["statut"] == "Libre"]))
    with col2:
        st.metric("Occupées", len(rooms[rooms["statut"] == "Occupée"]))
    with col3:
        st.metric("Maintenance", len(tasks))
    
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
            if st.button("Mettre à jour"):
                update_room_status(room_num, new_status)
        with tab2:
            st.dataframe(reservations)
        with tab3:
            chambre = st.selectbox("Chambre", rooms["numero"])
            type_panne = st.selectbox("Type", ["Plomberie", "Électricité"])
            desc = st.text_area("Description")
            if st.button("Signaler"):
                reclamations = load_reclamations()
                new_id = len(reclamations) + 1
                new_rec = pd.DataFrame({
                    "id": [new_id], "chambre": [chambre], "type_panne": [type_panne],
                    "description": [desc], "date_declaration": [datetime.now().strftime("%Y-%m-%d %H:%M")],
                    "statut": ["Déclaré"], "creé_par": [st.session_state.user_nom]
                })
                reclamations = pd.concat([reclamations, new_rec], ignore_index=True)
                save_df(reclamations, RECLAMATIONS_FILE)
                st.success("Panne signalée!")
    
    else:  # Admin
        tabs = st.tabs(["Dashboard", "Chambres", "Réservations", "Maintenance", "Réclamations"])
        with tabs[0]:
            st.dataframe(rooms.head())
        with tabs[1]:
            st.dataframe(rooms)
        with tabs[2]:
            st.dataframe(reservations)
        with tabs[3]:
            st.dataframe(tasks)
        with tabs[4]:
            st.dataframe(reclamations)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login()
else:
    show_main_app()

