# Generated by Django 3.2.10 on 2024-11-17 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0033_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.CharField(blank=True, default='祖国万岁', max_length=10, null=True, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='article',
            name='cover',
            field=models.URLField(default='https://i1.hdslb.com/bfs/article/986da61cd857a85708ef16f21ecc588e4c7edc5d.jpg@1192w.avif', verbose_name='文章封面'),
        ),
        migrations.AlterField(
            model_name='site',
            name='icp_url',
            field=models.URLField(default='#', max_length=100, verbose_name='备案链接'),
        ),
    ]
