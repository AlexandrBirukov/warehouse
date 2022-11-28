from django.db import models

from project.apps.place.models import Place
from project.apps.warehouse.models import ProductGroup
from project.utils.models import BaseModel


class MenuQuerySet(models.QuerySet):
    """Extended queryset for Menu model."""

    def active(self):
        """Return not deleted menus"""
        return self.filter(deleted_at=None)


class Menu(BaseModel):
    place = models.ForeignKey(
        Place,
        verbose_name='Ресторан',
        related_name='menus',
        on_delete=models.CASCADE,
    )
    title = models.CharField('Название', max_length=255, null=False)

    objects = MenuQuerySet.as_manager()

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ['title']

    def __str__(self):
        return self.title


class DishQuerySet(models.QuerySet):
    """Extended queryset for Dish model."""

    def active(self):
        """Return not deleted dishes"""
        return self.filter(deleted_at=None)


class Dish(BaseModel):
    menu = models.ForeignKey(
        Menu,
        verbose_name='Меню',
        related_name='dishes',
        on_delete=models.CASCADE,
    )
    title = models.CharField('Название', max_length=255, null=False)

    objects = DishQuerySet.as_manager()

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['title']

    def __str__(self):
        return self.title


class IngredientQuerySet(models.QuerySet):
    """Extended queryset for Ingredient model."""

    def active(self):
        """Return not deleted ingredients"""
        return self.filter(deleted_at=None)


class Ingredient(BaseModel):
    dish = models.ForeignKey(
        Dish,
        verbose_name='Блюдо',
        related_name='dishes',
        on_delete=models.CASCADE,
    )
    title = models.CharField('Название', max_length=255, null=False)

    objects = IngredientQuerySet.as_manager()

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['title']

    def __str__(self):
        return self.title


class TechMapQuerySet(models.QuerySet):
    """Extended queryset for TechMap model."""

    def active(self):
        """Return not deleted techmaps"""
        return self.filter(deleted_at=None)


class TechMap(BaseModel):
    dish = models.ForeignKey(
        Dish,
        verbose_name='Блюдо',
        related_name='techmaps',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='techmaps',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    product_group = models.ForeignKey(
        ProductGroup,
        verbose_name='Продукт',
        related_name='techmaps',
        on_delete=models.PROTECT,
    )
    net_weight = models.FloatField('Масса нетто')
    gross_weight = models.FloatField('Масса брутто')
    done_weight = models.FloatField('Выход готового продукта')
    uncritical = models.BooleanField('Не критичный для приготовления', default=False)

    objects = IngredientQuerySet.as_manager()

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.product_group.title
