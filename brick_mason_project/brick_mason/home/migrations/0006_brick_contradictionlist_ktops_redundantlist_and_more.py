# Generated by Django 4.1.4 on 2023-03-21 00:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_delete_sourceimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ContradictionList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.BigIntegerField()),
                ('ktops', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='KTOPS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ktops', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RedundantList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.BigIntegerField()),
                ('ktops', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ReferenceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='workfile')),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.brick')),
            ],
        ),
        migrations.CreateModel(
            name='SourceFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='file')),
                ('title', models.CharField(max_length=30)),
                ('date_modified', models.DateField()),
                ('proprocessed', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='SourceFiles',
        ),
        migrations.AddField(
            model_name='referencelist',
            name='fid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.sourcefile'),
        ),
        migrations.AddField(
            model_name='redundantlist',
            name='fid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.sourcefile'),
        ),
        migrations.AddField(
            model_name='ktops',
            name='fid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.sourcefile'),
        ),
        migrations.AddField(
            model_name='contradictionlist',
            name='fid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.sourcefile'),
        ),
    ]