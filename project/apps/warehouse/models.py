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
    """
    Склад
    """
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
    """
    Департамент

    могут быть как для хранения, так и для потребления
    ---
    пример департамента хранения: холодильник, овощи, алкоголь
    пример департамента потребления: бар, кухня, зал
    """
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


class MeasureUnitQuerySet(models.QuerySet):
    """Extended queryset for MeasureUnit model."""

    def active(self):
        """Return not deleted measure units"""
        return self.filter(deleted_at=None)


class MeasureUnit(BaseModel):
    """
    Единицы измерения

    пример:
    1. Родитель - title = Бутылка 0.7
    2. Потомок - parent = Бутылка 0.7, title = мл, ratio = 700
    те. Бутылка 0.7 = мл * 700 (parent title = children title * ratio)
    """
    place = models.ForeignKey(
        Place,
        verbose_name='Ресторан',
        related_name='units',
        on_delete=models.CASCADE,
    )
    title = models.CharField('Название', max_length=255, null=False)
    ratio = models.PositiveSmallIntegerField(
        'Коэффициент конвертации',
        help_text='Число, которое нужно умножить на единицу измерения, чтобы получить единицу родителя'
    )
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
    )

    objects = MeasureUnitQuerySet.as_manager()

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
        ordering = ['title']

    def __str__(self):
        return self.title


class NomenclatureGroupQuerySet(models.QuerySet):
    """Extended queryset for NomenclatureGroup model."""

    def active(self):
        """Return not deleted nomenclature groups"""
        return self.filter(deleted_at=None)


class NomenclatureGroup(BaseModel):
    """
    Номенклатурная группа

    пример: говядина, соль, хлеб белый
    """
    place = models.ForeignKey(
        Place,
        verbose_name='Ресторан',
        related_name='groups',
        on_delete=models.CASCADE,
    )
    vendor_code = models.PositiveIntegerField('Артикул')
    title = models.CharField('Название', max_length=255, null=False)
    default_department = models.ForeignKey(
        Department,
        verbose_name='Департамент',
        help_text='Департамент, в который попадает номенклатура при приемке на склад',
        related_name='groups',
        on_delete=models.CASCADE,
    )
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

    # measure_unit_small должна выбираться из потомка MeasureUnit выбранного в поле выше (measure_unit)
    measure_unit_small = models.ForeignKey(
        MeasureUnit,
        verbose_name='Единица измерения для малых порций',
        related_name='smallmesure',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
    )
    markup = models.DecimalField('Наценка %', max_digits=5, decimal_places=2)

    objects = NomenclatureGroupQuerySet.as_manager()

    class Meta:
        verbose_name = 'Номенклатурная группа'
        verbose_name_plural = 'Номенклатурные группы'
        ordering = ['vendor_code', 'title']

    def __str__(self):
        return self.title


class ProductPhotoQuerySet(models.QuerySet):
    """Extended queryset for ProductPhoto model."""

    def active(self):
        """Return not deleted photos"""
        return self.filter(deleted_at=None)


class ProductPhoto(BaseModel):
    """
    Фото для номенклатурной группы
    """
    image_url = models.URLField('Изображение продукта')
    nomenclature_group = models.ForeignKey(
        NomenclatureGroup,
        verbose_name='Номенклатурная группа',
        related_name='photos',
        on_delete=models.CASCADE,
    )

    objects = ProductPhotoQuerySet.as_manager()

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
    """
    Поставщик
    """
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


class InvoiceQuerySet(models.QuerySet):
    """Extended queryset for Invoice model."""

    def active(self):
        """Return not deleted invoices"""
        return self.filter(deleted_at=None)


class Invoice(BaseModel):
    """
    Накладная
    """
    provider = models.ForeignKey(
        Provider,
        verbose_name='Поставщик',
        related_name='invoices',
        on_delete=models.CASCADE,
    )
    invoice_number = models.CharField('Номер накладной', max_length=255, blank=True, null=True, default=None)
    invoice_data = models.DateField('Накладная от')

    objects = InvoiceQuerySet.as_manager()

    class Meta:
        verbose_name = 'Накладная'
        verbose_name_plural = 'Накладные'

    def __str__(self):
        return f'{self.invoice_number} от {self.invoice_data}'


class InvoicePhotoQuerySet(models.QuerySet):
    """Extended queryset for InvoicePhoto model."""

    def active(self):
        """Return not deleted photos"""
        return self.filter(deleted_at=None)


class InvoicePhoto(BaseModel):
    """
    Фотки накладной
    """
    image_url = models.URLField('Изображение накладной')
    invoice = models.ForeignKey(
        Invoice,
        verbose_name='Накладная',
        related_name='photos',
        on_delete=models.CASCADE,
    )

    objects = InvoicePhotoQuerySet.as_manager()

    class Meta:
        verbose_name = 'Накладная'
        verbose_name_plural = 'Накладные'

    def __str__(self):
        return self.image_url


class NomenclatureQuerySet(models.QuerySet):
    """Extended queryset for Nomenclature model."""

    def active(self):
        """Return not deleted nomenclatures"""
        return self.filter(deleted_at=None)


class Nomenclature(BaseModel):
    """
    Номенклатура
    """
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
    nomenclature_group = models.ForeignKey(
        NomenclatureGroup,
        verbose_name='Номенклатурная группа',
        related_name='products',
        on_delete=models.PROTECT,
    )
    # Единица измерения должна выбираться из доступных единиц измерения номенклатурной группы
    measure_unit = models.ForeignKey(
        MeasureUnit,
        verbose_name='Единица измерения',
        related_name='nomenclatures',
        on_delete=models.PROTECT,
    )
    net_weight = models.FloatField('Масса нетто')
    gross_weight = models.FloatField('Масса брутто')
    date_of_manufacture = models.DateTimeField('Время изготовления')
    expiration_date = models.PositiveIntegerField('Срок годности', help_text='В днях')
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2)
    price_without = models.DecimalField('Цена без НДС', max_digits=9, decimal_places=2)

    objects = NomenclatureQuerySet.as_manager()

    class Meta:
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатура'

    def __str__(self):
        return self.nomenclature_group.title


class ReasonForWriteOffQuerySet(models.QuerySet):
    """Extended queryset for ReasonForWriteOff model."""

    def active(self):
        """Return not deleted reasons"""
        return self.filter(deleted_at=None)


class ReasonForWriteOff(BaseModel):
    """
    Причина списания номенклатуры,
    предполагается что это будет стандартный набор причин,
    поэтому возможно их придется заполнить при создании таблицы
    или вообще вынести в переменную.
    """
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
    nomenclature_group = models.ForeignKey(
        NomenclatureGroup,
        verbose_name='Номенклатурная группа',
        related_name='writeoffs',
        on_delete=models.PROTECT,
    )

    # При списании необходимо привязываться к номенклатуре, иначе
    # не получится управлять просрочкой
    nomenclature = models.ForeignKey(
        Nomenclature,
        verbose_name='Номенклатура',
        related_name='writeoffs',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )
    reason = models.ForeignKey(
        ReasonForWriteOff,
        verbose_name='Продукт',
        related_name='writeoffs',
        on_delete=models.PROTECT,
    )
    comment = models.TextField('Комментарий')

    # Единица измерения должна выбираться из доступных единиц измерения номенклатурной группы
    measure_unit = models.ForeignKey(
        MeasureUnit,
        verbose_name='Единица измерения',
        related_name='writeoffs',
        on_delete=models.PROTECT,
    )
    net_weight = models.FloatField('Масса нетто')
    gross_weight = models.FloatField('Масса брутто')

    objects = WriteOffHistoryQuerySet.as_manager()

    class Meta:
        verbose_name = 'История списания'
        verbose_name_plural = 'История списаний'

    def __str__(self):
        return self.nomenclature_group.title


class MovementHistoryQuerySet(models.QuerySet):
    """Extended queryset for MovementHistory model."""

    def active(self):
        """Return not deleted history"""
        return self.filter(deleted_at=None)


class MovementHistory(BaseModel):
    """
    Перемещение
    """
    from_department = models.ForeignKey(
        Department,
        verbose_name='Перемещение из',
        related_name='frommovements',
        on_delete=models.CASCADE,
    )
    to_department = models.ForeignKey(
        Department,
        verbose_name='Перемещение в',
        related_name='tomovements',
        on_delete=models.CASCADE,
    )
    nomenclature_group = models.ForeignKey(
        NomenclatureGroup,
        verbose_name='Номенклатурная группа',
        related_name='movements',
        on_delete=models.PROTECT,
    )

    # При списании необходимо привязываться к номенклатуре, иначе
    # не получится управлять просрочкой
    nomenclature = models.ForeignKey(
        Nomenclature,
        verbose_name='Номенклатура',
        related_name='movements',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
    )

    # Единица измерения должна выбираться из доступных единиц измерения номенклатурной группы
    measure_unit = models.ForeignKey(
        MeasureUnit,
        verbose_name='Единица измерения',
        related_name='movements',
        on_delete=models.PROTECT,
    )
    net_weight = models.FloatField('Масса нетто')
    gross_weight = models.FloatField('Масса брутто')
    comment = models.TextField('Комментарий')

    objects = MovementHistoryQuerySet.as_manager()

    class Meta:
        verbose_name = 'История перемещения'
        verbose_name_plural = 'История перемещений'

    def __str__(self):
        return self.nomenclature_group.title
