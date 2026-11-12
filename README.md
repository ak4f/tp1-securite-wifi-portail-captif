# Travaux Pratiques N° 1 : Attaque sur Réseau sans Fil Wi-Fi
## Vecteurs d'Attaque 802.11, Rogue AP, Portail Captif et Interception HTTP en Clair

* **Établissement :** Institut de Formation et de Recherche en Informatique (IFRI) / Université d'Abomey-Calavi (UAC)
* **Formation :** Master 2 en Informatique : Option Génie Logiciel (GL)
* **Année Universitaire :** 2025-2026
* **Matière :** Sécurisation des Bases de Données et des Programmes
* **Sous la direction de :** Dr Ing. ZANNOU Boris
* **Auteurs :** ANATO Kodjo Freddy et GUENANON Ulysse
* **Dépôt officiel :** [https://github.com/ak4f/tp1-securite-wifi-portail-captif](https://github.com/ak4f/tp1-securite-wifi-portail-captif)

---

## 1. Contexte et Objectifs du TP

Ce dépôt regroupe l'outillage logiciel, les scripts d'émulation, les captures de preuves Wireshark (.pcap natif et extraits visuels) ainsi que le rapport académique officiel de 14 pages relatif au TP 1.

L'objectif de cette expérimentation est d'évaluer la confidentialité et l'intégrité des échanges sur un réseau local sans fil IEEE 802.11. L'étude démontre comment un point d'accès pirate (Rogue AP ou Evil Twin) associé à une mire d'authentification frauduleuse (portail captif) permet à un attaquant d'intercepter instantanément les identifiants d'utilisateurs légitimes lorsque le transport applicatif n'est pas protégé par le protocole TLS.

---

## 2. Architecture du Banc d'Essai

L'expérimentation a été réalisée sur une maquette physique réelle :

* **Station Victime :** Terminal mobile Android (modèle 2409BRN2CA), adresse IP `10.155.228.10`, navigateur Chrome Mobile.
* **Canal sans fil :** Segment Wi-Fi local partagé `10.155.228.0/24` (masque `255.255.255.0`), sans isolation des clients.
* **Station Attaquante :** PC portable sous Windows 11 Professionnel, adresse IP `10.155.228.110`, port d'écoute `8000`.
* **Interface de Capture :** Carte physique Wi-Fi 2 pilotée par la couche Npcap en mode promiscuous sous Wireshark.
* **Serveur de Démonstration :** Script Python autonome sans dépendance tierce (`demo_wifi/server_builtin.py`).

---

## 3. Démarrage Rapide et Reproduction

Le laboratoire peut être reproduit et validé en deux commandes depuis la racine du dépôt.

### 3.1. Lancement du serveur HTTP captif
Dans un premier terminal :
```bash
python demo_wifi/server_builtin.py
```
Le serveur écoute sur toutes les interfaces locales et sans fil (`0.0.0.0:8000`).

### 3.2. Exécution du test de transmission
Dans un second terminal :
```bash
python demo_wifi/test_demo.py etudiant1 demo1234
```
La console du serveur affiche immédiatement la capture des identifiants :
```text
Serveur HTTP actif sur http://0.0.0.0:8000 (écoute sur toutes les interfaces)
[2026-11-12 14:15:22] POST /login depuis 127.0.0.1 : login='etudiant1', password='demo1234'
[2026-11-12 14:15:22] 127.0.0.1 : "POST /login HTTP/1.1" 200 -
```
Le script de test confirme la transmission :
```text
OK : Requête transmise avec succès (HTTP 200, identifiant: 'etudiant1')
```

### 3.3. Test depuis un smartphone sur le réseau local
1. Connecter le terminal mobile sur le même point d'accès Wi-Fi.
2. Ouvrir le navigateur et se rendre sur `http://10.155.228.110:8000/`.
3. Saisir les identifiants de test et soumettre le formulaire.

---

## 4. Preuves Expérimentales sous Wireshark

Pendant l'activité sur l'interface sans fil, la sonde a capturé un flux global de **63 616 paquets**.

L'application du filtre d'affichage :
```text
http.request.method == "POST"
```
a permis d'isoler instantanément la requête d'authentification ciblée.

### Fiche technique de la trame de preuve N° 11823 :
* **Protocole de transport :** TCP (port source éphémère 49832 vers port destination 8000).
* **Méthode et cible :** `POST /login HTTP/1.1`.
* **Format des données :** `application/x-www-form-urlencoded`.
* **Charge utile capturée en texte clair :** `login=etudiant 1&password=demo1234`.
* **Constat :** Absence totale de TLS, compromission immédiate du mot de passe dès la première soumission.

Le fichier de capture natif et les captures d'écran probantes sont consultables dans le répertoire `captures/` :
* `captures/capture_tp1_http_credentials.pcap` : trace réseau native ouvrable directement dans Wireshark (Fichier > Ouvrir).
* `captures/figure_1_wireshark_credentials.png` : dissection de la trame sous Wireshark.
* `captures/figure_2_mobile_portal.png` : affichage du portail captif sur le terminal mobile Android.

---

## 5. Matrice des Contre-Mesures et Durcissement

| Vecteur de faille | Menace constatée | Contre-mesure obligatoire | Effet technique obtenu |
| :--- | :--- | :--- | :--- |
| **Transport HTTP en clair** | Interception passive des identifiants | **HTTPS / TLS 1.3** | Chiffrement complet de la couche applicative (corps POST opaque). |
| **Contournement de certificat** | Décapage SSL (SSL Stripping) | **En-tête HSTS** | Interdiction formelle du repli vers HTTP non sécurisé. |
| **Segment sans fil ouvert** | Communication directe inter-stations | **Client Isolation** (AP Isolation) | Blocage des flux Ethernet niveau 2 entre clients d'un même point d'accès. |
| **Segmentation réseau** | Accès aux serveurs sensibles | **VLAN dédié** | Isolement strict des hôtes invités en DMZ étroite. |
| **Point d'accès pirate** | Usurpation de SSID (Evil Twin) | **WPA3-Enterprise / 802.1X** | Authentification mutuelle par certificats numériques (PKI et RADIUS). |
| **Usage sur Wi-Fi non fiable** | Écoute sur borne publique | **VPN de transport** | Tunnel chiffré de bout en bout (WireGuard ou IPsec). |

### 5.1. Exemple de configuration Nginx (TLS 1.3 et HSTS)
```nginx
server {
    listen 443 ssl http2;
    server_name portail.ifri.uac.bj;

    ssl_certificate /etc/ssl/certs/portail.crt;
    ssl_certificate_key /etc/ssl/private/portail.key;
    ssl_protocols TLSv1.3;
    ssl_prefer_server_ciphers off;

    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

### 5.2. Isolation client sous hostapd
```ini
interface=wlan0
driver=nl80211
ssid=IFRI-Etudiants-Securise
hw_mode=g
channel=6
wmm_enabled=1
ap_isolate=1
```

---

## 6. Structure du Dépôt

```text
tp1-securite-wifi-portail-captif/
|-- README.md                                    # Documentation officielle du laboratoire
|-- .gitignore                                   # Exclusions des caches Python et artefacts LaTeX
|-- demo_wifi/
|   |-- server_builtin.py                        # Serveur HTTP autonome (bibliothèque standard Python)
|   |-- server.py                                # Variante optionnelle sous Flask
|   |-- index.html                               # Formulaire HTML du portail d'authentification
|   `-- test_demo.py                             # Script de vérification et test unitaire local
|-- captures/
|   |-- capture_tp1_http_credentials.pcap        # Trace réseau native ouvrable directement sous Wireshark
|   |-- figure_1_wireshark_credentials.png       # Preuve Wireshark avec trame POST et mot de passe clair
|   `-- figure_2_mobile_portal.png               # Preuve visuelle du portail sur smartphone Android
|-- rapport/
|   |-- Rapport_TP1_Attaque_WiFi.pdf             # Rapport académique officiel de 14 pages (format PDF)
|   `-- rapport_tp1_wifi.tex                     # Source LaTeX complète du rapport
`-- presentation/
    |-- Slides_Soutenance_TP1.pdf                # Diapositives de soutenance Beamer
    `-- Presentation_TP1_Attaque_WiFi_Epuree.pptx # Support PowerPoint de présentation
```

---

## 7. Livrables Académiques

* **Rapport officiel complet :** [`rapport/Rapport_TP1_Attaque_WiFi.pdf`](rapport/Rapport_TP1_Attaque_WiFi.pdf) (14 pages)
* **Support de soutenance :** [`presentation/Slides_Soutenance_TP1.pdf`](presentation/Slides_Soutenance_TP1.pdf)
