# Generated by Django 4.1.3 on 2022-11-29 07:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('place', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('department_type', models.PositiveSmallIntegerField(choices=[(0, 'Хранение'), (1, 'Потребление')], default=0, help_text='Хранение/Потребление', verbose_name='Тип департамента')),
            ],
            options={
                'verbose_name': 'Департамент',
                'verbose_name_plural': 'Департаменты',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('invoice_number', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Номер накладной')),
                ('invoice_data', models.DateField(verbose_name='Накладная от')),
            ],
            options={
                'verbose_name': 'Накладная',
                'verbose_name_plural': 'Накладные',
            },
        ),
        migrations.CreateModel(
            name='MeasureUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('ratio', models.PositiveSmallIntegerField(help_text='Число, которое нужно умножить на единицу измерения, чтобы получить единицу родителя', verbose_name='Коэффициент конвертации')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='warehouse.measureunit')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='place.place', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Nomenclature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('net_weight', models.FloatField(verbose_name='Масса нетто')),
                ('gross_weight', models.FloatField(verbose_name='Масса брутто')),
                ('date_of_manufacture', models.DateTimeField(verbose_name='Время изготовления')),
                ('expiration_date', models.PositiveIntegerField(help_text='В днях', verbose_name='Срок годности')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('price_without', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена без НДС')),
                ('invoice', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='warehouse.invoice', verbose_name='Накладная')),
                ('measure_unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='nomenclatures', to='warehouse.measureunit', verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Номенклатура',
                'verbose_name_plural': 'Номенклатура',
            },
        ),
        migrations.CreateModel(
            name='NomenclatureGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('vendor_code', models.PositiveIntegerField(verbose_name='Артикул')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('shelf_life', models.PositiveSmallIntegerField(blank=True, default=None, help_text='В днях', null=True, verbose_name='Базовый срок хранения')),
                ('minimum_balance', models.FloatField(blank=True, default=None, null=True, verbose_name='Минимальный остаток на складе')),
                ('markup', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Наценка %')),
                ('default_department', models.ForeignKey(help_text='Департамент, в который попадает номенклатура при приемке на склад', on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='warehouse.department', verbose_name='Департамент')),
                ('measure_unit', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='stdmesure', to='warehouse.measureunit', verbose_name='Единица измерения')),
                ('measure_unit_small', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='smallmesure', to='warehouse.measureunit', verbose_name='Единица измерения для малых порций')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='place.place', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Номенклатурная группа',
                'verbose_name_plural': 'Номенклатурные группы',
                'ordering': ['vendor_code', 'title'],
            },
        ),
        migrations.CreateModel(
            name='ReasonForWriteOff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Причина списания',
                'verbose_name_plural': 'Причины списаний',
            },
        ),
        migrations.CreateModel(
            name='WriteOffHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('net_weight', models.FloatField(verbose_name='Масса нетто')),
                ('gross_weight', models.FloatField(verbose_name='Масса брутто')),
                ('measure_unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='writeoffs', to='warehouse.measureunit', verbose_name='Единица измерения')),
                ('nomenclature', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='writeoffs', to='warehouse.nomenclature', verbose_name='Номенклатура')),
                ('nomenclature_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='writeoffs', to='warehouse.nomenclaturegroup', verbose_name='Номенклатурная группа')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='writeoffs', to='warehouse.reasonforwriteoff', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'История списания',
                'verbose_name_plural': 'История списаний',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('in_charge_user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='warehouses', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouses', to='place.place', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('phone', models.CharField(blank=True, max_length=30, null=True, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='E-mail')),
                ('address_actual', models.TextField(blank=True, default=None, null=True, verbose_name='Адрес фактический')),
                ('address_legal', models.TextField(blank=True, default=None, null=True, verbose_name='Адрес юридический')),
                ('description', models.TextField(blank=True, default=None, null=True, verbose_name='Описание')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='providers', to='place.place', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('image_url', models.URLField(verbose_name='Изображение продукта')),
                ('nomenclature_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='warehouse.nomenclaturegroup', verbose_name='Номенклатурная группа')),
            ],
            options={
                'verbose_name': 'Накладная',
                'verbose_name_plural': 'Накладные',
            },
        ),
        migrations.AddField(
            model_name='nomenclature',
            name='nomenclature_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='warehouse.nomenclaturegroup', verbose_name='Номенклатурная группа'),
        ),
        migrations.AddField(
            model_name='nomenclature',
            name='provider',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='warehouse.provider', verbose_name='Поставщик'),
        ),
        migrations.CreateModel(
            name='MovementHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('net_weight', models.FloatField(verbose_name='Масса нетто')),
                ('gross_weight', models.FloatField(verbose_name='Масса брутто')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('from_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='frommovements', to='warehouse.department', verbose_name='Перемещение из')),
                ('measure_unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movements', to='warehouse.measureunit', verbose_name='Единица измерения')),
                ('nomenclature', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movements', to='warehouse.nomenclature', verbose_name='Номенклатура')),
                ('nomenclature_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movements', to='warehouse.nomenclaturegroup', verbose_name='Номенклатурная группа')),
                ('to_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tomovements', to='warehouse.department', verbose_name='Перемещение в')),
            ],
            options={
                'verbose_name': 'История перемещения',
                'verbose_name_plural': 'История перемещений',
            },
        ),
        migrations.CreateModel(
            name='InvoicePhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('image_url', models.URLField(verbose_name='Изображение накладной')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='warehouse.invoice', verbose_name='Накладная')),
            ],
            options={
                'verbose_name': 'Накладная',
                'verbose_name_plural': 'Накладные',
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='warehouse.provider', verbose_name='Поставщик'),
        ),
        migrations.AddField(
            model_name='department',
            name='Warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='warehouse.warehouse', verbose_name='Склад'),
        ),
        migrations.AddField(
            model_name='department',
            name='in_charge_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to=settings.AUTH_USER_MODEL, verbose_name='Ответственный'),
        ),
        migrations.AddField(
            model_name='department',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='warehouse.department'),
        ),
    ]
