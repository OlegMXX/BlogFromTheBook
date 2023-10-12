from django.contrib import admin
from .models import Post, Comment


# Регистрация модели Пост в админке

# Простой способ:
# admin.site.register(Post)

# Адаптация под конкретную задачу:
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status'] # отображаемые поля
    list_filter = ['status', 'created', 'publish', 'author'] # фильтрация по полям
    search_fields = ['title', 'body'] # поиск по полям
    prepopulated_fields = {'slug': ('title',)} # теперь поле slug заполняется само при заполнении заголовка
    raw_id_fields = ['author'] # задавать автора с помощью его id, а не из выпадающего списка
    date_hierarchy = 'publish' # навигация по иерархии дат
    ordering = ['status', 'publish'] # критерии сортировки

@ admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']