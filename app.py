import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import hashlib
import base64

# ============================================
# CONFIGURATION PAGE
# ============================================
st.set_page_config(
    page_title="Hotel Mediterranee", 
    page_icon="🏨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# JAVASCRIPT POUR CONNEXION PERSISTANTE ET SONS
# ============================================
st.markdown("""
<script>
// Fonction pour jouer un son de notification (universel - fonctionne sur mobile/PC)
function playNotificationSound() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        // Son de notification agréable
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(1200, audioContext.currentTime + 0.1);
        oscillator.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.2);
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
        
        // Petit vibreur sur mobile si disponible
        if (navigator.vibrate) {
            navigator.vibrate(200);
        }
    } catch(e) {
        console.log('Audio not supported');
    }
}

// Sauvegarder la session dans localStorage
function saveSession(username, role, nom) {
    const sessionData = {
        username: username,
        role: role,
        nom: nom,
        timestamp: new Date().getTime()
    };
    localStorage.setItem('hotel_session', JSON.stringify(sessionData));
}

// Charger la session depuis localStorage
function loadSession() {
    const sessionStr = localStorage.getItem('hotel_session');
    if (sessionStr) {
        try {
            const session = JSON.parse(sessionStr);
            // Vérifier si la session a moins de 7 jours
            const weekInMillis = 7 * 24 * 60 * 60 * 1000;
            if (new Date().getTime() - session.timestamp < weekInMillis) {
                return session;
            }
        } catch(e) {}
    }
    return null;
}

// Supprimer la session
function clearSession() {
    localStorage.removeItem('hotel_session');
}

// Fonction pour restaurer la session au chargement
function tryRestoreSession() {
    const session = loadSession();
    if (session) {
        // Envoyer les infos de session à Streamlit via un champ caché
        // Cette fonction sera appelée automatiquement
        window.hotelSessionData = session;
    }
}

// Appeler au chargement
tryRestoreSession();

// Notifications en temps réel via polling
let lastNotifCount = 0;
function checkNotifications() {
    // Cette fonction peut être appelée périodiquement pour vérifier les nouvelles notifications
    // Pour l'instant, le son sera joué quand une nouvelle notification apparaît
}
</script>

<style>
    /* Styles pour mobile */
    @media (max-width: 768px) {
        .stButton > button { width: 100% !important; margin-bottom: 10px; }
        .room-card { padding: 10px !important; font-size: 12px; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# GESTION DES FICHIERS
# ============================================
USERS_FILE = "utilisateurs.json"
ROOMS_FILE = "chambres.csv"
MAINTENANCE_FILE = "maintenance_tasks.csv"
NOTIFICATIONS_FILE = "notifications.json"

def play_notification_sound():
    """Joue un son de notification (JavaScript universel)"""
    # Le son sera joué via JavaScript injecté dans la page
    st.markdown("""
    <script>
    if (typeof playNotificationSound === 'function') {
        playNotificationSound();
    }
    </script>
    """, unsafe_allow_html=True)

# ============================================
# GESTION DES NOTIFICATIONS
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
    """Ajoute une notification avec option de rôle cible"""
    notifications = load_notifications()
    new_notif = {
        "id": len(notifications) + 1,
        "title": title,
        "message": message,
        "type": type_notif,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "read": False,
        "target_role": target_role  # Rôle cible (admin, receptionist, maintenance, ou None pour tous)
    }
    notifications.insert(0, new_notif)  # Ajouter au début
    # Garder seulement les 50 dernières notifications
    notifications = notifications[:50]
    save_notifications(notifications)
    
    # Jouer le son de notification
    play_notification_sound()
    
    # Afficher une notification toast (visible sur mobile et PC)
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
    """Marque une notification comme lue"""
    notifications = load_notifications()
    for notif in notifications:
        if notif["id"] == notif_id:
            notif["read"] = True
    save_notifications(notifications)
    return notifications

def mark_all_notifications_read():
    """Marque toutes les notifications comme lues"""
    notifications = load_notifications()
    for notif in notifications:
        notif["read"] = True
    save_notifications(notifications)
    return notifications

def get_unread_count():
    """Retourne le nombre de notifications non lues"""
    notifications = load_notifications()
    current_role = st.session_state.get("user_role", "")
    
    # Filtrer par rôle si connecté
    if current_role:
        user_notifications = [n for n in notifications if n.get("target_role") is None or n.get("target_role") == current_role]
        return len([n for n in user_notifications if not n["read"]])
    
    return len([n for n in notifications if not n["read"]])

def get_user_notifications():
    """Retourne les notifications pour l'utilisateur actuel"""
    notifications = load_notifications()
    current_role = st.session_state.get("user_role", "")
    
    # Filtrer par rôle
    if current_role:
        return [n for n in notifications if n.get("target_role") is None or n.get("target_role") == current_role]
    
    return notifications

# ============================================
# GESTION DES UTILISATEURS
# ============================================
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
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
    """Supprime un utilisateur"""
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
    # Effacer la session localStorage
    st.markdown("""
    <script>
    clearSession();
    </script>
    """, unsafe_allow_html=True)

# ============================================
# GESTION DES CHAMBRES
# ============================================
def load_rooms():
    if os.path.exists(ROOMS_FILE):
        df = pd.read_csv(ROOMS_FILE)
        df["numero"] = df["numero"].astype(str)
        return df
    else:
        rooms_data = []
        for i in range(1, 75): rooms_data.append({"numero": str(1000+i), "type": "Standard", "aile": "A", "statut": "Libre", "etage": 1})
        for i in range(1, 66): rooms_data.append({"numero": str(2000+i), "type": "Standard", "aile": "A", "statut": "Occupée", "etage": 2})
        for i in range(33, 66): rooms_data.append({"numero": str(3000+i), "type": "Suite", "aile": "B", "statut": "Libre", "etage": 3})
        for i in range(0, 33): rooms_data.append({"numero": str(3200+i), "type": "Deluxe", "aile": "B", "statut": "Occupée", "etage": 3})
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
    """Sauvegarde immédiate dans le fichier CSV"""
    rooms.to_csv(ROOMS_FILE, index=False)

def update_room_status(room_num, new_statut):
    """Met à jour le statut d'une chambre spécifique - SAUVEGARDE IMMÉDIATE"""
    rooms = load_rooms()
    rooms.loc[rooms["numero"] == str(room_num), "statut"] = new_statut
    save_rooms(rooms)  # Sauvegarde immédiate
    return rooms

# ============================================
# GESTION DES TÂCHES DE MAINTENANCE
# ============================================
def load_maintenance_tasks():
    if os.path.exists(MAINTENANCE_FILE):
        return pd.read_csv(MAINTENANCE_FILE)
    else:
        df = pd.DataFrame(columns=["id", "chambre", "description", "assigned_to", "statut", "date_creation", "date_completion", "created_by"])
        df.to_csv(MAINTENANCE_FILE, index=False)
        return df

def save_maintenance_tasks(tasks):
    tasks.to_csv(MAINTENANCE_FILE, index=False)

def create_maintenance_task(chambre, description, assigned_to, created_by, type_panne="Autre"):
    """Crée une tâche de maintenance"""
    tasks = load_maintenance_tasks()
    rooms = load_rooms()
    
    # Générer un nouvel ID unique
    new_id = tasks["id"].max() + 1 if len(tasks) > 0 else 1
    
    new_task = pd.DataFrame([{
        "id": new_id,
        "chambre": chambre,
        "description": description,
        "type_panne": type_panne,
        "assigned_to": assigned_to,
        "statut": "En attente",
        "date_creation": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "date_completion": "",
        "created_by": created_by
    }])
    tasks = pd.concat([tasks, new_task], ignore_index=True)
    save_maintenance_tasks(tasks)
    
    # Mettre à jour le statut de la chambre
    current_status = rooms[rooms["numero"] == str(chambre)]["statut"].values
    if len(current_status) > 0 and current_status[0] != "Occupée":
        update_room_status(chambre, "Maintenance")
    
    # Notification générale (pour tous)
    add_notification(
        "🔧 Nouvelle tâche de maintenance",
        f"Chambre {chambre}: {type_panne} - {description[:50]}",
        "warning"
    )
    
    # Notification spécifique à l'agent assigné (rôle maintenance)
    add_notification(
        "🎯 Nouvelle tâche assignée",
        f"Chambre {chambre} - {type_panne}: {description[:40]}",
        "info",
        target_role="maintenance"
    )
    
    return tasks

def update_task_status(task_id, new_statut):
    """Met à jour le statut d'une tâche"""
    tasks = load_maintenance_tasks()
    
    task = tasks[tasks["id"] == task_id].iloc[0]
    old_statut = task["statut"]
    chambre = task["chambre"]
    
    tasks.loc[tasks["id"] == task_id, "statut"] = new_statut
    
    if new_statut == "Terminé":
        tasks.loc[tasks["id"] == task_id, "date_completion"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Libérer la chambre si plus de tâches actives
        other_active = tasks[(tasks["chambre"] == chambre) & (tasks["statut"] != "Terminé")]
        if len(other_active) == 0:
            update_room_status(chambre, "Libre")
        
        # Notification de terminaison (pour tous)
        add_notification(
            "✅ Maintenance terminée",
            f"La chambre {chambre} est maintenant libre",
            "success"
        )
        
        # Notification spécifique au réceptionniste
        add_notification(
            "📢 Chambre libéré",
            f"La chambre {chambre} est prête pour le check-in",
            "success",
            target_role="receptionniste"
        )
        
    elif new_statut == "En cours":
        # Notification de début (pour tous)
        add_notification(
            "▶ Maintenance démarrée",
            f"Chambre {chambre}: {task['description'][:50]}",
            "info"
        )
    
    save_maintenance_tasks(tasks)
    return tasks

def delete_maintenance_task(task_id, add_notif=True):
    """Supprime une tâche de maintenance"""
    tasks = load_maintenance_tasks()
    # Get task info before deleting
    task = None
    if len(tasks[tasks["id"] == task_id]) > 0:
        task = tasks[tasks["id"] == task_id].iloc[0]
    tasks = tasks[tasks["id"] != task_id]
    save_maintenance_tasks(tasks)
    
    # Notification de suppression (only if add_notif is True)
    if add_notif and task is not None:
        add_notification(
            "🗑️ Maintenance supprimée",
            f"Chambre {task['chambre']}: {task['description'][:50]}",
            "error"
        )
    
    return tasks

# ============================================
# GESTION HISTORIQUE MAINTENANCE
# ============================================
def get_maintenance_history(room_num):
    """Retourne l'historique complet des maintenances d'une chambre"""
    tasks = load_maintenance_tasks()
    # Convertir en entier pour la comparaison car le CSV stocke chambre comme int
    try:
        room_num_int = int(room_num)
        room_tasks = tasks[tasks["chambre"] == room_num_int].copy()
    except:
        room_tasks = tasks[tasks["chambre"] == str(room_num)].copy()
    room_tasks = room_tasks.sort_values("date_creation", ascending=False)
    return room_tasks

def get_maintenance_count(room_num):
    """Compte le nombre de maintenances terminées pour une chambre"""
    tasks = load_maintenance_tasks()
    # Convertir en entier pour la comparaison car le CSV stocke chambre comme int
    try:
        room_num_int = int(room_num)
        count = len(tasks[(tasks["chambre"] == room_num_int) & (tasks["statut"] == "Terminé")])
    except:
        count = len(tasks[(tasks["chambre"] == str(room_num)) & (tasks["statut"] == "Terminé")])
    return count

def delete_maintenance_task(task_id):
    """Supprime une tâche de maintenance"""
    tasks = load_maintenance_tasks()
    tasks = tasks[tasks["id"] != task_id]
    save_maintenance_tasks(tasks)
    return tasks

def clear_maintenance_history(room_num):
    """Supprime toutes les maintenances d'une chambre"""
    tasks = load_maintenance_tasks()
    # Convertir en entier pour la comparaison
    try:
        room_num_int = int(room_num)
        tasks = tasks[tasks["chambre"] != room_num_int]
    except:
        tasks = tasks[tasks["chambre"] != str(room_num)]
    save_maintenance_tasks(tasks)
    # Remettre le statut de la chambre à Libre
    update_room_status(room_num, "Libre")
    return tasks

def cancel_maintenance(task_id):
    """Annule une maintenance (supprime la tâche)"""
    return delete_maintenance_task(task_id)

def is_problem_room(room_num):
    """Vérifie si une chambre a eu 3 maintenances ou plus (classée comme problème)"""
    return get_maintenance_count(room_num) >= 3

# ============================================
# CONFIGURATION PAGE
# ============================================
st.set_page_config(page_title="Hotel Mediterranee", page_icon="🏨", layout="wide")

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
""", unsafe_allow_html=True)

# ============================================
# PAGE DE LOGIN
# ============================================
def show_login():
    # Script pour récupérer la session sauvegardée
    st.markdown("""
    <script>
    // Fonction pour restaurer automatiquement la session
    function getStoredSession() {
        const sessionStr = localStorage.getItem('hotel_session');
        if (sessionStr) {
            try {
                const session = JSON.parse(sessionStr);
                const weekInMillis = 7 * 24 * 60 * 60 * 1000;
                if (new Date().getTime() - session.timestamp < weekInMillis) {
                    return session;
                }
            } catch(e) {}
        }
        return null;
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Vérifier si une session est sauvegardée et proposer connexion automatique
    stored_session = None
    
    st.markdown("<div style='max-width: 400px; margin: 100px auto; padding: 40px; background: #1e293b; border-radius: 20px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>🏨 Hotel Mediterranee</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #CC6D3D;'>Connexion</h3>", unsafe_allow_html=True)
    
    # Bouton pour connexion automatique (si session sauvegardée)
    if st.button("🔄 Connexion automatique", key="auto_login"):
        st.markdown("""
        <script>
        const session = getStoredSession();
        if (session) {
            // Sauvegarder dans un champ pour Python
            window.sessionToRestore = session;
            // Trigger rerun
            window.location.reload();
        }
        </script>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    username = st.text_input("Nom d'utilisateur", key="login_user")
    password = st.text_input("Mot de passe", type="password", key="login_pass")
    
    # Case "Se souvenir de moi"
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
                
                # Sauvegarder dans localStorage si "Se souvenir de moi" est coché
                if remember_me:
                    st.markdown(f"""
                    <script>
                    saveSession("{username}", "{user['role']}", "{user['nom']}");
                    </script>
                    """, unsafe_allow_html=True)
                
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")
    
    st.markdown("---")
    
    # Message d'information
    st.info("💡 Astuce: Cochez \"Se souvenir de moi\" pour rester connecté pendant 7 jours")
   
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# PAGE PRINCIPALE
# ============================================
def show_main_app():
    rooms = load_rooms()
    
    with st.sidebar:
        st.markdown("<div style='text-align: center; padding: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("<h2>🏨 Mediterranee</h2>", unsafe_allow_html=True)
        st.markdown("<p>Hammamet</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Statistiques rapides
        st.markdown("### 📊 Aperçu")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            libre = len(rooms[rooms["statut"] == "Libre"])
            st.metric("Libres", libre)
        with col_s2:
            occupees = len(rooms[rooms["statut"] == "Occupée"])
            st.metric("Occupées", occupees)
        
        maintenance_count = len(rooms[rooms["statut"] == "Maintenance"])
        st.metric("Maintenance", maintenance_count)
        
        st.markdown("---")
        
        # Notifications
        st.markdown("### 🔔 Notifications")
        unread_count = get_unread_count()
        if unread_count > 0:
            st.warning(f"🔴 {unread_count} non lue(s)")
        else:
            st.success("✓ Toutes lues")
        
        # Bouton pour marquer tout comme lu (visible pour admin)
        if is_admin() and unread_count > 0:
            if st.button("✅ Tout marquer comme lu", use_container_width=True):
                mark_all_notifications_read()
                st.success("Toutes les notifications sont marquées comme lues!")
                st.rerun()
        
        with st.expander("Voir les notifications"):
            notifications = get_user_notifications()
            if len(notifications) > 0:
                for notif in notifications[:10]:  # Afficher les 10 dernières
                    notif_style = "background: #2d3748; padding: 10px; margin: 5px 0; border-radius: 8px;"
                    if notif["type"] == "success":
                        notif_style += "border-left: 4px solid #10b981;"
                    elif notif["type"] == "warning":
                        notif_style += "border-left: 4px solid #f59e0b;"
                    elif notif["type"] == "error":
                        notif_style += "border-left: 4px solid #ef4444;"
                    else:
                        notif_style += "border-left: 4px solid #3b82f6;"
                    
                    # Indicateur de notification non lue
                    unread_indicator = " 🔴" if not notif["read"] else ""
                    
                    st.markdown(f"""
                    <div style="{notif_style}">
                        <strong>{notif['title']}{unread_indicator}</strong><br>
                        <small>{notif['message']}</small><br>
                        <small style="color: #94a3b8;">{notif['date']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Bouton pour marquer comme lu (si non lue)
                    if not notif["read"]:
                        if st.button(f"✓ Marquer comme lu", key=f"read_{notif['id']}"):
                            mark_notification_read(notif["id"])
                            st.rerun()
            else:
                st.info("Aucune notification")
        
        st.markdown("---")
        
        # Informations utilisateur
        st.markdown(f"**Utilisateur:** {st.session_state.get('user_nom', 'Utilisateur')}")
        st.markdown(f"**Rôle:** {st.session_state.get('user_role', '').capitalize()}")
        
        if st.button("🚪 Déconnexion", use_container_width=True):
            logout()
            st.rerun()
        
        st.markdown("---")
        st.caption("🎓 PFE - Hotel Mediterranee")
    
    st.title("🏨 Hotel Mediterranee Hammamet")
    
    # Navigation par onglets
    if is_maintenance():
        tab1, tab2 = st.tabs(["🏠 Dashboard", "🔧 Mes Tâches"])
    else:
        tab_dash, tab_rooms, tab_maint, tab_users = st.tabs([
            "🏠 Dashboard", "🛏️ Chambres", "🔧 Maintenance", "👤 Utilisateurs"
        ])
    
    # ========== DASHBOARD ==========
    with tab1 if is_maintenance() else tab_dash:
        st.subheader("📊 Tableau de Bord")
        
        # Statistiques
        col_k1, col_k2, col_k3, col_k4 = st.columns(4)
        with col_k1:
            st.metric("Total Chambres", len(rooms))
        with col_k2:
            st.metric("Libres", len(rooms[rooms["statut"] == "Libre"]))
        with col_k3:
            st.metric("Occupées", len(rooms[rooms["statut"] == "Occupée"]))
        with col_k4:
            st.metric("Maintenance", len(rooms[rooms["statut"] == "Maintenance"]))
        
        st.markdown("---")
        
        # Chambres rapides
        st.subheader("🛏️ État des Chambres")
        
        # Filtres
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            aile_filter = st.selectbox("Aile", ["Tous", "A", "B"])
        with col_f2:
            statut_filter = st.selectbox("Statut", ["Tous", "Libre", "Occupée", "Maintenance"])
        with col_f3:
            etage_filter = st.selectbox("Étage", ["Tous", 0, 1, 2, 3])
        
        filtered = rooms.copy()
        if aile_filter != "Tous":
            filtered = filtered[filtered["aile"] == aile_filter]
        if statut_filter != "Tous":
            filtered = filtered[filtered["statut"] == statut_filter]
        if etage_filter != "Tous":
            filtered = filtered[filtered["etage"] == etage_filter]
        
        st.markdown(f"**{len(filtered)}/{len(rooms)} chambres**")
        
        # Affichage des cartes
        cols = st.columns(5)
        for i, row in filtered.head(20).iterrows():
            with cols[i % 5]:
                emoji = "✅" if row["statut"] == "Libre" else "🔒" if row["statut"] == "Occupée" else "🔧"
                st.markdown(f"""
                <div class="room-card {row['statut'].lower()}">
                    <b>🚪 {row['numero']}</b><br>
                    <span class="status-badge {row['statut'].lower()}">{emoji} {row['statut']}</span><br>
                    <small>{row['type']}</small>
                </div>
                """, unsafe_allow_html=True)
    
    # ========== TAB CHAMBRES (pour admin/réception) ==========
    if not is_maintenance():
        with tab_rooms:
            st.subheader("🛏️ Gestion des Chambres")
            
            # Filtres
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
            
            # Affichage avec boutons de changement de statut
            for i, row in filtered.iterrows():
                # Compter les maintenances et vérifier si problème
                maint_count = get_maintenance_count(row['numero'])
                is_problem = is_problem_room(row['numero'])
                
                problem_indicator = " ⚠️" if is_problem else ""
                with st.expander(f"🚪 Chambre {row['numero']} - {row['type']} ({row['aile']}){problem_indicator}"):
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.markdown(f"**Statut actuel:** {row['statut']}")
                        st.markdown(f"**Étage:** {row['etage']}")
                        st.markdown(f"**Aile:** {row['aile']}")
                        # Afficher le nombre de maintenances
                        st.markdown(f"**Maintenances:** {maint_count}")
                        if is_problem:
                            st.error("⚠️ Cette chambre est classé comme PROBLÈME (3+ maintenances)")
                    with col_r2:
                        st.markdown("**Changer le statut:**")
                        
                        # Boutons pour changer le statut
                        col_b1, col_b2, col_b3 = st.columns(3)
                        
                        with col_b1:
                            if st.button(f"✅ Libre", key=f"libre_{row['numero']}"):
                                update_room_status(row["numero"], "Libre")
                                st.success(f"Chambre {row['numero']} → Libre")
                                st.rerun()
                        
                        with col_b2:
                            if st.button(f"🔒 Occupée", key=f"occup_{row['numero']}"):
                                update_room_status(row["numero"], "Occupée")
                                st.success(f"Chambre {row['numero']} → Occupée")
                                st.rerun()
                        
                        with col_b3:
                            if st.button(f"🔧 Maintenance", key=f"maint_{row['numero']}"):
                                update_room_status(row["numero"], "Maintenance")
                                st.warning(f"Chambre {row['numero']} → Maintenance")
                                st.rerun()
                    
                    # Afficher l'historique de maintenance
                    st.markdown("---")
                    st.markdown("**📋 Historique de maintenance:**")
                    
                    if st.button(f"🔍 Voir l'historique", key=f"history_{row['numero']}"):
                        history = get_maintenance_history(row['numero'])
                        if len(history) > 0:
                            for _, task in history.iterrows():
                                type_panne = task.get('type_panne', 'Autre') if 'type_panne' in task.index else 'Autre'
                                status_icon = "🟢" if task['statut'] == "Terminé" else "🔵" if task['statut'] == "En cours" else "🟡"
                                with st.expander(f"#{task['id']} - {task['date_creation']}"):
                                    st.markdown(f"**Statut:** {status_icon} {task['statut']}")
                                    st.markdown(f"**Type:** {type_panne}")
                                    st.markdown(f"**Description:** {task['description']}")
                                    st.markdown(f"**Assigné à:** {task['assigned_to']}")
                                    if task['date_completion']:
                                        st.markdown(f"**Terminé le:** {task['date_completion']}")
                                    # Bouton pour annuler/supprimer cette maintenance
                                    if st.button(f"❌ Annuler cette maintenance", key=f"cancel_{task['id']}_{row['numero']}"):
                                        cancel_maintenance(task['id'])
                                        st.warning(f"Maintenance #{task['id']} annulée!")
                                        st.rerun()
                        else:
                            st.info("Aucune maintenance enregistrée")
                    
                    # Bouton pour effacer tout l'historique de cette chambre
                    if maint_count > 0:
                        st.markdown("---")
                        if st.button(f"🗑️ Effacer tout l'historique", key=f"clear_{row['numero']}"):
                            clear_maintenance_history(row['numero'])
                            st.success(f"Historique de la chambre {row['numero']} effacé!")
                            st.rerun()
            
            with st.expander("📋 Détail complet"):
                st.dataframe(filtered)
    
    # ========== TAB MAINTENANCE ==========
    with tab_maint if not is_maintenance() else tab2:
        st.subheader("🔧 Tâches de Maintenance")
        
        # Pour l'agent de maintenance : afficher uniquement ses propres tâches
        if is_maintenance():
            current_user = st.session_state.get("user_nom", "")
            tasks = load_maintenance_tasks()
            
            # Filtrer uniquement les tâches assignées à cet agent
            my_tasks = tasks[tasks["assigned_to"] == current_user].copy()
            
            # Statistiques personnelles
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                total = len(my_tasks)
                st.metric("Total tâches", total)
            with col_stat2:
                en_attente = len(my_tasks[my_tasks["statut"] == "En attente"])
                st.metric("En attente", en_attente)
            with col_stat3:
                en_cours = len(my_tasks[my_tasks["statut"] == "En cours"])
                st.metric("En cours", en_cours)
            
            st.markdown("---")
            
            # Afficher les tâches de l'agent
            if len(my_tasks) > 0:
                for idx, task in my_tasks.iterrows():
                    status_icon = "🟡" if task["statut"] == "En attente" else "🔵" if task["statut"] == "En cours" else "🟢"
                    type_panne = task.get('type_panne', 'Autre') if 'type_panne' in task.index else 'Autre'
                    
                    with st.expander(f"{status_icon} #{task['id']} - Chambre {task['chambre']} - {task['statut']}"):
                        st.markdown(f"**🔧 Type de panne:** {type_panne}")
                        st.markdown(f"**📝 Description:** {task['description']}")
                        st.markdown(f"**👤 Assigné par:** {task['created_by']}")
                        st.markdown(f"**📅 Créée le:** {task['date_creation']}")
                        if task["date_completion"]:
                            st.markdown(f"**✅ Terminée le:** {task['date_completion']}")
                        
                        # Boutons d'action pour l'agent
                        col_act1, col_act2 = st.columns(2)
                        
                        with col_act1:
                            if task["statut"] == "En attente":
                                if st.button(f"▶ Commencer", key=f"start_{task['id']}_{idx}"):
                                    update_task_status(task["id"], "En cours")
                                    st.rerun()
                            elif task["statut"] == "En cours":
                                st.success("🔧 En cours de traitement...")
                        
                        with col_act2:
                            if task["statut"] != "Terminé":
                                if st.button(f"✓ Terminer", key=f"end_{task['id']}_{idx}"):
                                    update_task_status(task["id"], "Terminé")
                                    st.success("Tâche terminée!")
                                    st.rerun()
            else:
                st.info("Aucune tâche assignée à votre nom. 🎉")
                st.markdown("**Vous n'avez pas de tâches de maintenance en attente.**")
            
            # Bouton pour voir les notifications
            st.markdown("---")
            st.markdown("### 🔔 Vos Notifications")
            if st.button("🔄 Actualiser les notifications"):
                st.rerun()
        
        else:
            # Pour admin/réception : afficher toutes les tâches avec possibilité de créer
            
            # Créer une nouvelle tâche
            with st.expander("➕ Créer une tâche"):
                with st.form("maintenance_form"):
                    col_m1, col_m2 = st.columns(2)
                    with col_m1:
                        maint_chambre = st.selectbox("Chambre", rooms["numero"].tolist())
                        maint_type_panne = st.selectbox("Type de panne", [
                            "Plomberie", "Électricité", "Climatisation", 
                            "Meuble", "Serrure", "Écran/TV", "WiFi", "Autre"
                        ])
                        maint_desc = st.text_area("Description du problème")
                    with col_m2:
                        users = load_users()
                        agents = [u["nom"] for u in users.values() if u["role"] == "maintenance"]
                        maint_agent = st.selectbox("Assigner à", agents)
                    
                    submit_maint = st.form_submit_button("Créer la tâche")
                    
                    if submit_maint and maint_desc and maint_agent:
                        create_maintenance_task(
                            maint_chambre,
                            maint_desc,
                            maint_agent,
                            st.session_state.get("user_nom"),
                            maint_type_panne
                        )
                        st.success("✅ Tâche créée!")
                        st.rerun()
            
            st.markdown("---")
            
            # Liste des tâches
            tasks = load_maintenance_tasks()
            
            col_mf1, col_mf2 = st.columns(2)
            with col_mf1:
                filter_statut = st.selectbox("Filtrer par statut", ["Tous", "En attente", "En cours", "Terminé"])
            with col_mf2:
                filter_agent = st.selectbox("Filtrer par agent", ["Tous"] + [u["nom"] for u in load_users().values() if u["role"] == "maintenance"])
            
            filtered_tasks = tasks.copy()
            if filter_statut != "Tous":
                filtered_tasks = filtered_tasks[filtered_tasks["statut"] == filter_statut]
            if filter_agent != "Tous":
                filtered_tasks = filtered_tasks[filtered_tasks["assigned_to"] == filter_agent]
            
            if len(filtered_tasks) > 0:
                for idx, task in filtered_tasks.iterrows():
                    status_icon = "🟡" if task["statut"] == "En attente" else "🔵" if task["statut"] == "En cours" else "🟢"
                    type_panne = task.get('type_panne', 'Autre') if 'type_panne' in task.index else 'Autre'
                    with st.expander(f"{status_icon} #{task['id']} - Chambre {task['chambre']} - {task['statut']}"):
                        st.markdown(f"**Type de panne:** {type_panne}")
                        st.markdown(f"**Description:** {task['description']}")
                        st.markdown(f"**Assigné à:** {task['assigned_to']}")
                        st.markdown(f"**Créée le:** {task['date_creation']}")
                        if task["date_completion"]:
                            st.markdown(f"**Terminée le:** {task['date_completion']}")
                        
                        # Boutons d'action
                        col_actions1, col_actions2, col_actions3 = st.columns(3)
                        
                        with col_actions1:
                            if task["statut"] != "Terminé":
                                if st.button(f"▶ Commencer", key=f"start_{task['id']}_{idx}"):
                                    update_task_status(task["id"], "En cours")
                                    st.rerun()
                        
                        with col_actions2:
                            if task["statut"] != "Terminé":
                                if st.button(f"✓ Terminer", key=f"end_{task['id']}_{idx}"):
                                    update_task_status(task["id"], "Terminé")
                                    st.success("Tâche terminée!")
                                    st.rerun()
                        
                        with col_actions3:
                            if st.button(f"🗑️ Supprimer", key=f"delete_{task['id']}_{idx}", type="primary"):
                                delete_maintenance_task(task['id'])
                                st.warning(f"Tâche #{task['id']} supprimée!")
                                st.rerun()
            else:
                st.info("Aucune tâche")
    
    # ========== USER MANAGEMENT (admin only) ==========
    if is_admin() and not is_maintenance():
        with tab_users:
            st.subheader("👤 Gestion des Utilisateurs")
            
            users = load_users()
            
            st.markdown("#### Utilisateurs existants:")
            col_u1, col_u2 = st.columns(2)
            
            admin_users = [(k, v) for k, v in users.items() if v["role"] == "admin"]
            other_users = [(k, v) for k, v in users.items() if v["role"] != "admin"]
            
            with col_u1:
                st.markdown("**Administrateurs:**")
                for username, user_data in admin_users:
                    st.markdown(f"- {username} ({user_data['nom']})")
            
            with col_u2:
                st.markdown("**Autres utilisateurs:**")
                for username, user_data in other_users:
                    col_del, _ = st.columns([3, 1])
                    with col_del:
                        st.markdown(f"- {username} ({user_data['nom']}) - {user_data['role']}")
            
            st.markdown("---")
            
            # Section supprimer un utilisateur
            with st.expander("🗑️ Supprimer un utilisateur"):
                users_list = list(users.keys())
                user_to_delete = st.selectbox("Sélectionner l'utilisateur à supprimer", users_list)
                
                if st.button("🗑️ Supprimer cet utilisateur", type="primary"):
                    if user_to_delete == "admin":
                        st.error("❌ Impossible de supprimer le compte admin!")
                    elif user_to_delete == st.session_state.get("username"):
                        st.error("❌ Vous ne pouvez pas supprimer votre propre compte!")
                    else:
                        delete_user(user_to_delete)
                        st.success(f"✅ Utilisateur {user_to_delete} supprimé!")
                        st.rerun()
                
                st.warning("⚠️ Attention: Cette action est irréversible!")
            
            with st.expander("➕ Créer un utilisateur"):
                with st.form("create_user_form"):
                    new_username = st.text_input("Nom d'utilisateur")
                    new_nom = st.text_input("Nom complet")
                    new_password = st.text_input("Mot de passe", type="password")
                    new_role = st.selectbox("Rôle", ["receptionniste", "maintenance"])
                    
                    submit_user = st.form_submit_button("Créer")
                    
                    if submit_user and new_username and new_password and new_nom:
                        users[new_username] = {
                            "password": hash_password(new_password),
                            "role": new_role,
                            "nom": new_nom
                        }
                        save_users(users)
                        st.success(f"✅ Utilisateur {new_username} créé!")
                        st.rerun()

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    # Essayer de restaurer la session depuis localStorage au premier chargement
    if not st.session_state.get("logged_in", False):
        # Le JavaScript essaie de restaurer la session
        # On affiche le login mais on peut aussi restaurer depuis Python si on avait un champ caché
        show_login()
    else:
        show_main_app()

