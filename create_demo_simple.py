#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Article, Comment

def create_demo_data():
    """Cree des donnees de demonstration pour le blog"""
    
    # Creer des utilisateurs de demonstration
    users_data = [
        {'username': 'gaetane', 'email': 'gaetane@example.com', 'password': 'demo123'},
        {'username': 'alice', 'email': 'alice@example.com', 'password': 'demo123'},
        {'username': 'bob', 'email': 'bob@example.com', 'password': 'demo123'},
        {'username': 'claire', 'email': 'claire@example.com', 'password': 'demo123'},
    ]
    
    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['username'].capitalize()
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"Utilisateur cree: {user.username}")
        users.append(user)
    
    # Articles de demonstration
    articles_data = [
        {
            'title': 'Bienvenue sur notre Blog Interactif',
            'content': '''Chers lecteurs,

C'est avec une immense joie que nous vous accueillons sur notre nouveau blog interactif ! Cette plateforme a ete concue avec amour pour creer un espace d'echange et de partage authentique.

Ce que vous trouverez ici :
- Des articles passionnants sur divers sujets
- Un systeme de commentaires interactif
- La possibilite de "liker" vos contenus preferes
- Une communaute bienveillante et engagee

Comment participer ?
1. Inscrivez-vous pour rejoindre notre communaute
2. Lisez et decouvrez nos articles
3. Commentez pour partager vos reflexions
4. Likez les contenus qui vous plaisent
5. Creez vos propres articles !

Nous avons hate de decouvrir vos contributions et d'echanger avec vous. Ensemble, construisons une communaute riche et inspirante !

Bonne lecture !''',
            'author': users[0]
        },
        {
            'title': 'L\'Art de la Communication Digitale',
            'content': '''Dans notre monde hyperconnecte, maitriser l'art de la communication digitale est devenu essentiel. Que ce soit pour le travail, les relations personnelles ou l'expression creative, nos interactions en ligne faconnent notre quotidien.

Les Fondamentaux :

1. L'Authenticite
Etre soi-meme, meme derriere un ecran. L'authenticite cree des connexions durables et significatives.

2. L'Empathie
Comprendre que derriere chaque profil se cache une personne reelle avec ses emotions et ses experiences.

3. La Clarte
Exprimer ses idees de maniere claire et concise pour eviter les malentendus.

Les Defis Modernes :
- La surcharge informationnelle
- La gestion du temps d'ecran
- L'equilibre vie privee/vie publique
- La lutte contre la desinformation

Conseils Pratiques :
- Prenez le temps de relire avant de publier
- Utilisez des emojis pour humaniser vos messages
- Respectez les opinions divergentes
- Creez du contenu de valeur

La communication digitale est un art qui s'apprend et se perfectionne. Chaque interaction est une opportunite de creer du lien et de l'impact positif.

Quelles sont vos meilleures pratiques en communication digitale ? Partagez-les en commentaires !''',
            'author': users[1]
        },
        {
            'title': 'Les Tendances Tech de 2024',
            'content': '''L'annee 2024 marque un tournant decisif dans l'evolution technologique. Entre intelligence artificielle, realite augmentee et developpement durable, decouvrons ensemble les tendances qui faconnent notre avenir.

Intelligence Artificielle : La Revolution Continue

L'IA n'est plus de la science-fiction. Elle s'integre dans :
- Les assistants personnels
- La creation de contenu
- L'analyse de donnees
- La medecine personnalisee

Impact sur le Quotidien
Nos smartphones deviennent plus intelligents, nos voitures plus autonomes, et nos maisons plus connectees. Cette revolution silencieuse transforme notre facon de vivre et de travailler.

Realite Augmentee et Metavers

Le metavers evolue vers des applications pratiques :
- Formation professionnelle immersive
- Shopping virtuel
- Collaboration a distance
- Divertissement interactif

Developpement Durable et Green Tech

La technologie se met au service de l'environnement :
- Energies renouvelables intelligentes
- Agriculture de precision
- Mobilite electrique
- Economie circulaire digitale

Cybersecurite : Un Enjeu Majeur

Avec la digitalisation croissante, la securite devient cruciale :
- Protection des donnees personnelles
- Securisation des objets connectes
- Lutte contre les cyberattaques
- Sensibilisation des utilisateurs

Conclusion

2024 s'annonce comme une annee charniere ou la technologie devient plus humaine, plus durable et plus accessible. L'enjeu n'est plus seulement d'innover, mais d'innover de maniere responsable.

Quelle tendance tech vous passionne le plus ?''',
            'author': users[2]
        }
    ]
    
    # Creer les articles
    articles = []
    for i, article_data in enumerate(articles_data):
        article, created = Article.objects.get_or_create(
            title=article_data['title'],
            defaults={
                'content': article_data['content'],
                'author': article_data['author'],
                'created_at': datetime.now() - timedelta(days=len(articles_data)-i)
            }
        )
        if created:
            print(f"Article cree: {article.title}")
        articles.append(article)
    
    # Ajouter des likes
    import random
    for article in articles:
        likers = random.sample(users, random.randint(1, len(users)))
        for user in likers:
            article.likes.add(user)
    
    # Creer des commentaires
    comments_data = [
        {
            'article': articles[0],
            'author': users[1],
            'body': 'Merci pour ce magnifique accueil ! J\'ai hate de decouvrir tous les articles.'
        },
        {
            'article': articles[0],
            'author': users[2],
            'body': 'Interface tres elegante ! Le design est vraiment reussi.'
        },
        {
            'article': articles[1],
            'author': users[0],
            'body': 'Excellent article Alice ! L\'empathie digitale est cruciale.'
        },
        {
            'article': articles[2],
            'author': users[3],
            'body': 'Tres interessant Bob ! L\'IA me fascine particulierement.'
        }
    ]
    
    for comment_data in comments_data:
        comment, created = Comment.objects.get_or_create(
            article=comment_data['article'],
            author=comment_data['author'],
            body=comment_data['body']
        )
        if created:
            print(f"Commentaire cree sur: {comment.article.title}")
    
    # Creer quelques reponses
    first_comment = Comment.objects.filter(body__contains='magnifique accueil').first()
    if first_comment:
        reply, created = Comment.objects.get_or_create(
            article=first_comment.article,
            author=users[0],
            body='Merci Alice ! Nous sommes ravis de t\'accueillir !',
            parent=first_comment
        )
        if created:
            print("Reponse creee")
    
    print(f"\nDonnees de demonstration creees avec succes !")
    print(f"Resume :")
    print(f"   - {User.objects.count()} utilisateurs")
    print(f"   - {Article.objects.count()} articles")
    print(f"   - {Comment.objects.count()} commentaires")
    print(f"\nComptes de test :")
    for user_data in users_data:
        print(f"   - {user_data['username']} / {user_data['password']}")

if __name__ == '__main__':
    create_demo_data()