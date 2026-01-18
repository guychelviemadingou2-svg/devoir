from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Article, Comment, Tag, UserProfile, ArticleView
from .forms import ArticleForm, CommentForm, SignUpForm, UserProfileForm
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Créer le profil utilisateur
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} ! Votre compte a été créé avec succès.')
            return redirect('article_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def article_list(request):
    articles = Article.objects.filter(status='published').select_related('author').prefetch_related('tags', 'likes')
    
    # Filtrage par tag
    tag_slug = request.GET.get('tag')
    if tag_slug:
        articles = articles.filter(tags__slug=tag_slug)
    
    # Recherche
    search_query = request.GET.get('search')
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Tri
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['-created_at', '-views', '-likes', 'title']:
        if sort_by == '-likes':
            articles = articles.annotate(likes_count=Count('likes')).order_by('-likes_count')
        else:
            articles = articles.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Tags populaires
    popular_tags = Tag.objects.annotate(article_count=Count('articles')).order_by('-article_count')[:10]
    
    context = {
        'page_obj': page_obj,
        'popular_tags': popular_tags,
        'current_tag': tag_slug,
        'search_query': search_query,
        'sort_by': sort_by
    }
    return render(request, 'blog/article_list.html', context)

def article_detail(request, pk):
    article = get_object_or_404(Article.objects.select_related('author').prefetch_related('tags', 'likes'), pk=pk)
    
    # Incrémenter les vues (une fois par IP/utilisateur)
    ip_address = get_client_ip(request)
    view_obj, created = ArticleView.objects.get_or_create(
        article=article,
        user=request.user if request.user.is_authenticated else None,
        ip_address=ip_address
    )
    if created:
        article.increment_views()
    
    comments = article.comments.filter(parent=None).select_related('author').prefetch_related('replies__author')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            messages.success(request, 'Commentaire ajouté avec succès !')
            return redirect('article_detail', pk=pk)
    else:
        form = CommentForm()
    
    # Articles similaires (même tags)
    similar_articles = Article.objects.filter(
        tags__in=article.tags.all(),
        status='published'
    ).exclude(pk=article.pk).distinct()[:3]
    
    context = {
        'article': article,
        'comments': comments,
        'form': form,
        'similar_articles': similar_articles
    }
    return render(request, 'blog/article_detail.html', context)

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, '✅ Article publié avec succès !')
            return redirect('article_detail', pk=article.pk)
        else:
            # Afficher les erreurs spécifiques
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form, 'title': 'Créer un article'})

@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author != request.user and not request.user.is_staff:
        messages.error(request, "Vous n'avez pas la permission de modifier cet article.")
        return redirect('article_detail', pk=pk)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Article modifié avec succès !')
            return redirect('article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {'form': form, 'title': 'Modifier l\'article'})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author == request.user or request.user.is_staff:
        article.delete()
        messages.success(request, "Article supprimé avec succès.")
    else:
        messages.error(request, "Permission refusée.")
    return redirect('article_list')

@login_required
@require_POST
def like_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    user_liked = article.likes.filter(id=request.user.id).exists()
    
    if user_liked:
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True
    
    # Réponse AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': article.total_likes
        })
    
    return redirect('article_detail', pk=pk)

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    user_articles = Article.objects.filter(author=user, status='published').order_by('-created_at')[:5]
    
    context = {
        'profile_user': user,
        'profile': profile,
        'user_articles': user_articles,
        'is_own_profile': request.user == user
    }
    return render(request, 'blog/user_profile.html', context)

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            # Mettre à jour les informations utilisateur
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.save()
            profile.save()
            messages.success(request, '✅ Profil mis à jour avec succès !')
            return redirect('user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=profile)
        # Pré-remplir les champs utilisateur
        form.fields['first_name'].initial = request.user.first_name
        form.fields['last_name'].initial = request.user.last_name
        form.fields['email'].initial = request.user.email
    
    return render(request, 'blog/edit_profile.html', {'form': form})

@login_required
def account_settings(request):
    """Vue pour les paramètres avancés du compte"""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            
            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, '🔒 Mot de passe modifié avec succès !')
            else:
                messages.error(request, '❌ Ancien mot de passe incorrect.')
        
        elif action == 'delete_account':
            # Logique de suppression de compte (à implémenter avec précaution)
            messages.warning(request, '⚠️ Fonctionnalité de suppression en cours de développement.')
    
    return render(request, 'blog/account_settings.html')

def tag_list(request):
    tags = Tag.objects.annotate(article_count=Count('articles')).order_by('-article_count')
    return render(request, 'blog/tag_list.html', {'tags': tags})

def search_articles(request):
    query = request.GET.get('q', '')
    articles = []
    
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        ).select_related('author').prefetch_related('tags')[:10]
    
    # Réponse AJAX pour l'autocomplétion
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        results = [{
            'id': article.id,
            'title': article.title,
            'author': article.author.username,
            'url': article.get_absolute_url()
        } for article in articles]
        return JsonResponse({'results': results})
    
    return render(request, 'blog/search_results.html', {
        'articles': articles,
        'query': query
    })
