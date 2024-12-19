from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.db import models


class Servers(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название сервера", blank=True)
    slug = models.SlugField(
        max_length=25, verbose_name="Слаг", unique=True, blank=False
    )
    max_online = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Серверы"


class News(models.Model):
    title = models.CharField(
        max_length=40,
        unique=True,
        blank=False,
        verbose_name="Название новости",
        name="title",
    )
    text = models.TextField(
        max_length=10000,
        unique=False,
        blank=False,
        verbose_name="Содержание новости",
    )
    image = models.ImageField(
        upload_to="media/news/%Y/%m/%d/",
        default="media/MinecraftLogo.png",
        verbose_name="Изображение новости",
    )
    time_create = models.DateTimeField(verbose_name="Дата создания", auto_now=True)
    time_update = models.DateTimeField(
        verbose_name="Дата обновления", auto_now_add=True
    )
    slug = models.SlugField(
        verbose_name="Слаг",
        max_length=50,
    )
    is_published = models.BooleanField(verbose_name="Опубликована", default=False)
    server = models.ForeignKey(
        "Servers",
        related_name="serv",
        on_delete=models.DO_NOTHING,
        verbose_name="Наименование сервера",
    )

    def get_absolute_url(self):
        return reverse("new", kwargs={"server": self.server.id, "new": self.slug})

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"




class Screenshot(models.Model):
    user = models.ForeignKey('user.Profile', on_delete=models.CASCADE, related_name="screenshots")
    image = models.ImageField(upload_to='screenshots/')
    description = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Скриншот от {self.user.username} - {self.description}"




class Event(models.Model):
    title = models.CharField(max_length=40, verbose_name="Название ивента")
    description = models.TextField(max_length=500, verbose_name="Описание ивента")
    date = models.DateField(verbose_name="Дата проведения")
    time = models.TimeField(verbose_name="Время начала")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активный ивент")
    participants = models.ManyToManyField(
        'user.Profile',
        related_name='participated_events',
        verbose_name="Участники"
    )
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(
        max_length=255,
        verbose_name="Место проведения",
        null=True,
        blank=True,
        default=""
    )
    coordinates = models.CharField(
        max_length=255,
        verbose_name="Координаты",
        null=True,
        blank=True,
        default=""
    )
    image1 = models.ImageField(upload_to="events/images", blank=True, null=True, verbose_name="Картинка 1")
    image2 = models.ImageField(upload_to="events/images", blank=True, null=True, verbose_name="Картинка 2")
    image3 = models.ImageField(upload_to="events/images", blank=True, null=True, verbose_name="Картинка 3")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_events",
        verbose_name="Автор",
        null=True,
        blank=True
    )
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('started', 'Начат'),
        ('finished', 'Закончен'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='waiting',
        verbose_name="Статус"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Event.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        if self.date < timezone.now().date() or (self.date == timezone.now().date() and self.time < timezone.now().time()):
            raise ValueError("Невозможно создать ивент в прошлом")
        if not self.status:
            self.status = 'waiting' 
        super().save(*args, **kwargs)

    def get_images(self):
        """
        Возвращает список всех доступных изображений.
        """
        return [self.image1, self.image2, self.image3]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ивент"
        verbose_name_plural = "Ивенты"





