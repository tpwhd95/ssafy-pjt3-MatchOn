# Generated by Django 3.0.5 on 2020-11-04 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beforematch',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='beforematch',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='beforematch',
            name='start_time',
            field=models.TimeField(),
        ),
    ]
