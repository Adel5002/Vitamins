# Generated by Django 4.2.3 on 2023-07-15 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vitamins', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='release_form',
            field=models.CharField(max_length=120, null=True),
        ),
    ]