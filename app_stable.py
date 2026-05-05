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
    
    # Load all data for comprehensive dashboard
    @st.cache_data
    def load_reclamations():
        if os.path.exists(RECLAMATIONS_FILE):
            return pd.read_csv(RECLAMATIONS_FILE)
        return pd.DataFrame()
    
    @st.cache_data
    def load_maintenance_tasks():
        if os.path.exists(MAINTENANCE_FILE):
            return pd.read_csv(MAINTENANCE_FILE)
        return pd.DataFrame()
    
    @st.cache_data
    def load_pannes():
        if os.path.exists(PANNES_FILE):
            return pd.read_csv(PANNES_FILE)
        return pd.DataFrame()
    
    @st.cache_data
    def load_composants():
        if os.path.exists(COMPOSANTS_FILE):
            return pd.read_csv(COMPOSANTS_FILE)
        return pd.DataFrame()
    
    @st.cache_data
    def load_users():
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    reclamations = load_reclamations()
    tasks = load_maintenance_tasks()
    pannes = load_pannes()
    composants = load_composants()
    users = load_users()
    
    # Calculate all key metrics
    # Rooms
    total_rooms = len(rooms)
    free_rooms = len(rooms[rooms["statut"] == "Libre"])
    occupied_rooms = len(rooms[rooms["statut"] == "Occupée"])
    maintenance_rooms = len(rooms[rooms["statut"] == "Maintenance"])
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    
    # Reclamations
    reclamations_pending = len(reclamations[reclamations["statut"] == "Déclaré"]) if len(reclamations) > 0 else 0
    reclamations_in_progress = len(reclamations[reclamations["statut"] == "En traitement"]) if len(reclamations) > 0 else 0
    
    # Maintenance Tasks
    total_tasks = len(tasks)
    tasks_pending = len(tasks[tasks["statut"] == "En attente"]) if len(tasks) > 0 else 0
    tasks_in_progress = len(tasks[tasks["statut"] == "En cours"]) if len(tasks) > 0 else 0
    tasks_completed = len(tasks[tasks["statut"] == "Terminé"]) if len(tasks) > 0 else 0
    
    # Pannes types
    pannes_haute = len(pannes[pannes["priorite"] == "Haute"]) if len(pannes) > 0 else 0
    pannes_moyenne = len(pannes[pannes["priorite"] == "Moyenne"]) if len(pannes) > 0 else 0
    pannes_basse = len(pannes[pannes["priorite"] == "Basse"]) if len(pannes) > 0 else 0
    
    # Composants
    total_composants = len(composants)
    composants_good = len(composants[composants["statut"] == "Bon"]) if len(composants) > 0 else 0
    composants_broken = len(composants[composants["statut"] == "Cassé"]) if len(composants) > 0 else 0
    composants_degraded = len(composants[composants["statut"] == "Dégradé"]) if len(composants) > 0 else 0
    
    # Users
    total_users = len(users)
    admin_users = len([u for u in users.values() if u["role"] == "admin"])
    maintenance_users = len([u for u in users.values() if u["role"] == "maintenance"])
    receptionist_users = len([u for u in users.values() if u["role"] == "reception"])
    
    # Initialize view section
    if "view_section" not in st.session_state:
        st.session_state["view_section"] = None
    
    # Main KPIs Section
    st.markdown("### 🎯 Indicateurs Clés")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 Taux d'Occupation", key="nav_occupancy", help="Cliquez pour voir les détails des chambres"):
            st.session_state["view_section"] = "rooms"
        st.metric("📈 Taux d'Occupation", f"{occupancy_rate:.1f}%", f"{occupied_rooms}/{total_rooms} chambres")
    
    with col2:
        if st.button("🛏️ Chambres Disponibles", key="nav_available", help="Cliquez pour gérer les chambres"):
            st.session_state["view_section"] = "rooms"
        st.metric("🛏️ Chambres Disponibles", free_rooms, f"sur {total_rooms} total")
    
    with col3:
        total_issues = reclamations_pending + tasks_pending
        if st.button("⚠️ Problèmes Actifs", key="nav_issues", help="Cliquez pour voir les réclamations et tâches"):
            st.session_state["view_section"] = "issues"
        st.metric("⚠️ Problèmes Actifs", total_issues, f"{reclamations_pending} pannes + {tasks_pending} tâches")
    
    st.markdown("---")
    
    # Detailed Sections
    st.markdown("### 📊 Sections Détaillées")
    
    # Row 1: Rooms & Reclamations
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
                st.session_state["view_section"] = "reclamations"
            st.metric("⏳ En Attente", reclamations_pending)
        
        with rec_cols[1]:
            if st.button("🔄 En Traitement", key="nav_rec_progress"):
                st.session_state["view_section"] = "reclamations"
            st.metric("🔄 En Traitement", reclamations_in_progress)
    
    st.markdown("---")
    
    # Row 2: Maintenance & Pannes
    col_b1, col_b2 = st.columns(2)
    
    with col_b1:
        st.markdown("#### 🔧 **Maintenance**")
        maint_cols = st.columns(3)
        with maint_cols[0]:
            if st.button("📋 Total Tâches", key="nav_total_tasks"):
                st.session_state["view_section"] = "maintenance"
            st.metric("📋 Total", total_tasks)
        
        with maint_cols[1]:
            if st.button("⏳ En Attente", key="nav_tasks_pending"):
                st.session_state["view_section"] = "maintenance"
            st.metric("⏳ En Attente", tasks_pending)
        
        with maint_cols[2]:
            if st.button("🔄 En Cours", key="nav_tasks_progress"):
                st.session_state["view_section"] = "maintenance"
            st.metric("🔄 En Cours", tasks_in_progress)
    
    with col_b2:
        st.markdown("#### ⚙️ **Types de Pannes**")
        panne_cols = st.columns(3)
        with panne_cols[0]:
            if st.button("🔴 Haute", key="nav_pannes_high"):
                st.session_state["view_section"] = "pannes"
            st.metric("🔴 Haute", pannes_haute)
        
        with panne_cols[1]:
            if st.button("🟡 Moyenne", key="nav_pannes_medium"):
                st.session_state["view_section"] = "pannes"
            st.metric("🟡 Moyenne", pannes_moyenne)
        
        with panne_cols[2]:
            if st.button("🟢 Basse", key="nav_pannes_low"):
                st.session_state["view_section"] = "pannes"
            st.metric("🟢 Basse", pannes_basse)
    
    st.markdown("---")
    
    # Row 3: Composants & Utilisateurs
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown("#### 🔩 **Composants**")
        comp_cols = st.columns(2)
        with comp_cols[0]:
            if st.button("📦 Total Composants", key="nav_total_comp"):
                st.session_state["view_section"] = "composants"
            st.metric("📦 Total", total_composants)
            
            if st.button("✅ Disponibles", key="nav_comp_good"):
                st.session_state["view_section"] = "composants"
            pct_good = (composants_good/total_composants*100) if total_composants > 0 else 0
            st.metric("✅ Disponibles", f"{composants_good}/{total_composants}", f"{pct_good:.1f}%")
        
        with comp_cols[1]:
            if st.button("❌ En Panne", key="nav_comp_broken"):
                st.session_state["view_section"] = "composants"
            st.metric("❌ En Panne", composants_broken)
            
            if st.button("⚠️ À Réviser", key="nav_comp_degraded"):
                st.session_state["view_section"] = "composants"
            st.metric("⚠️ À Réviser", composants_degraded)
    
    with col_c2:
        st.markdown("#### 👥 **Utilisateurs**")
        user_cols = st.columns(2)
        with user_cols[0]:
            if st.button("👤 Total Utilisateurs", key="nav_total_users"):
                st.session_state["view_section"] = "users"
            st.metric("👤 Total", total_users)
            
            if st.button("👑 Administrateurs", key="nav_admin_users"):
                st.session_state["view_section"] = "users"
            st.metric("👑 Admins", admin_users)
        
        with user_cols[1]:
            if st.button("🔧 Agents Maintenance", key="nav_maint_users"):
                st.session_state["view_section"] = "users"
            st.metric("🔧 Agents", maintenance_users)
            
            if st.button("🏨 Réceptionnistes", key="nav_recep_users"):
                st.session_state["view_section"] = "users"
            st.metric("🏨 Réception", receptionist_users)
    
    # Section détaillée basée sur la navigation
    if st.session_state["view_section"]:
        st.markdown("---")
        st.markdown(f"### 📋 Détails - {st.session_state['view_section'].title()}")
        
        if st.session_state["view_section"] == "rooms":
            st.markdown("**🛏️ Gestion des Chambres**")
            # Afficher un résumé des chambres
            room_status = rooms["statut"].value_counts()
            st.dataframe(room_status.to_frame(), use_container_width=True)
            
            # Boutons pour aller à la section complète
            col_nav1, col_nav2 = st.columns(2)
            with col_nav1:
                st.info("🔍 Fonctionnalité complète disponible dans app.py")
            with col_nav2:
                if st.button("❌ Fermer les détails", key="close_details"):
                    st.session_state["view_section"] = None
                    st.rerun()
                    
        elif st.session_state["view_section"] == "issues":
            st.markdown("**⚠️ Problèmes Actifs**")
            
            # Réclamations récentes
            if len(reclamations) > 0:
                st.markdown("**🔴 Réclamations récentes:**")
                recent_reclamations = reclamations[reclamations["statut"] == "Déclaré"].head(5)
                if len(recent_reclamations) > 0:
                    for _, rec in recent_reclamations.iterrows():
                        st.info(f"Chambre {rec['chambre']} - {rec['type_panne']}: {rec['description'][:50]}...")
                else:
                    st.success("Aucune réclamation en attente")
            
            # Tâches en attente
            if len(tasks) > 0:
                st.markdown("**📋 Tâches en attente:**")
                pending_tasks_list = tasks[tasks["statut"] == "En attente"].head(5)
                if len(pending_tasks_list) > 0:
                    for _, task in pending_tasks_list.iterrows():
                        st.warning(f"Chambre {task['chambre']} - {task.get('type_panne', 'Maintenance')}")
                else:
                    st.success("Aucune tâche en attente")
            
            # Boutons pour aller aux sections complètes
            col_nav1, col_nav2, col_nav3 = st.columns(3)
            with col_nav1:
                st.info("🔍 Fonctionnalités complètes dans app.py")
            with col_nav2:
                st.info("🔍 Fonctionnalités complètes dans app.py")
            with col_nav3:
                if st.button("❌ Fermer les détails", key="close_details_issues"):
                    st.session_state["view_section"] = None
                    st.rerun()
        
        elif st.session_state["view_section"] == "reclamations":
            st.markdown("**🔴 Réclamations de Pannes**")
            
            # Afficher les réclamations récentes
            if len(reclamations) > 0:
                recent_recs = reclamations.sort_values("date_declaration", ascending=False).head(10)
                for _, rec in recent_recs.iterrows():
                    status_icon = "🔴" if rec["statut"] == "Déclaré" else "🟡" if rec["statut"] == "En traitement" else "🟢"
                    with st.expander(f"{status_icon} Chambre {rec['chambre']} - {rec['type_panne']}"):
                        st.markdown(f"**Description:** {rec['description']}")
                        st.markdown(f"**Signalée par:** {rec['creé_par']}")
                        st.markdown(f"**Date:** {rec['date_declaration']}")
                        st.markdown(f"**Statut:** {rec['statut']}")
            else:
                st.info("Aucune réclamation")
            
            # Bouton pour aller à la section complète
            col_nav1, col_nav2 = st.columns(2)
            with col_nav1:
                st.info("🔍 Fonctionnalité complète dans app.py")
            with col_nav2:
                if st.button("❌ Fermer", key="close_reclamations"):
                    st.session_state["view_section"] = None
                    
        elif st.session_state["view_section"] == "maintenance":
            st.markdown("**🔧 Tâches de Maintenance**")
            
            # Afficher les tâches récentes
            if len(tasks) > 0:
                recent_tasks = tasks.sort_values("date_creation", ascending=False).head(10)
                for _, task in recent_tasks.iterrows():
                    status_icon = "🟡" if task["statut"] == "En attente" else "🔵" if task["statut"] == "En cours" else "🟢"
                    with st.expander(f"{status_icon} #{task['id']} - Chambre {task['chambre']}"):
                        st.markdown(f"**Description:** {task['description']}")
                        st.markdown(f"**Type:** {task.get('type_panne', 'Maintenance')}")
                        st.markdown(f"**Assigné à:** {task['assigned_to']}")
                        st.markdown(f"**Statut:** {task['statut']}")
                        if task['date_completion']:
                            st.markdown(f"**Terminée:** {task['date_completion']}")
            else:
                st.info("Aucune tâche")
            
            # Bouton pour aller à la section complète
            col_nav1, col_nav2 = st.columns(2)
            with col_nav1:
                st.info("🔍 Fonctionnalité complète dans app.py")
            with col_nav2:
                if st.button("❌ Fermer", key="close_maintenance"):
                    st.session_state["view_section"] = None
        
        elif st.session_state["view_section"] == "pannes":
            st.markdown("**⚙️ Types de Pannes**")
            if len(pannes) > 0:
                st.dataframe(pannes, use_container_width=True)
            else:
                st.info("Aucun type de panne défini")
            
            col_nav1, col_nav2 = st.columns(2)
            with col_nav1:
                st.info("🔍 Fonctionnalité complète dans app.py")
            with col_nav2:
                if st.button("❌ Fermer", key="close_pannes"):
                    st.session_state["view_section"] = None
        
        elif st.session_state["view_section"] == "composants":
            st.markdown("**🔩 Composants**")
            if len(composants) > 0:
                st.dataframe(composants.head(20), use_container_width=True)
                if len(composants) > 20:
                    st.info(f"Et {len(composants)-20} autres composants...")
            else:
                st.info("Aucun composant")
            
            col_nav1, col_nav2 = st.columns(2)
            with col_nav1:
                st.info("🔍 Fonctionnalité complète dans app.py")
            with col_nav2:
                if st.button("❌ Fermer", key="close_composants"):
                    st.session_state["view_section"] = None
        
        elif st.session_state["view_section"] == "users":
            st.markdown("**👥 Utilisateurs**")
            if len(users) > 0:
                user_data = []
                for username, user_info in users.items():
                    user_data.append({
                        "Utilisateur": username,
                        "Nom": user_info.get("nom", ""),
                        "Rôle": user_info.get("role", "")
                    })
                st.dataframe(pd.DataFrame(user_data), use_container_width=True)
            else:
                st.info("Aucun utilisateur")
            
            col_nav1, col_nav2 = st.columns(2)
            with col_nav1:
                st.info("🔍 Fonctionnalité complète dans app.py")
            with col_nav2:
                if st.button("❌ Fermer", key="close_users"):
                    st.session_state["view_section"] = None
    
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

