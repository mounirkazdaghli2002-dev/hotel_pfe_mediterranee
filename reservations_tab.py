import streamlit as st
import pandas as pd
from datetime import datetime
from app import load_reservations, get_reservations_stats, get_upcoming_checkins, create_reservation, load_rooms, delete_reservation

def reservations_tab(role, rooms):
    """Complete reservations tab content"""
    st.subheader("📅 Gestion des Réservations" + (" - Admin" if role == 'admin' else ''))
    
    total_res, confirmed_res, pending_res, res_occupancy = get_reservations_stats()
    upcoming_checkins = get_upcoming_checkins()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total", total_res)
    with col2:
        st.metric("Confirmées", confirmed_res)
    with col3:
        st.metric("En attente", pending_res)
    with col4:
        st.metric("Occupation", f"{res_occupancy:.1f}%")

    st.markdown("---")
    st.metric("Check-ins aujourd'hui", upcoming_checkins)
    
    # Reservations list
    reservations_df = load_reservations()
    if not reservations_df.empty:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            status_filter = st.selectbox("Statut", ["Tous"] + sorted(reservations_df["statut"].dropna().unique()))
        with col_f2:
            chambre_filter = st.selectbox("Chambre", ["Toutes"] + sorted(reservations_df["numero_chambre"].dropna().unique()))
        
        filtered_res = reservations_df.copy()
        if status_filter != "Tous":
            filtered_res = filtered_res[filtered_res["statut"] == status_filter]
        if chambre_filter != "Toutes":
            filtered_res = filtered_res[filtered_res["numero_chambre"] == chambre_filter]
        
        st.dataframe(filtered_res, use_container_width=True)
        
        # Admin delete actions
        if role == 'admin':
            st.markdown("---")
            for idx, row in filtered_res.iterrows():
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🗑️ #{row['id']}", key=f"delete_res_{row['id']}"):
                        success, msg = delete_reservation(row['id'])
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
    else:
        st.info("📭 Aucune réservation")
    
    # Create new reservation
    st.markdown("---")
    with st.expander("➕ Nouvelle Réservation"):
        with st.form("new_res_form" + ("_admin" if role == 'admin' else '')):
            col_n1, col_n2 = st.columns(2)
            with col_n1:
                nom_client = st.text_input("👤 Nom Client")
                num_chambre = st.selectbox("🛏️ Chambre", rooms[rooms["statut"] != "Maintenance"]["numero"].tolist())
                date_arr = st.date_input("📅 Date Arrivée", value=datetime.now().date())
            with col_n2:
                date_dep = st.date_input("📅 Date Départ", value=datetime.now().date() + pd.Timedelta(days=1))
                tel = st.text_input("📞 Téléphone")
                email = st.text_input("📧 Email")
            
            notes = st.text_area("📝 Notes")
            
            if st.form_submit_button("✅ Créer"):
                if date_arr >= date_dep:
                    st.error("❌ Date départ doit être après date arrivée")
                else:
                    success, msg = create_reservation(nom_client, num_chambre, date_arr, date_dep, tel, email, "Confirmée", notes)
                    if success:
                        st.success(msg)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(msg)
