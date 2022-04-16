from django.db import models
from django.urls import reverse

from users.models import User


# Модель секции
class Section(models.Model):
    name = models.CharField("Раздел", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"


# Модель топика
class Topic(models.Model):
    url = models.SlugField(max_length=130, unique=True, null=True)
    section = models.ForeignKey(Section, verbose_name="Секция",
                                null=True, related_name="topics", on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name="Автор",
                               related_name="topics", on_delete=models.PROTECT)
    title = models.CharField("Название", max_length=100)
    text = models.TextField("Основной текст", null=True, max_length=1000)
    views = models.IntegerField(default=0)
    datetime = models.DateTimeField("Дата и время создания", auto_now_add=True, blank=True)
    solved = models.BooleanField("Решено", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("forum:topic_detail", kwargs={"slug": self.url})

    class Meta:
        verbose_name = "Топик"
        verbose_name_plural = "Топики"


# Модель сообщения
class Message(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="messages")
    text = models.TextField("Текст сообщения", max_length=1000)
    datetime = models.DateTimeField("Дата и время добавления", auto_now=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
