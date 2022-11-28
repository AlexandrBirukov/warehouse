from django.db import models


class BaseModel(models.Model):
    """
    Basic model
    """
    created_at = models.DateTimeField('Время создания', auto_now_add=True)
    updated_at = models.DateTimeField('Время изменения', auto_now=True)
    deleted_at = models.DateTimeField('Время удаления', blank=True, null=True, default=None)

    class Meta:
        abstract = True


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
