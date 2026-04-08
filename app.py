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
PANNES_FILE = os.path.join(DATA_DIR, 'pannes.csv')
COMPOSANTS_FILE = os.path.join(DATA_DIR, 'composants_chambres.csv')
RAPPORTS_FILE = os.path.join(DATA_DIR, 'rapports_taches.csv')
RECLAMATIONS_FILE = os.path.join(DATA_DIR, 'reclamations.csv')

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
# GESTION DES PANNES
# ============================================
def load_pannes():
    """Charge la liste des types de pannes"""
    if os.path.exists(PANNES_FILE):
        return pd.read_csv(PANNES_FILE)
    else:
        # Données par défaut
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
            "date_creation": ["2024-01-01"]*10
        }
        df = pd.DataFrame(pannes_data)
        df.to_csv(PANNES_FILE, index=False)
        return df

def save_pannes(pannes):
    """Sauvegarde les pannes"""
    pannes.to_csv(PANNES_FILE, index=False)

def add_panne(nom_panne, description, priorite):
    """Ajoute un nouveau type de panne"""
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
    """Charge les composants des chambres"""
    if os.path.exists(COMPOSANTS_FILE):
        return pd.read_csv(COMPOSANTS_FILE)
    else:
        df = pd.DataFrame(columns=["id", "chambre", "composant_principal", "sous_composant", "statut", "date_installation", "derniere_maintenance"])
        df.to_csv(COMPOSANTS_FILE, index=False)
        return df

def save_composants(composants):
    """Sauvegarde les composants"""
    composants.to_csv(COMPOSANTS_FILE, index=False)

def add_composant(chambre, composant_principal, sous_composant, statut="Bon"):
    """Ajoute un composant de chambre"""
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
    """Met à jour le statut d'un composant"""
    composants = load_composants()
    composants.loc[composants["id"] == composant_id, "statut"] = new_status
    composants.loc[composants["id"] == composant_id, "derniere_maintenance"] = datetime.now().strftime("%Y-%m-%d")
    save_composants(composants)
    return composants

def delete_composant(composant_id):
    """Supprime un composant"""
    composants = load_composants()
    composants = composants[composants["id"] != composant_id]
    save_composants(composants)
    return composants

# ============================================
# GESTION DES RAPPORTS DE TÂCHES
# ============================================
def load_rapports():
    """Charge les rapports de tâches"""
    if os.path.exists(RAPPORTS_FILE):
        return pd.read_csv(RAPPORTS_FILE)
    else:
        df = pd.DataFrame(columns=["task_id", "agent", "rapport", "duree_travail_minutes", "date_rapport", "pieces_utilisees", "notes_agent"])
        df.to_csv(RAPPORTS_FILE, index=False)
        return df

def save_rapports(rapports):
    """Sauvegarde les rapports"""
    rapports.to_csv(RAPPORTS_FILE, index=False)

def add_rapport(task_id, agent, rapport, duree_travail, pieces_utilisees="", notes=""):
    """Ajoute un rapport de tâche"""
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
    """Obtient l'historique des tâches d'un agent"""
    tasks = load_maintenance_tasks()
    agent_tasks = tasks[tasks["assigned_to"] == agent_name].copy()
    return {
        "total": len(agent_tasks),
        "terminees": len(agent_tasks[agent_tasks["statut"] == "Terminé"]),
        "en_cours": len(agent_tasks[agent_tasks["statut"] == "En cours"]),
        "en_attente": len(agent_tasks[agent_tasks["statut"] == "En attente"])
    }

# ============================================
# GESTION DES RÉCLAMATIONS (Réceptionniste)
# ============================================
def load_reclamations():
    """Charge les réclamations de pannes"""
    if os.path.exists(RECLAMATIONS_FILE):
        return pd.read_csv(RECLAMATIONS_FILE)
    else:
        df = pd.DataFrame(columns=["id", "chambre", "type_panne", "description", "date_declaration", "statut", "creé_par"])
        df.to_csv(RECLAMATIONS_FILE, index=False)
        return df

def save_reclamations(reclamations):
    """Sauvegarde les réclamations"""
    reclamations.to_csv(RECLAMATIONS_FILE, index=False)

def add_reclamation(chambre, type_panne, description, created_by):
    """Ajoute une réclamation de panne (par réceptionniste)"""
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
    """Met à jour le statut d'une réclamation"""
    reclamations = load_reclamations()
    reclamations.loc[reclamations["id"] == reclamation_id, "statut"] = new_status
    save_reclamations(reclamations)
    return reclamations

def delete_reclamation(reclamation_id):
    """Supprime une réclamation"""
    reclamations = load_reclamations()
    reclamations = reclamations[reclamations["id"] != reclamation_id]
    save_reclamations(reclamations)
    return reclamations

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

def add_room(numero, type_room, aile, etage, statut="Libre"):
    """Ajoute une nouvelle chambre"""
    rooms = load_rooms()
    if str(numero) in rooms["numero"].values:
        return False, "Cette chambre existe déjà"
    
    new_room = pd.DataFrame([{
        "numero": str(numero),
        "type": type_room,
        "aile": aile,
        "etage": etage,
        "statut": statut
    }])
    rooms = pd.concat([rooms, new_room], ignore_index=True)
    save_rooms(rooms)
    return True, "Chambre ajoutée avec succès"

def delete_room(numero):
    """Supprime une chambre"""
    rooms = load_rooms()
    if str(numero) not in rooms["numero"].values:
        return False, "Cette chambre n'existe pas"
    
    # Vérifier s'il y a des tâches de maintenance en cours
    tasks = load_maintenance_tasks()
    active_tasks = tasks[(tasks["chambre"] == str(numero)) & (tasks["statut"] != "Terminé")]
    if len(active_tasks) > 0:
        return False, f"Impossible de supprimer: {len(active_tasks)} tâche(s) active(s)"
    
    rooms = rooms[rooms["numero"] != str(numero)]
    save_rooms(rooms)
    return True, "Chambre supprimée"

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
        df = pd.read_csv(MAINTENANCE_FILE)
        # Ensure all required columns exist
        if "priorite" not in df.columns:
            df["priorite"] = "Moyenne"
        if "duree_estimee_minutes" not in df.columns:
            df["duree_estimee_minutes"] = 0.0
        if "duree_reelle_minutes" not in df.columns:
            df["duree_reelle_minutes"] = 0.0
        if "type_panne" not in df.columns:
            df["type_panne"] = "Autre"
        return df
    else:
        df = pd.DataFrame(columns=["id", "chambre", "description", "assigned_to", "statut", "date_creation", "date_completion", "created_by", "priorite", "duree_estimee_minutes", "duree_reelle_minutes", "type_panne"])
        df.to_csv(MAINTENANCE_FILE, index=False)
        return df

def save_maintenance_tasks(tasks):
    tasks.to_csv(MAINTENANCE_FILE, index=False)

def create_maintenance_task(chambre, description, assigned_to, created_by, type_panne="Autre", duree_estimee=0, priorite="Moyenne"):
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
        "created_by": created_by,
        "duree_estimee_minutes": duree_estimee,
        "priorite": priorite
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

def update_task_duree(task_id, duree_reelle):
    """Met à jour la durée réelle d'une tâche (par le chef)"""
    tasks = load_maintenance_tasks()
    tasks.loc[tasks["id"] == task_id, "duree_reelle_minutes"] = duree_reelle
    save_maintenance_tasks(tasks)
    return tasks

def update_task_priorite(task_id, new_priorite):
    """Met à jour la priorité d'une tâche"""
    tasks = load_maintenance_tasks()
    tasks.loc[tasks["id"] == task_id, "priorite"] = new_priorite
    save_maintenance_tasks(tasks)
    return tasks
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
    elif is_receptionist():
        tab_recep1, tab_recep2 = st.tabs(["🏠 Dashboard", "🔴 Déclarer une Panne"])
    else:
        tab_dash, tab_reclamations, tab_rooms, tab_maint, tab_pannes, tab_composants, tab_agents, tab_users = st.tabs([
            "🏠 Dashboard", "🔴 Réclamations", "🛏️ Chambres", "🔧 Maintenance", "⚙️ Pannes", "🔩 Composants", "👥 Agents", "👤 Utilisateurs"
        ])
    
    # ========== DASHBOARD ==========
    with tab1 if is_maintenance() else (tab_recep1 if is_receptionist() else tab_dash):
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
        
        if is_receptionist():
            reclamations = load_reclamations()
            open_reclamations = len(reclamations[reclamations["statut"] == "Déclaré"])
            st.metric("Pannes signalées (en attente)", open_reclamations, delta="")
        
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
    
    # ========== TAB RÉCEPTIONNISTE: DÉCLARER UNE PANNE ==========
    if is_receptionist():
        with tab_recep2:
            st.subheader("🔴 Déclarer une Panne")
            
            st.markdown("**Signalez rapidement une panne dans la chambre:**")
            
            with st.form("declare_panne_form"):
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    panne_chambre = st.selectbox("🔑 N° Chambre", rooms[rooms["statut"] != "Libre"]["numero"].tolist() if len(rooms[rooms["statut"] != "Libre"]) > 0 else rooms["numero"].tolist())
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
    
    # ========== TAB RÉCLAMATIONS (Admin) ==========
    if is_admin():
        with tab_reclamations:
            st.subheader("🔴 Réclamations de Pannes Signalées")
            
            reclamations = load_reclamations()
            
            col_rec1, col_rec2 = st.columns(2)
            with col_rec1:
                declared = len(reclamations[reclamations["statut"] == "Déclaré"])
                st.metric("En attente", declared)
            with col_rec2:
                in_treatment = len(reclamations[reclamations["statut"] == "En traitement"])
                st.metric("En traitement", in_treatment)
            
            st.markdown("---")
            
            if len(reclamations) > 0:
                for idx, rec in reclamations.sort_values("date_declaration", ascending=False).iterrows():
                    status_icon = "🔴" if rec["statut"] == "Déclaré" else "🟡" if rec["statut"] == "En traitement" else "🟢"
                    
                    with st.expander(f"{status_icon} Chambre {rec['chambre']} - {rec['type_panne']} ({rec['statut']})"):
                        col_rec_info1, col_rec_info2 = st.columns(2)
                        with col_rec_info1:
                            st.markdown(f"**Type:** {rec['type_panne']}")
                            st.markdown(f"**Description:** {rec['description']}")
                            st.markdown(f"**Signalée par:** {rec['creé_par']}")
                        with col_rec_info2:
                            st.markdown(f"**Date:** {rec['date_declaration']}")
                            st.markdown(f"**Statut:** {rec['statut']}")
                        
                        st.markdown("---")
                        st.markdown("**🔧 Actions:**")
                        
                        col_rec_action1, col_rec_action2, col_rec_action3 = st.columns(3)
                        
                        with col_rec_action1:
                            if st.button("✅ Créer une tâche", key=f"create_task_{rec['id']}_{idx}"):
                                # Charger et afficher le formulaire pour créer la tâche
                                st.session_state[f"show_task_form_{rec['id']}"] = True
                        
                        with col_rec_action2:
                            if rec["statut"] != "En traitement":
                                if st.button("⏳ En traitement", key=f"in_treatment_{rec['id']}_{idx}"):
                                    update_reclamation_status(rec["id"], "En traitement")
                                    st.rerun()
                        
                        with col_rec_action3:
                            if st.button("🗑️ Supprimer", key=f"delete_rec_{rec['id']}_{idx}"):
                                delete_reclamation(rec["id"])
                                st.warning("Réclamation supprimée")
                                st.rerun()
                        
                        # Formulaire pour créer une tâche à partir de cette réclamation
                        if st.session_state.get(f"show_task_form_{rec['id']}", False):
                            st.markdown("---")
                            st.markdown("**📝 Créer une tâche de maintenance:**")
                            
                            with st.form(f"create_task_form_{rec['id']}"):
                                col_task1, col_task2 = st.columns(2)
                                with col_task1:
                                    task_priorite = st.selectbox("🚨 Priorité", ["Haute", "Moyenne", "Basse"], key=f"task_prio_{rec['id']}")
                                    task_duree = st.number_input("⏱️ Durée estimée (min)", min_value=10.0, value=30.0, step=5.0, key=f"task_dur_{rec['id']}")
                                with col_task2:
                                    users = load_users()
                                    agents = [u["nom"] for u in users.values() if u["role"] == "maintenance"]
                                    task_agent = st.selectbox("👤 Assigner à", agents, key=f"task_agent_{rec['id']}")
                                
                                task_desc_detail = st.text_area("📝 Description détaillée", value=rec["description"], key=f"task_desc_{rec['id']}")
                                
                                if st.form_submit_button("✅ Créer la tâche"):
                                    create_maintenance_task(
                                        rec["chambre"],
                                        task_desc_detail,
                                        task_agent,
                                        st.session_state.get("user_nom"),
                                        rec["type_panne"],
                                        task_duree,
                                        task_priorite
                                    )
                                    update_reclamation_status(rec["id"], "En traitement")
                                    st.success("✅ Tâche créée!")
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
    if is_maintenance():
        with tab2:
            st.subheader("🔧 Tâches de Maintenance")
            
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
                    duree_estimee = task.get('duree_estimee_minutes', 0) if 'duree_estimee_minutes' in task.index else 0
                    
                    with st.expander(f"{status_icon} #{task['id']} - Chambre {task['chambre']} - {task['statut']}"):
                        st.markdown(f"**🔧 Type de panne:** {type_panne}")
                        st.markdown(f"**📝 Description:** {task['description']}")
                        st.markdown(f"**👤 Assigné par:** {task['created_by']}")
                        st.markdown(f"**📅 Créée le:** {task['date_creation']}")
                        st.markdown(f"**⏱️ Durée estimée:** {duree_estimee} minutes")
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
                        
                        # Vérifier s'il y a déjà un rapport
                        rapports = load_rapports()
                        task_rapport = rapports[rapports["task_id"] == task['id']]
                        
                        st.markdown("---")
                        st.markdown("**📋 Rapport de tâche:**")
                        
                        if len(task_rapport) > 0:
                            st.success("✅ Rapport déjà enregistré")
                            for _, rapport in task_rapport.iterrows():
                                st.info(f"**Rapport:** {rapport['rapport']}")
                                st.markdown(f"- **Durée travail:** {rapport['duree_travail_minutes']} min")
                                st.markdown(f"- **Pièces utilisées:** {rapport['pieces_utilisees']}")
                                st.markdown(f"- **Notes:** {rapport['notes_agent']}")
                                st.markdown(f"- **Date:** {rapport['date_rapport']}")
                        elif task["statut"] == "Terminé":
                            with st.form(f"rapport_form_{task['id']}_{idx}"):
                                st.markdown("📝 Remplir le rapport de tâche:")
                                rapport_text = st.text_area("Résumé du travail effectué", key=f"rapport_{task['id']}")
                                duree_reelle = st.number_input("Durée réelle (minutes)", min_value=0.0, value=float(duree_estimee), step=1.0, key=f"duree_{task['id']}")
                                pieces = st.text_input("Pièces utilisées (séparées par virgule)", key=f"pieces_{task['id']}")
                                notes = st.text_area("Notes supplémentaires", key=f"notes_{task['id']}")
                                
                                if st.form_submit_button("Enregistrer le rapport"):
                                    if rapport_text:
                                        add_rapport(task['id'], current_user, rapport_text, duree_reelle, pieces, notes)
                                        st.success("✅ Rapport enregistré!")
                                        st.rerun()
                                    else:
                                        st.error("Veuillez remplir le rapport")
                        else:
                            st.info("Le rapport peut être enregistré une fois la tâche terminée")
            else:
                st.info("Aucune tâche assignée à votre nom. 🎉")
                st.markdown("**Vous n'avez pas de tâches de maintenance en attente.**")
            
            st.markdown("---")
            st.markdown("### 🔔 Vos Notifications")
            if st.button("🔄 Actualiser les notifications"):
                st.rerun()
    
    elif is_admin():
        with tab_maint:
            st.subheader("🔧 Tâches de Maintenance")
            
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
                        maint_duree = st.number_input("Durée estimée (minutes)", min_value=0.0, value=30.0, step=1.0)
                    with col_m2:
                        users = load_users()
                        agents = [u["nom"] for u in users.values() if u["role"] == "maintenance"]
                        maint_agent = st.selectbox("Assigner à", agents)
                        maint_priorite = st.selectbox("🚨 Priorité", ["Basse", "Moyenne", "Haute"])
                    
                    submit_maint = st.form_submit_button("Créer la tâche")
                    
                    if submit_maint and maint_desc and maint_agent:
                        create_maintenance_task(
                            maint_chambre,
                            maint_desc,
                            maint_agent,
                            st.session_state.get("user_nom"),
                            maint_type_panne,
                            maint_duree,
                            maint_priorite
                        )
                        st.success("✅ Tâche créée!")
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
            
            # Trier par priorité (Haute > Moyenne > Basse)
            priority_order = {"Haute": 0, "Moyenne": 1, "Basse": 2}
            # Ensure priorite column exists and has valid values
            if "priorite" in filtered_tasks.columns and len(filtered_tasks) > 0:
                filtered_tasks["priorite"] = filtered_tasks["priorite"].fillna("Moyenne")
                filtered_tasks["priority_sort"] = filtered_tasks["priorite"].map(priority_order).fillna(1)
                filtered_tasks = filtered_tasks.sort_values(["priority_sort", "date_creation"], ascending=[True, False]).drop("priority_sort", axis=1)
            
            if len(filtered_tasks) > 0:
                for idx, task in filtered_tasks.iterrows():
                    status_icon = "🟡" if task["statut"] == "En attente" else "🔵" if task["statut"] == "En cours" else "🟢"
                    priority_icon = "🚨" if task.get("priorite", "Moyenne") == "Haute" else "⚠️" if task.get("priorite", "Moyenne") == "Moyenne" else "ℹ️"
                    type_panne = task.get('type_panne', 'Autre') if 'type_panne' in task.index else 'Autre'
                    duree = float(task.get('duree_estimee_minutes', 0)) if 'duree_estimee_minutes' in task.index else 0.0
                    duree_reelle = float(task.get('duree_reelle_minutes', 0)) if (task.get('duree_reelle_minutes', 0) and 'duree_reelle_minutes' in task.index) else 0.0
                    
                    with st.expander(f"{status_icon} {priority_icon} #{task['id']} - Chambre {task['chambre']} - {task['statut']}"):
                        col_task1, col_task2 = st.columns(2)
                        with col_task1:
                            st.markdown(f"**Type de panne:** {type_panne}")
                            st.markdown(f"**Description:** {task['description']}")
                            st.markdown(f"**Assigné à:** {task['assigned_to']}")
                            st.markdown(f"**Créée le:** {task['date_creation']}")
                        with col_task2:
                            st.markdown(f"**🚨 Priorité:** {task.get('priorite', 'Moyenne')}")
                            st.markdown(f"**⏱️ Durée estimée:** {duree} min")
                            if duree_reelle:
                                st.markdown(f"**✓ Durée réelle:** {duree_reelle} min")
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
                        
                        st.markdown("---")
                        st.markdown("**⚙️ Gestion par le Chef:**")
                        
                        col_chef1, col_chef2, col_chef3 = st.columns(3)
                        with col_chef1:
                            new_priorite = st.selectbox(f"Changer priorité", ["Haute", "Moyenne", "Basse"], 
                                                        index=["Haute", "Moyenne", "Basse"].index(task.get("priorite", "Moyenne")),
                                                        key=f"prio_{task['id']}")
                            if new_priorite != task.get("priorite", "Moyenne"):
                                if st.button("💾 Mettre à jour priorité", key=f"update_prio_{task['id']}"):
                                    update_task_priorite(task["id"], new_priorite)
                                    st.success(f"Priorité changée à {new_priorite}")
                                    st.rerun()
                        
                        with col_chef2:
                            duree_reelle_input = st.number_input(f"Durée réelle à affecter (min)", min_value=0.0, 
                                                                 value=float(duree_reelle) if duree_reelle else float(duree),
                                                                 step=1.0,
                                                                 key=f"duree_real_{task['id']}")
                            if st.button("💾 Enregistrer durée réelle", key=f"update_duree_{task['id']}"):
                                update_task_duree(task["id"], duree_reelle_input)
                                st.success(f"Durée réelle: {duree_reelle_input} min")
                                st.rerun()
                        
                        with col_chef3:
                            st.info("Module de gestion chef")
            else:
                st.info("Aucune tâche")
    
    # ========== TAB GESTION DES PANNES ==========
    if is_admin():
        with tab_pannes:
            st.subheader("⚙️ Gestion des Types de Pannes")
            
            pannes = load_pannes()
            
            st.markdown(f"**{len(pannes)} types de pannes enregistrés**")
            
            with st.expander("➕ Ajouter un nouveau type de panne"):
                with st.form("add_panne_form"):
                    panne_nom = st.text_input("Nom de la panne")
                    panne_desc = st.text_area("Description")
                    panne_priorite = st.selectbox("Priorité", ["Basse", "Moyenne", "Haute"])
                    
                    submit_panne = st.form_submit_button("Ajouter")
                    
                    if submit_panne and panne_nom:
                        add_panne(panne_nom, panne_desc, panne_priorite)
                        st.success(f"✅ Type de panne '{panne_nom}' ajouté!")
                        st.rerun()
            
            st.markdown("---")
            st.markdown("**📋 Types de pannes existants:**")
            
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                st.markdown("**Haute Priorité:**")
                haute = pannes[pannes["priorite"] == "Haute"]
                for _, panne in haute.iterrows():
                    st.markdown(f"🔴 **{panne['nom_panne']}**  \n{panne['description'][:50]}...")
            
            with col_p2:
                st.markdown("**Priorité Moyenne:**")
                moyenne = pannes[pannes["priorite"] == "Moyenne"]
                for _, panne in moyenne.iterrows():
                    st.markdown(f"🟡 **{panne['nom_panne']}**  \n{panne['description'][:50]}...")
            
            with col_p3:
                st.markdown("**Basse Priorité:**")
                basse = pannes[pannes["priorite"] == "Basse"]
                for _, panne in basse.iterrows():
                    st.markdown(f"🟢 **{panne['nom_panne']}**  \n{panne['description'][:50]}...")
            
            st.markdown("---")
            with st.expander("📊 Voir le tableau complet des pannes"):
                st.dataframe(pannes)
    
    # ========== TAB GESTION DES COMPOSANTS ==========
    if is_admin():
        with tab_composants:
            st.subheader("🔩 Gestion des Composants de Chambres")
            
            composants = load_composants()
            rooms_list = rooms["numero"].tolist()
            
            tab_comp1, tab_comp2, tab_comp3 = st.tabs(["➕ Ajouter", "👁️ Vue Chambres", "📊 Tous les Composants"])
            
            with tab_comp1:
                st.markdown("**Ajouter un nouveau composant à une chambre:**")
                
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
                        comp_sous = st.text_input("Sous-composant (ex: Compresseur, Filtre...)")
                        comp_statut = st.selectbox("État", ["Bon", "Dégradé", "Cassé", "En maintenance"])
                    
                    submit_comp = st.form_submit_button("✅ Ajouter le composant", use_container_width=True)
                    
                    if submit_comp and comp_chambre and comp_principal and comp_sous:
                        add_composant(comp_chambre, comp_principal, comp_sous, comp_statut)
                        st.success("✅ Composant ajouté avec succès!")
                        st.rerun()
                    elif submit_comp:
                        st.error("❌ Veuillez remplir tous les champs")
            
            with tab_comp2:
                st.markdown("**Composants par chambre:**")
                selected_room = st.selectbox("Sélectionner une chambre", rooms_list, key="room_composant")
                room_comps = composants[composants["chambre"] == str(selected_room)]
                
                if len(room_comps) > 0:
                    st.markdown(f"### 🚪 Composants de la chambre **{selected_room}** ({len(room_comps)} composant(s))")
                    
                    for idx, comp in room_comps.iterrows():
                        status_icon = "✅" if comp["statut"] == "Bon" else "⚠️" if comp["statut"] == "Dégradé" else "❌" if comp["statut"] == "Cassé" else "🔧"
                        
                        with st.expander(f"{status_icon} {comp['composant_principal']} - {comp['sous_composant']}"):
                            col_info1, col_info2, col_info3 = st.columns([2, 2, 1.5])
                            
                            with col_info1:
                                st.markdown("**Informations:**")
                                st.markdown(f"- **Composant:** {comp['composant_principal']}")
                                st.markdown(f"- **Sous-composant:** {comp['sous_composant']}")
                                st.markdown(f"- **Statut:** {comp['statut']}")
                            
                            with col_info2:
                                st.markdown("**Dates:**")
                                st.markdown(f"- **Installation:** {comp['date_installation']}")
                                st.markdown(f"- **Maintenance:** {comp['derniere_maintenance'] or '❌ Jamais'}")
                            
                            with col_info3:
                                st.markdown("**Actions:**")
                                new_status = st.selectbox(
                                    f"Changer statut",
                                    ["Bon", "Dégradé", "Cassé", "En maintenance"],
                                    index=["Bon", "Dégradé", "Cassé", "En maintenance"].index(comp["statut"]),
                                    key=f"status_{comp['id']}"
                                )
                                if new_status != comp["statut"]:
                                    if st.button("💾 Actualiser", key=f"update_{comp['id']}"):
                                        update_composant_status(comp["id"], new_status)
                                        st.success(f"✅ Statut changé à {new_status}")
                                        st.rerun()
                                
                                if st.button("🗑️ Supprimer", key=f"delete_{comp['id']}", type="secondary"):
                                    delete_composant(comp["id"])
                                    st.warning("❌ Composant supprimé")
                                    st.rerun()
                else:
                    st.info(f"📭 Aucun composant enregistré pour la chambre {selected_room}")
                    st.markdown("**Utilisez l'onglet 'Ajouter' pour en créer un**")
            
            with tab_comp3:
                st.markdown("### 📊 Tous les Composants de l'Hôtel")
                
                if len(composants) > 0:
                    # Filtres
                    col_f1, col_f2, col_f3 = st.columns(3)
                    with col_f1:
                        filter_room = st.selectbox("Filtrer par chambre", ["Tous"] + sorted(composants["chambre"].unique().tolist()), key="comp_room_filter")
                    with col_f2:
                        filter_principal = st.selectbox("Filtrer par composant", ["Tous"] + sorted(composants["composant_principal"].unique().tolist()), key="comp_principal_filter")
                    with col_f3:
                        filter_status = st.selectbox("Filtrer par statut", ["Tous"] + sorted(composants["statut"].unique().tolist()), key="comp_status_filter")
                    
                    # Appliquer les filtres
                    filtered_comp = composants.copy()
                    if filter_room != "Tous":
                        filtered_comp = filtered_comp[filtered_comp["chambre"] == filter_room]
                    if filter_principal != "Tous":
                        filtered_comp = filtered_comp[filtered_comp["composant_principal"] == filter_principal]
                    if filter_status != "Tous":
                        filtered_comp = filtered_comp[filtered_comp["statut"] == filter_status]
                    
                    st.markdown(f"**Affichage: {len(filtered_comp)} composant(s) / {len(composants)} total**")
                    
                    # Tableau
                    display_cols = ["chambre", "composant_principal", "sous_composant", "statut", "date_installation", "derniere_maintenance"]
                    st.dataframe(filtered_comp[display_cols], use_container_width=True)
                    
                    # Statistiques
                    st.markdown("---")
                    st.markdown("### 📈 Statistiques")
                    
                    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                    with col_s1:
                        bon_count = len(composants[composants["statut"] == "Bon"])
                        st.metric("✅ En bon état", bon_count)
                    with col_s2:
                        degrade_count = len(composants[composants["statut"] == "Dégradé"])
                        st.metric("⚠️ Dégradés", degrade_count)
                    with col_s3:
                        casse_count = len(composants[composants["statut"] == "Cassé"])
                        st.metric("❌ Cassés", casse_count)
                    with col_s4:
                        maint_count = len(composants[composants["statut"] == "En maintenance"])
                        st.metric("🔧 En maintenance", maint_count)
                else:
                    st.info("📭 Aucun composant enregistré pour le moment")
    
    # ========== TAB HISTORIQUE AGENTS ==========
    if is_admin():
        with tab_agents:
            st.subheader("👥 Historique et Performance des Agents")
            
            users = load_users()
            agents = [u["nom"] for u in users.values() if u["role"] == "maintenance"]
            
            col_agent1, col_agent2 = st.columns(2)
            with col_agent1:
                selected_agent = st.selectbox("Sélectionner un agent", agents)
            with col_agent2:
                show_all = st.checkbox("Afficher tous les agents", value=False)
            
            if show_all:
                st.markdown("### 📊 Résumé de tous les agents:")
                
                agent_stats = []
                for agent in agents:
                    history = get_agent_history(agent)
                    agent_stats.append({
                        "Agent": agent,
                        "Total": history["total"],
                        "Terminées": history["terminees"],
                        "En cours": history["en_cours"],
                        "En attente": history["en_attente"]
                    })
                
                df_stats = pd.DataFrame(agent_stats)
                st.dataframe(df_stats, use_container_width=True)
                
                col_g1, col_g2, col_g3 = st.columns(3)
                with col_g1:
                    total_tasks = df_stats["Total"].sum()
                    st.metric("Total global", total_tasks)
                with col_g2:
                    total_done = df_stats["Terminées"].sum()
                    st.metric("Terminées totales", total_done)
                with col_g3:
                    if total_tasks > 0:
                        completion_rate = (total_done / total_tasks) * 100
                        st.metric("Taux de complétion", f"{completion_rate:.1f}%")
            
            else:
                st.markdown(f"### 📊 Historique: **{selected_agent}**")
                history = get_agent_history(selected_agent)
                
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                with col_stat1:
                    st.metric("Total tâches", history["total"])
                with col_stat2:
                    st.metric("Terminées", history["terminees"])
                with col_stat3:
                    st.metric("En cours", history["en_cours"])
                with col_stat4:
                    st.metric("En attente", history["en_attente"])
                
                st.markdown("---")
                st.markdown("**📋 Détail des tâches:**")
                
                tasks = load_maintenance_tasks()
                agent_tasks = tasks[tasks["assigned_to"] == selected_agent].copy()
                
                if len(agent_tasks) > 0:
                    for idx, task in agent_tasks.iterrows():
                        status_icon = "🟡" if task["statut"] == "En attente" else "🔵" if task["statut"] == "En cours" else "🟢"
                        duree = task.get('duree_estimee_minutes', 0) if 'duree_estimee_minutes' in task.index else 0
                        
                        with st.expander(f"{status_icon} #{task['id']} - Chambre {task['chambre']} - {task['statut']}"):
                            col_d1, col_d2 = st.columns(2)
                            with col_d1:
                                st.markdown(f"**Description:** {task['description']}")
                                st.markdown(f"**Type:** {task.get('type_panne', 'Autre')}")
                                st.markdown(f"**Créée:** {task['date_creation']}")
                            with col_d2:
                                st.markdown(f"**Durée estimée:** {duree} minutes")
                                st.markdown(f"**Statut:** {task['statut']}")
                                if task['date_completion']:
                                    st.markdown(f"**Terminée:** {task['date_completion']}")
                            
                            # Afficher ou ajouter rapport
                            rapports = load_rapports()
                            task_rapport = rapports[rapports["task_id"] == task['id']]
                            
                            if len(task_rapport) > 0:
                                st.markdown("**📝 Rapport existant:**")
                                for _, rapport in task_rapport.iterrows():
                                    st.info(f"**Rapport:** {rapport['rapport']}")
                                    st.markdown(f"- **Durée réelle:** {rapport['duree_travail_minutes']} minutes")
                                    st.markdown(f"- **Pièces utilisées:** {rapport['pieces_utilisees']}")
                                    st.markdown(f"- **Notes:** {rapport['notes_agent']}")
                            else:
                                if task['statut'] == "Terminé":
                                    st.markdown("**Aucun rapport pour cette tâche**")
    
    # ========== USER MANAGEMENT ==========
    if is_admin() and not is_maintenance():
        with tab_users:
            st.subheader("👤 Gestion des Utilisateurs")
            
            tab_users1, tab_users2 = st.tabs(["Utilisateurs", "Chambres"])
            
            with tab_users1:
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
            
            with tab_users2:
                st.markdown("### 🛏️ Gestion des Chambres")
                
                rooms = load_rooms()
                
                col_room1, col_room2 = st.columns(2)
                
                with col_room1:
                    with st.expander("➕ Ajouter une chambre"):
                        with st.form("add_room_form"):
                            room_numero = st.text_input("Numéro de chambre")
                            room_type = st.selectbox("Type", ["Standard", "Suite", "Deluxe", "Appartement"])
                            room_aile = st.selectbox("Aile", ["A", "B", "C"])
                            room_etage = st.number_input("Étage", min_value=0.0, max_value=10.0, value=1.0)
                            
                            submit_room = st.form_submit_button("Ajouter la chambre")
                            
                            if submit_room and room_numero:
                                success, message = add_room(room_numero, room_type, room_aile, room_etage)
                                if success:
                                    st.success(f"✅ {message}")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                
                with col_room2:
                    with st.expander("🗑️ Supprimer une chambre"):
                        room_to_delete = st.selectbox("Sélectionner la chambre à supprimer", rooms["numero"].tolist())
                        st.warning("⚠️ Les chambres avec tâches actives ne peuvent pas être supprimées")
                        
                        if st.button("🗑️ Supprimer cette chambre", type="primary"):
                            success, message = delete_room(room_to_delete)
                            if success:
                                st.success(f"✅ {message}")
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                
                st.markdown("---")
                st.markdown("### 📋 Liste des chambres")
                
                col_room_f1, col_room_f2 = st.columns(2)
                with col_room_f1:
                    aile_filter = st.selectbox("Filtrer par Aile", ["Tous"] + rooms["aile"].unique().tolist(), key="aile_mgmt")
                with col_room_f2:
                    type_filter = st.selectbox("Filtrer par Type", ["Tous"] + rooms["type"].unique().tolist(), key="type_mgmt")
                
                filtered_rooms = rooms.copy()
                if aile_filter != "Tous":
                    filtered_rooms = filtered_rooms[filtered_rooms["aile"] == aile_filter]
                if type_filter != "Tous":
                    filtered_rooms = filtered_rooms[filtered_rooms["type"] == type_filter]
                
                st.dataframe(filtered_rooms, use_container_width=True)
                
                st.markdown(f"**Total:** {len(filtered_rooms)} chambres")

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
