# Generated by Django 4.0.6 on 2022-07-15 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_upload_remove_opinion_image_opinion_image_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upload',
            name='title',
        ),
    ]
