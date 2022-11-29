from django.db import models

from project.apps.place.models import Place
from project.apps.warehouse.models import NomenclatureGroup, MeasureUnit
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


class ModifierQuerySet(models.QuerySet):
    """Extended queryset for Modifier model."""

    def active(self):
        """Return not deleted modifiers"""
        return self.filter(deleted_at=None)


class Modifier(BaseModel):
    """
    Модификатор
    """
    dish = models.ForeignKey(
        Dish,
        verbose_name='Блюдо',
        related_name='modifiers',
        on_delete=models.CASCADE,
    )
    title = models.CharField('Название', max_length=255, null=False)

    objects = ModifierQuerySet.as_manager()

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
    """
    Тех.карта
    """
    dish = models.OneToOneField(
        Dish,
        verbose_name='Блюдо',
        on_delete=models.CASCADE,
    )
    description = models.TextField('Описание')
    measure_unit = models.ForeignKey(
        MeasureUnit,
        verbose_name='Единица измерения',
        related_name='techmaps',
        on_delete=models.PROTECT,
    )
    output = models.FloatField('Суммарный выход продукта')
    price = models.DecimalField('Розничная цена', max_digits=9, decimal_places=2)
    bookmark_rate = models.PositiveSmallIntegerField('Норма закладки (порций)')

    objects = TechMapQuerySet.as_manager()

    class Meta:
        verbose_name = 'Тех.карта'
        verbose_name_plural = 'Тех.карты'

    def __str__(self):
        return self.dish.title


class TechMapPhotoQuerySet(models.QuerySet):
    """Extended queryset for TechMapPhoto model."""

    def active(self):
        """Return not deleted photos"""
        return self.filter(deleted_at=None)


class TechMapPhoto(BaseModel):
    """
    Фотки накладной
    """
    image_url = models.URLField('Изображение накладной')
    tech_map = models.ForeignKey(
        TechMap,
        verbose_name='Тех.карта',
        related_name='photos',
        on_delete=models.CASCADE,
    )

    objects = TechMapPhotoQuerySet.as_manager()

    class Meta:
        verbose_name = 'Фото тех.карты'
        verbose_name_plural = 'Фото тех.карты'

    def __str__(self):
        return self.image_url


class IngredientQuerySet(models.QuerySet):
    """Extended queryset for Ingredient model."""

    def active(self):
        """Return not deleted ingredients"""
        return self.filter(deleted_at=None)


class Ingredient(BaseModel):
    """
    Ингредиенты тех.карты
    """
    dish = models.ForeignKey(
        Dish,
        verbose_name='Блюдо',
        related_name='ingredients',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    modifier = models.ForeignKey(
        Modifier,
        verbose_name='Модификатор',
        related_name='ingredients',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    nomenclature_group = models.ForeignKey(
        NomenclatureGroup,
        verbose_name='Номенклатурная группа',
        related_name='ingredients',
        on_delete=models.PROTECT,
    )

    # Единица измерения должна выбираться из доступных единиц измерения номенклатурной группы
    measure_unit = models.ForeignKey(
        MeasureUnit,
        verbose_name='Единица измерения',
        related_name='ingredients',
        on_delete=models.PROTECT,
    )
    amount = models.FloatField('Количество', default=1)
    done_weight = models.FloatField('Выход готового продукта')
    uncritical = models.BooleanField('Не критичный для приготовления', default=False)

    objects = IngredientQuerySet.as_manager()

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.nomenclature_group.title
