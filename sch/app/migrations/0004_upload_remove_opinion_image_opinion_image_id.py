# Generated by Django 4.0.6 on 2022-07-14 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_opinion_pr_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('upload', models.FileField(upload_to='static/img/opinion/')),
            ],
        ),
        migrations.RemoveField(
            model_name='opinion',
            name='image',
        ),
        migrations.AddField(
            model_name='opinion',
            name='image_id',
            field=models.IntegerField(null=True),
        ),
    ]
