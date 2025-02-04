from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """
    Модель для представления группы.
    Хранит информацию о названии группы,
    ее уникальном идентификаторе и описании.
    """
    title = models.CharField(max_length=200)  # Название группы
    slug = models.SlugField(unique=True)  # Уникальный идентификатор для группы
    description = models.TextField()  # Описание группы

    def __str__(self):
        """
        Возвращает строковое представление объекта Group.
        Используется для отображения названия группы в админке.
        """
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("-pub_date",)  # Сортировка по дате публикации по убыванию

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField()
    created = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True,
    )


class Follow(models.Model):
    """
    Модель для представления подписок пользователей.
    Хранит информацию о том, кто на кого подписан.
    """
    user = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE,  # Удаляем подписки, если пользователь удален
    )
    following = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("user", "following")

    def __str__(self):
        """
        Возвращает строковое представление объекта Follow.
        """
        return f"{self.user.username} follows {self.following.username}"
