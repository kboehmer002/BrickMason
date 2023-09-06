# Generated by Django 4.1.4 on 2023-03-27 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_sourcefile_preprocessed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contradictionlist',
            old_name='ktops',
            new_name='sentence',
        ),
        migrations.RenameField(
            model_name='redundantlist',
            old_name='ktops',
            new_name='sentence',
        ),
        migrations.AddField(
            model_name='sourcefile',
            name='word_count',
            field=models.IntegerField(default=0),
        ),
    ]