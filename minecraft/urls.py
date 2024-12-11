from django.urls import path
import minecraft.views as views
from django.views.decorators.cache import cache_page
from django.urls import path
from . import views

from minecraft import ollama_api
from minecraft.views import MapPage
from django.urls import path
from minecraft.views import EventsPage, RulesPage, AchievementsPage
urlpatterns = [
    path("", cache_page(30)(views.HomePage.as_view()), name="home"),
    path("about/", (views.AboutPage.as_view()), name="about"),
    path("contacts/", views.ContactsPage.as_view(), name="contacts"),
    path("donate/", views.DonatePage.as_view(), name="donate"),
    path('map/', MapPage.as_view(), name='map'),
    path('events/', views.events_page, name='events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),  # Добавьте этот маршрут
    path('events/create/', views.create_event, name='create_event'),  # Новый путь для создания ивента
    path("rules/", RulesPage.as_view(), name="rules"),
    path("advancements/", AchievementsPage.as_view(), name="advancements"),
    path("news/<int:server>/<slug:new>",cache_page(5 * 60)(views.NewPage.as_view()),name="new",),
    path('chat/', ollama_api.chat_view, name='chat'),
    path('event/<int:event_id>/leave/', views.leave_event, name='leave_event'),
    path('event/<int:event_id>/mark_attendance/', views.mark_attendance, name='event_mark_attendance'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('users/', views.user_list, name='user_list'),  # Страница с пользователями
]
