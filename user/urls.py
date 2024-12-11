from django.urls import path

from user import views
from user.views import (
    RegisterView,
    ProfileView,
    LoginProfileView,
    EditProfileView,
    logout_profile,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<str:username>/", ProfileView.as_view(), name="profile"),
    path("login/", LoginProfileView.as_view(), name="login"),
    path("logout/", logout_profile, name="logout"),
    path("profile/<int:id>/", views.ProfileView.as_view(), name="profile"),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),  # Профиль по имени
    path("profile/<str:username>/edit/", EditProfileView.as_view(), name="profile_edit"),

]
