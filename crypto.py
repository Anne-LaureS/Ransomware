"""
Module crypto.py
----------------

Ce module regroupe les fonctions cryptographiques du client pédagogique :

- génération d'une clé aléatoire
- structure pour le chiffrement XOR

Les opérations sensibles (application réelle du XOR sur des fichiers)
sont volontairement laissées à compléter dans un environnement
de laboratoire contrôlé.
"""

import os
from typing import ByteString


def generate_key(length: int = 32) -> str:
    """
    Génère une clé aléatoire composée uniquement de lettres A-Z.

    Paramètres :
        length : longueur de la clé (32 par défaut)

    Retour :
        Une chaîne de caractères aléatoire en majuscules.
    """
    raw = os.urandom(length)
    key = "".join(chr((b % 26) + 65) for b in raw)
    return key


def xor_data(data: ByteString, key: str) -> bytes:
    """
    Structure de fonction pour appliquer un XOR entre des données
    et une clé répétée.

    Paramètres :
        data : données brutes (bytes)
        key  : clé de chiffrement (str)

    Retour :
        Les données XORées (bytes)
    """
    # TODO : implémenter le XOR réel dans ta VM
    # Exemple de structure :
    #
    # key_bytes = key.encode()
    # out = bytearray()
    # for i, b in enumerate(data):
    #     out.append(b ^ key_bytes[i % len(key_bytes)])
    # return bytes(out)

    return data  # placeholder pédagogique
