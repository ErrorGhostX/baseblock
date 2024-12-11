from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class LoginForm(AuthenticationForm):

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]

from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm

class EditProfileForm(ModelForm):
    # Параметры для редактирования
    username = forms.CharField(
        disabled=True,  # Имя пользователя нельзя редактировать
        label="Имя профиля",
        widget=forms.TextInput(attrs={"class": "w-full p-2 bg-gray-900 border border-purple-600 rounded-lg"})
    )
    first_name = forms.CharField(
        label="Ваше имя",
        widget=forms.TextInput(attrs={"class": "w-full p-2 bg-gray-900 border border-purple-600 rounded-lg"})
    )
    profile_image = forms.ImageField(
        required=False,
        label="Фото профиля",
        widget=forms.FileInput(attrs={"class": "w-full p-2 bg-gray-900 border border-purple-600 rounded-lg"})
    )
    description = forms.CharField(
        required=False,
        label="Описание",
        widget=forms.Textarea(attrs={"class": "w-full p-2 bg-gray-900 border border-purple-600 rounded-lg"})
    )
    city = forms.CharField(
        required=False,
        label="Город",
        widget=forms.TextInput(attrs={"class": "w-full p-2 bg-gray-900 border border-purple-600 rounded-lg"})
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "profile_image", "first_name", "description", "city"]


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=50,
        label="Придумайте логин",
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    password1 = forms.CharField(
        max_length=50,
        label="Придумайте пароль",
        widget=forms.PasswordInput(
            {
                "class": "password-input",
            }
        ),
    )
    password2 = forms.CharField(
        max_length=50,
        label="Повторите пароль",
        widget=forms.PasswordInput(
            {
                "class": "password-input",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "email": "Введите имейл",
        }
        widgets = {
            "email": forms.EmailInput(attrs={"class": "email-field"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой e-mail уже существует")
        return email

