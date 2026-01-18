# Guide d'Installation et d'Utilisation - Module de Blog Interactif

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel, pour le versioning)

## 🚀 Installation

### 1. Cloner ou télécharger le projet

```bash
# Si vous utilisez Git
git clone <url-du-repository>
cd monprojet

# Ou téléchargez et décompressez le dossier du projet
```

### 2. Créer un environnement virtuel (recommandé)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Si le fichier `requirements.txt` n'existe pas, installez manuellement :

```bash
pip install django pillow
```

### 4. Configuration de la base de données

```bash
# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

### 5. Créer un superutilisateur (optionnel)

```bash
python manage.py createsuperuser
```

### 6. Lancer le serveur de développement

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : `http://127.0.0.1:8000/`

## 📱 Guide d'Utilisation

### Pour les Visiteurs (Non connectés)

- **Consulter les articles** : Accédez à la page d'accueil pour voir la liste des articles
- **Lire un article** : Cliquez sur un article pour le lire en détail
- **Voir les commentaires** : Les commentaires sont visibles sous chaque article

### Pour les Utilisateurs Connectés

#### 1. Inscription et Connexion

- **S'inscrire** : Cliquez sur "S'inscrire" et remplissez le formulaire
- **Se connecter** : Utilisez vos identifiants sur la page de connexion
- **Se déconnecter** : Cliquez sur "Déconnexion" dans le menu

#### 2. Gestion des Articles

- **Créer un article** : 
  - Cliquez sur "Nouvel Article"
  - Remplissez le titre et le contenu
  - Ajoutez une image (optionnel)
  - Cliquez sur "Publier"

- **Modifier un article** :
  - Seul l'auteur peut modifier son article
  - Cliquez sur "Modifier" sur la page de détail de l'article
  - Effectuez vos modifications et sauvegardez

- **Supprimer un article** :
  - Seul l'auteur peut supprimer son article
  - Cliquez sur "Supprimer" sur la page de détail de l'article

#### 3. Système de "J'aime"

- **Liker un article** : Cliquez sur le bouton "❤️" ou "J'aime"
- **Retirer un like** : Cliquez à nouveau sur le bouton pour retirer votre like
- **Voir les likes** : Le nombre total de likes est affiché sous chaque article

#### 4. Système de Commentaires

- **Commenter un article** :
  - Utilisez le formulaire en bas de la page de détail de l'article
  - Tapez votre commentaire et cliquez sur "Publier"

- **Répondre à un commentaire** :
  - Cliquez sur "Répondre" sous le commentaire souhaité
  - Tapez votre réponse et cliquez sur "Publier"

- **Hiérarchie des commentaires** :
  - Les réponses sont indentées sous le commentaire parent
  - Vous pouvez répondre à une réponse pour créer des conversations

## 🔧 Administration

### Accès à l'interface d'administration

1. Créez un superutilisateur (voir section installation)
2. Accédez à `http://127.0.0.1:8000/admin/`
3. Connectez-vous avec vos identifiants de superutilisateur

### Fonctionnalités d'administration

- **Gestion des utilisateurs** : Créer, modifier, supprimer des comptes
- **Modération des articles** : Voir, modifier, supprimer tous les articles
- **Modération des commentaires** : Gérer tous les commentaires
- **Statistiques** : Voir les likes et interactions

## 🛠️ Structure du Projet

```
monprojet/
├── blog/                    # Application principale
│   ├── migrations/         # Migrations de base de données
│   ├── templates/          # Templates HTML
│   │   ├── blog/          # Templates spécifiques au blog
│   │   ├── registration/  # Templates d'authentification
│   │   └── base.html      # Template de base
│   ├── models.py          # Modèles de données
│   ├── views.py           # Vues (logique métier)
│   ├── forms.py           # Formulaires
│   ├── urls.py            # URLs de l'application
│   └── admin.py           # Configuration admin
├── monprojet/              # Configuration du projet
│   ├── settings.py        # Paramètres Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuration WSGI
├── db.sqlite3             # Base de données SQLite
└── manage.py              # Script de gestion Django
```

## 🔍 Fonctionnalités Principales

### ✅ Implémentées

- [x] Authentification (inscription, connexion, déconnexion)
- [x] CRUD complet des articles
- [x] Système de likes avec toggle
- [x] Commentaires hiérarchiques (réponses aux commentaires)
- [x] Interface responsive
- [x] Sécurité (permissions, CSRF protection)
- [x] Validation des formulaires

### 🎯 Caractéristiques Techniques

- **Framework** : Django 4.x
- **Base de données** : SQLite (développement)
- **Frontend** : HTML5, CSS3, Bootstrap
- **Sécurité** : Protection CSRF, authentification requise
- **Performance** : Requêtes optimisées, pagination

## 🐛 Dépannage

### Problèmes Courants

1. **Erreur de migration** :
   ```bash
   python manage.py makemigrations blog
   python manage.py migrate
   ```

2. **Problème de permissions** :
   - Vérifiez que l'utilisateur est connecté
   - Seul l'auteur peut modifier/supprimer ses articles

3. **Images ne s'affichent pas** :
   - Vérifiez que `MEDIA_URL` et `MEDIA_ROOT` sont configurés
   - Assurez-vous que Pillow est installé

4. **Erreur 404** :
   - Vérifiez que les URLs sont correctement configurées
   - Vérifiez que l'article/commentaire existe

## 📞 Support

Pour toute question ou problème :
1. Vérifiez ce guide d'utilisation
2. Consultez la documentation Django officielle
3. Contactez l'équipe de développement

## 🔄 Mises à Jour

Pour mettre à jour l'application :
1. Sauvegardez votre base de données
2. Téléchargez la nouvelle version
3. Exécutez les migrations : `python manage.py migrate`
4. Redémarrez le serveur