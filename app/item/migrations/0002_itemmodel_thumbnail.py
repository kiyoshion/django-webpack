# Generated by Django 3.2.3 on 2021-06-04 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmodel',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
