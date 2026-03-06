import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import hashlib

# ============================================
# GESTION DES FICHIERS
# ============================================
USERS_FILE = "utilisateurs.json"
ROOMS_FILE = "chambres.csv"
MAINTENANCE_FILE = "maintenance_tasks.csv"

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

def create_maintenance_task(chambre, description, assigned_to, created_by):
    """Crée une tâche de maintenance"""
    tasks = load_maintenance_tasks()
    rooms = load_rooms()
    
    new_task = pd.DataFrame([{
        "id": len(tasks) + 1,
        "chambre": chambre,
        "description": description,
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
    
    save_maintenance_tasks(tasks)
    return tasks

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
    
    username = st.text_input("Nom d'utilisateur", key="login_user")
    password = st.text_input("Mot de passe", type="password", key="login_pass")
    
    col_login, _ = st.columns([1, 1])
    with col_login:
        if st.button("🔑 Se connecter", use_container_width=True):
            user = authenticate(username, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["user_role"] = user["role"]
                st.session_state["user_nom"] = user["nom"]
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")
    
    st.markdown("---")
   
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
                with st.expander(f"🚪 Chambre {row['numero']} - {row['type']} ({row['aile']})"):
                    col_r1, col_r2 = st.columns(2)
                    with col_r1:
                        st.markdown(f"**Statut actuel:** {row['statut']}")
                        st.markdown(f"**Étage:** {row['etage']}")
                        st.markdown(f"**Aile:** {row['aile']}")
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
            
            with st.expander("📋 Détail complet"):
                st.dataframe(filtered)
    
    # ========== TAB MAINTENANCE ==========
    with tab_maint if not is_maintenance() else tab2:
        st.subheader("🔧 Tâches de Maintenance")
        
        # Créer une nouvelle tâche
        with st.expander("➕ Créer une tâche"):
            with st.form("maintenance_form"):
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    maint_chambre = st.selectbox("Chambre", rooms["numero"].tolist())
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
                        st.session_state.get("user_nom")
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
            for _, task in filtered_tasks.iterrows():
                status_icon = "🟡" if task["statut"] == "En attente" else "🔵" if task["statut"] == "En cours" else "🟢"
                with st.expander(f"{status_icon} #{task['id']} - Chambre {task['chambre']} - {task['statut']}"):
                    st.markdown(f"**Description:** {task['description']}")
                    st.markdown(f"**Assigné à:** {task['assigned_to']}")
                    st.markdown(f"**Créée le:** {task['date_creation']}")
                    if task["date_completion"]:
                        st.markdown(f"**Terminée le:** {task['date_completion']}")
                    
                    if task["statut"] != "Terminé":
                        col_t1, col_t2 = st.columns(2)
                        with col_t1:
                            if st.button(f"Commencer", key=f"start_{task['id']}"):
                                update_task_status(task["id"], "En cours")
                                st.rerun()
                        with col_t2:
                            if st.button(f"Terminer", key=f"end_{task['id']}"):
                                update_task_status(task["id"], "Terminé")
                                st.success("Tâche terminée!")
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
    
    if not st.session_state.get("logged_in", False):
        show_login()
    else:
        show_main_app()

