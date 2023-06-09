from django.db import models
from django.utils import timezone

from core.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)

    class Meta:
        abstract = True


class Board(BaseModel):
    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    title = models.CharField(verbose_name='Название', max_length=255)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)

    def __str__(self):
        return f'{self.title}'


class BoardParticipant(BaseModel):
    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Доски'
        unique_together = ('board', 'user')

    class Role(models.IntegerChoices):
        owner = 1, 'Владелец'
        writer = 2, 'Редактор'
        reader = 3, 'Читатель'

    board = models.ForeignKey(Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='participants')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT, related_name='participants')
    role = models.PositiveSmallIntegerField(verbose_name='Роль', choices=Role.choices, default=Role.owner)

    def __str__(self):
        return f'{self.board}: {self.user}'


class GoalCategory(BaseModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(max_length=255, verbose_name='Название')
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)
    board = models.ForeignKey(Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='categories')

    def __str__(self):
        return self.title


class Goal(BaseModel):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='', null=True, blank=True)
    category = models.ForeignKey(
        to=GoalCategory,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='goals'
    )
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус',
        choices=Status.choices,
        default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name='Приоритет',
        choices=Priority.choices,
        default=Priority.medium
    )
    due_date = models.DateTimeField(verbose_name='Дата выполнения', null=True, blank=True)
    user = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        on_delete=models.PROTECT,
        related_name='goals'
    )

    def __str__(self):
        return self.title


class GoalComment(BaseModel):
    user = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.PROTECT, related_name='comments')
    goal = models.ForeignKey(to=Goal, verbose_name='Цель', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


