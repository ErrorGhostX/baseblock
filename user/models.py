from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class Donate(models.Model):
    name = models.CharField(
        verbose_name="Наименование доната",
        max_length=50,
        blank=False,
        unique=True,
    )
    responsobility = models.IntegerField("Сила доната", blank=False)
    image = models.ImageField(
        blank=True,
        verbose_name="Изображение доната",
        upload_to="donates/",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Донат"
        verbose_name_plural = "Донаты"

class Role(models.Model):
    name = models.CharField(
        verbose_name="Наименование роли",
        max_length=50,
        blank=False,
        unique=True,
    )
    responsobility = models.IntegerField("Сила роли", blank=False)
    image = models.ImageField(
        blank=True,
        verbose_name="Изображение роли",
        upload_to="roles/",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Роли"
        verbose_name_plural = "Роли"

class Achievement(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название достижения"
    )
    description = models.TextField(
        verbose_name="Описание достижения"
    )
    earned_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата получения"
    )
    image = models.ImageField(
        blank=True,
        verbose_name="Изображение достижения",
        upload_to="achivements/",
    )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"

class Conviction(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название судимости"
    )
    description = models.TextField(
        verbose_name="Описание судимости"
    )
    earned_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата получения"
    )
    image = models.ImageField(
        blank=True,
        verbose_name="Изображение судимсоти",
        upload_to="conviction/",
    )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Судимость"
        verbose_name_plural = "Судимости"

from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    profile_image = models.ImageField(
        upload_to="media/profiles/%Y/%m/%d",
        default="media/MinecraftLogo.png",
        verbose_name="Фото пользователя",
    )
    donate = models.ForeignKey(
        "Donate",
        related_name="don",
        verbose_name="Донат пользователя",
        on_delete=models.SET_NULL,
        default=None,
        null=True,
    )
    role = models.ForeignKey(
        "Role",
        related_name="role",
        verbose_name="Роль пользователя",
        on_delete=models.SET_NULL,
        default=None,
        null=True,
    )
    achievement = models.ManyToManyField(
        "Achievement",
        related_name="achive",
        verbose_name="Достижение пользователя",
        default=None,
        null=True,
    )
    conviction = models.ManyToManyField(
        "Conviction",
        related_name="conviction",
        verbose_name="Судимости пользователя",
    )

    description = models.TextField(
        verbose_name="Описание", blank=True, null=True, default="Описание отсутствует"
    )
    city = models.CharField(
        verbose_name="Город", max_length=100, blank=True, null=True, default="Не указан"
    )
    social_rating = models.IntegerField(
        verbose_name="Социальный рейтинг", default=0
    )
    passed_events = models.ManyToManyField(
        'minecraft.Event',
        related_name='passed_by',
        blank=True)
  # judgments = models.ManyToManyField(
  #      "Judgment", blank=True, verbose_name="Судимости"
   # )


    def get_absolute_url(self):
        return reverse("profile")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
