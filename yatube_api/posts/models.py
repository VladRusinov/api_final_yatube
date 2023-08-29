from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


TITLE_LETTER_LIMIT = 30


class Group(models.Model):
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('Слаг', unique=True)
    description = models.TextField('Описание')

    def __str__(self):
        return self.title[:TITLE_LETTER_LIMIT]


class Post(models.Model):
    """Модель публикации"""

    text = models.TextField("текст")
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='posts/', verbose_name="Изображение", null=True, blank=True
    )
    group = models.ForeignKey(
        Group,
        verbose_name='Группа',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        default_related_name = 'posts'
        ordering = ['pub_date']

    def __str__(self):
        return self.text[:TITLE_LETTER_LIMIT]


class Comment(models.Model):
    """Модель комментария"""

    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        Post,
        verbose_name="Публикация",
        on_delete=models.CASCADE,
    )
    text = models.TextField("Текст")
    created = models.DateTimeField(
        'Дата создания', auto_now_add=True, db_index=True
    )

    class Meta:
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:TITLE_LETTER_LIMIT]


class Follow(models.Model):
    """Модель подписки"""

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name='follow',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_following'
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_follow",
                check=~models.Q(user=models.F("following")),
            ),
        ]

    def __str__(self):
        return (self.user + self.following)[:TITLE_LETTER_LIMIT]
