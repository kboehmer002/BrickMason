# Generated by Django 4.1.4 on 2023-04-14 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_sourcefile_preprocessed'),
    ]

    operations = [
        migrations.AddField(
            model_name='brick',
            name='file',
            field=models.FileField(default=None),
        ),
    ]