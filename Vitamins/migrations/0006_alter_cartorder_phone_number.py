# Generated by Django 4.2.3 on 2023-09-10 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vitamins', '0005_alter_cartorder_address_alter_cartorder_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='phone_number',
            field=models.BigIntegerField(verbose_name='Номер телефона'),
        ),
    ]
