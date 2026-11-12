# Travaux Pratiques N 1 : Attaque sur Reseau sans Fil Wi-Fi
## Vecteurs d'Attaque 802.11, Rogue AP, Portail Captif et Interception HTTP en Clair

* **Etablissement :** Institut de Formation et de Recherche en Informatique (IFRI) / Universite d'Abomey-Calavi (UAC)
* **Formation :** Master 2 en Informatique : Option Genie Logiciel (GL)
* **Annee Universitaire :** 2025-2026
* **Matiere :** Securisation des Bases de Donnees et des Programmes
* **Sous la direction de :** Dr Ing. ZANNOU Boris
* **Auteurs :** ANATO Kodjo Freddy & GUENANON Ulysse

---

## 1. Contexte et Objectifs du TP

Ce depot regroupe l'outillage logiciel, les scripts d'emulation, les captures de preuves Wireshark et le rapport academique officiel relatifs au TP 1.

L'objectif de cette experimentation est d'evaluer la confidentialite et l'integrite des echanges sur un reseau sans fil IEEE 802.11. L'etude demontre comment un point d'acces pirate (Rogue AP) associe a une mire d'authentification frauduleuse (portail captif) permet a un attaquant d'intercepter instantanement les identifiants d'utilisateurs legitimes lorsque le transport applicatif n'est pas protege par le protocole TLS.

---

## 2. Architecture du Banc d'Essai

L'experimentation a ete realisee sur une maquette physique reelle :

* **Station Victime :** Terminal mobile Android (modele 2409BRN2CA), adresse IP `10.155.228.10`, navigateur Chrome Mobile.
* **Canal sans fil :** Segment Wi-Fi local partage `10.155.228.0/24` (masque `255.255.255.0`), sans isolation des clients.
* **Station Attaquante :** PC portable sous Windows 11 Professionnel, adresse IP `10.155.228.110`, port d'ecoute `8000`.
* **Interface de Capture :** Carte physique Wi-Fi 2 pilotee par la couche Npcap en mode promiscuous sous Wireshark.
* **Serveur de Demonstration :** Script Python autonome sans dependance tierce (`demo_wifi/server_builtin.py`).

---

## 3. Demarrage Rapide et Reproduction

Le laboratoire peut etre reproduit et valide en deux commandes simples depuis la racine du depot.

### 3.1. Lancement du serveur HTTP captif
Dans un premier terminal :
```bash
python demo_wifi/server_builtin.py
```
Le serveur ecoute sur toutes les interfaces locales et sans fil (`0.0.0.0:8000`).

### 3.2. Execution du test de transmission
Dans un second terminal :
```bash
python demo_wifi/test_demo.py etudiant1 demo1234
```
La console du serveur affiche immediatement la capture des identifiants :
```text
[DEMARRAGE] Serveur HTTP de demonstration actif sur le port 8000
[INFO] En attente de connexions sur l'interface locale ou Wi-Fi (0.0.0.0)...
[INTERCEPTION] Requete POST recue depuis 127.0.0.1
 -> Identifiant : etudiant1
 -> Mot de passe : demo1234
 -> Corps brut : login=etudiant1&password=demo1234
```

### 3.3. Test depuis un smartphone sur le reseau local
1. Connecter le terminal mobile sur le meme point d'acces Wi-Fi.
2. Ouvrir le navigateur et se rendre sur `http://10.155.228.110:8000/`.
3. Saisir les identifiants de test et soumettre le formulaire.

---

## 4. Preuves Experimentales sous Wireshark

Pendant l'activite sur l'interface sans fil, la sonde a capture un flux global de **63 616 paquets**.

L'application du filtre d'affichage :
```text
http.request.method == "POST"
```
a permis d'isoler instantanement la requete d'authentification ciblee.

### Fiche technique de la trame de preuve N 11823 :
* **Protocole de transport :** TCP (port source ephemere 49832 vers port destination 8000).
* **Methode et cible :** `POST /login HTTP/1.1`.
* **Format des donnees :** `application/x-www-form-urlencoded`.
* **Charge utile capturee en texte clair :** `login=etudiant 1&password=demo1234`.
* **Constat :** Absence totale de TLS, compromission immediate du mot de passe des la premiere soumission.

Les captures d'ecran probantes sont consultables dans le repertoire `captures/` :
* `captures/figure_1_wireshark_credentials.png` : dissection de la trame 11823 sous Wireshark.
* `captures/figure_2_mobile_portal.png` : affichage du portail captif sur le terminal mobile Android.

---

## 5. Matrice des Contre-Mesures et Durcissement

| Vecteur de faille | Menace constatee | Contre-mesure obligatoire | Effet technique obtenu |
| :--- | :--- | :--- | :--- |
| **Transport HTTP en clair** | Interception passive des identifiants | **HTTPS / TLS 1.3** | Chiffrement complet de la couche applicative (corps POST opaque). |
| **Contournement de certificat** | Decapage SSL (SSL Stripping) | **En-tete HSTS** | Interdiction formelle du repli vers HTTP non securise. |
| **Segment sans fil ouvert** | Communication directe inter-stations | **Client Isolation** (AP Isolation) | Blocage des flux Ethernet niveau 2 entre clients d'un meme point d'acces. |
| **Segmentation reseau** | Acces aux serveurs sensibles | **VLAN dedie** | Isolement strict des hotes invites en DMZ etroite. |
| **Point d'acces pirate** | Usurpation de SSID (Evil Twin) | **WPA3-Enterprise / 802.1X** | Authentification mutuelle par certificats numeriques (PKI et RADIUS). |
| **Usage sur Wi-Fi non fiable** | Ecoute sur borne publique | **VPN de transport** | Tunnel chiffre de bout en bout (WireGuard ou IPsec). |

---

## 6. Structure du Depot

```text
tp1-securite-wifi-portail-captif/
|-- README.md                                    # Documentation officielle du laboratoire
|-- .gitignore                                   # Exclusions des caches Python et artefacts LaTeX
|-- demo_wifi/
|   |-- server_builtin.py                        # Serveur HTTP autonome (bibliotheque standard Python)
|   |-- server.py                                # Variante optionnelle sous Flask
|   |-- index.html                               # Formulaire HTML du portail d'authentification
|   `-- test_demo.py                             # Script de verification et test unitaire local
|-- captures/
|   |-- figure_1_wireshark_credentials.png       # Preuve Wireshark avec trame POST et mot de passe clair
|   `-- figure_2_mobile_portal.png               # Preuve visuelle du portail sur smartphone Android
|-- rapport/
|   |-- Rapport_TP1_Attaque_WiFi.pdf             # Rapport academique officiel de 12 pages (format PDF)
|   `-- rapport_tp1_wifi.tex                     # Source LaTeX complete du rapport
`-- presentation/
    |-- Slides_Soutenance_TP1.pdf                # Diapositives de soutenance Beamer
    `-- Presentation_TP1_Attaque_WiFi_Epuree.pptx # Support PowerPoint de presentation
```

---

## 7. Livrables Academiques

* **Rapport officiel complet :** [`rapport/Rapport_TP1_Attaque_WiFi.pdf`](rapport/Rapport_TP1_Attaque_WiFi.pdf)
* **Support de soutenance :** [`presentation/Slides_Soutenance_TP1.pdf`](presentation/Slides_Soutenance_TP1.pdf)
