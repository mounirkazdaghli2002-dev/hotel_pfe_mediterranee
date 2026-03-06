"""
Script pour lancer l'application Streamlit en arrière-plan
L'application sera accessible même après la fermeture de VS Code
"""
import subprocess
import sys
import os
import time
import threading

def launch_streamlit_background():
    """Lance Streamlit en arrière-plan sur Windows"""
    
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")
    
    print("=" * 50)
    print("🏨 Lancement Hotel Mediterranee en arriere-plan")
    print("=" * 50)
    print(f"Application: {app_path}")
    print("URL d'acces: http://localhost:8501")
    print("=" * 50)
    print("\nPour arreter l'application:")
    print("  - Ouvrez le Gestionnaire des taches")
    print("  - Cherchez 'streamlit.exe' ou 'python.exe'")
    print("  - Terminez le processus\n")
    
    # Commande pour lancer Streamlit en arriere-plan
    cmd = [sys.executable, "-m", "streamlit", "run", app_path, 
           "--server.port=8501", 
           "--server.address=localhost",
           "--server.headless=true",
           "--browser.gatherUsageStats=false"]
    
    # Creer un fichier de log pour voir les erreurs
    log_file = open("streamlit.log", "w")
    
    # Lancer le processus en arriere-plan (detache du terminal)
    # CREATE_NO_WINDOW = 0x08000000 pour ne pas afficher la fenetre
    # DETACHED_PROCESS = 0x00000008 pour detacher le processus
    process = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=log_file,
        stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    log_file.close()
    
    print(f"✅ Processus demarre (PID: {process.pid})")
    print("⏳ Demarrage du serveur Streamlit...")
    time.sleep(3)
    
    print("\n🎉 L'application est maintenant accessible!")
    print("📱 Ouvrez votre navigateur et allez sur: http://localhost:8501")
    
    # Ecrire le PID dans un fichier pour pouvoir arreter le processus plus tard
    with open("streamlit.pid", "w") as f:
        f.write(str(process.pid))
    
    return process

if __name__ == "__main__":
    launch_streamlit_background()
    print("\nAppuyez sur Entree pour fermer cette fenetre...")
    input()

