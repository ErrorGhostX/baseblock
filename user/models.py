from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Create your models here.
class Donate(models.Model):
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
        upload_to="donates/",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Роли"
        verbose_name_plural = "Роли"


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
    description = models.TextField(
        verbose_name="Описание", blank=True, null=True, default="Описание отсутствует"
    )
    city = models.CharField(
        verbose_name="Город", max_length=100, blank=True, null=True, default="Не указан"
    )
    social_rating = models.IntegerField(
        verbose_name="Социальный рейтинг", default=0
    )
 #  events = models.ManyToManyField(
   #    "Event", blank=True, verbose_name="Пройденные ивенты"
 # )
  # judgments = models.ManyToManyField(
  #      "Judgment", blank=True, verbose_name="Судимости"
   # )


    def get_absolute_url(self):
        return reverse("profile")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
