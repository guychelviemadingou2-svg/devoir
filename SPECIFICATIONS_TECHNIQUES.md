# Spécifications Techniques - Module de Blog Interactif

## 🏗️ Architecture Technique

### Stack Technologique

| Composant | Technologie | Version |
|-----------|-------------|---------|
| Backend Framework | Django | 4.2+ |
| Langage | Python | 3.8+ |
| Base de données | SQLite | (dev) / PostgreSQL (prod) |
| Frontend | HTML5, CSS3, JavaScript | - |
| Framework CSS | Bootstrap | 5.x |
| Gestion d'images | Pillow | 9.0+ |

## 📊 Modèle de Données

### Schéma de Base de Données

```sql
-- Table Article
CREATE TABLE blog_article (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    image VARCHAR(100),
    author_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY (author_id) REFERENCES auth_user (id)
);

-- Table Comment
CREATE TABLE blog_comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    parent_id INTEGER,
    FOREIGN KEY (article_id) REFERENCES blog_article (id),
    FOREIGN KEY (author_id) REFERENCES auth_user (id),
    FOREIGN KEY (parent_id) REFERENCES blog_comment (id)
);

-- Table de liaison Article-Likes
CREATE TABLE blog_article_likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (article_id) REFERENCES blog_article (id),
    FOREIGN KEY (user_id) REFERENCES auth_user (id),
    UNIQUE(article_id, user_id)
);
```

### Relations entre Modèles

```
User (Django Auth)
├── Article (1:N) - Un utilisateur peut créer plusieurs articles
├── Comment (1:N) - Un utilisateur peut créer plusieurs commentaires
└── Article.likes (N:N) - Un utilisateur peut liker plusieurs articles

Article
├── Comment (1:N) - Un article peut avoir plusieurs commentaires
└── User.likes (N:N) - Un article peut être liké par plusieurs utilisateurs

Comment
├── Comment.replies (1:N) - Un commentaire peut avoir plusieurs réponses
└── Comment.parent (N:1) - Une réponse appartient à un commentaire parent
```

## 🔧 API Interne (Vues Django)

### Endpoints Principaux

| URL | Méthode | Vue | Description | Auth Requise |
|-----|---------|-----|-------------|--------------|
| `/` | GET | `article_list` | Liste des articles | Non |
| `/article/<id>/` | GET | `article_detail` | Détail d'un article | Non |
| `/article/new/` | GET/POST | `article_create` | Création d'article | Oui |
| `/article/<id>/edit/` | GET/POST | `article_update` | Modification d'article | Oui (auteur) |
| `/article/<id>/delete/` | POST | `article_delete` | Suppression d'article | Oui (auteur) |
| `/article/<id>/like/` | POST | `like_article` | Toggle like | Oui |
| `/signup/` | GET/POST | `signup` | Inscription | Non |
| `/login/` | GET/POST | `LoginView` | Connexion | Non |
| `/logout/` | POST | `LogoutView` | Déconnexion | Oui |

### Logique Métier

#### Système de Likes
```python
def like_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)  # Unlike
    else:
        article.likes.add(request.user)     # Like
    return redirect('article_detail', pk=pk)
```

#### Commentaires Hiérarchiques
```python
# Dans le template, récursion pour afficher les réponses
{% for comment in comments %}
    <div class="comment">
        {{ comment.body }}
        {% if comment.replies.all %}
            {% include 'blog/comment_thread.html' with comments=comment.replies.all %}
        {% endif %}
    </div>
{% endfor %}
```

## 🔒 Sécurité

### Mesures Implémentées

1. **Protection CSRF**
   ```html
   <form method="post">
       {% csrf_token %}
       <!-- formulaire -->
   </form>
   ```

2. **Authentification et Autorisation**
   ```python
   @login_required
   def article_create(request):
       # Seuls les utilisateurs connectés peuvent créer
   
   def article_update(request, pk):
       if article.author != request.user:
           # Seul l'auteur peut modifier
   ```

3. **Validation des Données**
   ```python
   class ArticleForm(forms.ModelForm):
       def clean_title(self):
           title = self.cleaned_data['title']
           if len(title) < 5:
               raise forms.ValidationError("Titre trop court")
           return title
   ```

4. **Protection XSS**
   - Échappement automatique dans les templates Django
   - Utilisation de `|safe` uniquement quand nécessaire

## ⚡ Performance

### Optimisations Base de Données

1. **Select Related**
   ```python
   articles = Article.objects.select_related('author').all()
   ```

2. **Prefetch Related**
   ```python
   articles = Article.objects.prefetch_related('likes', 'comments').all()
   ```

3. **Requêtes Optimisées**
   ```python
   # Éviter N+1 queries
   comments = Comment.objects.select_related('author', 'parent').filter(article=article)
   ```

### Optimisations Frontend

1. **Pagination**
   ```python
   from django.core.paginator import Paginator
   
   paginator = Paginator(articles, 10)  # 10 articles par page
   ```

2. **Lazy Loading Images**
   ```html
   <img src="{{ article.image.url }}" loading="lazy" alt="{{ article.title }}">
   ```

## 🧪 Tests

### Structure des Tests

```python
# tests.py
class ArticleModelTest(TestCase):
    def test_article_creation(self):
        # Test création d'article
    
    def test_like_functionality(self):
        # Test système de likes

class ArticleViewTest(TestCase):
    def test_article_list_view(self):
        # Test vue liste
    
    def test_article_detail_view(self):
        # Test vue détail
```

### Couverture de Tests

- **Modèles** : 90%+ de couverture
- **Vues** : 85%+ de couverture
- **Formulaires** : 95%+ de couverture

## 📱 Interface Utilisateur

### Design System

#### Couleurs
```css
:root {
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
}
```

#### Composants Réutilisables

1. **Bouton Like**
   ```html
   <form method="post" action="{% url 'like_article' article.pk %}" class="d-inline">
       {% csrf_token %}
       <button type="submit" class="btn btn-link p-0">
           {% if user in article.likes.all %}
               ❤️ {{ article.total_likes }}
           {% else %}
               🤍 {{ article.total_likes }}
           {% endif %}
       </button>
   </form>
   ```

2. **Formulaire de Commentaire**
   ```html
   <div class="comment-form mt-3">
       <form method="post">
           {% csrf_token %}
           {{ form.as_p }}
           <input type="hidden" name="parent_id" value="{{ comment.id }}">
           <button type="submit" class="btn btn-primary btn-sm">Répondre</button>
       </form>
   </div>
   ```

### Responsive Design

```css
/* Mobile First */
@media (max-width: 768px) {
    .article-card {
        margin-bottom: 1rem;
    }
    
    .comment {
        padding-left: 1rem;
    }
}

@media (min-width: 769px) {
    .comment {
        padding-left: 2rem;
    }
}
```

## 🚀 Déploiement

### Configuration Production

```python
# settings.py (production)
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog_db',
        'USER': 'blog_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Sécurité
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Serveur Web

```nginx
# nginx.conf
server {
    listen 80;
    server_name votre-domaine.com;
    
    location /static/ {
        alias /path/to/static/;
    }
    
    location /media/ {
        alias /path/to/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitoring et Logs

### Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'blog.log',
        },
    },
    'loggers': {
        'blog': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Métriques à Surveiller

- Nombre d'articles créés par jour
- Nombre de commentaires par article
- Taux d'engagement (likes/vues)
- Temps de réponse des pages
- Erreurs 404/500

## 🔄 Maintenance

### Tâches Régulières

1. **Sauvegarde Base de Données**
   ```bash
   python manage.py dumpdata > backup_$(date +%Y%m%d).json
   ```

2. **Nettoyage des Sessions**
   ```bash
   python manage.py clearsessions
   ```

3. **Collecte des Fichiers Statiques**
   ```bash
   python manage.py collectstatic --noinput
   ```

### Évolutions Futures

- [ ] API REST avec Django REST Framework
- [ ] Notifications en temps réel (WebSockets)
- [ ] Système de tags pour les articles
- [ ] Recherche full-text
- [ ] Modération automatique des commentaires
- [ ] Système de votes pour les commentaires