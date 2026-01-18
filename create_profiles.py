#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import UserProfile

# Créer les profils manquants
for user in User.objects.all():
    profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        print(f"Profil créé pour {user.username}")
    else:
        print(f"Profil existe déjà pour {user.username}")

print("Tous les profils sont créés !")