# Plan de Tests et Validation - Module de Blog Interactif

## 🧪 Stratégie de Tests

### Types de Tests Implémentés

1. **Tests Unitaires** - Modèles et fonctions isolées
2. **Tests d'Intégration** - Vues et workflows complets
3. **Tests Fonctionnels** - Parcours utilisateur end-to-end
4. **Tests de Sécurité** - Permissions et authentification

## 📋 Plan de Tests Détaillé

### 1. Tests des Modèles (Models)

#### Test Article Model
```python
class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_article_creation(self):
        """Test création d'un article"""
        article = Article.objects.create(
            title='Test Article',
            content='Contenu de test',
            author=self.user
        )
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.author, self.user)
        self.assertTrue(article.created_at)
    
    def test_article_str_method(self):
        """Test méthode __str__ de Article"""
        article = Article.objects.create(
            title='Test Article',
            content='Contenu',
            author=self.user
        )
        self.assertEqual(str(article), 'Test Article')
    
    def test_total_likes_property(self):
        """Test propriété total_likes"""
        article = Article.objects.create(
            title='Test Article',
            content='Contenu',
            author=self.user
        )
        self.assertEqual(article.total_likes, 0)
        
        # Ajouter un like
        article.likes.add(self.user)
        self.assertEqual(article.total_likes, 1)
```

#### Test Comment Model
```python
class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.article = Article.objects.create(
            title='Test Article',
            content='Contenu',
            author=self.user
        )
    
    def test_comment_creation(self):
        """Test création d'un commentaire"""
        comment = Comment.objects.create(
            article=self.article,
            author=self.user,
            body='Test commentaire'
        )
        self.assertEqual(comment.body, 'Test commentaire')
        self.assertEqual(comment.article, self.article)
        self.assertFalse(comment.is_reply)
    
    def test_reply_creation(self):
        """Test création d'une réponse"""
        parent_comment = Comment.objects.create(
            article=self.article,
            author=self.user,
            body='Commentaire parent'
        )
        
        reply = Comment.objects.create(
            article=self.article,
            author=self.user,
            body='Réponse',
            parent=parent_comment
        )
        
        self.assertTrue(reply.is_reply)
        self.assertEqual(reply.parent, parent_comment)
```

### 2. Tests des Vues (Views)

#### Test Article Views
```python
class ArticleViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.article = Article.objects.create(
            title='Test Article',
            content='Contenu de test',
            author=self.user
        )
    
    def test_article_list_view(self):
        """Test vue liste des articles"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')
    
    def test_article_detail_view(self):
        """Test vue détail d'un article"""
        response = self.client.get(f'/article/{self.article.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')
        self.assertContains(response, 'Contenu de test')
    
    def test_article_create_requires_login(self):
        """Test que la création d'article nécessite une connexion"""
        response = self.client.get('/article/new/')
        self.assertRedirects(response, '/login/?next=/article/new/')
    
    def test_article_create_authenticated(self):
        """Test création d'article avec utilisateur connecté"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/article/new/')
        self.assertEqual(response.status_code, 200)
    
    def test_article_create_post(self):
        """Test soumission du formulaire de création"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post('/article/new/', {
            'title': 'Nouvel Article',
            'content': 'Contenu du nouvel article'
        })
        self.assertEqual(Article.objects.count(), 2)
        new_article = Article.objects.get(title='Nouvel Article')
        self.assertEqual(new_article.author, self.user)
```

#### Test Like System
```python
class LikeSystemTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.article = Article.objects.create(
            title='Test Article',
            content='Contenu',
            author=self.user
        )
    
    def test_like_article_requires_login(self):
        """Test que liker nécessite une connexion"""
        response = self.client.post(f'/article/{self.article.pk}/like/')
        self.assertRedirects(response, f'/login/?next=/article/{self.article.pk}/like/')
    
    def test_like_article_authenticated(self):
        """Test like avec utilisateur connecté"""
        self.client.login(username='testuser', password='testpass123')
        
        # Premier like
        response = self.client.post(f'/article/{self.article.pk}/like/')
        self.assertEqual(self.article.likes.count(), 1)
        self.assertTrue(self.article.likes.filter(id=self.user.id).exists())
        
        # Unlike (toggle)
        response = self.client.post(f'/article/{self.article.pk}/like/')
        self.assertEqual(self.article.likes.count(), 0)
        self.assertFalse(self.article.likes.filter(id=self.user.id).exists())
```

### 3. Tests de Sécurité

#### Test Permissions
```python
class SecurityTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.article = Article.objects.create(
            title='Article User1',
            content='Contenu',
            author=self.user1
        )
    
    def test_only_author_can_edit(self):
        """Test que seul l'auteur peut modifier son article"""
        self.client.login(username='user2', password='testpass123')
        response = self.client.get(f'/article/{self.article.pk}/edit/')
        # Devrait rediriger ou afficher une erreur
        self.assertNotEqual(response.status_code, 200)
    
    def test_only_author_can_delete(self):
        """Test que seul l'auteur peut supprimer son article"""
        self.client.login(username='user2', password='testpass123')
        response = self.client.post(f'/article/{self.article.pk}/delete/')
        # L'article ne devrait pas être supprimé
        self.assertTrue(Article.objects.filter(pk=self.article.pk).exists())
    
    def test_csrf_protection(self):
        """Test protection CSRF"""
        self.client.login(username='user1', password='testpass123')
        # Tentative sans token CSRF
        response = self.client.post('/article/new/', {
            'title': 'Test',
            'content': 'Test'
        }, HTTP_X_CSRFTOKEN='invalid')
        # Devrait échouer
        self.assertNotEqual(response.status_code, 302)
```

### 4. Tests des Formulaires

#### Test Article Form
```python
class ArticleFormTest(TestCase):
    def test_article_form_valid_data(self):
        """Test formulaire avec données valides"""
        form = ArticleForm(data={
            'title': 'Test Article',
            'content': 'Contenu de test'
        })
        self.assertTrue(form.is_valid())
    
    def test_article_form_no_data(self):
        """Test formulaire sans données"""
        form = ArticleForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('content', form.errors)
    
    def test_article_form_title_too_long(self):
        """Test titre trop long"""
        form = ArticleForm(data={
            'title': 'x' * 201,  # Plus de 200 caractères
            'content': 'Contenu'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
```

#### Test Comment Form
```python
class CommentFormTest(TestCase):
    def test_comment_form_valid(self):
        """Test formulaire commentaire valide"""
        form = CommentForm(data={'body': 'Test commentaire'})
        self.assertTrue(form.is_valid())
    
    def test_comment_form_empty(self):
        """Test formulaire commentaire vide"""
        form = CommentForm(data={'body': ''})
        self.assertFalse(form.is_valid())
```

## 🔍 Tests Fonctionnels (End-to-End)

### Scénarios de Test Utilisateur

#### Scénario 1: Parcours Complet Utilisateur
```python
class UserJourneyTest(TestCase):
    def test_complete_user_journey(self):
        """Test parcours complet: inscription -> création article -> commentaire -> like"""
        
        # 1. Inscription
        response = self.client.post('/signup/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'password_confirm': 'securepass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après inscription
        
        # 2. Création d'article
        response = self.client.post('/article/new/', {
            'title': 'Mon Premier Article',
            'content': 'Contenu de mon premier article'
        })
        self.assertEqual(response.status_code, 302)
        article = Article.objects.get(title='Mon Premier Article')
        
        # 3. Ajout d'un commentaire
        response = self.client.post(f'/article/{article.pk}/', {
            'body': 'Super article !'
        })
        self.assertEqual(Comment.objects.count(), 1)
        
        # 4. Like de l'article
        response = self.client.post(f'/article/{article.pk}/like/')
        self.assertEqual(article.likes.count(), 1)
```

#### Scénario 2: Commentaires Hiérarchiques
```python
class NestedCommentsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.article = Article.objects.create(
            title='Test Article',
            content='Contenu',
            author=self.user
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_nested_comments_creation(self):
        """Test création de commentaires imbriqués"""
        
        # Commentaire parent
        response = self.client.post(f'/article/{self.article.pk}/', {
            'body': 'Commentaire parent'
        })
        parent_comment = Comment.objects.get(body='Commentaire parent')
        
        # Réponse au commentaire
        response = self.client.post(f'/article/{self.article.pk}/', {
            'body': 'Réponse au commentaire',
            'parent_id': parent_comment.id
        })
        
        reply = Comment.objects.get(body='Réponse au commentaire')
        self.assertEqual(reply.parent, parent_comment)
        self.assertTrue(reply.is_reply)
```

## ✅ Checklist de Validation

### Fonctionnalités Core

- [ ] **Authentification**
  - [ ] Inscription utilisateur
  - [ ] Connexion/Déconnexion
  - [ ] Validation des mots de passe
  - [ ] Gestion des sessions

- [ ] **Gestion des Articles**
  - [ ] Création d'article (utilisateur connecté uniquement)
  - [ ] Affichage liste des articles
  - [ ] Affichage détail d'un article
  - [ ] Modification d'article (auteur uniquement)
  - [ ] Suppression d'article (auteur uniquement)

- [ ] **Système de Likes**
  - [ ] Like/Unlike toggle
  - [ ] Comptage des likes
  - [ ] Restriction aux utilisateurs connectés
  - [ ] Un like par utilisateur par article

- [ ] **Commentaires Hiérarchiques**
  - [ ] Commentaire sur article
  - [ ] Réponse à un commentaire
  - [ ] Affichage hiérarchique (indentation)
  - [ ] Comptage total des commentaires

### Sécurité

- [ ] **Protection CSRF** sur tous les formulaires
- [ ] **Authentification** requise pour les actions sensibles
- [ ] **Autorisation** - seul l'auteur peut modifier/supprimer
- [ ] **Validation** des données côté serveur
- [ ] **Échappement XSS** dans les templates

### Performance

- [ ] **Requêtes optimisées** (select_related, prefetch_related)
- [ ] **Pagination** pour les listes longues
- [ ] **Images optimisées** (taille, format)

### Interface Utilisateur

- [ ] **Design responsive** (mobile, tablette, desktop)
- [ ] **Navigation intuitive**
- [ ] **Feedback visuel** pour les actions
- [ ] **Messages d'erreur** clairs en français
- [ ] **Accessibilité** de base

## 🚀 Commandes de Test

### Exécution des Tests

```bash
# Tous les tests
python manage.py test

# Tests d'une app spécifique
python manage.py test blog

# Tests avec couverture
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Génère un rapport HTML
```

### Tests de Performance

```bash
# Test de charge avec Apache Bench
ab -n 1000 -c 10 http://127.0.0.1:8000/

# Profiling Django
pip install django-debug-toolbar
# Ajouter à INSTALLED_APPS et MIDDLEWARE
```

## 📊 Métriques de Qualité

### Objectifs de Couverture

- **Modèles**: 95%+
- **Vues**: 90%+
- **Formulaires**: 95%+
- **Utilitaires**: 85%+

### Critères de Validation

1. **Tous les tests passent** ✅
2. **Couverture de code** > 90% ✅
3. **Aucune vulnérabilité** de sécurité ✅
4. **Performance** acceptable (< 2s par page) ✅
5. **Interface responsive** sur tous les appareils ✅

## 🐛 Gestion des Bugs

### Processus de Signalement

1. **Reproduction** du bug
2. **Documentation** des étapes
3. **Création** d'un test qui échoue
4. **Correction** du code
5. **Validation** que le test passe
6. **Tests de régression**

### Types de Bugs Prioritaires

1. **Sécurité** - Correction immédiate
2. **Fonctionnalité critique** - Correction rapide
3. **Interface utilisateur** - Correction planifiée
4. **Performance** - Optimisation continue