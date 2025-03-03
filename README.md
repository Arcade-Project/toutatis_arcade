## 📖 Présentation
Ce script permet de récupérer des informations sur un utilisateur Instagram à partir de son nom d'utilisateur et d'une session Instagram valide.

---

## 🛠️ Prérequis
Avant d'utiliser ce script, assure-toi d'avoir installé les dépendances nécessaires. Celles-ci sont listées dans le fichier `requirements.txt`.

## 🚀 Installation
1. Assure-toi d'avoir **Python 3.x** installé sur ton système.
2. Installe les dépendances en exécutant la commande suivante :
   ```sh
   pip install -r requirements.txt
   ```

---

## 🔧 Utilisation
Le script `core.py` s'exécute en ligne de commande avec les arguments suivants :

```sh
python core.py -s <SESSION_ID> -u <USERNAME>
```

### 📌 Arguments requis
- `-s`, `--sessionid` : ID de session Instagram (**obligatoire**)
- `-u`, `--username` : Nom d'utilisateur Instagram à analyser (**obligatoire**)

### 💡 Exemple d'exécution
```sh
python core.py -s 1234567890abcdef -u instagramuser
```

---

## 🎯 Fonctionnalités
✅ Récupère l'ID de l'utilisateur à partir de son nom d'utilisateur.
✅ Obtient les informations détaillées de l'utilisateur grâce à l'ID et la session Instagram.
✅ Récupère des informations avancées comme l'e-mail et le numéro de téléphone masqués.
✅ Affiche les données récupérées au format **JSON**, facilement lisible et exploitable.

---

## ⚠️ Remarque
🔹 Ce script peut être soumis aux **restrictions d'Instagram**, notamment en ce qui concerne la limite de requêtes (*rate limit*). 
🔹 En cas d'erreur, patiente quelques minutes avant de réessayer.
