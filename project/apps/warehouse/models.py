from django.conf import settings
from django.db import models

from project.apps.place.models import Place
from project.utils.models import BaseModel


class WarehouseQuerySet(models.QuerySet):
    """Extended queryset for Warehouse model."""

    def active(self):
        """Return not deleted warehouses"""
        return self.filter(deleted_at=None)


class Warehouse(BaseModel):
    place = models.ForeignKey(
        Place,
        verbose_name='Ресторан',
        related_name='warehouses',
        on_delete=models.CASCADE,
    )
    in_charge_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Ответственный',
        related_name='warehouses',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    title = models.CharField('Название', max_length=255, null=False)

    objects = WarehouseQuerySet.as_manager()

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'
        ordering = ['title']

    def __str__(self):
        return self.title


class DepartmentTypes:
    STORAGE = 0
    CONSUMING = 1

    DEPARTMENT_TYPES_CHOICES = [
        (STORAGE, 'Хранение'),
        (CONSUMING, 'Потребление'),
    ]


class DepartmentQuerySet(models.QuerySet):
    """Extended queryset for Department model."""

    def active(self):
        """Return not deleted departments"""
        return self.filter(deleted_at=None)


class Department(BaseModel):
    Warehouse = models.ForeignKey(
        Warehouse,
        verbose_name='Склад',
        related_name='departments',
        on_delete=models.CASCADE,
    )
    in_charge_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Ответственный',
        related_name='departments',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
    )
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
    )
    title = models.CharField('Название', max_length=255, null=False)
    department_type = models.PositiveSmallIntegerField(
        'Тип департамента',
        help_text='Хранение/Потребление',
        choices=DepartmentTypes.DEPARTMENT_TYPES_CHOICES,
        default=DepartmentTypes.STORAGE,
    )

    objects = DepartmentQuerySet.as_manager()

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'
        ordering = ['title']

    def __str__(self):
        return self.title


class MeasurementSystems:
    METRIC = 0
    IMPERIAL = 1

    MEASUREMENT_SYSTEMS_CHOICES = [
        (METRIC, 'Метрическая'),
        (IMPERIAL, 'Имперская'),
    ]


class MeasureUnitQuerySet(models.QuerySet):
    """Extended queryset for MeasureUnit model."""

    def active(self):
        """Return not deleted measure units"""
        return self.filter(deleted_at=None)


class MeasureUnit(BaseModel):
    place = models.ForeignKey(
        Place,
        verbose_name='Ресторан',
        related_name='units',
        on_delete=models.CASCADE,
    )
    title = models.CharField('Название', max_length=255, null=False)
    measurement_system = models.PositiveSmallIntegerField(
        'Система измерений',
        choices=MeasurementSystems.MEASUREMENT_SYSTEMS_CHOICES,
        default=MeasurementSystems.METRIC,
    )

    objects = MeasureUnitQuerySet.as_manager()

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ['title']

    def __str__(self):
        return self.title


class ProductGroupQuerySet(models.QuerySet):
    """Extended queryset for ProductGroup model."""

    def active(self):
        """Return not deleted product groups"""
        return self.filter(deleted_at=None)


class ProductGroup(BaseModel):
    place = models.ForeignKey(
        Place,
        verbose_name='Ресторан',
        related_name='groups',
        on_delete=models.CASCADE,
    )
    vendor_code = models.PositiveIntegerField('Артикул')
    title = models.CharField('Название', max_length=255, null=False)
    shelf_life = models.PositiveSmallIntegerField(
        'Базовый срок хранения',
        help_text='В днях',
        blank=True,
        null=True,
        default=None,
    )
    minimum_balance = models.FloatField(
        'Минимальный остаток на складе',
        blank=True,
        null=True,
        default=None,
    )
    measure_unit = models.ForeignKey(
        MeasureUnit,
        verbose_name='Единица измерения',
        related_name='stdmesure',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
    )
    measure_unit_small = models.ForeignKey(
        MeasureUnit,
        verbose_name='Единица измерения для малых порций',
        related_name='smallmesure',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
    )

    objects = ProductGroupQuerySet.as_manager()

    class Meta:
        verbose_name = 'Группа товаров'
        verbose_name_plural = 'Группы товаров'
        ordering = ['vendor_code', 'title']

    def __str__(self):
        return self.title


class ProductPhotoQuerySet(models.QuerySet):
    """Extended queryset for ProductPhoto model."""

    def active(self):
        """Return not deleted photos"""
        return self.filter(deleted_at=None)


class ProductPhoto(BaseModel):
    image_url = models.URLField('Изображение продукта')

    objects = ProductPhotoQuerySet.as_manager()

    class Meta:
        verbose_name = 'Накладная'
        verbose_name_plural = 'Накладные'

    def __str__(self):
        return self.image_url


class InvoiceQuerySet(models.QuerySet):
    """Extended queryset for Invoice model."""

    def active(self):
        """Return not deleted invoices"""
        return self.filter(deleted_at=None)


class Invoice(BaseModel):
    image_url = models.URLField('Изображение накладной')
    invoice_number = models.CharField('Номер накладной', max_length=255, blank=True, null=True, default=None)
    invoice_data = models.DateField('Накладная от')

    objects = InvoiceQuerySet.as_manager()

    class Meta:
        verbose_name = 'Накладная'
        verbose_name_plural = 'Накладные'

    def __str__(self):
        return self.image_url


class ProviderQuerySet(models.QuerySet):
    """Extended queryset for Provider model."""

    def active(self):
        """Return not deleted providers"""
        return self.filter(deleted_at=None)


class Provider(BaseModel):
    place = models.ForeignKey(
        Place,
        verbose_name='Ресторан',
        related_name='providers',
        on_delete=models.CASCADE,
    )
    title = models.CharField('Название', max_length=255, null=False)
    phone = models.CharField('Телефон', max_length=30, blank=True, null=True)
    email = models.EmailField('E-mail', blank=True, null=True)
    address_actual = models.TextField('Адрес фактический', blank=True, null=True, default=None)
    address_legal = models.TextField('Адрес юридический', blank=True, null=True, default=None)
    description = models.TextField('Описание', blank=True, null=True, default=None)

    objects = ProviderQuerySet.as_manager()

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        ordering = ['title']

    def __str__(self):
        return self.title


class ProductQuerySet(models.QuerySet):
    """Extended queryset for Product model."""

    def active(self):
        """Return not deleted products"""
        return self.filter(deleted_at=None)


class Product(BaseModel):
    invoice = models.ForeignKey(
        Invoice,
        verbose_name='Накладная',
        related_name='products',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    provider = models.ForeignKey(
        Provider,
        verbose_name='Поставщик',
        related_name='products',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    department = models.ForeignKey(
        Department,
        verbose_name='Департамент',
        related_name='products',
        on_delete=models.PROTECT,
    )
    product_group = models.ForeignKey(
        ProductGroup,
        verbose_name='Группа товаров',
        related_name='products',
        on_delete=models.PROTECT,
    )
    net_weight = models.FloatField('Масса нетто')
    gross_weight = models.FloatField('Масса брутто')
    date_of_manufacture = models.DateTimeField('Время изготовления')
    expiration_date = models.PositiveIntegerField('Срок годности', help_text='В днях')
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.product_group.title


class ReasonForWriteOffQuerySet(models.QuerySet):
    """Extended queryset for ReasonForWriteOff model."""

    def active(self):
        """Return not deleted reasons"""
        return self.filter(deleted_at=None)


class ReasonForWriteOff(BaseModel):
    title = models.CharField('Название', max_length=255, null=False)

    objects = ReasonForWriteOffQuerySet.as_manager()

    class Meta:
        verbose_name = 'Причина списания'
        verbose_name_plural = 'Причины списаний'

    def __str__(self):
        return self.title


class WriteOffHistoryQuerySet(models.QuerySet):
    """Extended queryset for WriteOffHistory model."""

    def active(self):
        """Return not deleted history"""
        return self.filter(deleted_at=None)


class WriteOffHistory(BaseModel):
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        related_name='writeoffs',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    reason = models.ForeignKey(
        ReasonForWriteOff,
        verbose_name='Продукт',
        related_name='write_offs',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    comment = models.TextField('Комментарий')
    net_weight = models.FloatField('Масса нетто')
    gross_weight = models.FloatField('Масса брутто')

    objects = WriteOffHistoryQuerySet.as_manager()

    class Meta:
        verbose_name = 'История списания'
        verbose_name_plural = 'История списаний'

    def __str__(self):
        return str(self.product.id)


class MovementHistoryQuerySet(models.QuerySet):
    """Extended queryset for MovementHistory model."""

    def active(self):
        """Return not deleted history"""
        return self.filter(deleted_at=None)


class MovementHistory(BaseModel):
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        related_name='write_offs',
        on_delete=models.CASCADE,
    )
    net_weight = models.FloatField('Масса нетто')
    gross_weight = models.FloatField('Масса брутто')
    measure_unit = models.ForeignKey(
        MeasureUnit,
        verbose_name='Единица измерения',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
    )
    comment = models.TextField('Комментарий')

    objects = MovementHistoryQuerySet.as_manager()

    class Meta:
        verbose_name = 'История перемещения'
        verbose_name_plural = 'История перемещений'

    def __str__(self):
        return str(self.product.id)
