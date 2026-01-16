## 🎯 Objectif du projet

Ce projet a été réalisé dans le cadre du module **Ecriture d'un malware en Python**.  
L’objectif est de comprendre l’architecture interne d’un ransomware moderne en développant :
- un **client (malware pédagogique)**
- un **serveur de contrôle (C2)**
- un **protocole de communication** simple basé en JSON
Le tout dans un environnement **strictement isolé** (VM dédiée).

Le projet permet d’explorer :
- la manipulation du système de fichiers  
- un chiffrement réversible simple (XOR)  
- la communication client/serveur  
- la structuration modulaire d’un malware  
- l’analyse des limites d’un ransomware artisanal  

### ⚠️ Ce travail est **strictement pédagogique** et ne doit jamais être utilisé hors laboratoire (VM dédiée).

---

## 🏗️ Architecture globale

Le projet est composé de la manière suivante :
```text
                +----------------------+
                |      Opérateur       |
                |  (menu texte C2)     |
                +----------+-----------+
                           |
                           v
                  +--------+--------+
                  |     Serveur C2  |
                  |  main.py        |
                  |  handler.py     |
                  |  storage.py     |
                  +--------+--------+
                           |
                 Connexions TCP (JSON)
                           |
           +---------------+----------------+
           |                                |
           v                                v
 +-------------------+             +-------------------+
 |     Client 1      |             |     Client 2      |
 |  main.py          |             |  main.py          |
 |  network.py       |             |  network.py       |
 |  system.py        |             |  system.py        |
 |  crypto.py        |             |  crypto.py        |
 |  commands.py      |             |  commands.py      |
 | ransomware_test/  |             | ransomware_test/  |
 +-------------------+             +-------------------+
```

### 🔹 Côté client

- **crypto.py** : génération de clé + XOR  
- **system.py** : UUID machine + chiffrement/déchiffrement fichiers  
- **network.py** : communication TCP avec le serveur  
- **commands.py** : exécution des commandes reçues  
- **main.py** : point d’entrée, enregistrement, chiffrement, boucle de commandes  

### 🔹 Côté serveur

- **main.py** : socket d’écoute + gestion multi‑clients  
- **handler.py** : parsing JSON + traitement des messages  
- **storage.py** : stockage persistant des victimes  
- **operator_menu.py** : interface texte permettant à l’opérateur d’interagir avec le serveur (liste des victimes, envoi de commandes JSON, gestion des UUID connectés)
- **victims.json** : base de données locale des machines enregistrées

---

## 🔐 Fonctionnalités implémentées

### ✔️ Côté client

- Génération d’une clé aléatoire `A-Z`  
- Récupération de l’UUID machine via `/proc/sys/kernel/random/uuid`
- Envoi initial : `{uuid, key}` 
- Chiffrement XOR réversible de ~/ransomware_test 
- Parcours récursif du `$HOME`  
- Communication TCP avec le serveur  
- Réception et traitement structurés de commandes

### ✔️ Côté serveur

- Écoute TCP sur un port dédié  
- Gestion multi‑clients via threads  
- Parsing JSON ligne par ligne  
- Enregistrement des victimes dans `victims.json`  
- Affichage propre des réponses ([RESULT]...)

---

## 🔌 Protocole de communication

Les messages échangés entre client et serveur utilisent un format **JSON** simple, envoyés **ligne par ligne**.

### 📥 Enregistrement du client

**Client → Serveur**

```json
{
  "type": "register",
  "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "key": "ABCDEFGHIJKLMNOPQRSTUVWXYZ..."
}
```

### 📤 Commandes C2

**Serveur → Client**

```json
{"type": "encrypt"}
{"type": "decrypt"}
{"type": "ls"}
{"type": "pwd"}
{"type": "uname"}
{"type": "cmd", "command": "texte"}  
```
La commande cmd est volontairement non exécutée. Elle sert uniquement à montrer comment un ransomware pourrait recevoir une commande système, mais sans jamais l’exécuter pour des raisons de sécurité.

### 📬 Réponses du client

**Client → Serveur**

```json
{"type": "ls_result", "files": [...]}
{"type": "pwd_result", "cwd": "..."}
{"type": "encrypt_result", "status": "ok"}
```

---

## ▶️ Comment lancer le projet

### 1. Lancer le serveur

Depuis le dossier `server/` :

```
python3 main.py
```

Le serveur :

- charge les victimes existantes  
- écoute sur `0.0.0.0:4444`  
- crée un thread par client  

### 2. Lancer le client

Depuis le dossier `client/` :

```
python3 main.py
```

Le client :

- génère une clé  
- récupère l’UUID  
- se connecte au serveur  
- chiffre le dossier test
- attend les commandes

---

## 🧪 Tests réalisés

- Vérification du XOR (encrypt/decrypt identiques)
- Test de génération de clé (32 caractères A‑Z)
- Test de récupération UUID
- Test de connexion client → serveur
- Test d’enregistrement dans victims.json
- Test des commandes pédagogiques (ls, pwd, uname)
- Test du cycle complet encrypt → decrypt

---

## 🛡️ Limites et faiblesses volontaires du ransomware

Ce ransomware est **artisanal** et présente de nombreuses faiblesses :

### 🔸 Chiffrement faible
- XOR est trivial à casser  
- Clé transmise en clair au serveur  
- Pas de chiffrement asymétrique (RSA/AES)

### 🔸 Détection facile
- Activité réseau non chiffrée  
- Parcours récursif du home détectable  
- Pas d’obfuscation du code  

### 🔸 Architecture simplifiée
- Pas de persistance  
- Pas de mécanisme d’évasion  
- Pas de chiffrement des communications  

### 🔸 Serveur vulnérable
- Pas d’authentification  
- Pas de chiffrement TLS  
- Pas de gestion avancée des erreurs  

Ces faiblesses sont **volontaires** dans un cadre pédagogique.

---

## 📚 Conclusion

Ce projet permet de comprendre :

- comment un ransomware structure ses modules  
- comment fonctionne un C2 basique  
- comment un chiffrement réversible peut être implémenté  
- quelles sont les limites d’un malware artisanal  

Il constitue une base solide pour analyser, améliorer ou sécuriser des environnements face à ce type de menace.
