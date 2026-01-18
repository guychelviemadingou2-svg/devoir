from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Articles
    path('', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/new/', views.article_create, name='article_create'),
    path('article/<int:pk>/edit/', views.article_update, name='article_update'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('article/<int:pk>/like/', views.like_article, name='like_article'),
    
    # Authentification
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='article_list'), name='logout'),
    
    # Profils utilisateur
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('account-settings/', views.account_settings, name='account_settings'),
    
    # Tags
    path('tags/', views.tag_list, name='tag_list'),
    
    # Recherche
    path('search/', views.search_articles, name='search_articles'),
]
