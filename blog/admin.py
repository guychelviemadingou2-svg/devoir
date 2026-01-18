from django.contrib import admin
from .models import Article, Comment, Tag, UserProfile, ArticleView

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'article_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Nombre d\'articles'

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'is_featured', 'views', 'total_likes', 'total_comments', 'created_at']
    list_filter = ['status', 'is_featured', 'created_at', 'tags']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at', 'views']
    filter_horizontal = ['tags', 'likes']
    list_editable = ['status', 'is_featured']
    
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'content', 'image')
        }),
        ('Métadonnées', {
            'fields': ('author', 'tags', 'status', 'is_featured')
        }),
        ('Statistiques', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'author', 'body_preview', 'parent', 'created_at']
    list_filter = ['created_at', 'article']
    search_fields = ['body', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body
    body_preview.short_description = 'Aperçu du commentaire'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'website', 'created_at']
    list_filter = ['created_at', 'location']
    search_fields = ['user__username', 'user__email', 'bio']
    readonly_fields = ['created_at']

@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'ip_address', 'timestamp']
    list_filter = ['timestamp', 'article']
    readonly_fields = ['timestamp']
    
    def has_add_permission(self, request):
        return False  # Empêcher l'ajout manuel
