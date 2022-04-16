from django.db import models
from django.urls import reverse

from users.models import User


# Модель ветки
class Branch(models.Model):
    name = models.CharField("Ветка", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ветка"
        verbose_name_plural = "Ветки"


# Модель лекции
class Lesson(models.Model):
    authors = models.ManyToManyField(User, related_name='authors')
    title = models.CharField("Урок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='lessons')
    content = models.TextField("Содержание")
    task = models.TextField("Задание")
    url = models.SlugField(max_length=130, unique=True, null=True)
    draft = models.BooleanField("Черновик", default=False)
    branch = models.ForeignKey(
        Branch, verbose_name="Ветка", related_name="lessons", on_delete=models.SET_NULL, null=True
    )
    date = models.DateField("Дата создания", auto_now_add=True)
    count = models.PositiveIntegerField("Количество просмотров", default=0)
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tutorial:lesson_detail", kwargs={"slug": self.url})


# Модель комментария
class Comment(models.Model):
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        "self", verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    lesson = models.ForeignKey(Lesson, verbose_name="Лекция", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
