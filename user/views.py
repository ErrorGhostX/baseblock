
from django.views.generic import DetailView
from django.http import Http404
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EditProfileForm, LoginForm
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password

from django.shortcuts import redirect
from django.views.generic.edit import FormView

from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from user.custom_hashers import BCrypt2aPasswordHasher  # Импортируем кастомный хешер

from django.contrib.auth import login
from user.custom_hashers import BCrypt2aPasswordHasher
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

class LoginProfileView(FormView):
    template_name = "user/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        # Получаем введённые данные
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Пытаемся найти пользователя
        user = get_user_model().objects.filter(username=username).first()

        if user:
            # Инициализируем кастомный хешер
            hasher = BCrypt2aPasswordHasher()

            # Получаем пароль из базы данных
            user_password = user.password

            # Генерация хеша для проверки введённого пароля
            hashed_password_for_check = hasher.encode(password, user_password.encode('utf-8'))

            # Проверяем пароль с помощью кастомного метода verify
            if hasher.verify(password, user.password):
                # Если пароль корректный, авторизуем пользователя
                login(self.request, user)
                return redirect('profile', username=user.username)
            else:
                form.add_error('password', 'Неверный пароль.')

            # Передаем данные в контекст для отображения в шаблоне
            context = {
                'form': form,
                'user_password': user_password,
                'hashed_password_for_check': hashed_password_for_check,
            }
            return render(self.request, self.template_name, context)

        else:
            form.add_error('username', 'Пользователь не найден.')

        return self.form_invalid(form)





class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'user/register.html'
    success_url = '/'  # Здесь пока будет главная страница (можно будет поменять)

    def form_valid(self, form):
        # Сохраняем форму и логиним пользователя
        user = form.save()
        login(self.request, user)

        # Перенаправляем на профиль пользователя
        return redirect('profile', username=user.username)  # Это исправление

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
                # Профиль уже привязан к пользователю через AbstractUser, он не нуждается в создании вручную
                user.profile_image = 'media/MinecraftLogo.png'  # Устанавливаем дефолтное изображение
                user.donate = None  # В зависимости от вашей логики
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
    # Вызов функции для импорта пользователей из auth таблицы
    # Вызов функции для импорта пользователей из auth таблицы
    import_users_from_auth()

    # Возвращаем страницу login.html
    return render(request, './user/login.html')



