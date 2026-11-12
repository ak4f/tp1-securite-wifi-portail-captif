"""
Serveur de demonstration pedagogique utilisant Flask.
Interception de donnees transmises en clair via HTTP.
"""

from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    file_path = os.path.join(BASE_DIR, "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@app.route("/login", methods=["POST"])
def login():
    login_val = request.form.get("login")
    password_val = request.form.get("password")
    
    print(f"[INTERCEPTION] Requete recue -> identifiant: {login_val} | mot de passe: {password_val}")
    
    return """
    <html>
      <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
        <h3 style="color: #2e7d32;">Connexion recue (demo pedagogique)</h3>
        <p>Les donnees ont bien ete interceptees cote serveur.</p>
        <a href="/">Retour</a>
      </body>
    </html>
    """

if __name__ == "__main__":
    print("Demarrage du serveur Flask sur http://0.0.0.0:8000 ...")
    app.run(host="0.0.0.0", port=8000)
