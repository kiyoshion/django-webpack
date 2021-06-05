# Generated by Django 3.2.4 on 2021-06-05 20:18

from django.db import migrations
import imagekit.models.fields
import item.models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_alter_itemmodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemmodel',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=item.models.upload_directory_path),
        ),
    ]