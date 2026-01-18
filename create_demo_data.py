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
    """Crée des données de démonstration pour le blog"""
    
    # Créer des utilisateurs de démonstration
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
            print(f"[OK] Utilisateur cree: {user.username}")
        users.append(user)
    
    # Articles de demonstration
    articles_data = [
        {
            'title': 'Bienvenue sur notre Blog Interactif',
            'content': '''Chers lecteurs,

C'est avec une immense joie que nous vous accueillons sur notre nouveau blog interactif ! Cette plateforme a ete concue avec amour pour creer un espace d'echange et de partage authentique.

## Ce que vous trouverez ici

Notre blog vous offre une experience unique :
- Des articles passionnants sur divers sujets
- Un systeme de commentaires interactif
- La possibilite de "liker" vos contenus preferes
- Une communaute bienveillante et engagee

## Comment participer ?

1. **Inscrivez-vous** pour rejoindre notre communaute
2. **Lisez** et decouvrez nos articles
3. **Commentez** pour partager vos reflexions
4. **Likez** les contenus qui vous plaisent
5. **Creez** vos propres articles !

Nous avons hate de decouvrir vos contributions et d'echanger avec vous. Ensemble, construisons une communaute riche et inspirante !

Bonne lecture !''',
            'author': users[0]  # gaetane
        },
        {
            'title': 'L\'Art de la Communication Digitale',
            'content': '''Dans notre monde hyperconnecté, maîtriser l'art de la communication digitale est devenu essentiel. Que ce soit pour le travail, les relations personnelles ou l'expression créative, nos interactions en ligne façonnent notre quotidien.

## Les Fondamentaux

La communication digitale repose sur plusieurs piliers :

**1. L'Authenticité**
Être soi-même, même derrière un écran. L'authenticité crée des connexions durables et significatives.

**2. L'Empathie**
Comprendre que derrière chaque profil se cache une personne réelle avec ses émotions et ses expériences.

**3. La Clarté**
Exprimer ses idées de manière claire et concise pour éviter les malentendus.

## Les Défis Modernes

- La surcharge informationnelle
- La gestion du temps d'écran
- L'équilibre vie privée/vie publique
- La lutte contre la désinformation

## Conseils Pratiques

✨ Prenez le temps de relire avant de publier
✨ Utilisez des émojis pour humaniser vos messages
✨ Respectez les opinions divergentes
✨ Créez du contenu de valeur

La communication digitale est un art qui s'apprend et se perfectionne. Chaque interaction est une opportunité de créer du lien et de l'impact positif.

Quelles sont vos meilleures pratiques en communication digitale ? Partagez-les en commentaires ! 💬''',
            'author': users[1]  # alice
        },
        {
            'title': 'Les Tendances Tech de 2024 🚀',
            'content': '''L'année 2024 marque un tournant décisif dans l'évolution technologique. Entre intelligence artificielle, réalité augmentée et développement durable, découvrons ensemble les tendances qui façonnent notre avenir.

## Intelligence Artificielle : La Révolution Continue

L'IA n'est plus de la science-fiction. Elle s'intègre dans :
- Les assistants personnels
- La création de contenu
- L'analyse de données
- La médecine personnalisée

### Impact sur le Quotidien
Nos smartphones deviennent plus intelligents, nos voitures plus autonomes, et nos maisons plus connectées. Cette révolution silencieuse transforme notre façon de vivre et de travailler.

## Réalité Augmentée et Métavers

Le métavers évolue vers des applications pratiques :
- Formation professionnelle immersive
- Shopping virtuel
- Collaboration à distance
- Divertissement interactif

## Développement Durable et Green Tech

La technologie se met au service de l'environnement :
- Énergies renouvelables intelligentes
- Agriculture de précision
- Mobilité électrique
- Économie circulaire digitale

## Cybersécurité : Un Enjeu Majeur

Avec la digitalisation croissante, la sécurité devient cruciale :
- Protection des données personnelles
- Sécurisation des objets connectés
- Lutte contre les cyberattaques
- Sensibilisation des utilisateurs

## Conclusion

2024 s'annonce comme une année charnière où la technologie devient plus humaine, plus durable et plus accessible. L'enjeu n'est plus seulement d'innover, mais d'innover de manière responsable.

Quelle tendance tech vous passionne le plus ? 🤔''',
            'author': users[2]  # bob
        },
        {
            'title': 'Créativité et Innovation : Libérer son Potentiel',
            'content': '''La créativité n'est pas un don réservé à quelques élus. C'est une compétence que chacun peut développer et cultiver. Dans un monde en constante évolution, notre capacité à innover devient notre plus grand atout.

## Qu'est-ce que la Créativité ?

La créativité, c'est :
- **L'art de voir différemment** : Observer le monde avec un regard neuf
- **La connexion d'idées** : Relier des concepts apparemment sans rapport
- **L'audace d'expérimenter** : Oser sortir de sa zone de confort
- **La persévérance** : Continuer malgré les échecs

## Les Blocages Créatifs

Nous avons tous des freins à la créativité :

### Le Perfectionnisme
"Ce n'est pas assez bien" - Cette petite voix qui nous paralyse avant même de commencer.

### La Peur du Jugement
L'angoisse de ce que les autres vont penser de nos idées "folles".

### Le Manque de Temps
"Je n'ai pas le temps d'être créatif" - Un piège dans lequel nous tombons tous.

## Techniques pour Stimuler la Créativité

### 1. Le Brainstorming Libre
- Notez toutes vos idées sans jugement
- Quantité avant qualité
- Construisez sur les idées des autres

### 2. La Technique des 6 Chapeaux
Explorez un problème sous différents angles :
- 🎩 Blanc : Les faits
- 🔴 Rouge : Les émotions
- ⚫ Noir : La critique
- 💛 Jaune : L'optimisme
- 💚 Vert : La créativité
- 🔵 Bleu : Le contrôle

### 3. L'Inspiration Croisée
Cherchez l'inspiration dans des domaines éloignés du vôtre. Comment un chef cuisinier résoudrait-il votre problème de marketing ?

## Créer un Environnement Propice

### Votre Espace Physique
- Lumière naturelle
- Couleurs inspirantes
- Objets qui stimulent l'imagination
- Absence de distractions

### Votre Espace Mental
- Méditation quotidienne
- Lectures variées
- Rencontres enrichissantes
- Temps de réflexion

## L'Innovation au Quotidien

L'innovation ne se limite pas aux grandes découvertes :
- Améliorer un processus existant
- Trouver une nouvelle utilisation à un objet
- Combiner deux idées simples
- Questionner les habitudes

## Exercices Pratiques

### Défi des 30 Idées
Chaque jour, trouvez 30 nouvelles utilisations pour un objet banal (un trombone, une chaussette, etc.).

### Journal Créatif
Tenez un carnet où vous notez :
- Vos observations insolites
- Vos rêves
- Vos questions sans réponse
- Vos connexions d'idées

### La Règle des 5 Pourquoi
Face à un problème, demandez-vous "pourquoi ?" cinq fois de suite pour aller au cœur du sujet.

## Conclusion

La créativité est un muscle qui se développe avec l'entraînement. Chaque jour offre des opportunités d'innover, que ce soit dans notre travail, nos relations ou nos loisirs.

N'ayez pas peur d'échouer. Chaque "échec" est une leçon qui vous rapproche de votre prochaine grande idée.

**Question pour vous** : Quel est votre dernier moment de créativité ? Comment l'avez-vous vécu ? 🎨✨

*"La créativité, c'est l'intelligence qui s'amuse." - Albert Einstein*''',
            'author': users[3]  # claire
        },
        {
            'title': 'Le Pouvoir des Habitudes Positives',
            'content': '''Nos habitudes façonnent notre vie plus que nous ne l'imaginons. Elles représentent environ 40% de nos actions quotidiennes et déterminent largement qui nous devenons. Découvrons ensemble comment cultiver des habitudes qui nous élèvent.

## La Science des Habitudes

### Le Cycle de l'Habitude
Toute habitude suit un schéma simple :
1. **Le Déclencheur** : Ce qui initie l'habitude
2. **La Routine** : L'action elle-même
3. **La Récompense** : Le bénéfice obtenu

### Pourquoi C'est Si Puissant ?
Notre cerveau automatise les habitudes pour économiser de l'énergie. Une fois ancrée, une habitude ne demande plus d'effort conscient.

## Habitudes Transformatrices

### 🌅 La Routine Matinale
- Réveil à heure fixe
- Hydratation immédiate
- 10 minutes de méditation
- Planification de la journée

**Impact** : Démarre la journée avec intention et énergie.

### 📚 L'Apprentissage Continu
- 20 minutes de lecture quotidienne
- Un podcast éducatif par jour
- Une nouvelle compétence par mois

**Impact** : Croissance personnelle constante.

### 💪 Le Mouvement Quotidien
- 30 minutes d'activité physique
- Marche après les repas
- Étirements réguliers

**Impact** : Santé physique et mentale optimisée.

### 🙏 La Gratitude
- Noter 3 choses positives chaque soir
- Remercier une personne par jour
- Célébrer les petites victoires

**Impact** : Perspective positive et relations enrichies.

## Comment Installer une Nouvelle Habitude

### 1. Commencer Petit
Au lieu de "faire du sport 1h par jour", commencez par "faire 5 pompes".

### 2. L'Ancrage
Attachez votre nouvelle habitude à une habitude existante :
"Après mon café du matin, je médite 5 minutes."

### 3. La Règle des 2 Minutes
Si une habitude prend moins de 2 minutes, faites-la immédiatement.

### 4. L'Environnement
Modifiez votre environnement pour faciliter la bonne habitude :
- Laissez vos chaussures de sport près du lit
- Placez un livre sur votre table de chevet
- Préparez vos vêtements la veille

## Surmonter les Obstacles

### La Motivation Fluctue
Ne comptez pas sur la motivation. Comptez sur le système.

### Les Rechutes Sont Normales
Une rechute n'annule pas vos progrès. Reprenez simplement le lendemain.

### La Patience Est Clé
Il faut en moyenne 66 jours pour qu'une habitude devienne automatique.

## Habitudes à Éviter

### Le Multitasking
Concentrez-vous sur une tâche à la fois pour plus d'efficacité.

### La Procrastination Digitale
Limitez le temps d'écran non productif.

### Le Perfectionnisme
Mieux vaut fait qu'imparfait.

## Mesurer ses Progrès

### Le Tracker d'Habitudes
Utilisez un calendrier pour marquer chaque jour où vous respectez votre habitude.

### Les Récompenses
Célébrez vos succès, même petits.

### L'Ajustement
Adaptez vos habitudes selon vos résultats et votre évolution.

## Habitudes Sociales

### L'Entourage Influence
Entourez-vous de personnes qui partagent vos valeurs et objectifs.

### La Responsabilité
Partagez vos objectifs avec un proche qui vous soutiendra.

### L'Exemple
Soyez le changement que vous voulez voir chez les autres.

## Conclusion

Les habitudes sont des investissements dans votre futur. Chaque petite action répétée quotidiennement crée un effet composé extraordinaire sur le long terme.

Commencez aujourd'hui. Choisissez UNE habitude simple et engagez-vous pour 30 jours. Votre futur vous remerciera.

**Question de réflexion** : Quelle habitude positive aimeriez-vous développer en premier ? Quel sera votre premier petit pas ? 🌱

*"Nous sommes ce que nous répétons chaque jour. L'excellence n'est donc pas un acte, mais une habitude." - Aristote*''',
            'author': users[0]  # gaetane
        }
    ]
    
    # Créer les articles
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
            print(f"[OK] Article cree: {article.title}")
        articles.append(article)
    
    # Ajouter des likes
    for article in articles:
        # Chaque article recoit des likes aleatoirement
        import random
        likers = random.sample(users, random.randint(1, len(users)))
        for user in likers:
            article.likes.add(user)
    
    # Creer des commentaires de demonstration
    comments_data = [
        {
            'article': articles[0],
            'author': users[1],
            'body': 'Merci pour ce magnifique accueil ! J\'ai hate de decouvrir tous les articles et de participer aux discussions.'
        },
        {
            'article': articles[0],
            'author': users[2],
            'body': 'Interface tres elegante ! Le design avec les papillons est vraiment reussi. Bravo a l\'equipe !'
        },
        {
            'article': articles[1],
            'author': users[0],
            'body': 'Excellent article Alice ! L\'empathie digitale est effectivement cruciale dans nos interactions en ligne.'
        },
        {
            'article': articles[2],
            'author': users[3],
            'body': 'Tres interessant Bob ! L\'IA me fascine particulierement. As-tu des recommandations de lectures sur le sujet ?'
        },
        {
            'article': articles[3],
            'author': users[0],
            'body': 'Claire, ton article sur la creativite est inspirant ! J\'adore la technique des 6 chapeaux, je vais l\'essayer.'
        },
        {
            'article': articles[4],
            'author': users[2],
            'body': 'Merci Gaetane pour ces conseils pratiques ! Je vais commencer par la routine matinale.'
        }
    ]
    
    # Creer les commentaires
    for comment_data in comments_data:
        comment, created = Comment.objects.get_or_create(
            article=comment_data['article'],
            author=comment_data['author'],
            body=comment_data['body']
        )
        if created:
            print(f"[OK] Commentaire cree sur: {comment.article.title}")
    
    # Creer quelques reponses aux commentaires
    replies_data = [
        {
            'parent': Comment.objects.filter(body__contains='magnifique accueil').first(),
            'author': users[0],
            'body': 'Merci Alice ! Nous sommes ravis de t\'accueillir dans notre communaute !'
        },
        {
            'parent': Comment.objects.filter(body__contains='recommandations de lectures').first(),
            'author': users[2],
            'body': 'Je recommande "Life 3.0" de Max Tegmark et "Superintelligence" de Nick Bostrom. Excellentes lectures !'
        }
    ]
    
    for reply_data in replies_data:
        if reply_data['parent']:
            reply, created = Comment.objects.get_or_create(
                article=reply_data['parent'].article,
                author=reply_data['author'],
                body=reply_data['body'],
                parent=reply_data['parent']
            )
            if created:
                print(f"[OK] Reponse creee")
    
    print(f"\n[SUCCESS] Donnees de demonstration creees avec succes !")
    print(f"[INFO] Resume :")
    print(f"   - {User.objects.count()} utilisateurs")
    print(f"   - {Article.objects.count()} articles")
    print(f"   - {Comment.objects.count()} commentaires")
    print(f"\n[ACCOUNTS] Comptes de test :")
    for user_data in users_data:
        print(f"   - {user_data['username']} / {user_data['password']}")

if __name__ == '__main__':
    create_demo_data()