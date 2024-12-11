from django.contrib import admin
from minecraft.models import News, Servers
from django.contrib import admin
from .models import Event

# Register your models here.
@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ["title", "text", "slug", "is_published", "server"]
    list_display_links = ["server"]
    list_editable = ["title", "text", "is_published"]


@admin.register(Servers)
class AdminServers(admin.ModelAdmin):
    list_display = ["max_online", "slug"]
    list_editable = ["slug"]


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'is_active')  # Что отображать в списке
    list_filter = ('is_active', 'date')  # Фильтры
    search_fields = ('title', 'description')  # Поиск по этим полям
    prepopulated_fields = {'slug': ('title',)}  # Если у вас есть поле slug

admin.site.register(Event, EventAdmin)
