## 🎯 Objectif du projet

Ce projet a été réalisé dans le cadre du module **Malware et Sécurité Offensive en Python**.  
L’objectif est de comprendre l’architecture interne d’un ransomware moderne en développant un **client (malware pédagogique)** et un **serveur de contrôle (C2)** dans un environnement **strictement isolé** (VM dédiée).

Le projet permet d’explorer :
- la manipulation du système de fichiers  
- un chiffrement réversible simple (XOR)  
- la communication client/serveur  
- la structuration modulaire d’un malware  
- l’analyse des limites d’un ransomware artisanal  

Ce travail est **strictement pédagogique** et ne doit jamais être utilisé hors laboratoire.

---

## 🏗️ Architecture globale

Le projet est divisé en deux composants :

```
client/
│── main.py
│── crypto.py
│── system.py
│── network.py
│── commands.py

server/
│── main.py
│── handler.py
│── storage.py
│── victims.json
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
- **victims.json** : base de données locale  

---

## 🔐 Fonctionnalités implémentées

### ✔️ Côté client

- Génération d’une clé aléatoire depuis `/dev/urandom`  
- Filtrage ASCII pour obtenir uniquement `A-Z`  
- Récupération de l’UUID machine via `/proc/sys/kernel/random/uuid`  
- Chiffrement XOR réversible  
- Parcours récursif du `$HOME`  
- Communication TCP avec le serveur  
- Envoi initial : `{uuid, key}`  
- Réception et traitement de commandes (structure prête)  

### ✔️ Côté serveur

- Écoute TCP sur un port dédié  
- Gestion multi‑clients via threads  
- Parsing JSON ligne par ligne  
- Enregistrement des victimes dans `victims.json`  
- Architecture extensible pour les commandes C2  

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

### 📤 Commandes (structure prévue)

- `cmd` : exécution de commande système  
- `encrypt` / `decrypt` : opérations sur fichiers  
- `upload` / `download` : transfert de fichiers  

Ces commandes sont définies dans l’architecture mais leur logique dépend de l’implémentation choisie.

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
- envoie les informations  
- chiffre le `$HOME`  
- attend les commandes  

⚠️ **À exécuter uniquement dans une VM dédiée.**

---

## 🧪 Tests réalisés

- Vérification du XOR (chiffrement/déchiffrement identiques)  
- Test de génération de clé (32 caractères A‑Z)  
- Test de récupération UUID  
- Test de connexion client → serveur  
- Test d’enregistrement dans `victims.json`  
- Test de parsing JSON côté serveur  

---

## 🛡️ Limites et faiblesses du ransomware

Ce ransomware est **artisanal** et présente de nombreuses faiblesses :

### 🔸 Chiffrement faible
- XOR est trivial à casser  
- Clé transmise en clair au serveur  
- Pas de chiffrement asymétrique  

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
