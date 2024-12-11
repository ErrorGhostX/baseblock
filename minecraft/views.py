from django.views.generic import ListView, TemplateView, DetailView
from minecraft.models import News
from minecraft.service import get_online_servers
from django.views.generic import ListView
from minecraft.models import Achievement
from .forms import EventAttendanceForm
from django.contrib.auth.decorators import login_required
from .forms import EventCreateForm
from .models import Event
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages



class HomePage(ListView):
    template_name = "minecraft/index.html"
    news = {
        "title": "BaseBlock",
        "servers": get_online_servers([("188.190.219.169", "25577"),("188.190.219.169", "36656")]),
    }
    allow_empty = True
    model = News
    context_object_name = "news"

    def get_queryset(self):
        return News.objects.filter(is_published=True)


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




class EventsPage(ListView):
    template_name = "minecraft/events.html"
    model = Event
    context_object_name = "events"
    extra_context = {"title": "Ивенты"}

    def get_queryset(self):
        return Event.objects.filter(is_active=True).order_by("date")



class RulesPage(TemplateView):
    template_name = "minecraft/rules.html"
    extra_context = {"title": "Правила"}


class AchievementsPage(ListView):
    template_name = "minecraft/achievements.html"
    model = Achievement
    context_object_name = "achievements"
    extra_context = {"title": "Достижения"}

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)


def event_list(request):
    events = Event.objects.filter(is_active=True)  # Фильтруем активные ивенты
    form = EventAttendanceForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        event = form.save(commit=False)
        event.save()  # Сохраняем изменения в объекте
        form.save_m2m()  # Сохраняем many-to-many отношения

        return redirect('event_list')  # Перенаправляем на страницу с ивентами

    return render(request, 'minecraft/events.html', {'events': events, 'form': form})

def events_page(request):
    events = Event.objects.filter(is_active=True).order_by('date', 'time')  # Получаем активные ивенты
    return render(request, 'minecraft/events.html', {'events': events})


@login_required
def mark_attendance(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.participants.add(request.user)
    return redirect('event_detail', event_id=event.id)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'minecraft/event_detail.html', {'event': event})



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

    # Удаляем текущего пользователя из участников
    event.participants.remove(request.user)

    # Выводим сообщение и перенаправляем назад на страницу с ивентами
    messages.success(request, "Вы больше не участвуете в этом ивенте.")
    return redirect('event_detail', event_id=event.id)


from django.shortcuts import render
from django.contrib.auth import get_user_model

def user_list(request):
    users = get_user_model().objects.all()  # Получаем всех пользователей
    return render(request, 'minecraft/user_list.html', {'users': users})


