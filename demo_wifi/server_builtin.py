"""
Serveur de demonstration pedagogique - Utilise uniquement la bibliotheque standard Python.
Aucune dependance externe (pip / Flask) requise.
Interception de flux HTTP non chiffre.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class DemoHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            file_path = os.path.join(BASE_DIR, "index.html")
            if os.path.exists(file_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Fichier index.html introuvable")
        else:
            self.send_error(404, "Page non trouvee")

    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length).decode("utf-8", errors="replace")
            
            parsed_data = urllib.parse.parse_qs(post_body)
            login = parsed_data.get("login", [""])[0]
            password = parsed_data.get("password", [""])[0]

            print(f"[INTERCEPTION] Requete POST recue depuis {self.client_address[0]}")
            print(f" -> Identifiant : {login}")
            print(f" -> Mot de passe : {password}")
            print(f" -> Corps brut : {post_body}")

            response_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Reponse serveur</title>
  <style>
    body {{ font-family: Arial, sans-serif; background-color: #f4f6f8; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
    .card {{ background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); text-align: center; }}
    h3 {{ color: #2e7d32; }}
  </style>
</head>
<body>
  <div class="card">
    <h3>Connexion recue (Demonstration pedagogique)</h3>
    <p>L'identifiant <b>{login}</b> a ete transmis en clair au serveur.</p>
    <a href="/">Retour au formulaire</a>
  </div>
</body>
</html>"""
            
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(response_content.encode("utf-8"))
        else:
            self.send_error(404, "Route non trouvee")

    def log_message(self, format, *args):
        # Format sobre pour la console
        print(f"[REQUETE] {self.address_string()} - {format % args}")

if __name__ == "__main__":
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, DemoHTTPHandler)
    print(f"[DEMARRAGE] Serveur HTTP de demonstration actif sur le port {PORT}")
    print("[INFO] En attente de connexions sur l'interface locale ou Wi-Fi (0.0.0.0)...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nArret du serveur.")
        httpd.server_close()
