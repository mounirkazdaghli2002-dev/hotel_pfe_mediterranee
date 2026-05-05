import streamlit as st
import pandas as pd
import os
import json
import base64
from datetime import datetime
import hashlib

# ============================================
# CONFIGURATION PAGE (only once, at the top)
# ============================================
st.set_page_config(page_title="Hotel Mediterranee", page_icon="🏨", layout="wide")

# Data files
DATA_DIR = os.getenv('DATA_DIR', '.')
USERS_FILE = os.path.join(DATA_DIR, 'utilisateurs.json')
ROOMS_FILE = os.path.join(DATA_DIR, 'chambres.csv')
MAINTENANCE_FILE = os.path.join(DATA_DIR, 'maintenance_tasks.csv')
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, 'notifications.json')
PANNES_FILE = os.path.join(DATA_DIR, 'pannes.csv')
COMPOSANTS_FILE = os.path.join(DATA_DIR, 'composants_chambres.csv')
RAPPORTS_FILE = os.path.join(DATA_DIR, 'rapports_taches.csv')
RECLAMATIONS_FILE = os.path.join(DATA_DIR, 'reclamations.csv')
RESERVATIONS_FILE = os.path.join(DATA_DIR, 'reservations.csv')

COLORS = {
    "background": "#0f172a",
    "card_bg": "#1e293b",
    "sidebar_bg": "#022E51",
    "text_white": "#ffffff",
    "text_light": "#cbd5e1",
    "secondary": "#CC6D3D",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#3b82f6"
}

st.markdown(f"""
<style>
.stApp {{background: linear-gradient(135deg, {COLORS['background']} 0%, #1e293b 100%);}}
h1, h2, h3, h4, p, div, label {{color: {COLORS['text_white']} !important;}}
.room-card {{background: {COLORS['card_bg']}; border-radius: 16px; padding: 20px; text-align: center;}}
.room-card:hover {{transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4);}}
.room-card.free {{border-left: 5px solid {COLORS['success']};}}
.room-card.occupied {{border-left: 5px solid {COLORS['info']};}}
.room-card.maintenance {{border-left: 5px solid {COLORS['danger']};}}
section[data-testid="stSidebar"] {{background: {COLORS['sidebar_bg']};}}
section[data-testid="stSidebar"] * {{color: {COLORS['text_white']} !important;}}
.stTextInput > div > div {{background: {COLORS['card_bg']} !important; color: white !important;}}
.stSelectbox > div > div {{background: {COLORS['card_bg']} !important; color: white !important;}}
.stButton > button {{background: {COLORS['secondary']}; color: white; border-radius: 10px;}}
.status-badge {{padding: 6px 14px; border-radius: 20px; font-weight: 600;}}
.status-badge.free {{background: {COLORS['success']};}}
.status-badge.occupied {{background: {COLORS['info']};}}
.status-badge.maintenance {{background: {COLORS['danger']};}}
</style>
<script>
function playNotificationSound() {{
    try {{
        var ctx = new (window.AudioContext || window.webkitAudioContext)();
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.frequency.value = 880;
        gain.gain.setValueAtTime(0.3, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
        osc.start(ctx.currentTime);
        osc.stop(ctx.currentTime + 0.5);
    }} catch(e) {{}}
}}
function startNotificationPolling() {{
    setInterval(function() {{
        var el = document.getElementById('notification-count-data');
        if (el) {{
            var count = parseInt(el.getAttribute('data-count') || '0');
            if (count > 0) {{
                var badge = document.getElementById('live-notif-badge');
                if (!badge) {{
                    badge = document.createElement('div');
                    badge.id = 'live-notif-badge';
                    badge.className = 'live-notification-badge';
                    document.body.appendChild(badge);
                }}
                badge.textContent = count + ' notification(s)';
            }}
        }}
    }}, 5000);
}}
if (document.readyState === 'complete') {{
    startNotificationPolling();
}} else {{
    window.addEventListener('load', startNotificationPolling);
}}
</script>
<style>
    @media (max-width: 768px) {{
        .stButton > button {{ width: 100% !important; margin-bottom: 10px; }}
        .room-card {{ padding: 10px !important; font-size: 12px; }}
    }}
    @keyframes slideIn {{
        from {{ transform: translateX(100%); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    .live-notification-badge {{
        position: fixed;
        top: 10px;
        right: 10px;
        background: #ef4444;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        z-index: 9998;
        animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
</style>
""", unsafe_allow_html=True)


# ============================================
# GESTION DES NOTIFICATIONS
# ============================================
def play_notification_sound():
    st.markdown("""
    <script>
    if (typeof playNotificationSound === 'function') {
        playNotificationSound();
    }
    </script>
    """, unsafe_allow_html=True)

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
        "title": title,
        "message": message,
        "type": type_notif,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "read": False,
        "target_role": target_role
    }
    notifications.insert(0, new_notif)
    notifications = notifications[:50]
    save_notifications(notifications)
    play_notification_sound()
    if type_notif == "success":
        st.toast(f"✅ {title}: {message}")
    elif type_notif == "warning":
        st.toast(f"⚠️ {title}: {message}")
    elif type_notif == "error":
        st.toast(f"❌ {title}: {message}")
    else:
        st.toast(f"ℹ️ {title}: {message}")
    return notifications

def mark_notification_read(notif_id):
    notifications = load_notifications()
    for notif in notifications:
        if notif["id"] == notif_id:
            notif["read"] = True
    save_notifications(notifications)
    return notifications

def mark_all_notifications_read():
    notifications = load_notifications()
    for notif in notifications:
        notif["read"] = True
    save_notifications(notifications)
    return notifications

def get_unread_count():
    notifications = load_notifications()
    current_role = st.session_state.get("user_role", "")
    if current_role:
        user_notifications = [n for n in notifications if n.get("target_role") is None or n.get("target_role") == current_role]
        return len([n for n in user_notifications if not n["read"]])
    return len([n for n in notifications if not n["read"]])

def get_user_notifications():
    notifications = load_notifications()
    current_role = st.session_state.get("user_role", "")
    if current_role:
        return [n for n in notifications if n.get("target_role") is None or n.get("target_role") == current_role]
    return notifications


# ============================================
# GESTION DES PANNES
# ============================================
def load_pannes():
    if os.path.exists(PANNES_FILE):
        return pd.read_csv(PANNES_FILE)
    pannes_data = {
        "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "nom_panne": ["Plomberie", "Électricité", "Climatisation", "Meuble", "Serrure",
                      "Écran/TV", "WiFi", "Chauffage", "Nettoyage", "Accessibilité"],
        "description": ["Fuites d'eau et problèmes de tuyauterie", "Pannes électriques et court-circuits",
                        "Panne du système de climatisation", "Mobilier endommagé ou brisé",
                        "Coffre-fort ou serrure de porte", "Téléviseur ou écran cassé",
                        "Perte de connexion internet", "Problème de chauffage",
                        "Nécessite nettoyage professionnel", "Problèmes d'accessibilité"],
        "priorite": ["Haute", "Haute", "Moyenne", "Basse", "Haute", "Basse", "Moyenne", "Moyenne", "Basse", "Haute"],
        "date_creation": ["2024-01-01"] * 10
    }
    df = pd.DataFrame(pannes_data)
    df.to_csv(PANNES_FILE, index=False)
    return df

def save_pannes(pannes):
    pannes.to_csv(PANNES_FILE, index=False)

def add_panne(nom_panne, description, priorite):
    pannes = load_pannes()
    new_id = pannes["id"].max() + 1 if len(pannes) > 0 else 1
    new_panne = pd.DataFrame([{
        "id": new_id,
        "nom_panne": nom_panne,
        "description": description,
        "priorite": priorite,
        "date_creation": datetime.now().strftime("%Y-%m-%d")
    }])
    pannes = pd.concat([pannes, new_panne], ignore_index=True)
    save_pannes(pannes)
    return pannes


# ============================================
# GESTION DES COMPOSANTS DE CHAMBRES
# ============================================
def load_composants():
    if os.path.exists(COMPOSANTS_FILE):
        df = pd.read_csv(COMPOSANTS_FILE)
        if "id" in df.columns:
            df["id"] = df["id"].astype("Int64")
        for col in ["chambre", "composant_principal", "sous_composant", "statut", "date_installation", "derniere_maintenance"]:
            if col in df.columns:
                df[col] = df[col].astype(str)
        return df
    df = pd.DataFrame(columns=["id", "chambre", "composant_principal", "sous_composant", "statut", "date_installation", "derniere_maintenance"])
    df = df.astype({"id": "Int64", "chambre": str, "composant_principal": str, "sous_composant": str,
                    "statut": str, "date_installation": str, "derniere_maintenance": str})
    df.to_csv(COMPOSANTS_FILE, index=False)
    return df

def save_composants(composants):
    composants.to_csv(COMPOSANTS_FILE, index=False)

def add_composant(chambre, composant_principal, sous_composant, statut="Bon"):
    composants = load_composants()
    new_id = composants["id"].max() + 1 if len(composants) > 0 else 1
    new_composant = pd.DataFrame([{
        "id": new_id,
        "chambre": chambre,
        "composant_principal": composant_principal,
        "sous_composant": sous_composant,
        "statut": statut,
        "date_installation": datetime.now().strftime("%Y-%m-%d"),
        "derniere_maintenance": ""
    }])
    composants = pd.concat([composants, new_composant], ignore_index=True)
    save_composants(composants)
    return composants

def update_composant_status(composant_id, new_status):
    composants = load_composants()
    composants.loc[composants["id"] == composant_id, "statut"] = new_status
    composants.loc[composants["id"] == composant_id, "derniere_maintenance"] = datetime.now().strftime("%Y-%m-%d")
    save_composants(composants)
    return composants

def delete_composant(composant_id):
    composants = load_composants()
    composants = composants[composants["id"] != composant_id]
    save_composants(composants)
    return composants


# ============================================
# GESTION DES RAPPORTS DE TÂCHES
# ============================================
def load_rapports():
    if os.path.exists(RAPPORTS_FILE):
        return pd.read_csv(RAPPORTS_FILE)
    df = pd.DataFrame(columns=["task_id", "agent", "rapport", "duree_travail_minutes",
                                "date_rapport", "pieces_utilisees", "notes_agent"])
    df.to_csv(RAPPORTS_FILE, index=False)
    return df

def save_rapports(rapports):
    rapports.to_csv(RAPPORTS_FILE, index=False)

def add_rapport(task_id, agent, rapport, duree_travail, pieces_utilisees="", notes=""):
    rapports = load_rapports()
    new_rapport = pd.DataFrame([{
        "task_id": task_id,
        "agent": agent,
        "rapport": rapport,
        "duree_travail_minutes": duree_travail,
        "date_rapport": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "pieces_utilisees": pieces_utilisees,
        "notes_agent": notes
    }])
    rapports = pd.concat([rapports, new_rapport], ignore_index=True)
    save_rapports(rapports)
    return rapports

def get_agent_history(agent_name):
    tasks = load_maintenance_tasks()
    agent_tasks = tasks[tasks["assigned_to"] == agent_name].copy()
    return {
        "total": len(agent_tasks),
        "terminees": len(agent_tasks[agent_tasks["statut"] == "Terminé"]),
        "en_cours": len(agent_tasks[agent_tasks["statut"] == "En cours"]),
        "en_attente": len(agent_tasks[agent_tasks["statut"] == "En attente"])
    }


# ============================================
# GESTION DES RÉCLAMATIONS
# ============================================
def load_reclamations():
    if os.path.exists(RECLAMATIONS_FILE):
        return pd.read_csv(RECLAMATIONS_FILE)
    df = pd.DataFrame(columns=["id", "chambre", "type_panne", "description",
                                "date_declaration", "statut", "creé_par"])
    df.to_csv(RECLAMATIONS_FILE, index=False)
    return df

def save_reclamations(reclamations):
    reclamations.to_csv(RECLAMATIONS_FILE, index=False)

def add_reclamation(chambre, type_panne, description, created_by):
    reclamations = load_reclamations()
    new_id = reclamations["id"].max() + 1 if len(reclamations) > 0 else 1
    new_reclamation = pd.DataFrame([{
        "id": new_id,
        "chambre": str(chambre),
        "type_panne": type_panne,
        "description": description,
        "date_declaration": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "statut": "Déclaré",
        "creé_par": created_by
    }])
    reclamations = pd.concat([reclamations, new_reclamation], ignore_index=True)
    save_reclamations(reclamations)
    add_notification(
        "🔴 Nouvelle panne signalée",
        f"Chambre {chambre}: {type_panne} - {description[:40]}",
        "warning",
        target_role="admin"
    )
    return reclamations

def update_reclamation_status(reclamation_id, new_status):
    reclamations = load_reclamations()
    reclamations.loc[reclamations["id"] == reclamation_id, "statut"] = new_status
    save_reclamations(reclamations)
    return reclamations

def delete_reclamation(reclamation_id):
    reclamations = load_reclamations()
    reclamations = reclamations[reclamations["id"] != reclamation_id]
    save_reclamations(reclamations)
    return reclamations


# ============================================
# GESTION DES RÉSERVATIONS
# ============================================
def load_reservations():
    if os.path.exists(RESERVATIONS_FILE):
        df = pd.read_csv(RESERVATIONS_FILE)
        for col in ['date_arrivee', 'date_depart']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        if 'id' in df.columns:
            df['id'] = pd.to_numeric(df['id'], errors='coerce').astype('Int64')
        return df
    df = pd.DataFrame(columns=[
        'id', 'nom_client', 'numero_chambre', 'date_arrivee', 'date_depart',
        'nbre_nuits', 'telephone', 'email', 'statut', 'prix_nuit', 'total_prix',
        'checkin_time', 'checkout_time', 'notes'
    ])
    df.to_csv(RESERVATIONS_FILE, index=False)
    return df

def save_reservations(reservations):
    reservations.to_csv(RESERVATIONS_FILE, index=False)

def check_availability(numero_chambre, date_debut, date_fin):
    reservations = load_reservations()
    rooms = load_rooms()
    room_row = rooms[rooms['numero'] == str(numero_chambre)]
    if len(room_row) == 0 or room_row.iloc[0]['statut'] == 'Maintenance':
        return False
    conflicting = reservations[
        (reservations['numero_chambre'] == str(numero_chambre)) &
        (reservations['statut'] != 'Annulée') &
        (reservations['date_arrivee'] <= date_fin) &
        (reservations['date_depart'] >= date_debut)
    ]
    return len(conflicting) == 0

def create_reservation(nom_client, numero_chambre, date_arrivee, date_depart,
                       telephone="", email="", statut="Confirmée", notes=""):
    reservations = load_reservations()
    rooms = load_rooms()
    if not check_availability(numero_chambre, date_arrivee, date_depart):
        return False, "Chambre non disponible pour ces dates."
    room_row = rooms[rooms['numero'] == str(numero_chambre)]
    if len(room_row) == 0:
        return False, "Chambre inexistante."
    prix_nuit = 120.0
    nbre_nuits = (date_depart - date_arrivee).days
    total_prix = prix_nuit * nbre_nuits
    new_id = reservations['id'].max() + 1 if len(reservations) > 0 else 1
    new_res = pd.DataFrame([{
        'id': new_id, 'nom_client': nom_client, 'numero_chambre': str(numero_chambre),
        'date_arrivee': date_arrivee, 'date_depart': date_depart, 'nbre_nuits': nbre_nuits,
        'telephone': telephone, 'email': email, 'statut': statut, 'prix_nuit': prix_nuit,
        'total_prix': total_prix, 'checkin_time': '14:00', 'checkout_time': '12:00', 'notes': notes
    }])
    reservations = pd.concat([reservations, new_res], ignore_index=True)
    save_reservations(reservations)
    add_notification(
        "📅 Nouvelle réservation",
        f"{nom_client} - Chambre {numero_chambre} ({date_arrivee.date()} → {date_depart.date()})",
        "success", target_role="receptionniste"
    )
    return True, f"Réservation #{new_id} créée avec succès (Total: {total_prix} DT)"

def update_reservation(res_id, **kwargs):
    reservations = load_reservations()
    if res_id not in reservations['id'].values:
        return False, "Réservation inexistante."
    for key, value in kwargs.items():
        reservations.loc[reservations['id'] == res_id, key] = value
    save_reservations(reservations)
    return True, "Réservation mise à jour."

def delete_reservation(res_id):
    reservations = load_reservations()
    if res_id not in reservations['id'].values:
        return False, "Réservation inexistante."
    res_row = reservations[reservations['id'] == res_id].iloc[0]
    reservations = reservations[reservations['id'] != res_id]
    save_reservations(reservations)
    add_notification(
        "📅 Réservation annulée",
        f"#{res_id} - {res_row['nom_client']} - Chambre {res_row['numero_chambre']}",
        "warning"
    )
    return True, "Réservation annulée."

def get_upcoming_checkins(today=datetime.now()):
    reservations = load_reservations()
    today_str = today.date()
    checkins = reservations[
        (reservations['date_arrivee'].dt.date == today_str) &
        (reservations['statut'] == 'Confirmée')
    ]
    return len(checkins)

def get_reservations_stats():
    reservations = load_reservations()
    total = len(reservations)
    confirmed = len(reservations[reservations['statut'] == 'Confirmée'])
    pending = len(reservations[reservations['statut'] == 'En attente'])
    occupancy = (confirmed / total * 100) if total > 0 else 0
    return total, confirmed, pending, occupancy


# ============================================
# GESTION DES UTILISATEURS
# ============================================
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    default_users = {
        "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "admin", "nom": "Chef Maintenance"},
        "receptionniste": {"password": hashlib.sha256("reception123".encode()).hexdigest(), "role": "receptionniste", "nom": "Receptionniste"},
        "maintenance": {"password": hashlib.sha256("maintenance123".encode()).hexdigest(), "role": "maintenance", "nom": "Agent Maintenance"}
    }
    save_users(default_users)
    return default_users

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def delete_user(username):
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
        return True
    return False

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

def is_receptionist():
    return st.session_state.get("user_role") == "receptionniste"

def is_maintenance():
    return st.session_state.get("user_role") == "maintenance"

def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["user_role"] = ""
    st.session_state["user_nom"] = ""
    st.query_params.clear()


# ============================================
# NAVIGATION
# ============================================
def navigate_to_tab(tab_index):
    st.session_state["active_tab"] = tab_index
    st.rerun()

def get_tabs_for_role():
    if is_maintenance():
        tab_names = ["🏠 Dashboard", "🔧 Mes Tâches"]
        return tab_names, st.tabs(tab_names)
    elif is_receptionist():
        tab_names = ["🏠 Dashboard", "📅 Réservations", "🔴 Déclarer une Panne", "🛏️ Gestion Chambres"]
        tabs = st.tabs(tab_names)
        return tab_names, tabs
    else:  # Admin
        tab_names = [
            "🏠 Dashboard", "📅 Réservations", "🔴 Réclamations", "🛏️ Chambres", "🔧 Maintenance",
            "⚙️ Pannes", "🔩 Composants", "👥 Agents", "👤 Utilisateurs"
        ]
        tabs = st.tabs(tab_names)
        return tab_names, tabs

def navigate_to_section(section_name):
    st.session_state["view_section"] = section_name


# ============================================
# GESTION DES CHAMBRES
# ============================================
def load_rooms():
    if os.path.exists(ROOMS_FILE):
        df = pd.read_csv(ROOMS_FILE)
        df["numero"] = df["numero"].astype(str)
        return df
    rooms_data = []
    for i in range(1, 75):
        rooms_data.append({"numero": str(1000 + i), "type": "Standard", "aile": "A", "statut": "Libre", "etage": 1})
    for i in range(1, 66):
        rooms_data.append({"numero": str(2000 + i), "type": "Standard", "aile": "A", "statut": "Occupée", "etage": 2})
    for i in range(33, 66):
        rooms_data.append({"numero": str(3000 + i), "type": "Suite", "aile": "B", "statut": "Libre", "etage": 3})
    for i in range(0, 33):
        rooms_data.append({"numero": str(3200 + i), "type": "Deluxe", "aile": "B", "statut": "Occupée", "etage": 3})
    rooms_data.extend([
        {"numero": "A1", "type": "Appartement", "aile": "B", "statut": "Libre", "etage": 0},
        {"numero": "A2", "type": "Appartement", "aile": "B", "statut": "Libre", "etage": 0},
        {"numero": "A3", "type": "Appartement", "aile": "A", "statut": "Occupée", "etage": 0},
        {"numero": "A4", "type": "Appartement", "aile": "A", "statut": "Libre", "etage": 0}
    ])
    df = pd.DataFrame(rooms_data)
    df.to_csv(ROOMS_FILE, index=False)
    return df

def save_rooms(rooms):
    rooms.to_csv(ROOMS_FILE, index=False)

def add_room(numero, type_room, aile, etage, statut="Libre"):
    rooms = load_rooms()
    if str(numero) in rooms["numero"].values:
        return False, "Cette chambre existe déjà"
    new_room = pd.DataFrame([{"numero": str(numero), "type": type_room, "aile": aile, "etage": etage, "statut": statut}])
    rooms = pd.concat([rooms, new_room], ignore_index=True)
    save_rooms(rooms)
    return True, "Chambre ajoutée avec succès"

def delete_room(numero):
    rooms = load_rooms()
    if str(numero) not in rooms["numero"].values:
        return False, "Cette chambre n'existe pas"
    tasks = load_maintenance_tasks()
    active_tasks = tasks[(tasks["chambre"] == str(numero)) & (tasks["statut"] != "Terminé")]
    if len(active_tasks) > 0:
        return False, f"Impossible de supprimer: {len(active_tasks)} tâche(s) active(s)"
    rooms = rooms[rooms["numero"] != str(numero)]
    save_rooms(rooms)
    return True, "Chambre supprimée"

def update_room_status(room_num, new_statut):
    rooms = load_rooms()
    rooms.loc[rooms["numero"] == str(room_num), "statut"] = new_statut
    save_rooms(rooms)
    return rooms

def update_room_status_with_notification(room_num, new_statut, changed_by):
    rooms = load_rooms()
    room_row = rooms[rooms["numero"] == str(room_num)]
    old_statut = room_row.iloc[0]["statut"] if len(room_row) > 0 else "?"
    update_room_status(room_num, new_statut)
    add_notification(
        "🏨 Statut chambre modifié",
        f"Chambre {room_num}: {old_statut} → {new_statut} par {changed_by}",
        "warning", target_role="admin"
    )
    return True


# ============================================
# GESTION DES TÂCHES DE MAINTENANCE
# ============================================
def load_maintenance_tasks():
    if os.path.exists(MAINTENANCE_FILE):
        df = pd.read_csv(MAINTENANCE_FILE)
        if "priorite" not in df.columns:
            df["priorite"] = "Moyenne"
        if "duree_estimee_minutes" not in df.columns:
            df["duree_estimee_minutes"] = 0.0
        if "duree_reelle_minutes" not in df.columns:
            df["duree_reelle_minutes"] = 0.0
        if "type_panne" not in df.columns:
            df["type_panne"] = "Autre"
        if "date_completion" in df.columns:
            df["date_completion"] = df["date_completion"].astype(str)
        return df
    df = pd.DataFrame(columns=["id", "chambre", "description", "assigned_to", "statut",
                                "date_creation", "date_completion", "created_by", "priorite",
                                "duree_estimee_minutes", "duree_reelle_minutes", "type_panne"])
    df.to_csv(MAINTENANCE_FILE, index=False)
    return df

def save_maintenance_tasks(tasks):
    tasks.to_csv(MAINTENANCE_FILE, index=False)

def create_maintenance_task(chambre, description, assigned_to, created_by,
                            type_panne="Autre", duree_estimee=0, priorite="Moyenne"):
    tasks = load_maintenance_tasks()
    rooms = load_rooms()
    new_id = tasks["id"].max() + 1 if len(tasks) > 0 else 1
    new_task = pd.DataFrame([{
        "id": new_id, "chambre": chambre, "description": description, "type_panne": type_panne,
        "assigned_to": assigned_to, "statut": "En attente",
        "date_creation": datetime.now().strftime("%Y-%m-%d %H:%M"), "date_completion": "",
        "created_by": created_by, "duree_estimee_minutes": duree_estimee, "priorite": priorite
    }])
    tasks = pd.concat([tasks, new_task], ignore_index=True)
    save_maintenance_tasks(tasks)
    current_status = rooms[rooms["numero"] == str(chambre)]["statut"].values
    if len(current_status) > 0 and current_status[0] != "Occupée":
        update_room_status(chambre, "Maintenance")
    add_notification("🔧 Nouvelle tâche de maintenance",
                     f"Chambre {chambre}: {type_panne} - {description[:50]}", "warning")
    add_notification("🎯 Nouvelle tâche assignée",
                     f"Chambre {chambre} - {type_panne}: {description[:40]}", "info",
                     target_role="maintenance")
    return tasks

def update_task_status(task_id, new_statut):
    tasks = load_maintenance_tasks()
    task = tasks[tasks["id"] == task_id].iloc[0]
    chambre = task["chambre"]
    tasks.loc[tasks["id"] == task_id, "statut"] = new_statut
    if new_statut == "Terminé":
        idx = tasks[tasks["id"] == task_id].index[0]
        tasks.at[idx, "date_completion"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        other_active = tasks[(tasks["chambre"] == chambre) & (tasks["statut"] != "Terminé")]
        if len(other_active) == 0:
            update_room_status(chambre, "Libre")
        add_notification("✅ Maintenance terminée", f"La chambre {chambre} est maintenant libre", "success")
        add_notification("📢 Chambre libérée", f"La chambre {chambre} est prête pour le check-in",
                         "success", target_role="receptionniste")
    elif new_statut == "En cours":
        add_notification("▶ Maintenance démarrée", f"Chambre {chambre}: {task['description'][:50]}", "info")
    save_maintenance_tasks(tasks)
    return tasks

def update_task_duree(task_id, duree_reelle):
    tasks = load_maintenance_tasks()
    tasks.loc[tasks["id"] == task_id, "duree_reelle_minutes"] = duree_reelle
    save_maintenance_tasks(tasks)
    return tasks

def update_task_priorite(task_id, new_priorite):
    tasks = load_maintenance_tasks()
    tasks.loc[tasks["id"] == task_id, "priorite"] = new_priorite
    save_maintenance_tasks(tasks)
    return tasks

def delete_maintenance_task(task_id, add_notif=True):
    tasks = load_maintenance_tasks()
    task = None
    if len(tasks[tasks["id"] == task_id]) > 0:
        task = tasks[tasks["id"] == task_id].iloc[0]
    tasks = tasks[tasks["id"] != task_id]
    save_maintenance_tasks(tasks)
    if add_notif and task is not None:
        add_notification("🗑️ Maintenance supprimée",
                         f"Chambre {task['chambre']}: {task['description'][:50]}", "error")
    return tasks

def get_maintenance_history(room_num):
    tasks = load_maintenance_tasks()
    try:
        room_num_int = int(room_num)
        room_tasks = tasks[tasks["chambre"] == room_num_int].copy()
    except Exception:
        room_tasks = tasks[tasks["chambre"] == str(room_num)].copy()
    return room_tasks.sort_values("date_creation", ascending=False)

def get_maintenance_count(room_num):
    tasks = load_maintenance_tasks()
    try:
        room_num_int = int(room_num)
        return len(tasks[(tasks["chambre"] == room_num_int) & (tasks["statut"] == "Terminé")])
    except Exception:
        return len(tasks[(tasks["chambre"] == str(room_num)) & (tasks["statut"] == "Terminé")])

def clear_maintenance_history(room_num):
    tasks = load_maintenance_tasks()
    try:
        room_num_int = int(room_num)
        tasks = tasks[tasks["chambre"] != room_num_int]
    except Exception:
        tasks = tasks[tasks["chambre"] != str(room_num)]
    save_maintenance_tasks(tasks)
    update_room_status(room_num, "Libre")
    return tasks

def cancel_maintenance(task_id):
    return delete_maintenance_task(task_id, add_notif=False)

def is_problem_room(room_num):
    return get_maintenance_count(room_num) >= 3

def check_and_restore_session():
    try:
        encoded = st.query_params.get("session")
        if encoded:
            session_data = json.loads(base64.b64decode(encoded).decode())
            age = datetime.now().timestamp() - session_data.get("timestamp", 0)
            if age < 7 * 24 * 3600:
                st.session_state["logged_in"] = True
                st.session_state["username"] = session_data["username"]
                st.session_state["user_role"] = session_data["role"]
                st.session_state["user_nom"] = session_data["nom"]
                return True
    except Exception:
        pass
    return False


# ============================================
# PAGE DE LOGIN
# ============================================
def show_login():
    st.markdown("<div style='max-width: 400px; margin: 100px auto; padding: 40px; background: #1e293b; border-radius: 20px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>🏨 Hotel Mediterranee</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #CC6D3D;'>Connexion</h3>", unsafe_allow_html=True)

    if check_and_restore_session():
        st.rerun()

    st.markdown("---")
    username = st.text_input("Nom d'utilisateur", key="login_user")
    password = st.text_input("Mot de passe", type="password", key="login_pass")
    remember_me = st.checkbox("✅ Se souvenir de moi", value=True, key="remember_me")

    col_login, _ = st.columns([1, 1])
    with col_login:
        if st.button("🔑 Se connecter", use_container_width=True):
            user = authenticate(username, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["user_role"] = user["role"]
                st.session_state["user_nom"] = user["nom"]
                if remember_me:
                    session_data = {
                        "username": username,
                        "role": user["role"],
                        "nom": user["nom"],
                        "timestamp": int(datetime.now().timestamp())
                    }
                    encoded = base64.b64encode(json.dumps(session_data).encode()).decode()
                    st.query_params["session"] = encoded
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")

    st.markdown("---")
    st.info("💡 Astuce: Cochez \"Se souvenir de moi\" pour rester connecté pendant 7 jours")
    st.markdown("</div>", unsafe_allow_html=True)


# ============================================
# PAGE PRINCIPALE
# ============================================
def show_main_app():
    rooms = load_rooms()

    unread_count = get_unread_count()
    current_time = int(datetime.now().timestamp())
    st.markdown(f"""
    <div id="notification-count-data" data-count="{unread_count}" data-time="{current_time}" style="display:none;"></div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<div style='text-align: center; padding: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("<h2>🏨 Mediterranee</h2>", unsafe_allow_html=True)
        st.markdown("<p>Hammamet</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

        st.markdown("### 📊 Aperçu")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("Libres", len(rooms[rooms["statut"] == "Libre"]))
        with col_s2:
            st.metric("Occupées", len(rooms[rooms["statut"] == "Occupée"]))
        st.metric("Maintenance", len(rooms[rooms["statut"] == "Maintenance"]))
        st.markdown("---")

        st.markdown("### 🔔 Notifications")
        unread_count = get_unread_count()
        if unread_count > 0:
            st.warning(f"🔴 {unread_count} non lue(s)")
        else:
            st.success("✓ Toutes lues")

        if is_admin() and unread_count > 0:
            if st.button("✅ Tout marquer comme lu", use_container_width=True):
                mark_all_notifications_read()
                st.rerun()

        with st.expander("Voir les notifications"):
            notifications = get_user_notifications()
            if notifications:
                for notif in notifications[:10]:
                    notif_style = "background: #2d3748; padding: 10px; margin: 5px 0; border-radius: 8px;"
                    if notif["type"] == "success":
                        notif_style += "border-left: 4px solid #10b981;"
                    elif notif["type"] == "warning":
                        notif_style += "border-left: 4px solid #f59e0b;"
                    elif notif["type"] == "error":
                        notif_style += "border-left: 4px solid #ef4444;"
                    else:
                        notif_style += "border-left: 4px solid #3b82f6;"
                    unread_indicator = " 🔴" if not notif["read"] else ""
                    st.markdown(f"""
                    <div style="{notif_style}">
                        <strong>{notif['title']}{unread_indicator}</strong><br>
                        <small>{notif['message']}</small><br>
                        <small style="color: #94a3b8;">{notif['date']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    if not notif["read"]:
                        if st.button("✓ Marquer comme lu", key=f"read_{notif['id']}"):
                            mark_notification_read(notif["id"])
                            st.rerun()
            else:
                st.info("Aucune notification")

        st.markdown("---")
        st.markdown(f"**Utilisateur:** {st.session_state.get('user_nom', 'Utilisateur')}")
        st.markdown(f"**Rôle:** {st.session_state.get('user_role', '').capitalize()}")
        if st.button("🚪 Déconnexion", use_container_width=True):
            logout()
            st.rerun()
        st.markdown("---")
        st.caption("🎓 PFE - Hotel Mediterranee")

    st.title("🏨 Hotel Mediterranee Hammamet")

    tab_names, tabs = get_tabs_for_role()

    if is_maintenance():
        tab1, tab2 = tabs
    elif is_receptionist():
        tab_recep1, tab_reservations, tab_recep2, tab_recep3 = tabs
    else:
        tab_dash, tab_reserv_admin, tab_reclamations, tab_rooms, tab_maint, tab_pannes, tab_composants, tab_agents, tab_users = tabs

    # ========== DASHBOARD ==========
    with (tab1 if is_maintenance() else (tab_recep1 if is_receptionist() else tab_dash)):
        st.subheader("📊 Tableau de Bord - Vue d'Ensemble")

        rooms = load_rooms()
        reclamations = load_reclamations()
        tasks = load_maintenance_tasks()
        pannes = load_pannes()
        composants = load_composants()
        users = load_users()

        total_rooms = len(rooms)
        free_rooms = len(rooms[rooms["statut"] == "Libre"])
        occupied_rooms = len(rooms[rooms["statut"] == "Occupée"])
        maintenance_rooms = len(rooms[rooms["statut"] == "Maintenance"])
        occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0

        reclamations_pending = len(reclamations[reclamations["statut"] == "Déclaré"]) if len(reclamations) > 0 else 0
        reclamations_in_progress = len(reclamations[reclamations["statut"] == "En traitement"]) if len(reclamations) > 0 else 0

        total_tasks = len(tasks)
        tasks_pending = len(tasks[tasks["statut"] == "En attente"]) if len(tasks) > 0 else 0
        tasks_in_progress = len(tasks[tasks["statut"] == "En cours"]) if len(tasks) > 0 else 0
        tasks_completed = len(tasks[tasks["statut"] == "Terminé"]) if len(tasks) > 0 else 0

        pannes_haute = len(pannes[pannes["priorite"] == "Haute"]) if len(pannes) > 0 else 0
        pannes_moyenne = len(pannes[pannes["priorite"] == "Moyenne"]) if len(pannes) > 0 else 0
        pannes_basse = len(pannes[pannes["priorite"] == "Basse"]) if len(pannes) > 0 else 0

        total_composants = len(composants)
        composants_good = len(composants[composants["statut"] == "Bon"]) if len(composants) > 0 else 0
        composants_broken = len(composants[composants["statut"] == "Cassé"]) if len(composants) > 0 else 0
        composants_degraded = len(composants[composants["statut"] == "Dégradé"]) if len(composants) > 0 else 0

        total_users = len(users)
        admin_users_count = len([u for u in users.values() if u["role"] == "admin"])
        maintenance_users_count = len([u for u in users.values() if u["role"] == "maintenance"])
        receptionist_users_count = len([u for u in users.values() if u["role"] == "receptionniste"])

        if "view_section" not in st.session_state:
            st.session_state["view_section"] = None

        st.markdown("### 🎯 Indicateurs Clés")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📈 Taux d'Occupation", key="nav_occupancy"):
                st.session_state["view_section"] = "rooms"
            st.metric("📈 Taux d'Occupation", f"{occupancy_rate:.1f}%", f"{occupied_rooms}/{total_rooms} chambres")
        with col2:
            if st.button("🛏️ Chambres Disponibles", key="nav_available"):
                st.session_state["view_section"] = "rooms"
            st.metric("🛏️ Chambres Disponibles", free_rooms, f"sur {total_rooms} total")
        with col3:
            total_issues = reclamations_pending + tasks_pending
            if st.button("⚠️ Problèmes Actifs", key="nav_issues"):
                st.session_state["view_section"] = "issues"
            st.metric("⚠️ Problèmes Actifs", total_issues, f"{reclamations_pending} pannes + {tasks_pending} tâches")

        st.markdown("---")
        st.markdown("### 📊 Sections Détaillées")

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.markdown("#### 🛏️ **Chambres**")
            room_cols = st.columns(2)
            with room_cols[0]:
                if st.button("🏨 Total Chambres", key="nav_total_rooms"):
                    st.session_state["view_section"] = "rooms"
                st.metric("🏨 Total", total_rooms)
                if st.button("🔧 En Maintenance", key="nav_maint_rooms"):
                    st.session_state["view_section"] = "rooms"
                st.metric("🔧 Maintenance", maintenance_rooms)
            with room_cols[1]:
                if st.button("✅ Libres", key="nav_free_rooms"):
                    st.session_state["view_section"] = "rooms"
                st.metric("✅ Libres", free_rooms)
                if st.button("🔒 Occupées", key="nav_occupied_rooms"):
                    st.session_state["view_section"] = "rooms"
                st.metric("🔒 Occupées", occupied_rooms)

        with col_a2:
            st.markdown("#### 🔴 **Réclamations**")
            rec_cols = st.columns(2)
            with rec_cols[0]:
                if st.button("⏳ En Attente", key="nav_rec_pending"):
                    navigate_to_section("reclamations")
                st.metric("⏳ En Attente", reclamations_pending)
            with rec_cols[1]:
                if st.button("🔄 En Traitement", key="nav_rec_progress"):
                    navigate_to_section("reclamations")
                st.metric("🔄 En Traitement", reclamations_in_progress)

        st.markdown("---")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown("#### 🔧 **Maintenance**")
            maint_cols = st.columns(3)
            with maint_cols[0]:
                if st.button("📋 Total Tâches", key="nav_total_tasks"):
                    navigate_to_section("maintenance")
                st.metric("📋 Total", total_tasks)
            with maint_cols[1]:
                if st.button("⏳ En Attente", key="nav_tasks_pending"):
                    navigate_to_section("maintenance")
                st.metric("⏳ En Attente", tasks_pending)
            with maint_cols[2]:
                if st.button("🔄 En Cours", key="nav_tasks_progress"):
                    navigate_to_section("maintenance")
                st.metric("🔄 En Cours", tasks_in_progress)

        with col_b2:
            st.markdown("#### ⚙️ **Types de Pannes**")
            panne_cols = st.columns(3)
            with panne_cols[0]:
                if st.button("🔴 Haute", key="nav_pannes_high"):
                    if is_admin():
                        st.session_state["active_tab"] = 4
                        st.rerun()
                st.metric("🔴 Haute", pannes_haute)
            with panne_cols[1]:
                if st.button("🟡 Moyenne", key="nav_pannes_medium"):
                    if is_admin():
                        st.session_state["active_tab"] = 4
                        st.rerun()
                st.metric("🟡 Moyenne", pannes_moyenne)
            with panne_cols[2]:
                if st.button("🟢 Basse", key="nav_pannes_low"):
                    if is_admin():
                        st.session_state["active_tab"] = 4
                        st.rerun()
                st.metric("🟢 Basse", pannes_basse)

        st.markdown("---")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("#### 🔩 **Composants**")
            comp_cols = st.columns(2)
            with comp_cols[0]:
                if st.button("📦 Total Composants", key="nav_total_comp"):
                    if is_admin():
                        st.session_state["active_tab"] = 5
                        st.rerun()
                st.metric("📦 Total", total_composants)
                if st.button("✅ Disponibles", key="nav_comp_good"):
                    if is_admin():
                        st.session_state["active_tab"] = 5
                        st.rerun()
                pct_good = (composants_good / total_composants * 100) if total_composants > 0 else 0
                st.metric("✅ Disponibles", f"{composants_good}/{total_composants}", f"{pct_good:.1f}%")
            with comp_cols[1]:
                if st.button("❌ En Panne", key="nav_comp_broken"):
                    if is_admin():
                        st.session_state["active_tab"] = 5
                        st.rerun()
                st.metric("❌ En Panne", composants_broken)
                if st.button("⚠️ À Réviser", key="nav_comp_degraded"):
                    if is_admin():
                        st.session_state["active_tab"] = 5
                        st.rerun()
                st.metric("⚠️ À Réviser", composants_degraded)

        with col_c2:
            st.markdown("#### 👥 **Utilisateurs**")
            user_cols = st.columns(2)
            with user_cols[0]:
                if st.button("👤 Total Utilisateurs", key="nav_total_users"):
                    if is_admin():
                        st.session_state["active_tab"] = 7
                        st.rerun()
                st.metric("👤 Total", total_users)
                if st.button("👑 Administrateurs", key="nav_admin_users"):
                    if is_admin():
                        st.session_state["active_tab"] = 7
                        st.rerun()
                st.metric("👑 Admins", admin_users_count)
            with user_cols[1]:
                if st.button("🔧 Agents Maintenance", key="nav_maint_users"):
                    if is_admin():
                        st.session_state["active_tab"] = 6
                        st.rerun()
                st.metric("🔧 Agents", maintenance_users_count)
                if st.button("🏨 Réceptionnistes", key="nav_recep_users"):
                    if is_admin():
                        st.session_state["active_tab"] = 7
                        st.rerun()
                st.metric("🏨 Réception", receptionist_users_count)

        if st.session_state.get("view_section"):
            st.markdown("---")
            section = st.session_state["view_section"]
            st.markdown(f"### 📋 Détails - {section.title()}")

            if section == "rooms":
                st.markdown("**🛏️ Gestion des Chambres**")
                st.dataframe(rooms["statut"].value_counts().to_frame(), use_container_width=True)
                col_nav1, col_nav2 = st.columns(2)
                with col_nav1:
                    if st.button("🔍 Voir toutes les chambres", key="go_to_rooms"):
                        st.session_state["active_tab"] = 2
                        st.session_state["view_section"] = None
                        st.rerun()
                with col_nav2:
                    if st.button("❌ Fermer les détails", key="close_details"):
                        st.session_state["view_section"] = None
                        st.rerun()

            elif section == "reclamations":
                st.markdown("**🔴 Réclamations de Pannes**")
                if len(reclamations) > 0:
                    recent_recs = reclamations.sort_values("date_declaration", ascending=False).head(10)
                    for _, rec in recent_recs.iterrows():
                        icon = "🔴" if rec["statut"] == "Déclaré" else "🟡" if rec["statut"] == "En traitement" else "🟢"
                        with st.expander(f"{icon} Chambre {rec['chambre']} - {rec['type_panne']}"):
                            st.markdown(f"**Description:** {rec['description']}")
                            st.markdown(f"**Signalée par:** {rec['creé_par']}")
                            st.markdown(f"**Date:** {rec['date_declaration']}")
                            st.markdown(f"**Statut:** {rec['statut']}")
                else:
                    st.info("Aucune réclamation")
                col_nav1, col_nav2 = st.columns(2)
                with col_nav1:
                    if st.button("🔍 Voir toutes les réclamations", key="go_to_reclamations_full"):
                        st.session_state["active_tab"] = 1
                        st.session_state["view_section"] = None
                        st.rerun()
                with col_nav2:
                    if st.button("❌ Fermer", key="close_reclamations"):
                        st.session_state["view_section"] = None

            elif section == "maintenance":
                st.markdown("**🔧 Tâches de Maintenance**")
                if len(tasks) > 0:
                    recent_tasks = tasks.sort_values("date_creation", ascending=False).head(10)
                    for _, task in recent_tasks.iterrows():
                        icon = "🟡" if task["statut"] == "En attente" else "🔵" if task["statut"] == "En cours" else "🟢"
                        with st.expander(f"{icon} #{task['id']} - Chambre {task['chambre']}"):
                            st.markdown(f"**Description:** {task['description']}")
                            st.markdown(f"**Type:** {task.get('type_panne', 'Maintenance')}")
                            st.markdown(f"**Assigné à:** {task['assigned_to']}")
                            st.markdown(f"**Statut:** {task['statut']}")
                else:
                    st.info("Aucune tâche")
                col_nav1, col_nav2 = st.columns(2)
                with col_nav1:
                    if st.button("🔍 Voir toutes les tâches", key="go_to_maintenance_full"):
                        st.session_state["active_tab"] = 3
                        st.session_state["view_section"] = None
                        st.rerun()
                with col_nav2:
                    if st.button("❌ Fermer", key="close_maintenance"):
                        st.session_state["view_section"] = None

    # ========== TAB RÉCEPTIONNISTE: DÉCLARER UNE PANNE ==========
    if is_receptionist():
        with tab_recep2:
            st.subheader("🔴 Déclarer une Panne")
            with st.form("declare_panne_form"):
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    occupied = rooms[rooms["statut"] != "Libre"]["numero"].tolist()
                    panne_chambre = st.selectbox("🔑 N° Chambre", occupied if occupied else rooms["numero"].tolist())
                    panne_type = st.selectbox("🔧 Type de panne", [
                        "Plomberie", "Électricité", "Climatisation", "Chauffage",
                        "Meuble", "Serrure", "Écran/TV", "WiFi", "Salle de bain", "Autre"
                    ])
                with col_d2:
                    st.info("💡 Décrivez le problème rapidement")
                    panne_desc = st.text_area("Description courte (max 100 caractères)", max_chars=100, height=100)
                submit_panne = st.form_submit_button("🚀 Signaler la panne", use_container_width=True)
                if submit_panne and panne_chambre and panne_type and panne_desc:
                    add_reclamation(panne_chambre, panne_type, panne_desc, st.session_state.get("user_nom"))
                    st.success("✅ Panne signalée à l'administrateur!")
                    st.balloons()
                    st.rerun()
            st.markdown("---")
            st.info("📌 L'administrateur sera notifié immédiatement et créera une tâche de maintenance.")

    # ========== TAB RÉCEPTIONNISTE: GESTION CHAMBRES ==========
    if is_receptionist():
        with tab_recep3:
            st.subheader("🛏️ Gestion des Chambres")
            rooms = load_rooms()
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                aile_filter = st.selectbox("Aile", ["Tous", "A", "B"], key="recep_aile_f")
            with col_f2:
                statut_filter = st.selectbox("Statut actuel", ["Tous", "Libre", "Occupée", "Maintenance"], key="recep_statut_f")
            filtered = rooms.copy()
            if aile_filter != "Tous":
                filtered = filtered[filtered["aile"] == aile_filter]
            if statut_filter != "Tous":
                filtered = filtered[filtered["statut"] == statut_filter]
            st.markdown(f"**{len(filtered)} chambres affichées**")
            for i, row in filtered.iterrows():
                icon = "🟢" if row['statut'] == "Libre" else "🔴" if row['statut'] == "Occupée" else "🟡"
                with st.expander(f"{icon} Chambre {row['numero']} - {row['type']} ({row['statut']})"):
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.markdown(f"**Type:** {row['type']}")
                        st.markdown(f"**Étage:** {row['etage']}")
                        st.markdown(f"**Aile:** {row['aile']}")
                    with col_r2:
                        col_b1, col_b2 = st.columns(2)
                        with col_b1:
                            if row['statut'] != "Libre":
                                if st.button("✅ Libre", key=f"recep_libre_{row['numero']}"):
                                    update_room_status_with_notification(row["numero"], "Libre", st.session_state.get("user_nom", "Réceptionniste"))
                                    st.rerun()
                        with col_b2:
                            if row['statut'] != "Occupée":
                                if st.button("🔒 Occupée", key=f"recep_occup_{row['numero']}"):
                                    update_room_status_with_notification(row["numero"], "Occupée", st.session_state.get("user_nom", "Réceptionniste"))
                                    st.rerun()
                        if row['statut'] != "Maintenance":
                            if st.button("🔧 Maintenance", key=f"recep_maint_{row['numero']}", type="secondary"):
                                update_room_status_with_notification(row["numero"], "Maintenance", st.session_state.get("user_nom", "Réceptionniste"))
                                st.rerun()
            with st.expander("📋 Vue tableau complète"):
                st.dataframe(filtered, use_container_width=True)

    # ========== TAB RÉCLAMATIONS (Admin) ==========
    if is_admin():
        with tab_reclamations:
            st.subheader("🔴 Réclamations de Pannes Signalées")
            reclamations = load_reclamations()
            col_rec1, col_rec2 = st.columns(2)
            with col_rec1:
                st.metric("En attente", len(reclamations[reclamations["statut"] == "Déclaré"]) if len(reclamations) > 0 else 0)
            with col_rec2:
                st.metric("En traitement", len(reclamations[reclamations["statut"] == "En traitement"]) if len(reclamations) > 0 else 0)
            st.markdown("---")
            if len(reclamations) > 0:
                for idx, rec in reclamations.sort_values("date_declaration", ascending=False).iterrows():
                    icon = "🔴" if rec["statut"] == "Déclaré" else "🟡" if rec["statut"] == "En traitement" else "🟢"
                    with st.expander(f"{icon} Chambre {rec['chambre']} - {rec['type_panne']} ({rec['statut']})"):
                        col_r1, col_r2 = st.columns(2)
                        with col_r1:
                            st.markdown(f"**Type:** {rec['type_panne']}")
                            st.markdown(f"**Description:** {rec['description']}")
                            st.markdown(f"**Signalée par:** {rec['creé_par']}")
                        with col_r2:
                            st.markdown(f"**Date:** {rec['date_declaration']}")
                            st.markdown(f"**Statut:** {rec['statut']}")
                        col_a1, col_a2, col_a3 = st.columns(3)
                        with col_a1:
                            if st.button("✅ Créer une tâche", key=f"create_task_{rec['id']}_{idx}"):
                                st.session_state[f"show_task_form_{rec['id']}"] = True
                        with col_a2:
                            if rec["statut"] != "En traitement":
                                if st.button("⏳ En traitement", key=f"in_treatment_{rec['id']}_{idx}"):
                                    update_reclamation_status(rec["id"], "En traitement")
                                    st.rerun()
                        with col_a3:
                            if st.button("🗑️ Supprimer", key=f"delete_rec_{rec['id']}_{idx}"):
                                delete_reclamation(rec["id"])
                                st.rerun()
                        if st.session_state.get(f"show_task_form_{rec['id']}", False):
                            st.markdown("---")
                            with st.form(f"create_task_form_{rec['id']}"):
                                col_t1, col_t2 = st.columns(2)
                                with col_t1:
                                    task_priorite = st.selectbox("🚨 Priorité", ["Haute", "Moyenne", "Basse"], key=f"task_prio_{rec['id']}")
                                    task_duree = st.number_input("⏱️ Durée estimée (min)", min_value=10.0, value=30.0, step=5.0, key=f"task_dur_{rec['id']}")
                                with col_t2:
                                    agents = [u["nom"] for u in load_users().values() if u["role"] == "maintenance"]
                                    task_agent = st.selectbox("👤 Assigner à", agents, key=f"task_agent_{rec['id']}")
                                task_desc_detail = st.text_area("📝 Description", value=rec["description"], key=f"task_desc_{rec['id']}")
                                if st.form_submit_button("✅ Créer la tâche"):
                                    create_maintenance_task(rec["chambre"], task_desc_detail, task_agent,
                                                            st.session_state.get("user_nom"), rec["type_panne"],
                                                            task_duree, task_priorite)
                                    update_reclamation_status(rec["id"], "En traitement")
                                    st.session_state[f"show_task_form_{rec['id']}"] = False
                                    st.rerun()
            else:
                st.info("Aucune réclamation pour le moment. ✨")

    # ========== TAB CHAMBRES ==========
    if not is_maintenance() and not is_receptionist():
        with tab_rooms:
            st.subheader("🛏️ Gestion des Chambres")
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                aile_filter = st.selectbox("Aile", ["Tous", "A", "B"], key="aile_f")
            with col_f2:
                statut_filter = st.selectbox("Statut", ["Tous", "Libre", "Occupée", "Maintenance"], key="statut_f")
            with col_f3:
                etage_filter = st.selectbox("Étage", ["Tous", 0, 1, 2, 3], key="etage_f")
            filtered = rooms.copy()
            if aile_filter != "Tous":
                filtered = filtered[filtered["aile"] == aile_filter]
            if statut_filter != "Tous":
                filtered = filtered[filtered["statut"] == statut_filter]
            if etage_filter != "Tous":
                filtered = filtered[filtered["etage"] == etage_filter]
            st.markdown(f"**{len(filtered)}/{len(rooms)} chambres**")
            for i, row in filtered.iterrows():
                maint_count = get_maintenance_count(row['numero'])
                is_prob = is_problem_room(row['numero'])
                with st.expander(f"🚪 Chambre {row['numero']} - {row['type']} ({row['aile']}){' ⚠️' if is_prob else ''}"):
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.markdown(f"**Statut actuel:** {row['statut']}")
                        st.markdown(f"**Étage:** {row['etage']}")
                        st.markdown(f"**Aile:** {row['aile']}")
                        st.markdown(f"**Maintenances:** {maint_count}")
                        if is_prob:
                            st.error("⚠️ Chambre PROBLÈME (3+ maintenances)")
                    with col_r2:
                        col_b1, col_b2, col_b3 = st.columns(3)
                        with col_b1:
                            if st.button("✅ Libre", key=f"libre_{row['numero']}"):
                                update_room_status(row["numero"], "Libre")
                                st.rerun()
                        with col_b2:
                            if st.button("🔒 Occupée", key=f"occup_{row['numero']}"):
                                update_room_status(row["numero"], "Occupée")
                                st.rerun()
                        with col_b3:
                            if st.button("🔧 Maintenance", key=f"maint_{row['numero']}"):
                                update_room_status(row["numero"], "Maintenance")
                                st.rerun()
                    if st.button(f"🔍 Voir l'historique", key=f"history_{row['numero']}"):
                        history = get_maintenance_history(row['numero'])
                        if len(history) > 0:
                            for _, task in history.iterrows():
                                type_panne = task.get('type_panne', 'Autre') if 'type_panne' in task.index else 'Autre'
                                icon = "🟢" if task['statut'] == "Terminé" else "🔵" if task['statut'] == "En cours" else "🟡"
                                with st.expander(f"#{task['id']} - {task['date_creation']}"):
                                    st.markdown(f"**Statut:** {icon} {task['statut']}")
                                    st.markdown(f"**Type:** {type_panne}")
                                    st.markdown(f"**Description:** {task['description']}")
                                    st.markdown(f"**Assigné à:** {task['assigned_to']}")
                                    if st.button(f"❌ Annuler", key=f"cancel_{task['id']}_{row['numero']}"):
                                        cancel_maintenance(task['id'])
                                        st.rerun()
                        else:
                            st.info("Aucune maintenance enregistrée")
                    if maint_count > 0:
                        if st.button(f"🗑️ Effacer tout l'historique", key=f"clear_{row['numero']}"):
                            clear_maintenance_history(row['numero'])
                            st.rerun()
            with st.expander("📋 Détail complet"):
                st.dataframe(filtered)

    # ========== TAB MAINTENANCE ==========
    if is_maintenance():
        with tab2:
            st.subheader("🔧 Tâches de Maintenance")
            current_user = st.session_state.get("user_nom", "")
            tasks = load_maintenance_tasks()
            my_tasks = tasks[tasks["assigned_to"] == current_user].copy()
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("Total tâches", len(my_tasks))
            with col_s2:
                st.metric("En attente", len(my_tasks[my_tasks["statut"] == "En attente"]))
            with col_s3:
                st.metric("En cours", len(my_tasks[my_tasks["statut"] == "En cours"]))
            st.markdown("---")
            if len(my_tasks) > 0:
                for idx, task in my_tasks.iterrows():
                    icon = "🟡" if task["statut"] == "En attente" else "🔵" if task["statut"] == "En cours" else "🟢"
                    type_panne = task.get('type_panne', 'Autre') if 'type_panne' in task.index else 'Autre'
                    duree_estimee = task.get('duree_estimee_minutes', 0) if 'duree_estimee_minutes' in task.index else 0
                    with st.expander(f"{icon} #{task['id']} - Chambre {task['chambre']} - {task['statut']}"):
                        st.markdown(f"**🔧 Type de panne:** {type_panne}")
                        st.markdown(f"**📝 Description:** {task['description']}")
                        st.markdown(f"**👤 Assigné par:** {task['created_by']}")
                        st.markdown(f"**📅 Créée le:** {task['date_creation']}")
                        st.markdown(f"**⏱️ Durée estimée:** {duree_estimee} minutes")
                        col_a1, col_a2 = st.columns(2)
                        with col_a1:
                            if task["statut"] == "En attente":
                                if st.button("▶ Commencer", key=f"start_{task['id']}_{idx}"):
                                    update_task_status(task["id"], "En cours")
                                    st.rerun()
                        with col_a2:
                            if task["statut"] != "Terminé":
                                if st.button("✓ Terminer", key=f"end_{task['id']}_{idx}"):
                                    update_task_status(task["id"], "Terminé")
                                    st.rerun()
                        rapports = load_rapports()
                        task_rapport = rapports[rapports["task_id"] == task['id']]
                        st.markdown("---")
                        st.markdown("**📋 Rapport de tâche:**")
                        if len(task_rapport) > 0:
                            for _, rapport in task_rapport.iterrows():
                                st.success("✅ Rapport enregistré")
                                st.info(f"**Rapport:** {rapport['rapport']}")
                        elif task["statut"] == "Terminé":
                            with st.form(f"rapport_form_{task['id']}_{idx}"):
                                rapport_text = st.text_area("Résumé du travail", key=f"rapport_{task['id']}")
                                duree_reelle = st.number_input("Durée réelle (min)", min_value=0.0, value=float(duree_estimee), step=1.0, key=f"duree_{task['id']}")
                                pieces = st.text_input("Pièces utilisées", key=f"pieces_{task['id']}")
                                notes = st.text_area("Notes", key=f"notes_{task['id']}")
                                if st.form_submit_button("Enregistrer le rapport"):
                                    if rapport_text:
                                        add_rapport(task['id'], current_user, rapport_text, duree_reelle, pieces, notes)
                                        st.rerun()
            else:
                st.info("Aucune tâche assignée. 🎉")

    elif is_admin():
        with tab_maint:
            st.subheader("🔧 Tâches de Maintenance")
            with st.expander("➕ Créer une tâche"):
                with st.form("maintenance_form"):
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        maint_chambre = st.selectbox("Chambre", rooms["numero"].tolist())
                        maint_type_panne = st.selectbox("Type de panne", [
                            "Plomberie", "Électricité", "Climatisation", "Meuble",
                            "Serrure", "Écran/TV", "WiFi", "Autre"
                        ])
                        maint_desc = st.text_area("Description du problème")
                        maint_duree = st.number_input("Durée estimée (min)", min_value=0.0, value=30.0, step=1.0)
                    with col_m2:
                        agents = [u["nom"] for u in load_users().values() if u["role"] == "maintenance"]
                        maint_agent = st.selectbox("Assigner à", agents)
                        maint_priorite = st.selectbox("🚨 Priorité", ["Basse", "Moyenne", "Haute"])
                    if st.form_submit_button("Créer la tâche") and maint_desc and maint_agent:
                        create_maintenance_task(maint_chambre, maint_desc, maint_agent,
                                                st.session_state.get("user_nom"), maint_type_panne,
                                                maint_duree, maint_priorite)
                        st.rerun()
            st.markdown("---")
            tasks = load_maintenance_tasks()
            col_mf1, col_mf2, col_mf3 = st.columns(3)
            with col_mf1:
                filter_statut = st.selectbox("Filtrer par statut", ["Tous", "En attente", "En cours", "Terminé"])
            with col_mf2:
                filter_agent = st.selectbox("Filtrer par agent", ["Tous"] + [u["nom"] for u in load_users().values() if u["role"] == "maintenance"])
            with col_mf3:
                filter_priorite = st.selectbox("Filtrer par priorité", ["Tous", "Haute", "Moyenne", "Basse"])
            filtered_tasks = tasks.copy()
            if filter_statut != "Tous":
                filtered_tasks = filtered_tasks[filtered_tasks["statut"] == filter_statut]
            if filter_agent != "Tous":
                filtered_tasks = filtered_tasks[filtered_tasks["assigned_to"] == filter_agent]
            if filter_priorite != "Tous":
                filtered_tasks = filtered_tasks[filtered_tasks["priorite"] == filter_priorite]
            priority_order = {"Haute": 0, "Moyenne": 1, "Basse": 2}
            if "priorite" in filtered_tasks.columns and len(filtered_tasks) > 0:
                filtered_tasks["priorite"] = filtered_tasks["priorite"].fillna("Moyenne")
                filtered_tasks["priority_sort"] = filtered_tasks["priorite"].map(priority_order).fillna(1)
                filtered_tasks = filtered_tasks.sort_values(["priority_sort", "date_creation"],
                                                            ascending=[True, False]).drop("priority_sort", axis=1)
            if len(filtered_tasks) > 0:
                for idx, task in filtered_tasks.iterrows():
                    icon = "🟡" if task["statut"] == "En attente" else "🔵" if task["statut"] == "En cours" else "🟢"
                    p_icon = "🚨" if task.get("priorite", "Moyenne") == "Haute" else "⚠️" if task.get("priorite", "Moyenne") == "Moyenne" else "ℹ️"
                    type_panne = task.get('type_panne', 'Autre') if 'type_panne' in task.index else 'Autre'
                    duree = float(task.get('duree_estimee_minutes', 0) or 0)
                    duree_reelle = float(task.get('duree_reelle_minutes', 0) or 0)
                    with st.expander(f"{icon} {p_icon} #{task['id']} - Chambre {task['chambre']} - {task['statut']}"):
                        col_t1, col_t2 = st.columns(2)
                        with col_t1:
                            st.markdown(f"**Type:** {type_panne}")
                            st.markdown(f"**Description:** {task['description']}")
                            st.markdown(f"**Assigné à:** {task['assigned_to']}")
                        with col_t2:
                            st.markdown(f"**🚨 Priorité:** {task.get('priorite', 'Moyenne')}")
                            st.markdown(f"**⏱️ Durée estimée:** {duree} min")
                            if duree_reelle:
                                st.markdown(f"**✓ Durée réelle:** {duree_reelle} min")
                        col_ac1, col_ac2, col_ac3 = st.columns(3)
                        with col_ac1:
                            if task["statut"] != "Terminé":
                                if st.button("▶ Commencer", key=f"start_{task['id']}_{idx}"):
                                    update_task_status(task["id"], "En cours")
                                    st.rerun()
                        with col_ac2:
                            if task["statut"] != "Terminé":
                                if st.button("✓ Terminer", key=f"end_{task['id']}_{idx}"):
                                    update_task_status(task["id"], "Terminé")
                                    st.rerun()
                        with col_ac3:
                            if st.button("🗑️ Supprimer", key=f"delete_{task['id']}_{idx}", type="primary"):
                                delete_maintenance_task(task['id'])
                                st.rerun()
                        st.markdown("---")
                        col_ch1, col_ch2, col_ch3 = st.columns(3)
                        with col_ch1:
                            new_priorite = st.selectbox("Changer priorité", ["Haute", "Moyenne", "Basse"],
                                                        index=["Haute", "Moyenne", "Basse"].index(task.get("priorite", "Moyenne")),
                                                        key=f"prio_{task['id']}")
                            if new_priorite != task.get("priorite", "Moyenne"):
                                if st.button("💾 Mettre à jour priorité", key=f"update_prio_{task['id']}"):
                                    update_task_priorite(task["id"], new_priorite)
                                    st.rerun()
                        with col_ch2:
                            duree_input = st.number_input("Durée réelle (min)", min_value=0.0,
                                                          value=duree_reelle if duree_reelle else duree,
                                                          step=1.0, key=f"duree_real_{task['id']}")
                            if st.button("💾 Enregistrer durée", key=f"update_duree_{task['id']}"):
                                update_task_duree(task["id"], duree_input)
                                st.rerun()
            else:
                st.info("Aucune tâche")

    # ========== TAB PANNES ==========
    if is_admin():
        with tab_pannes:
            st.subheader("⚙️ Gestion des Types de Pannes")
            pannes = load_pannes()
            with st.expander("➕ Ajouter un nouveau type de panne"):
                with st.form("add_panne_form"):
                    panne_nom = st.text_input("Nom de la panne")
                    panne_desc_inp = st.text_area("Description")
                    panne_priorite = st.selectbox("Priorité", ["Basse", "Moyenne", "Haute"])
                    if st.form_submit_button("Ajouter") and panne_nom:
                        add_panne(panne_nom, panne_desc_inp, panne_priorite)
                        st.rerun()
            st.markdown("---")
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                st.markdown("**Haute Priorité:**")
                for _, p in pannes[pannes["priorite"] == "Haute"].iterrows():
                    st.markdown(f"🔴 **{p['nom_panne']}**  \n{str(p['description'])[:50]}...")
            with col_p2:
                st.markdown("**Priorité Moyenne:**")
                for _, p in pannes[pannes["priorite"] == "Moyenne"].iterrows():
                    st.markdown(f"🟡 **{p['nom_panne']}**  \n{str(p['description'])[:50]}...")
            with col_p3:
                st.markdown("**Basse Priorité:**")
                for _, p in pannes[pannes["priorite"] == "Basse"].iterrows():
                    st.markdown(f"🟢 **{p['nom_panne']}**  \n{str(p['description'])[:50]}...")
            with st.expander("📊 Tableau complet"):
                st.dataframe(pannes)

    # ========== TAB COMPOSANTS ==========
    if is_admin():
        with tab_composants:
            st.subheader("🔩 Gestion des Composants de Chambres")
            composants = load_composants()
            rooms_list = rooms["numero"].tolist()
            tab_comp1, tab_comp2, tab_comp3 = st.tabs(["➕ Ajouter", "👁️ Vue Chambres", "📊 Tous les Composants"])
            with tab_comp1:
                with st.form("add_composant_form"):
                    col_c1, col_c2 = st.columns(2)
                    with col_c1:
                        comp_chambre = st.selectbox("🔑 Chambre", rooms_list)
                        comp_principal = st.selectbox("🔧 Composant Principal", [
                            "Climatisation", "Chauffage", "Serrure", "Plomberie",
                            "Éclairage", "Électricité", "Meuble", "Télévision",
                            "Lavabo", "Salle de bain", "Téléphone", "WiFi", "Matelas", "Rideau"
                        ])
                    with col_c2:
                        comp_sous = st.text_input("Sous-composant")
                        comp_statut = st.selectbox("État", ["Bon", "Dégradé", "Cassé", "En maintenance"])
                    if st.form_submit_button("✅ Ajouter le composant", use_container_width=True):
                        if comp_chambre and comp_principal and comp_sous:
                            add_composant(comp_chambre, comp_principal, comp_sous, comp_statut)
                            st.rerun()
                        else:
                            st.error("❌ Veuillez remplir tous les champs")
            with tab_comp2:
                selected_room = st.selectbox("Sélectionner une chambre", rooms_list, key="room_composant")
                room_comps = composants[composants["chambre"] == str(selected_room)]
                if len(room_comps) > 0:
                    for idx, comp in room_comps.iterrows():
                        icon = "✅" if comp["statut"] == "Bon" else "⚠️" if comp["statut"] == "Dégradé" else "❌" if comp["statut"] == "Cassé" else "🔧"
                        with st.expander(f"{icon} {comp['composant_principal']} - {comp['sous_composant']}"):
                            col_i1, col_i2, col_i3 = st.columns([2, 2, 1.5])
                            with col_i1:
                                st.markdown(f"- **Composant:** {comp['composant_principal']}")
                                st.markdown(f"- **Sous-composant:** {comp['sous_composant']}")
                            with col_i2:
                                st.markdown(f"- **Installation:** {comp['date_installation']}")
                                st.markdown(f"- **Maintenance:** {comp['derniere_maintenance'] or '❌ Jamais'}")
                            with col_i3:
                                new_status = st.selectbox("Statut", ["Bon", "Dégradé", "Cassé", "En maintenance"],
                                                          index=["Bon", "Dégradé", "Cassé", "En maintenance"].index(comp["statut"]),
                                                          key=f"status_{comp['id']}")
                                if new_status != comp["statut"]:
                                    if st.button("💾 Actualiser", key=f"update_{comp['id']}"):
                                        update_composant_status(comp["id"], new_status)
                                        st.rerun()
                                if st.button("🗑️ Supprimer", key=f"delete_{comp['id']}", type="secondary"):
                                    delete_composant(comp["id"])
                                    st.rerun()
                else:
                    st.info(f"Aucun composant pour la chambre {selected_room}")
            with tab_comp3:
                if len(composants) > 0:
                    col_s, col_e = st.columns([3, 1])
                    with col_s:
                        search_term = st.text_input("🔍 Rechercher")
                    with col_e:
                        st.download_button("📥 Exporter CSV", composants.to_csv(index=False).encode('utf-8'),
                                           "composants.csv", "text/csv")
                    filtered_comp = composants.copy()
                    if search_term:
                        mask = (filtered_comp["chambre"].astype(str).str.contains(search_term, case=False) |
                                filtered_comp["composant_principal"].str.contains(search_term, case=False) |
                                filtered_comp["sous_composant"].str.contains(search_term, case=False))
                        filtered_comp = filtered_comp[mask]
                    edited = st.data_editor(filtered_comp, num_rows="dynamic", use_container_width=True,
                                            column_config={
                                                "statut": st.column_config.SelectboxColumn(
                                                    "Statut", options=["Bon", "Dégradé", "Cassé", "En maintenance"], required=True)
                                            })
                    if st.button("💾 Sauvegarder", use_container_width=True, type="primary"):
                        save_composants(edited)
                        st.rerun()
                else:
                    st.warning("Aucun composant.")

    # ========== TAB AGENTS ==========
    if is_admin():
        with tab_agents:
            st.subheader("👥 Historique et Performance des Agents")
            users_data = load_users()
            agents = [u["nom"] for u in users_data.values() if u["role"] == "maintenance"]
            col_ag1, col_ag2 = st.columns(2)
            with col_ag1:
                selected_agent = st.selectbox("Sélectionner un agent", agents)
            with col_ag2:
                show_all = st.checkbox("Afficher tous les agents", value=False)
            if show_all:
                agent_stats = []
                for agent in agents:
                    h = get_agent_history(agent)
                    agent_stats.append({"Agent": agent, "Total": h["total"], "Terminées": h["terminees"],
                                        "En cours": h["en_cours"], "En attente": h["en_attente"]})
                df_stats = pd.DataFrame(agent_stats)
                st.dataframe(df_stats, use_container_width=True)
            else:
                history = get_agent_history(selected_agent)
                col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                with col_s1:
                    st.metric("Total", history["total"])
                with col_s2:
                    st.metric("Terminées", history["terminees"])
                with col_s3:
                    st.metric("En cours", history["en_cours"])
                with col_s4:
                    st.metric("En attente", history["en_attente"])
                tasks = load_maintenance_tasks()
                agent_tasks = tasks[tasks["assigned_to"] == selected_agent]
                if len(agent_tasks) > 0:
                    for idx, task in agent_tasks.iterrows():
                        icon = "🟡" if task["statut"] == "En attente" else "🔵" if task["statut"] == "En cours" else "🟢"
                        with st.expander(f"{icon} #{task['id']} - Chambre {task['chambre']}"):
                            st.markdown(f"**Description:** {task['description']}")
                            st.markdown(f"**Statut:** {task['statut']}")
                            st.markdown(f"**Créée:** {task['date_creation']}")
                else:
                    st.info("Aucune tâche pour cet agent.")

    # ========== USER MANAGEMENT ==========
    if is_admin():
        with tab_users:
            st.subheader("👤 Gestion des Utilisateurs")
            tab_u1, tab_u2 = st.tabs(["Utilisateurs", "Chambres"])
            with tab_u1:
                users_data = load_users()
                col_u1, col_u2 = st.columns(2)
                with col_u1:
                    st.markdown("**Administrateurs:**")
                    for k, v in users_data.items():
                        if v["role"] == "admin":
                            st.markdown(f"- {k} ({v['nom']})")
                with col_u2:
                    st.markdown("**Autres utilisateurs:**")
                    for k, v in users_data.items():
                        if v["role"] != "admin":
                            st.markdown(f"- {k} ({v['nom']}) - {v['role']}")
                st.markdown("---")
                with st.expander("🗑️ Supprimer un utilisateur"):
                    user_to_delete = st.selectbox("Utilisateur à supprimer", list(users_data.keys()))
                    if st.button("🗑️ Supprimer", type="primary"):
                        if user_to_delete == "admin":
                            st.error("❌ Impossible de supprimer le compte admin!")
                        elif user_to_delete == st.session_state.get("username"):
                            st.error("❌ Vous ne pouvez pas supprimer votre propre compte!")
                        else:
                            delete_user(user_to_delete)
                            st.rerun()
                with st.expander("➕ Créer un utilisateur"):
                    with st.form("create_user_form"):
                        new_username = st.text_input("Nom d'utilisateur")
                        new_nom = st.text_input("Nom complet")
                        new_password = st.text_input("Mot de passe", type="password")
                        new_role = st.selectbox("Rôle", ["receptionniste", "maintenance"])
                        if st.form_submit_button("Créer") and new_username and new_password and new_nom:
                            users_data[new_username] = {"password": hash_password(new_password),
                                                        "role": new_role, "nom": new_nom}
                            save_users(users_data)
                            st.rerun()
            with tab_u2:
                st.markdown("### 🛏️ Gestion des Chambres")
                rooms = load_rooms()
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    with st.expander("➕ Ajouter une chambre"):
                        with st.form("add_room_form"):
                            room_numero = st.text_input("Numéro")
                            room_type = st.selectbox("Type", ["Standard", "Suite", "Deluxe", "Appartement"])
                            room_aile = st.selectbox("Aile", ["A", "B", "C"])
                            room_etage = st.number_input("Étage", min_value=0.0, max_value=10.0, value=1.0)
                            if st.form_submit_button("Ajouter") and room_numero:
                                success, message = add_room(room_numero, room_type, room_aile, room_etage)
                                if success:
                                    st.rerun()
                                else:
                                    st.error(message)
                with col_r2:
                    with st.expander("🗑️ Supprimer une chambre"):
                        room_to_delete = st.selectbox("Chambre à supprimer", rooms["numero"].tolist())
                        if st.button("🗑️ Supprimer cette chambre", type="primary"):
                            success, message = delete_room(room_to_delete)
                            if success:
                                st.rerun()
                            else:
                                st.error(message)
                st.dataframe(rooms, use_container_width=True)


# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state.get("logged_in", False):
        show_login()
    else:
        show_main_app()