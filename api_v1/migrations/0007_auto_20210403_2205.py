# Generated by Django 3.0.12 on 2021-04-03 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_v1', '0006_auto_20210403_2136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
