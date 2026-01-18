# Cahier des Charges : Module de Blog Interactif

## 1. Contexte et Objectifs

La Directrice Générale Gaetane MVIBUNDULU vous demande de développer une application web permettant la publication d'articles, avec un système d'interaction sociale complet (J'aime, Commentaires, Réponses).

**Technologie imposée :** Framework Django (Python) + Django Templates (HTML/CSS/JS).

## 2. Spécifications Fonctionnelles (Ce que l'application doit faire)

### A. Gestion des Utilisateurs (Authentification)

• **Inscription :** Formulaire pour créer un compte (Nom d'utilisateur, Email, Mot de passe).
• **Connexion / Déconnexion :** Système standard de login/logout.
• **Contrainte de sécurité :** Un utilisateur doit être connecté pour :
  - Publier un article.
  - Liker un article.
  - Poster un commentaire ou une réponse.
• **Note :** Les visiteurs non connectés peuvent lire les articles et les commentaires, mais ne peuvent pas interagir.

### B. Gestion des Articles

• **Création (C) :** Formulaire avec Titre, Contenu (Texte), et éventuellement une Image de couverture.
• **Lecture (R) :**
  - Liste des articles : Affichage des articles par ordre chronologique inversé (le plus récent en haut).
  - Détail de l'article : Page dédiée pour lire un article complet.
• **Modification/Suppression (U/D) :** Seul l'auteur de l'article (ou un admin) peut modifier ou supprimer son article.

### C. Système de "J'aime" (Likes)

• Un utilisateur ne peut liker un article qu'une seule fois.
• Il doit pouvoir "dé-liker" (toggle) en cliquant à nouveau.
• **Affichage :** Le nombre total de likes doit être visible sur la liste des articles et sur la page de détail.

### D. Système de Commentaires (Hiérarchiques)

• **Commentaire simple :** Un utilisateur commente l'article.
• **Réponse (Nested Comments) :** Un utilisateur peut répondre spécifiquement à un commentaire existant (Commenter un commentaire).
• **Affichage :**
  - Les réponses doivent être décalées visuellement (indentation) sous le commentaire parent pour bien comprendre la conversation.
  - Le nombre total de commentaires (parents + réponses) doit être affiché.

## 3. Modélisation des Données (Backend - Django Models)

Voici la structure de base de données recommandée pour respecter les contraintes (notamment les réponses aux commentaires).

### Modèle Article

• **title :** CharField
• **content :** TextField
• **author :** ForeignKey (vers User)
• **created_at :** DateTimeField
• **likes :** ManyToManyField (vers User, related_name='blog_posts') -> Astuce : Cela permet de faire article.likes.count() facilement.

### Modèle Commentaire

C'est ici que se joue la fonctionnalité "répondre à un commentaire".

• **article :** ForeignKey (vers Article)
• **author :** ForeignKey (vers User)
• **body :** TextField (Le contenu du message)
• **created_at :** DateTimeField
• **parent :** ForeignKey (vers 'self', null=True, blank=True)
  - **Explication :** Si parent est vide, c'est un commentaire principal. Si parent est rempli, c'est une réponse à un autre commentaire.

## 4. Spécifications Techniques & Conseils pour l'équipe

### Stack Technique

• **Backend :** Python / Django.
• **Base de données :** SQLite pour le développement.
• **Frontend :** HTML5, CSS3, JS Django Template Language (DTL).
• **Framework CSS suggéré :** Bootstrap ou Tailwind CSS (pour gagner du temps sur le design des formulaires et des boutons).

### Points de vigilance (Challenges techniques)

1. **Le comptage (Counts) :**
   - Utiliser les méthodes {{ article.likes.count }} dans le template.
   - Pour les commentaires, s'assurer de compter les parents ET les enfants.

2. **Afficher les commentaires imbriqués (Templates) :**
   - C'est la partie la plus complexe avec les Templates Django.
   - **Conseil :** Ils devront soit utiliser une boucle récursive dans le template (via un include qui s'appelle lui-même), soit trier les données dans la View pour envoyer les commentaires parents et leurs enfants de manière structurée.

3. **Expérience Utilisateur (UX) :**
   - Après avoir posté un commentaire ou un like, la page ne doit pas "crasher".
   - L'idéal est de recharger la page au même endroit sinon le rechargement de la page standard suffit.

## 5. Architecture et Structure du Projet (PARTIE AJOUTÉE)

### Structure des URLs

```
/                    -> Liste des articles (page d'accueil)
/article/<id>/       -> Détail d'un article
/article/create/     -> Création d'un nouvel article
/article/<id>/edit/  -> Modification d'un article
/article/<id>/delete/ -> Suppression d'un article
/article/<id>/like/  -> Toggle like/unlike (AJAX)
/login/              -> Page de connexion
/signup/             -> Page d'inscription
/logout/             -> Déconnexion
```

### Structure des Templates

```
templates/
├── base.html                    # Template de base
├── blog/
│   ├── article_list.html       # Liste des articles
│   ├── article_detail.html     # Détail d'un article
│   ├── article_form.html       # Formulaire création/édition
│   └── comment_thread.html     # Template récursif pour commentaires
└── registration/
    ├── login.html              # Page de connexion
    └── signup.html             # Page d'inscription
```

## 6. Spécifications d'Interface Utilisateur (PARTIE AJOUTÉE)

### Design et Ergonomie

• **Responsive Design :** L'application doit être utilisable sur mobile, tablette et desktop.
• **Navigation intuitive :** Menu de navigation clair avec liens vers accueil, création d'article, profil.
• **Feedback visuel :** Indication claire des actions (like activé/désactivé, commentaire posté).

### Éléments d'Interface

• **Bouton "J'aime" :** Icône cœur avec compteur, changement de couleur selon l'état.
• **Formulaire de commentaire :** Zone de texte avec bouton "Publier" sous chaque article et commentaire.
• **Hiérarchie visuelle :** Indentation progressive pour les réponses aux commentaires.

## 7. Gestion des Erreurs et Validation (PARTIE AJOUTÉE)

### Validation des Données

• **Articles :** Titre obligatoire (max 200 caractères), contenu obligatoire.
• **Commentaires :** Contenu obligatoire (min 1 caractère, max 1000 caractères).
• **Utilisateurs :** Email valide, mot de passe sécurisé (min 8 caractères).

### Gestion des Erreurs

• **Erreurs 404 :** Page personnalisée pour les articles inexistants.
• **Erreurs 403 :** Message clair pour les actions non autorisées.
• **Validation formulaires :** Messages d'erreur explicites en français.

## 8. Sécurité (PARTIE AJOUTÉE)

### Mesures de Sécurité

• **CSRF Protection :** Utilisation des tokens CSRF Django sur tous les formulaires.
• **Authentification :** Vérification des permissions avant chaque action sensible.
• **Validation côté serveur :** Toutes les données utilisateur doivent être validées.
• **Protection XSS :** Échappement automatique des données dans les templates.

## 9. Performance et Optimisation (PARTIE AJOUTÉE)

### Optimisations Base de Données

• **Select Related :** Utilisation de select_related() pour éviter les requêtes N+1.
• **Prefetch Related :** Chargement optimisé des likes et commentaires.
• **Pagination :** Limitation du nombre d'articles par page (ex: 10 articles).

### Optimisations Frontend

• **Minification CSS/JS :** En production, minifier les ressources statiques.
• **Images :** Optimisation et redimensionnement automatique des images uploadées.

## 10. Tests et Qualité (PARTIE AJOUTÉE)

### Tests Unitaires

• **Models :** Tests des méthodes et contraintes des modèles.
• **Views :** Tests des réponses HTTP et redirections.
• **Forms :** Tests de validation des formulaires.

### Tests d'Intégration

• **Workflow complet :** Test du parcours utilisateur complet.
• **Permissions :** Vérification des droits d'accès.

## 11. Déploiement et Maintenance (PARTIE AJOUTÉE)

### Environnements

• **Développement :** SQLite, DEBUG=True, données de test.
• **Production :** PostgreSQL recommandé, DEBUG=False, HTTPS obligatoire.

### Maintenance

• **Logs :** Système de logging pour tracer les erreurs.
• **Backup :** Sauvegarde régulière de la base de données.
• **Monitoring :** Surveillance des performances et erreurs.

## 12. Livrables Attendus (PARTIE AJOUTÉE)

### Code Source

• **Repository Git :** Code versionné avec commits explicites.
• **Documentation :** README avec instructions d'installation et utilisation.
• **Requirements :** Fichier requirements.txt avec toutes les dépendances.

### Documentation

• **Guide d'installation :** Procédure complète de mise en place.
• **Guide utilisateur :** Manuel d'utilisation de l'application.
• **Documentation technique :** Architecture et choix techniques.

## 13. Planning et Jalons (PARTIE AJOUTÉE)

### Phase 1 : Base (Semaine 1-2)
- Modèles Django
- Authentification
- CRUD Articles basique

### Phase 2 : Interactions (Semaine 3)
- Système de likes
- Commentaires simples

### Phase 3 : Avancé (Semaine 4)
- Commentaires hiérarchiques
- Interface utilisateur complète

### Phase 4 : Finalisation (Semaine 5)
- Tests
- Optimisations
- Documentation