# Generated by Django 3.2.10 on 2024-11-14 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_auto_20241114_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='year',
            name='year',
            field=models.DateField(unique=True, verbose_name='年份'),
        ),
    ]