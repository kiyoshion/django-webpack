# Generated by Django 3.2.4 on 2021-06-14 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_auto_20210613_1905'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='author',
            new_name='user',
        ),
    ]
