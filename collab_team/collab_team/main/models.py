from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Project(models.Model):
    objects = None
    title = models.CharField(_('Название проекта'), max_length=70)
    description = models.TextField(_('Описание'), max_length=255)
    cover_image = models.ImageField(_('Изображение обложки'), upload_to='projects/')
    author = models.ForeignKey(User, verbose_name=_('Автор'), on_delete=models.CASCADE)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')  # Связь с проектом
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, оставивший комментарий
    text = models.TextField()  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания
    file = models.FileField(upload_to='comment_files/', blank=True, null=True)  # Опциональный файл

    def __str__(self):
        return f'{self.author.username}: {self.text[:20]}'
