from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager): # прикладной менеджер запросов
    def get_queryset(self):
        """
        :return: QuerySet, отфильтрованный по значению PB
        """
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


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
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish') # для URL, на одну дату запрет на одинаковые слаги.
                                                       # параметр работат на уровне Джанго, а не БД.
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
    objects = models.Manager() # менеджер по умолчанию
    published = PublishedManager() # конкретно-прикладной менеджер

    class Meta:
        # чтобы выдача по умолчанию была от более свежего к более старому посту
        ordering = ['-publish']
        # индексирование в БД помогает быстрее находить физическое расположение записи в памяти по значению поля
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Динамически формирует URL-адрес.
        :return:
        """
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments') # вместо стандартного comment_set
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'