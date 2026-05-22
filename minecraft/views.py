from django.views.generic import ListView, TemplateView, DetailView
from minecraft.models import News
from minecraft.service import get_online_servers
from django.views.generic import ListView
from user.models import Achievement
from .forms import EventAttendanceForm
from .forms import EventCreateForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ScreenshotForm
from django.http import JsonResponse
from .models import Screenshot
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Event
import requests
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.conf import settings
import os

class HomePage(ListView):
    template_name = "minecraft/index.html"
    model = News
    context_object_name = "news"
    allow_empty = True

    def get_queryset(self):
        return News.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)


        context["servers"] = get_online_servers([
            ("Выживание", "188.190.219.169", 25577),
        ])
        return context



class AboutPage(TemplateView):
    template_name = "minecraft/about.html"
    extra_context = {"title": "О нас"}


class ContactsPage(TemplateView):
    template_name = "minecraft/contacts.html"
    extra_context = {"title": "Контакты"}


class DonatePage(TemplateView):
    template_name = "minecraft/donate.html"
    extra_context = {"title": "Донат"}


class NewPage(DetailView):
    template_name = "minecraft/new.html"
    model = News
    context_object_name = "new"
    extra_context = {"title": "Новость"}

    def get_object(self, queryset=None):
        server_id = self.kwargs.get("server")
        new_slug = self.kwargs.get("new")
        return News.objects.get(server_id=server_id, slug=new_slug)

class MapPage(TemplateView):
    template_name = "minecraft/map.html"
    extra_context = {"title": "Карта"}

class RulesPage(TemplateView):
    template_name = "minecraft/rules.html"
    extra_context = {"title": "Правила"}


class EventsPage(ListView):
    template_name = "minecraft/events.html"
    model = Event
    context_object_name = "events"
    extra_context = {"title": "Ивенты"}

    def get_queryset(self):
        return Event.objects.filter(is_active=True).order_by("date")



def event_list(request):
    events = Event.objects.filter(is_active=True)  # Фильтруем активные ивенты
    form = EventAttendanceForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        event = form.save(commit=False)
        event.save()  # Сохраняем изменения в объекте
        form.save_m2m()  # Сохраняем many-to-many отношения

        return redirect('event_list')  # Перенаправляем на страницу с ивентами

    return render(request, 'minecraft/events.html', {'events': events, 'form': form})



@login_required(login_url='login')  # Указываем маршрут для страницы входа
def events_page(request):
    events = Event.objects.filter(is_active=True).order_by('date', 'time')  # Получаем активные ивенты
    return render(request, 'minecraft/events.html', {'events': events})


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_participant = event.participants.filter(id=request.user.id).exists()

    context = {
        "event": event,
        "is_participant": is_participant,
    }
    return render(request, "minecraft/event_detail.html", context)


@login_required
def update_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Получаем список участников
    participants = event.participants.all()

    participants_list = []
    for participant in participants:
        participants_list.append({
            'username': participant.username,
            'role': participant.role,
            'profile_url': reverse('profile', args=[participant.username]),
        })

    return JsonResponse({
        'participants': participants_list,
    })


@login_required
def start_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.author == request.user and event.status == 'waiting':
        event.status = 'started'
        event.save()
        messages.success(request, "Ивент начался!")

        # Кнопки не должны отображаться, когда ивент начался
        # Участников очищать не нужно, они остаются

    else:
        messages.error(request, "Вы не можете начать этот ивент.")
    return redirect('event_detail', event_id=event.id)

@login_required
def finish_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.author == request.user and event.status == 'started':
        event.status = 'finished'
        event.is_active = False  # Делаем ивент неактивным
        event.save()

        # Добавляем участникам ивента этот ивент в список пройденных
        for participant in event.participants.all():
            participant.passed_events.add(event)
            participant.save()

        messages.success(request, "Ивент завершен!")
    else:
        messages.error(request, "Вы не можете завершить этот ивент.")
    return redirect('event_detail', event_id=event.id)






def download_mods_page(request):
    return render(request, 'minecraft/download_mods.html')
def download_mods(request):
    # Путь к архиву
    mod_archive_path = os.path.join(settings.BASE_DIR, 'static', 'mods', 'mods.zip')
    if os.path.exists(mod_archive_path):
        with open(mod_archive_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="mods.zip"'
            return response
    else:
        return HttpResponse("Архив с модами не найден.", status=404)



@login_required
def screenshots_page(request):
    # Получение всех скриншотов
    screenshots = Screenshot.objects.select_related('user').all()

    # Обработка формы
    if request.method == 'POST':
        form = ScreenshotForm(request.POST, request.FILES)
        if form.is_valid():
            screenshot = form.save(commit=False)
            screenshot.user = request.user  # Привязываем скриншот к текущему пользователю
            screenshot.save()
            return redirect('view_screenshots')  # Перезагрузка страницы после успешной загрузки
    else:
        form = ScreenshotForm()

    # Рендеринг страницы
    return render(request, 'minecraft/view_screenshots.html', {'screenshots': screenshots, 'form': form})


@login_required
def event_mark_attendance(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.status == 'started':
        messages.error(request, "Невозможно присоединиться к ивенту, так как он уже начался.")
    else:
        if request.user in event.participants.all():
            event.participants.remove(request.user)
            messages.success(request, "Вы отказались от участия в ивенте.")
        else:
            event.participants.add(request.user)
            messages.success(request, "Вы успешно присоединились к ивенту.")
    return redirect('event_detail', event_id=event.id)


@login_required
def create_event(request):
    if request.method == "POST":
        form = EventCreateForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user  # Назначаем автора
            event.save()
            return redirect("event_detail", event_id=event.id)
    else:
        form = EventCreateForm()
    return render(request, "minecraft/create_event.html", {"form": form})



@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user in event.participants.all():
        event.participants.remove(request.user)
        messages.success(request, "Вы успешно отказались от участия в ивенте.")
    else:
        messages.info(request, "Вы не зарегистрированы на этот ивент.")
    return redirect("event_detail", event_id=event.id)

def user_list(request):
    users = get_user_model().objects.all()  # Получаем всех пользователей
    return render(request, 'minecraft/user_list.html', {'users': users})


#На будущее
class AchievementsPage(ListView):
    template_name = "minecraft/achievements.html"
    model = Achievement
    context_object_name = "achievements"
    extra_context = {"title": "Достижения"}

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)


def get_skin_url(self):
    if not self.minecraft_username:
        return "https://crafatar.com/renders/body/00000000000000000000000000000000?size=512&overlay"  # Заглушка

    try:
        # Получаем UUID игрока
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{self.minecraft_username}")
        if response.status_code == 200:
            uuid = response.json()["id"]
            return f"https://crafatar.com/renders/body/{uuid}?size=512&overlay"
    except Exception as e:
        print(f"Ошибка при получении UUID: {e}")
        pass

    return "https://crafatar.com/renders/body/00000000000000000000000000000000?size=512&overlay"  # Заглушка
