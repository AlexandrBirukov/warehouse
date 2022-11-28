from django.db import models

from project.utils.models import BaseModel


class PlaceQuerySet(models.QuerySet):
    """Extended queryset for Place model."""

    def active(self):
        """Return not deleted places"""
        return self.filter(deleted_at=None)


class Place(BaseModel):
    title = models.CharField('Название', max_length=255, null=False)

    objects = PlaceQuerySet.as_manager()

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'
        ordering = ['title']

    def __str__(self):
        return self.title
