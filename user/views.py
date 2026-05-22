
from django.db import connection
from django.views.generic import DetailView
from django.http import Http404
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EditProfileForm
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .forms import LoginForm
import bcrypt
from user.models import Profile

class LoginProfileView(FormView):
    template_name = './user/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        try:
            # Пытаемся найти пользователя по имени в вашей модели
            user = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            form.add_error(None, "Неправильное имя пользователя или пароль")
            return self.form_invalid(form)

        # Проверяем введённый пароль с хэшем в базе данных
        hashed_password = user.password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            # Если пароль верный, логиним пользователя
            login(self.request, user)
            return HttpResponseRedirect(f'/profile/{user.username}/')

        else:
            # Если пароль неверный, возвращаем ошибку
            form.add_error(None, "Неправильное имя пользователя или пароль")
            return self.form_invalid(form)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'user/register.html'
    success_url = '/'

    def form_valid(self, form):
        # Сохраняем форму и логиним пользователя
        user = form.save()
        login(self.request, user)


        return redirect('profile', username=user.username)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

class ProfileView(DetailView):
    model = get_user_model()
    template_name = "user/profile.html"
    context_object_name = "profile"
    extra_context = {"title": "Профиль"}

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")  # Получаем имя пользователя из URL
        try:
            if username:
                return self.model.objects.get(username=username)  # Ищем пользователя по имени
            return self.request.user  # Если имя не передано, показываем профиль текущего пользователя
        except self.model.DoesNotExist:
            raise Http404("Пользователь не найден")


def logout_profile(request: HttpRequest) -> HttpResponse:
    logout(request=request)
    return redirect("home")



class EditProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = EditProfileForm
    template_name = "user/edit_profile.html"
    extra_context = {"title": "Редактировать профиль"}

    def get_success_url(self):
        return reverse_lazy("profile", kwargs={"username": self.request.user.username})

    def get_object(self):
        return self.request.user

    def form_invalid(self, form):
        return super().form_invalid(form)


def import_users_from_auth():
    try:
        print("Запуск импорта пользователей...")

        # Извлечение данных из таблицы auth
        with connection.cursor() as cursor:
            cursor.execute("""SELECT `NICKNAME`, `HASH` FROM `baseblock`.`auth`""")
            users = cursor.fetchall()

        # Перебираем пользователей и создаем их в Django
        for user_data in users:
            nickname = user_data[0]
            hashed_password = user_data[1]  # Уже захешированный пароль

            # Используем get_or_create, чтобы избежать дублирования
            user_model = get_user_model()  # Получаем модель, указанную в AUTH_USER_MODEL
            user, created = user_model.objects.get_or_create(
                username=nickname,
                defaults={'password': hashed_password}  # Храним bcrypt хэш пароля
            )

            if created:

                user.profile_image = 'media/MinecraftLogo.png'  # Устанавливаем дефолтное изображение
                user.donate = None
                user.description = "Описание отсутствует"
                user.city = "Не указан"
                user.social_rating = 0
                user.save()
                print(f"Пользователь {nickname} успешно добавлен.")
            else:
                print(f"Пользователь {nickname} уже существует.")
    except Exception as e:
        print(f"Ошибка: {e}")


def login_view(request):
    import_users_from_auth()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")  # Редирект после успешного входа
            else:
                # Добавление ошибки в форму
                form.add_error(None, "Неверное имя пользователя или пароль")
    else:
        form = LoginForm()

    return render(request, "user/login.html", {"form": form})
