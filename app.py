import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import hashlib
import base64
from dotenv import load_dotenv
import os
load_dotenv()

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
# SESSION PERSISTANCE USING QUERY PARAMS
# ============================================
def check_and_restore_session():
    """Check for session in query params and restore if valid"""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    # Check if we have query params with session data
    query_params = st.query_params
    
    if "session" in query_params and not st.session_state.get("logged_in", False):
        try:
            session_data = json.loads(query_params["session"])
            username = session_data.get("username", "")
            users = load_users()
            
            if username in users:
                # Validate session is not expired (7 days)
                session_time = session_data.get("timestamp", 0)
                current_time = datetime.now().timestamp()
                week_in_seconds = 7 * 24 * 60 * 60
                
                if current_time - session_time < week_in_seconds:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["user_role"] = users[username]["role"]
                    st.session_state["user_nom"] = users[username]["nom"]
                    
                    # Clear the query param after successful restore
                    st.query_params.clear()
                    return True
        except Exception as e:
            print(f"Session restore error: {e}")
    
    return False

# Try to restore session at startup
check_and_restore_session()

# ============================================
# JAVASCRIPT FOR SESSION PERSISTANCE AND NOTIFICATIONS
# ============================================
st.markdown("""
<script>
// =======================
// SESSION PERSISTENCE
// =======================

// Save session to URL query params (survives refresh and sharing)
function saveSessionToURL(username, role, nom) {
    const sessionData = {
        username: username,
        role: role,
        nom: nom,
        timestamp: Math.floor(Date.now() / 1000)
    };
    
    // Use Streamlit's setQueryParams via the native method
    if (window.Streamlit) {
        const encoded = btoa(encodeURIComponent(JSON.stringify(sessionData)));
        window.Streamlit.setQueryParams({session: encoded});
    }
}

// Clear session from URL
function clearSessionFromURL() {
    if (window.Streamlit) {
        window.Streamlit.setQueryParams({});
    }
}

// =======================
// NOTIFICATION SOUND
// =======================

function playNotificationSound() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        // Pleasant notification sound
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(1200, audioContext.currentTime + 0.1);
        oscillator.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.2);
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
        
        // Vibration on mobile if available
        if (navigator.vibrate) {
            navigator.vibrate(200);
        }
    } catch(e) {
        console.log('Audio not supported');
    }
}

// =======================
// REAL-TIME NOTIFICATIONS VIA POLLING
// =======================

let notificationCheckInterval = null;
let lastNotificationCount = 0;
let lastNotificationTime = 0;

function startNotificationPolling() {
    if (notificationCheckInterval) return;
    
    notificationCheckInterval = setInterval(async () => {
        try {
            // Poll notifications.json directly using fetch
            const response = await fetch('notifications.json?t=' + Date.now());
            if (!response.ok) return;
            
            const notifications = await response.json();
            
            // Get current user from page data
            const notifCountElem = document.getElementById('notification-count-data');
            if (!notifCountElem) return;
            
            const currentCount = parseInt(notifCountElem.getAttribute('data-count') || '0');
            const currentTime = parseInt(notifCountElem.getAttribute('data-time') || '0');
            
            // Check for new notifications
            if (notifications.length > currentCount || (currentTime > lastNotificationTime && currentTime > 0)) {
                playNotificationSound();
                showNewNotificationAlert();
                lastNotificationCount = notifications.length;
                lastNotificationTime = currentTime;
            }
        } catch(e) {
            console.log('Notification polling error:', e);
        }
    }, 3000); // Check every 3 seconds
}

function showNewNotificationAlert() {
    let alertDiv = document.getElementById('new-notif-alert');
    if (!alertDiv) {
        alertDiv = document.createElement('div');
        alertDiv.id = 'new-notif-alert';
        alertDiv.style.cssText = 'position:fixed;top:20px;right:20px;background:#10b981;color:white;padding:15px 25px;border-radius:10px;z-index:9999;box-shadow:0 4px 12px rgba(0,0,0,0.3);animation:slideIn 0.3s ease;cursor:pointer;';
        alertDiv.innerHTML = '🔔 <strong>Nouvelle notification!</strong>';
        alertDiv.onclick = function() { this.remove(); };
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            if (alertDiv) alertDiv.remove();
        }, 4000);
    }
}

// Start polling when page loads
if (document.readyState === 'complete') {
    startNotificationPolling();
} else {
    window.addEventListener('load', startNotificationPolling);
}
</script>

<style>
    @media (max-width: 768px) {
        .stButton > button { width: 100% !important; margin-bottom: 10px; }
        .room-card { padding: 10px !important; font-size: 12px; }
    }
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    .live-notification-badge {
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
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# GESTION DES FICHIERS (CONFIGURABLE VIA .env)
# ============================================
DATA_DIR = os.getenv('DATA_DIR', '.')
USERS_FILE = os.path.join(DATA_DIR, 'utilisateurs.json')
ROOMS_FILE = os.path.join(DATA_DIR, 'chambres.csv')
MAINTENANCE_FILE = os.path.join(DATA_DIR, 'maintenance_tasks.csv')
NOTIFICATIONS_FILE = os.path.join(DATA_DIR, 'notifications.json')

def play_notification_sound():
    """Joue un son de notification (JavaScript universel)"""
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
    
    if current_role:
        user_notifications = [n for n in notifications if n.get("target_role") is None or n.get("target_role") == current_role]
        return len([n for n in user_notifications if not n["read"]])
    
    return len([n for n in notifications if not n["read"]])

def get_user_notifications():
    """Retourne les notifications pour l'utilisateur actuel"""
    notifications = load_notifications()
    current_role = st.session_state.get("user_role", "")
    
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
    # Clear query params on logout
    st.query_params.clear()

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
    save_rooms(rooms)
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
    
    current_status = rooms[rooms["numero"] == str(chambre)]["statut"].values
    if len(current_status) > 0 and current_status[0] != "Occupée":
        update_room_status(chambre, "Maintenance")
    
    add_notification(
        "🔧 Nouvelle tâche de maintenance",
        f"Chambre {chambre}: {type_panne} - {description[:50]}",
        "warning"
    )
    
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
        
        other_active = tasks[(tasks["chambre"] == chambre) & (tasks["statut"] != "Terminé")]
        if len(other_active) == 0:
            update_room_status(chambre, "Libre")
        
        add_notification(
            "✅ Maintenance terminée",
            f"La chambre {chambre} est maintenant libre",
            "success"
        )
        
        add_notification(
            "📢 Chambre libéré",
            f"La chambre {chambre} est prête pour le check-in",
            "success",
            target_role="receptionniste"
        )
        
    elif new_statut == "En cours":
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
    task = None
    if len(tasks[tasks["id"] == task_id]) > 0:
        task = tasks[tasks["id"] == task_id].iloc[0]
    tasks = tasks[tasks["id"] != task_id]
    save_maintenance_tasks(tasks)
    
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
    try:
        room_num_int = int(room_num)
        count = len(tasks[(tasks["chambre"] == room_num_int) & (tasks["statut"] == "Terminé")])
    except:
        count = len(tasks[(tasks["chambre"] == str(room_num)) & (tasks["statut"] == "Terminé")])
    return count

def delete_maintenance_task_by_id(task_id):
    """Supprime une tâche de maintenance"""
    tasks = load_maintenance_tasks()
    tasks = tasks[tasks["id"] != task_id]
    save_maintenance_tasks(tasks)
    return tasks

def clear_maintenance_history(room_num):
    """Supprime toutes les maintenances d'une chambre"""
    tasks = load_maintenance_tasks()
    try:
        room_num_int = int(room_num)
        tasks = tasks[tasks["chambre"] != room_num_int]
    except:
        tasks = tasks[tasks["chambre"] != str(room_num)]
    save_maintenance_tasks(tasks)
    update_room_status(room_num, "Libre")
    return tasks

def cancel_maintenance(task_id):
    """Annule une maintenance (supprime la tâche)"""
    return delete_maintenance_task_by_id(task_id)

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
    st.markdown("<div style='max-width: 400px; margin: 100px auto; padding: 40px; background: #1e293b; border-radius: 20px; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>🏨 Hotel Mediterranee</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #CC6D3D;'>Connexion</h3>", unsafe_allow_html=True)
    
    # Auto-restore session from query params if available
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
                    # Save session to query params using Streamlit's native method
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
    
    # Ajouter l'élément de données pour les notifications en temps réel
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
            libre = len(rooms[rooms["statut"] == "Libre"])
            st.metric("Libres", libre)
        with col_s2:
            occupees = len(rooms[rooms["statut"] == "Occupée"])
            st.metric("Occupées", occupees)
        
        maintenance_count = len(rooms[rooms["statut"] == "Maintenance"])
        st.metric("Maintenance", maintenance_count)
        
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
                st.success("Toutes les notifications sont marquées comme lues!")
                st.rerun()
        
        with st.expander("Voir les notifications"):
            notifications = get_user_notifications()
            if len(notifications) > 0:
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
                        if st.button(f"✓ Marquer comme lu", key=f"read_{notif['id']}"):
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
    
    if is_maintenance():
        tab1, tab2 = st.tabs(["🏠 Dashboard", "🔧 Mes Tâches"])
    else:
        tab_dash, tab_rooms, tab_maint, tab_users = st.tabs([
            "🏠 Dashboard", "🛏️ Chambres", "🔧 Maintenance", "👤 Utilisateurs"
        ])
    
    # ========== DASHBOARD ==========
    with tab1 if is_maintenance() else tab_dash:
        st.subheader("📊 Tableau de Bord")
        
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
        
        st.subheader("🛏️ État des Chambres")
        
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
    
    # ========== TAB CHAMBRES ==========
    if not is_maintenance():
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
                is_problem = is_problem_room(row['numero'])
                
                problem_indicator = " ⚠️" if is_problem else ""
                with st.expander(f"🚪 Chambre {row['numero']} - {row['type']} ({row['aile']}){problem_indicator}"):
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.markdown(f"**Statut actuel:** {row['statut']}")
                        st.markdown(f"**Étage:** {row['etage']}")
                        st.markdown(f"**Aile:** {row['aile']}")
                        st.markdown(f"**Maintenances:** {maint_count}")
                        if is_problem:
                            st.error("⚠️ Cette chambre est classé comme PROBLÈME (3+ maintenances)")
                    with col_r2:
                        st.markdown("**Changer le statut:**")
                        
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
                                    if st.button(f"❌ Annuler cette maintenance", key=f"cancel_{task['id']}_{row['numero']}"):
                                        cancel_maintenance(task['id'])
                                        st.warning(f"Maintenance #{task['id']} annulée!")
                                        st.rerun()
                        else:
                            st.info("Aucune maintenance enregistrée")
                    
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
        
        if is_maintenance():
            current_user = st.session_state.get("user_nom", "")
            tasks = load_maintenance_tasks()
            
            my_tasks = tasks[tasks["assigned_to"] == current_user].copy()
            
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
            
            st.markdown("---")
            st.markdown("### 🔔 Vos Notifications")
            if st.button("🔄 Actualiser les notifications"):
                st.rerun()
        
        else:
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
    
    # ========== USER MANAGEMENT ==========
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
                    st.markdown(f"- {username} ({user_data['nom']}) - {user_data['role']}")
            
            st.markdown("---")
            
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
    
    if not st.session_state.get("logged_in", False):
        show_login()
    else:
        show_main_app()
