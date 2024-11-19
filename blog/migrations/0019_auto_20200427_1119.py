# Generated by Django 3.0.5 on 2020-04-27 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_skill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='title',
        ),
        migrations.AddField(
            model_name='about',
            name='skill_title',
            field=models.CharField(default='技能', max_length=50, verbose_name='技能标题'),
        ),
    ]
