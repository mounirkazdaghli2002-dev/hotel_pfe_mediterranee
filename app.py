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
RAPPORTS_FILE = os.path.join(DATA_DIR, 'rapports_taches.csv')
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, 'notifications.json')

# ============================================
# UTILS: Load/Save DataFrames & JSON
# ============================================
@st.cache_data
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
        "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "admin", "nom": "Chef Maintenance"},
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

def authenticate(username, password):
    users = load_users()
    hashed = hash_password(password)
    if username in users and users[username]["password"] == hashed:
        return users[username]
    return None

# Role checks
def is_admin():
    return st.session_state.get("user_role") == "admin"

def is_receptionniste():
    return st.session_state.get("user_role") == "receptionniste"

def is_maintenance():
    return st.session_state.get("user_role") == "maintenance"

# Session management
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

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.query_params.clear()
    st.rerun()

# ============================================
# ROOMS MANAGEMENT
# ============================================
def load_rooms():
    df = load_df(ROOMS_FILE, {'numero': '', 'type': '', 'aile': '', 'statut': 'Libre', 'etage': 1})
    if df.empty:
        data = [{'numero': str(i), 'type': 'Standard', 'aile': 'A', 'statut': 'Libre', 'etage': 1} for i in range(101, 175)]
        df = pd.DataFrame(data)
        save_df(df, ROOMS_FILE)
    df["numero"] = df["numero"].astype(str)
    return df

def save_rooms(rooms):
    save_df(rooms, ROOMS_FILE)

def update_room_status(room_num, new_statut, changed_by=""):
    rooms = load_rooms()
    old_status = rooms[rooms["numero"] == str(room_num)]["statut"].iloc[0] if len(rooms[rooms["numero"] == str(room_num)]) > 0 else ""
    rooms.loc[rooms["numero"] == str(room_num), "statut"] = new_statut
    save_rooms(rooms)
    if changed_by:
        add_notification(f"Chambre {room_num}: {old_status} → {new_statut}", f"Par {changed_by}", "info")
    return rooms

# ============================================
# RESERVATIONS
# ============================================
def load_reservations():
    df = load_df(RESERVATIONS_FILE)
    for col in ['date_arrivee', 'date_depart']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    if 'id' in df.columns:
        df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')
    return df

def check_availability(numero_chambre, date_debut, date_fin):
    reservations = load_reservations()
    rooms = load_rooms()
    room_row = rooms[rooms['numero'] == str(numero_chambre)]
    if len(room_row) == 0 or room_row.iloc[0]['statut'] == 'Maintenance':
        return False
    conflicting = reservations[
        (reservations['numero_chambre'] == str(numero_chambre)) &
        (reservations['statut'] != 'Annulée') &
        ((reservations['date_arrivee'] <= date_fin) & (reservations['date_depart'] >= date_debut))
    ]
    return len(conflicting) == 0

def create_reservation(nom_client, numero_chambre, date_arrivee, date_depart, **kwargs):
    if not check_availability(numero_chambre, date_arrivee, date_depart):
        return False, "Chambre non disponible"
    reservations = load_reservations()
    prix_nuit = 120.0
    nbre_nuits = (date_depart - date_arrivee).days
    total_prix = prix_nuit * nbre_nuits
    new_id = reservations['id'].max() + 1 if len(reservations) > 0 and not reservations['id'].isna().all() else 1
    new_res = pd.DataFrame([{
        'id': new_id, 'nom_client': nom_client, 'numero_chambre': str(numero_chambre),
        'date_arrivee': date_arrivee, 'date_depart': date_depart, 'nbre_nuits': nbre_nuits,
        'prix_nuit': prix_nuit, 'total_prix': total_prix, 'statut': 'Confirmée', **kwargs
    }])
    reservations = pd.concat([reservations, new_res], ignore_index=True)
    save_df(reservations, RESERVATIONS_FILE)
    add_notification("Nouvelle réservation", f"{nom_client} - {numero_chambre}", "success")
    return True, f"Reservation #{new_id} créée"

# ============================================
# MAINTENANCE & RECLAMATIONS
# ============================================
def load_maintenance_tasks():
    df = load_df(MAINTENANCE_FILE, {'priorite': 'Moyenne', 'duree_estimee_minutes': 0.0})
    if "date_completion" in df.columns:
        df["date_completion"] = df["date_completion"].astype(str)
    return df

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
    update_room_status(chambre, "Maintenance")
    add_notification("Nouvelle tâche maintenance", f"Chambre {chambre}", "warning")
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
# NOTIFICATIONS SYSTEM
# ============================================
def load_notifications():
    if os.path.exists(NOTIFICATIONS_FILE):
        with open(NOTIFICATIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_notifications(notifications):
    with open(NOTIFICATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(notifications, f, indent=4, ensure_ascii=False)

def add_notification(title, message, type_notif="info", target_role=None):
    notifications = load_notifications()
    new_notif = {
        "id": len(notifications) + 1,
        "title": title, "message": message, "type": type_notif,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "read": False, "target_role": target_role
    }
    notifications.insert(0, new_notif)
    notifications = notifications[:50]
    save_notifications(notifications)
    st.toast(f"{title}: {message}")
    return notifications

def get_unread_count():
    notifications = load_notifications()
    current_role = st.session_state.get("user_role", "")
    user_notifications = [n for n in notifications if n.get("target_role") is None or n.get("target_role") == current_role]
    return len([n for n in user_notifications if not n["read"]])

# ============================================
# PANNES & COMPOSANTS
# ============================================
def load_pannes():
    return load_df(PANNES_FILE)

def load_composants():
    df = load_df(COMPOSANTS_FILE)
    if "id" in df.columns:
        df["id"] = df["id"].astype("Int64")
    return df

# ============================================
# AGENT HISTORY
# ============================================
def get_agent_history(agent_name):
    tasks = load_maintenance_tasks()
    agent_tasks = tasks[tasks["assigned_to"] == agent_name]
    return {
        "total": len(agent_tasks),
        "terminees": len(agent_tasks[agent_tasks["statut"] == "Terminé"]),
        "en_cours": len(agent_tasks[agent_tasks["statut"] == "En cours"]),
        "en_attente": len(agent_tasks[agent_tasks["statut"] == "En attente"])
    }

# ============================================
# LOGIN PAGE
# ============================================
def show_login():
    st.markdown("""
    <div style='max-width: 400px; margin: 100px auto; padding: 40px; background: #1e293b; border-radius: 20px; text-align: center;'>
        <h1 style='text-align: center;'>🏨 Hotel Mediterranee</h1>
        <h3 style='text-align: center; color: #CC6D3D;'>Connexion</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if check_and_restore_session():
        st.rerun()
    
    username = st.text_input("👤 Nom d'utilisateur")
    password = st.text_input("🔒 Mot de passe", type="password")
    remember_me = st.checkbox("✅ Se souvenir de moi")
    
    if st.button("🔑 Se connecter", use_container_width=True):
        user = authenticate(username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["user_role"] = user["role"]
            st.session_state["user_nom"] = user["nom"]
            if remember_me:
                session_data = {"username": username, "role": user["role"], "nom": user["nom"], "timestamp": int(datetime.now().timestamp())}
                encoded = base64.b64encode(json.dumps(session_data).encode()).decode()
                st.query_params["session"] = encoded
            st.success("✅ Connecté!")
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects")
    
    st.info("💡 admin/admin123 | receptionniste/reception123 | maintenance/maintenance123")
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# MAIN APP
# ============================================
def show_main_app():
    # Sidebar with notifications
    with st.sidebar:
        st.markdown(f"**👋 Bonjour {st.session_state.user_nom}**")
        st.markdown(f"**🎭 Rôle:** {st.session_state.user_role.title()}")
        
        unread = get_unread_count()
        if unread > 0:
            st.error(f"🔔 {unread} notification(s) non lue(s)")
        else:
            st.success("✅ Pas de notifications")
        
        st.markdown("---")
        if st.button("🚪 Déconnexion", use_container_width=True):
            logout()
    
    rooms = load_rooms()
    
    # Role-based dashboard
    if is_maintenance():
        tabs = st.tabs(["📊 Dashboard", "🔧 Mes Tâches"])
        with tabs[0]:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("🆓 Libres", len(rooms[rooms['statut']=='Libre']))
            with col2:
                st.metric("🔒 Occupées", len(rooms[rooms['statut']=='Occupée']))
            st.dataframe(rooms[['numero','type','aile','statut']].head(10))
        with tabs[1]:
            tasks = load_maintenance_tasks()
            my_tasks = tasks[tasks['assigned_to']==st.session_state.user_nom]
            st.dataframe(my_tasks)
    
    elif is_receptionniste():
        tabs = st.tabs(["📊 Dashboard", "📅 Réservations", "🔴 Déclarer Panne"])
        with tabs[0]:
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Libres", len(rooms[rooms["statut"] == "Libre"]))
            with col2: st.metric("Occupées", len(rooms[rooms["statut"] == "Occupée"]))
            with col3: st.metric("Maintenance", len(rooms[rooms["statut"] == "Maintenance"]))
        with tabs[1]:
            st.subheader("📋 Réservations")
            reservations = load_reservations()
            st.dataframe(reservations)
        with tabs[2]:
            st.subheader("🚨 Déclarer une panne")
            col1, col2 = st.columns(2)
            with col1:
                chambre = st.selectbox("Chambre", rooms["numero"])
                type_panne = st.selectbox("Type", ["Plomberie", "Électricité", "Climatisation", "Meubles"])
            with col2:
                description = st.text_area("Description du problème", height=100)
            if st.button("🚨 Signaler", use_container_width=True):
                add_reclamation(chambre, type_panne, description, st.session_state.user_nom)
                st.success("✅ Panne signalée à l'admin!")
    
    else:  # Admin full access
        tabs = st.tabs([
            "📊 Dashboard", "🛏️ Chambres", "📅 Réservations", 
            "🔧 Maintenance", "🔴 Réclamations", "⚙️ Pannes", 
            "🔩 Composants", "📈 Agents", "👥 Users"
        ])
        
        with tabs[0]:
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.metric("Libres", len(rooms[rooms["statut"] == "Libre"]))
            with col2: st.metric("Occupées", len(rooms[rooms["statut"] == "Occupée"]))
            with col3: st.metric("Maintenance", len(rooms[rooms["statut"] == "Maintenance"]))
            with col4: st.metric("Alertes", get_unread_count())
            st.dataframe(rooms.head(10))
        
        with tabs[1]: st.dataframe(load_rooms())
        with tabs[2]: st.dataframe(load_reservations())
        with tabs[3]: st.dataframe(load_maintenance_tasks())
        with tabs[4]: st.dataframe(load_reclamations())
        with tabs[5]: st.dataframe(load_pannes())
        with tabs[6]: st.dataframe(load_composants())
        with tabs[7]:
            agents = [u["nom"] for u in load_users().values() if u["role"] == "maintenance"]
            agent = st.selectbox("Agent", agents)
            st.json(get_agent_history(agent))
        with tabs[8]:
            users = load_users()
            st.json({k: {"role": v["role"], "nom": v["nom"]} for k,v in users.items()})

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        show_login()
    else:
        show_main_app()

