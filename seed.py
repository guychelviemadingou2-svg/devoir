import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Article

# 1. Création de l'admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Utilisateur 'admin' créé (mdp: admin123)")

admin_user = User.objects.get(username='admin')

# 2. Ajout d'articles de test
articles_data = [
    {
        'title': 'Le Vol du Monarque 🦋',
        'content': 'Le voyage épique des papillons monarques à travers le continent est l\'un des spectacles les plus fascinants de la nature. Ils parcourent des milliers de kilomètres avec une précision incroyable.'
    },
    {
        'title': 'L\'Élégance du Violet 💜',
        'content': 'Pourquoi le violet est-il associé à la royauté et à la créativité ? Dans cet article, nous explorons la psychologie des couleurs et l\'impact du violet sur notre imagination.'
    },
    {
        'title': 'Le Blog de Gaetane 🚀',
        'content': 'Bienvenue sur cette plateforme interactive. Ici, nous partageons, nous likons et nous discutons dans un environnement moderne et sécurisé.'
    }
]

for data in articles_data:
    if not Article.objects.filter(title=data['title']).exists():
        Article.objects.create(
            title=data['title'],
            content=data['content'],
            author=admin_user
        )
        print(f"✅ Article '{data['title']}' ajouté.")

print("\n🚀 Prêt ! Lancez 'python manage.py runserver' et connectez-vous avec 'admin'.")
