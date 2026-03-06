import re

# Read the file
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the checkin_client function
old_func = '''def checkin_client(nom, chambre, date_arrivee, date_depart):
    """Enregistre un client et change le statut de la chambre"""
    clients = load_clients()
    rooms = load_rooms()
    
    new_client = pd.DataFrame([{
        "id": len(clients) + 1,
        "nom": nom,
        "chambre": chambre,
        "date_arrivee": date_arrivee,
        "date_depart": date_depart,
        "actif": True
    }])
    clients = pd.concat([clients, new_client], ignore_index=True)
    save_clients(clients)
    
    # Mettre a jour le statut de la chambre
    rooms.loc[rooms["numero"] == chambre, "statut"] = "Occupée"
    save_rooms(rooms)
    
    return clients'''

new_func = '''def checkin_client(nom, chambre, date_arrivee, date_depart):
    """Enregistre un client et change le statut de la chambre"""
    clients = load_clients()
    rooms = load_rooms()
    
    # Convertir chambre en string pour la comparaison
    chambre_str = str(chambre)
    
    new_client = pd.DataFrame([{
        "id": len(clients) + 1,
        "nom": nom,
        "chambre": chambre,
        "date_arrivee": date_arrivee,
        "date_depart": date_depart,
        "actif": True
    }])
    clients = pd.concat([clients, new_client], ignore_index=True)
    save_clients(clients)
    
    # Mettre a jour le statut de la chambre - convertir en string pour la comparaison
    rooms["numero"] = rooms["numero"].astype(str)
    rooms.loc[rooms["numero"] == chambre_str, "statut"] = "Occupée"
    save_rooms(rooms)
    
    return clients'''

content = content.replace(old_func, new_func)

# Write the file
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Function updated successfully!')

