"""
Script de test unitaire et de verification locale de la chaine d'interception HTTP.
Permet a Ulysse ou a l'evaluateur de tester la soumission et la reception sans materiel supplementaire.
Auteurs : ANATO Freddy & GUENANON Ulysse
"""

import urllib.request
import urllib.parse
import sys

TARGET_URL = "http://127.0.0.1:8000/login"

def tester_soumission(login="etudiant1", password="demo1234"):
    print(f"[TEST] Envoi de la requete d'authentification vers {TARGET_URL}...")
    donnees = urllib.parse.urlencode({
        "login": login,
        "password": password
    }).encode("utf-8")

    requete = urllib.request.Request(
        TARGET_URL,
        data=donnees,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    try:
        with urllib.request.urlopen(requete, timeout=5) as reponse:
            corps = reponse.read().decode("utf-8", errors="replace")
            print(f"[TEST] Reponse recue avec statut HTTP {reponse.status}")
            if "Connexion recue" in corps:
                print("[TEST] Succes : Le serveur a bien receptionne et traite la requete HTTP en clair.")
                return True
            else:
                print("[TEST] Avertissement : Reponse inattendue.")
                return False
    except Exception as e:
        print(f"[ERREUR] Impossible de joindre le serveur de demonstration : {e}")
        print("[CONSEIL] Assurez-vous d'avoir demarre 'python server_builtin.py' prealablement.")
        return False

if __name__ == "__main__":
    login_arg = sys.argv[1] if len(sys.argv) > 1 else "etudiant1"
    pass_arg = sys.argv[2] if len(sys.argv) > 2 else "demo1234"
    succes = tester_soumission(login_arg, pass_arg)
    sys.exit(0 if succes else 1)
