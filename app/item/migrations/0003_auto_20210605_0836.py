# Generated by Django 3.2.4 on 2021-06-04 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_itemmodel_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemmodel',
            name='thumbnail',
        ),
        migrations.AddField(
            model_name='itemmodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/item/'),
        ),
    ]