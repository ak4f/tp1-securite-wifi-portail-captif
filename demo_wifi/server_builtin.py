"""
Serveur de démonstration pédagogique : interception de flux HTTP non chiffré.
Bibliothèque standard Python 3 uniquement (sans dépendance tierce).
Auteurs : ANATO Kodjo Freddy et GUENANON Ulysse
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
import time

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class DemoHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
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
            self.send_error(404, "Ressource non trouvée")

    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length).decode("utf-8", errors="replace")
            
            parsed_data = urllib.parse.parse_qs(post_body)
            login = parsed_data.get("login", [""])[0]
            password = parsed_data.get("password", [""])[0]

            client_ip = self.client_address[0]
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] POST /login depuis {client_ip} : login='{login}', password='{password}'")

            response_content = (
                "<!DOCTYPE html>\n"
                "<html lang=\"fr\">\n"
                "<head>\n"
                "  <meta charset=\"UTF-8\">\n"
                "  <title>Authentification reçue</title>\n"
                "  <style>\n"
                "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }\n"
                "    .card { background: #ffffff; padding: 32px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; text-align: center; max-width: 400px; }\n"
                "    h3 { color: #166534; margin-top: 0; font-size: 18px; }\n"
                "    p { color: #475569; font-size: 14px; line-height: 1.5; }\n"
                "    a { display: inline-block; margin-top: 16px; color: #0284c7; text-decoration: none; font-size: 14px; font-weight: 500; }\n"
                "  </style>\n"
                "</head>\n"
                "<body>\n"
                "  <div class=\"card\">\n"
                "    <h3>Authentification enregistrée</h3>\n"
                f"    <p>Identifiant reçu en clair : <strong>{login}</strong></p>\n"
                "    <p>Démonstration de vulnérabilité : transmission en texte brut sans couche TLS.</p>\n"
                "    <a href=\"/\">Retour au formulaire</a>\n"
                "  </div>\n"
                "</body>\n"
                "</html>\n"
            )
            
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(response_content.encode("utf-8"))
        else:
            self.send_error(404, "Route non trouvée")

    def log_message(self, format, *args):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {self.address_string()} : {format % args}")

if __name__ == "__main__":
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, DemoHTTPHandler)
    print(f"Serveur HTTP actif sur http://0.0.0.0:{PORT} (écoute sur toutes les interfaces)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du serveur.")
        httpd.server_close()
