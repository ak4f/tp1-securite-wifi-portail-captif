"""
Script de test de validation locale pour le serveur d'interception HTTP.
Permet d'émettre une requête POST formatée vers http://127.0.0.1:8000/login.
Auteurs : ANATO Kodjo Freddy et GUENANON Ulysse
"""

import urllib.request
import urllib.parse
import sys

TARGET_URL = "http://127.0.0.1:8000/login"

def executer_test(login="etudiant1", password="demo1234"):
    payload = urllib.parse.urlencode({
        "login": login,
        "password": password
    }).encode("utf-8")

    requete = urllib.request.Request(
        TARGET_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    try:
        with urllib.request.urlopen(requete, timeout=3) as reponse:
            corps = reponse.read().decode("utf-8", errors="replace")
            if reponse.status == 200 and "Authentification" in corps:
                print(f"OK : Requête transmise avec succès (HTTP 200, identifiant: '{login}')")
                return True
            else:
                print(f"Statut HTTP inattendu : {reponse.status}")
                return False
    except Exception as e:
        print(f"Erreur de connexion vers {TARGET_URL} : {e}")
        print("Vérifiez que 'python demo_wifi/server_builtin.py' est démarré.")
        return False

if __name__ == "__main__":
    u = sys.argv[1] if len(sys.argv) > 1 else "etudiant1"
    p = sys.argv[2] if len(sys.argv) > 2 else "demo1234"
    succes = executer_test(u, p)
    sys.exit(0 if succes else 1)
