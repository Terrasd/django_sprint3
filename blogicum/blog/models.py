from django.contrib.auth import get_user_model
from django.db import models

from blog.constants import MAX_LENGTH_FOR_CHARFIELDS, CONST_TRUNCATECHAR

User = get_user_model()


class PublishedCreatedModel(models.Model):
    """
    Абстрактный класс для описывания статуса и времени публикации.
    Метод "truncate" возвращает обрезанную строку с "..." на конце
    (длина обрезки задается константой CONST_TRUNCATECHAR).
    """

    def truncate(self, text):
        return (text if len(text) < CONST_TRUNCATECHAR + 1
                else text[:CONST_TRUNCATECHAR] + '...')

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(PublishedCreatedModel):
    """Категории постов."""

    title = models.CharField(
        max_length=MAX_LENGTH_FOR_CHARFIELDS,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.truncate(self.title)


class Location(PublishedCreatedModel):
    """
    Местоположение. Если оставить поле пустым,
    будет указано "Планета Земля" (условие задано в шаблоне "post_card.html").
    """

    name = models.CharField(
        max_length=MAX_LENGTH_FOR_CHARFIELDS,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.truncate(self.name)


class Post(PublishedCreatedModel):
    """
    Пост собственной персоной. Поля "author", "location" и "category"
    связываются по внешнему ключу.
    """

    title = models.CharField(
        max_length=MAX_LENGTH_FOR_CHARFIELDS,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-is_published', '-pub_date')

    def __str__(self):
        return self.truncate(self.title)
