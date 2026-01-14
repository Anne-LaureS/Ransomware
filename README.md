## Structure du projet 

Dossier client/
│── main.py
│── crypto.py
│── system.py
│── network.py
│── commands.py

Dossier server/
- main.py → point d’entrée, socket d’écoute, boucle d’acceptation
- client_manager.py → gestion des connexions clientes (threads ou select)
- storage.py → stockage persistant des {uuid, key} (JSON ou SQLite)
- commands.py → interface pour envoyer des commandes à un client donné
