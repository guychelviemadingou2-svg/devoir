@echo off
echo.
echo ========================================
echo   🦋 BLOG INTERACTIF - DEMARRAGE RAPIDE
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo    Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.

REM Créer l'environnement virtuel s'il n'existe pas
if not exist "venv" (
    echo 📦 Création de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erreur lors de la création de l'environnement virtuel
        pause
        exit /b 1
    )
    echo ✅ Environnement virtuel créé
) else (
    echo ✅ Environnement virtuel existant
)

echo.

REM Activer l'environnement virtuel
echo 🔄 Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo 📚 Installation des dépendances...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances
    pause
    exit /b 1
)

echo ✅ Dépendances installées
echo.

REM Migrations de base de données
echo 🗄️ Configuration de la base de données...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ❌ Erreur lors des migrations
    pause
    exit /b 1
)

echo ✅ Base de données configurée
echo.

REM Vérifier si des données de démo existent
python -c "import django; django.setup(); from blog.models import Article; print('DEMO_EXISTS' if Article.objects.exists() else 'NO_DEMO')" > temp_check.txt
set /p DEMO_STATUS=<temp_check.txt
del temp_check.txt

if "%DEMO_STATUS%"=="NO_DEMO" (
    echo 🎭 Création des données de démonstration...
    python create_demo_data.py
    if errorlevel 1 (
        echo ⚠️ Erreur lors de la création des données de démo (non critique)
    ) else (
        echo ✅ Données de démonstration créées
    )
) else (
    echo ✅ Données de démonstration déjà présentes
)

echo.
echo ========================================
echo   🚀 LANCEMENT DU SERVEUR
echo ========================================
echo.
echo 🌐 Le blog sera accessible sur : http://127.0.0.1:8000/
echo 🔧 Interface admin sur : http://127.0.0.1:8000/admin/
echo.
echo 👥 Comptes de test disponibles :
echo    - gaetane / demo123
echo    - alice / demo123  
echo    - bob / demo123
echo    - claire / demo123
echo.
echo 💡 Appuyez sur Ctrl+C pour arrêter le serveur
echo.

REM Lancer le serveur
python manage.py runserver

echo.
echo 👋 Serveur arrêté. À bientôt !
pause