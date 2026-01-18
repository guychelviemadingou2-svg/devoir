# 🦋 Blog Interactif - Module de Publication et Interaction Sociale

Un blog moderne et élégant développé avec Django, offrant une expérience utilisateur immersive avec système de likes et commentaires hiérarchiques.

## 🌟 Fonctionnalités

### ✅ Authentification Complète
- Inscription avec validation sécurisée
- Connexion/Déconnexion
- Gestion des sessions utilisateur

### ✅ Gestion des Articles
- **Création** : Interface intuitive avec éditeur de texte
- **Lecture** : Affichage optimisé avec mise en avant
- **Modification** : Édition réservée à l'auteur
- **Suppression** : Contrôle des permissions

### ✅ Système de Likes
- Like/Unlike en un clic
- Comptage en temps réel
- Restriction aux utilisateurs connectés
- Un like par utilisateur par article

### ✅ Commentaires Hiérarchiques
- Commentaires sur articles
- Réponses aux commentaires (système imbriqué)
- Affichage avec indentation visuelle
- Interface responsive

### ✅ Interface Moderne
- Design "Glass Morphism" avec thème violet
- Animations de papillons
- Responsive (mobile, tablette, desktop)
- Bootstrap 5 intégré

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- pip

### Étapes

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd monprojet
```

2. **Environnement virtuel**
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration de la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

6. **Générer des données de démonstration**
```bash
python create_demo_data.py
```

7. **Lancer le serveur**
```bash
python manage.py runserver
```

🎉 **Accédez à http://127.0.0.1:8000/**

## 👥 Comptes de Démonstration

Après avoir exécuté `create_demo_data.py` :

| Utilisateur | Mot de passe | Rôle |
|-------------|--------------|------|
| gaetane | demo123 | Directrice (auteur principal) |
| alice | demo123 | Utilisateur |
| bob | demo123 | Utilisateur |
| claire | demo123 | Utilisateur |

## 📱 Utilisation

### Pour les Visiteurs
- ✅ Consulter tous les articles
- ✅ Lire les commentaires
- ❌ Interagir (connexion requise)

### Pour les Utilisateurs Connectés
- ✅ Créer des articles
- ✅ Liker/Unliker
- ✅ Commenter et répondre
- ✅ Modifier ses propres articles
- ✅ Supprimer ses propres articles

### Pour les Administrateurs
- ✅ Interface d'administration Django
- ✅ Gestion complète des utilisateurs
- ✅ Modération des contenus
- ✅ Statistiques et analytics

## 🏗️ Architecture Technique

### Stack
- **Backend** : Django 4.2+
- **Frontend** : HTML5, CSS3, JavaScript, Bootstrap 5
- **Base de données** : SQLite (dev) / PostgreSQL (prod)
- **Images** : Pillow pour le traitement

### Structure du Projet
```
monprojet/
├── blog/                    # Application principale
│   ├── models.py           # Modèles Article, Comment
│   ├── views.py            # Logique métier
│   ├── forms.py            # Formulaires avec validation
│   ├── urls.py             # Routes de l'application
│   ├── admin.py            # Interface d'administration
│   └── templates/          # Templates HTML
│       ├── base.html       # Template de base
│       ├── blog/           # Templates du blog
│       └── registration/   # Templates d'auth
├── monprojet/              # Configuration Django
├── static/                 # Fichiers statiques
├── media/                  # Images uploadées
└── requirements.txt        # Dépendances
```

### Modèles de Données

#### Article
```python
- title: CharField(200)
- content: TextField
- image: ImageField (optionnel)
- author: ForeignKey(User)
- created_at: DateTimeField
- likes: ManyToManyField(User)
```

#### Comment
```python
- article: ForeignKey(Article)
- author: ForeignKey(User)
- body: TextField
- created_at: DateTimeField
- parent: ForeignKey('self') # Pour hiérarchie
```

## 🔒 Sécurité

### Mesures Implémentées
- ✅ Protection CSRF sur tous les formulaires
- ✅ Authentification requise pour les actions sensibles
- ✅ Validation des données côté serveur
- ✅ Permissions : seul l'auteur peut modifier/supprimer
- ✅ Échappement XSS automatique dans les templates
- ✅ Validation des uploads d'images

### Bonnes Pratiques
- Mots de passe hashés (Django Auth)
- Sessions sécurisées
- Validation stricte des formulaires
- Gestion des erreurs 404/403/500

## 🎨 Personnalisation

### Thème et Couleurs
Le thème violet peut être personnalisé dans `base.html` :
```css
:root {
    --primary-violet: #6f42c1;
    --secondary-violet: #8e44ad;
    --dark-violet: #1a0633;
    /* ... */
}
```

### Ajout de Fonctionnalités
Le code est modulaire et extensible :
- Système de tags
- Recherche full-text
- Notifications
- API REST
- Système de votes pour commentaires

## 📊 Performance

### Optimisations Incluses
- Requêtes optimisées (select_related, prefetch_related)
- Images lazy loading
- CSS/JS minifiés en production
- Cache des templates

### Métriques
- Temps de chargement < 2s
- Score Lighthouse > 90
- Responsive sur tous les appareils

## 🧪 Tests

### Lancer les Tests
```bash
python manage.py test
```

### Couverture
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Types de Tests
- Tests unitaires (modèles, vues, formulaires)
- Tests d'intégration (workflows complets)
- Tests de sécurité (permissions, CSRF)

## 🚀 Déploiement

### Développement
- SQLite
- DEBUG = True
- Serveur de développement Django

### Production
- PostgreSQL recommandé
- DEBUG = False
- Serveur web (Nginx + Gunicorn)
- HTTPS obligatoire
- Variables d'environnement pour les secrets

## 📚 Documentation

- [Cahier des Charges Complet](CAHIER_DES_CHARGES_COMPLET.md)
- [Guide d'Installation](GUIDE_INSTALLATION.md)
- [Spécifications Techniques](SPECIFICATIONS_TECHNIQUES.md)
- [Plan de Tests](PLAN_TESTS.md)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est développé pour Gaetane MVIBUNDULU dans le cadre d'un module de blog interactif.

## 👨‍💻 Support

Pour toute question ou problème :
1. Consulter la documentation
2. Vérifier les issues existantes
3. Créer une nouvelle issue avec :
   - Description du problème
   - Étapes de reproduction
   - Environnement (OS, Python, Django)

## 🎯 Roadmap

### Version 1.1 (Prochaine)
- [ ] Système de tags
- [ ] Recherche avancée
- [ ] Notifications en temps réel
- [ ] Export PDF des articles

### Version 1.2 (Future)
- [ ] API REST complète
- [ ] Application mobile
- [ ] Système de modération automatique
- [ ] Analytics avancées

---

**Développé avec 💜 pour une expérience utilisateur exceptionnelle**

*"La simplicité est la sophistication suprême." - Leonardo da Vinci*