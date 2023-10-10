from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Модель поста
    """

    # вложенный класс, чтобы выдавать одну из строк в поле status, экземпляр не предполагается - без self
    class Status(models.TextChoices):
        """
        Класс на TextChoices основан на enum, но можно обратиться к
        его атрибутам в shell или любом месте проекта:

        choices =[('DF', 'Draft'), ('PB', 'Published')]
        labels = ['Draft', 'Published']
        values = ['DF', 'PB']
        names = ['DRAFT', 'PUBLISHED']
        """

        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now()) # как datetime.now() с учетом пояса
    created = models.DateTimeField(auto_now_add=True) # время создания объекта
    updated = models.DateTimeField(auto_now=True) # время сохранения (редактирования)
    status = models.CharField(max_length=2,
                              choices=Status.choices, # вложенный класс
                              default=Status.DRAFT)

    class Meta:
        # чтобы выдача по умолчанию была от более свежего к более старому посту
        ordering = ['-publish']
        # индексирование в БД помогает быстрее находить физическое расположение записи в памяти по значению поля
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
