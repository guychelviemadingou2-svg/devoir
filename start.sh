#!/bin/bash

echo ""
echo "========================================"
echo "  🦋 BLOG INTERACTIF - DÉMARRAGE RAPIDE"
echo "========================================"
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    echo "   Veuillez installer Python 3.8+ depuis https://python.org"
    exit 1
fi

echo "✅ Python détecté"
echo ""

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de la création de l'environnement virtuel"
        exit 1
    fi
    echo "✅ Environnement virtuel créé"
else
    echo "✅ Environnement virtuel existant"
fi

echo ""

# Activer l'environnement virtuel
echo "🔄 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📚 Installation des dépendances..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi

echo "✅ Dépendances installées"
echo ""

# Migrations de base de données
echo "🗄️ Configuration de la base de données..."
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Erreur lors des migrations"
    exit 1
fi

echo "✅ Base de données configurée"
echo ""

# Vérifier si des données de démo existent
DEMO_STATUS=$(python -c "import django; django.setup(); from blog.models import Article; print('DEMO_EXISTS' if Article.objects.exists() else 'NO_DEMO')")

if [ "$DEMO_STATUS" = "NO_DEMO" ]; then
    echo "🎭 Création des données de démonstration..."
    python create_demo_data.py
    if [ $? -ne 0 ]; then
        echo "⚠️ Erreur lors de la création des données de démo (non critique)"
    else
        echo "✅ Données de démonstration créées"
    fi
else
    echo "✅ Données de démonstration déjà présentes"
fi

echo ""
echo "========================================"
echo "  🚀 LANCEMENT DU SERVEUR"
echo "========================================"
echo ""
echo "🌐 Le blog sera accessible sur : http://127.0.0.1:8000/"
echo "🔧 Interface admin sur : http://127.0.0.1:8000/admin/"
echo ""
echo "👥 Comptes de test disponibles :"
echo "   - gaetane / demo123"
echo "   - alice / demo123"
echo "   - bob / demo123"
echo "   - claire / demo123"
echo ""
echo "💡 Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

# Lancer le serveur
python manage.py runserver

echo ""
echo "👋 Serveur arrêté. À bientôt !"