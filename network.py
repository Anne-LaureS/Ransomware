"""
Module network.py
-----------------

Ce module gère la communication réseau entre le client pédagogique
et le serveur C2. Il fournit une classe simple permettant :

- d'établir une connexion TCP
- d'envoyer des messages JSON
- de recevoir des messages JSON ligne par ligne

Aucune action sensible n'est implémentée ici.
"""

import json
import socket
from typing import Dict, Any


class ClientConnection:
    """
    Classe représentant la connexion réseau du client vers le serveur.
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = None
        self.buffer = ""

    def connect(self) -> None:
        """
        Établit une connexion TCP vers le serveur.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_json(self, data: Dict[str, Any]) -> None:
        """
        Envoie un dictionnaire JSON au serveur, suivi d'un saut de ligne.
        """
        try:
            message = json.dumps(data) + "\n"
            self.sock.sendall(message.encode())
        except Exception as e:
            print(f"[ERROR] Impossible d'envoyer le message : {e}")

    def recv_json(self) -> Dict[str, Any]:
        """
        Reçoit un message JSON complet (terminé par un '\n').
        Retourne un dictionnaire Python.
        """
        try:
            data = self.sock.recv(4096)
            if not data:
                return {}

            self.buffer += data.decode()

            if "\n" not in self.buffer:
                return {}

            line, self.buffer = self.buffer.split("\n", 1)

            try:
                return json.loads(line)
            except json.JSONDecodeError:
                print("[ERROR] Message JSON invalide reçu")
                return {}

        except Exception as e:
            print(f"[ERROR] Erreur réseau : {e}")
            return {}
