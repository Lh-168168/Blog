# Generated by Django 3.0.5 on 2020-04-27 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20200427_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('skill_name', models.CharField(max_length=50, verbose_name='方向名')),
                ('skill_precent', models.CharField(max_length=50, verbose_name='百分比')),
            ],
            options={
                'verbose_name': '技能设置',
                'verbose_name_plural': '技能设置',
            },
        ),
    ]
