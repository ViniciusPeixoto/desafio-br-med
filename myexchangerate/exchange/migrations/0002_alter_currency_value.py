# Generated by Django 4.1.1 on 2022-09-20 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='value',
            field=models.FloatField(default=1),
        ),
    ]