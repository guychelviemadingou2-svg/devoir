# Plan d'implémentation du Module de Blog Interactif

## Phase 1 : Configuration et Modèles [ ]
- [ ] Ajouter `blog` aux `INSTALLED_APPS` dans `settings.py`.
- [ ] Implémenter les modèles `Article` et `Commentaire` dans `blog/models.py`.
- [ ] Configurer `MEDIA_URL` et `MEDIA_ROOT` pour les images des articles.
- [ ] Créer et appliquer les migrations.

## Phase 2 : Authentification [ ]
- [ ] Créer les vues pour l'Inscription, la Connexion et la Déconnexion.
- [ ] Créer les templates d'authentification.

## Phase 3 : Fonctionnalités du Blog (Articles) [ ]
- [ ] Implémenter les vues Liste et Détail des articles.
- [ ] Implémenter la création, modification et suppression d'articles (avec permissions).
- [ ] Créer les templates pour la gestion des articles.

## Phase 4 : Interactions (Likes & Commentaires) [ ]
- [ ] Implémenter le système de "J'aime" (toggle).
- [ ] Implémenter le système de commentaires hiérarchiques (réponses).
- [ ] Mettre à jour les templates pour afficher les likes et les commentaires imbriqués.

## Phase 5 : Style et Finitions [ ]
- [ ] Appliquer le thème "Violet" avec Bootstrap/Tailwind.
- [ ] Assurer le design responsive et une UX fluide.
- [ ] Vérification finale de toutes les spécifications.
