from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from followers.models import Follow


# Модель пользователя
class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    avatar = models.ImageField("Файл аватара", upload_to='users', null=True, blank=True)
    site = models.CharField("Сайт", max_length=200, blank=True)
    age = models.IntegerField("Возраст", default=0, blank=True)
    city = models.CharField("Город", max_length=30, blank=True)
    about_us = models.TextField("О себе", blank=True)
    status = models.TextField("Статус", max_length=250, blank=True)
    following = models.ManyToManyField('self', through=Follow, related_name="followers", symmetrical=False)

    class Gender(models.TextChoices):
        MAN = 'M', 'Мужчина'
        WOMAN = 'W', 'Женщина'

    gender = models.CharField(
        "Пол",
        max_length=1,
        choices=Gender.choices,
    )

    class Master(models.TextChoices):
        PHILOSOPHER = 'PHIL', 'Философ'
        PSYCHOLOGIST = 'PS', 'Психолог'
        PROGRAMMER = 'PR', 'Программист'
        ENGINEER = 'ENG', 'Инженер'
        PHYSICIST = 'PHYS', 'Физик'
        BIOLOGIST = 'BI', 'Биолог'
        HISTORIAN = 'HIS', 'Историк'

    master = models.CharField(
        "Мастер",
        max_length=4,
        choices=Master.choices,
        blank=True,
    )

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        print(self)
        self.is_active = False
        self.save()
        return self

    def get_absolute_url(self):
        return reverse('users:user_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
