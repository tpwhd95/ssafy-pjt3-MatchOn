# Generated by Django 3.0.5 on 2020-11-11 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aftermatch',
            name='fixed_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]