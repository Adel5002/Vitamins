# Generated by Django 4.2.3 on 2023-09-04 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vitamins', '0002_cartorder_phone_number_cartorder_track_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='phone_number',
            field=models.BigIntegerField(),
        ),
    ]
