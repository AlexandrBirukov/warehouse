# Generated by Django 4.1.3 on 2022-11-28 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('place', '0001_initial'),
        ('warehouse', '0002_productphoto_invoice_invoice_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='menu.dish', verbose_name='Блюдо')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='TechMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('net_weight', models.FloatField(verbose_name='Масса нетто')),
                ('gross_weight', models.FloatField(verbose_name='Масса брутто')),
                ('done_weight', models.FloatField(verbose_name='Выход готового продукта')),
                ('uncritical', models.BooleanField(default=False, verbose_name='Не критичный для приготовления')),
                ('dish', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='techmaps', to='menu.dish', verbose_name='Блюдо')),
                ('ingredient', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='techmaps', to='menu.ingredient', verbose_name='Ингредиент')),
                ('product_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='techmaps', to='warehouse.productgroup', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Время удаления')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='place.place', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
                'ordering': ['title'],
            },
        ),
        migrations.AddField(
            model_name='dish',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='menu.menu', verbose_name='Меню'),
        ),
    ]