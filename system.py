"""
Module system.py
----------------

Ce module regroupe les fonctions liées au système de fichiers :

- récupération de l'UUID machine
- gestion des chemins
- structure pour le chiffrement/déchiffrement local

Les fonctions sensibles (chiffrement réel, écriture de fichiers)
sont volontairement laissées à compléter dans un environnement
de laboratoire contrôlé.
"""

from pathlib import Path
from typing import Optional


def get_machine_uuid() -> str:
    """
    Récupère l'UUID unique de la machine depuis /proc.
    """
    try:
        with open("/proc/sys/kernel/random/uuid", "r") as f:
            return f.read().strip()
    except Exception:
        return "unknown-uuid"


# Dossiers à exclure pour éviter les problèmes dans un environnement réel
EXCLUDED_DIRS = {
    ".cache",
    ".config",
    ".local",
    ".vscode-server",
    ".ssh",
    ".gnupg",
    ".mozilla",
    ".thunderbird",
    "snap",
}


def should_exclude(path: Path) -> bool:
    """
    Détermine si un fichier ou dossier doit être exclu du traitement.
    """
    return any(part in EXCLUDED_DIRS for part in path.parts)


def encrypt_file(path: Path, key: str) -> None:
    """
    Squelette de fonction pour chiffrer un fichier local.
    À compléter dans un environnement de laboratoire.

    Paramètres :
        path : chemin du fichier
        key  : clé de chiffrement
    """
    # TODO : lire le fichier, appliquer XOR, réécrire
    pass


def decrypt_file(path: Path, key: str) -> None:
    """
    Squelette de fonction pour déchiffrer un fichier local.
    """
    # TODO : même logique que encrypt_file
    pass


def encrypt_directory(root: Path, key: str):
    """
    Parcourt récursivement un dossier et applique le chiffrement
    aux fichiers non exclus.
    """
    for path in root.rglob("*"):
        if path.is_file() and not should_exclude(path):
           encrypt_file(path, key)
            pass


def decrypt_directory(root: Path, key: str) -> None:
    """
    Parcourt récursivement un dossier et applique le déchiffrement.
    """
    for path in root.rglob("*"):
        if path.is_file() and not should_exclude(path):
            # TODO : appeler decrypt_file(path, key)
            pass
