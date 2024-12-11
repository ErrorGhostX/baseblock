from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from user.forms import RegisterForm, LoginForm, EditProfileForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.http import Http404
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EditProfileForm



from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from .forms import RegisterForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import RegisterForm  # Ваш RegisterForm


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



class LoginProfileView(LoginView):
    template_name = "user/login.html"
    form_class = LoginForm
    extra_context = {"title": "Авторизация пользователя"}

    def get_success_url(self) -> str:
        # Получаем пользователя из запроса
        user = self.request.user
        # Перенаправляем на страницу профиля с аргументом username
        return reverse("profile", kwargs={"username": user.username})

def logout_profile(request: HttpRequest) -> HttpResponse:
    logout(request=request)
    return redirect("home")

import logging



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
