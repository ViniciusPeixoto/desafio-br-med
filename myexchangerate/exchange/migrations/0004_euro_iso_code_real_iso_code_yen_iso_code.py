# Generated by Django 4.1.1 on 2022-09-21 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0003_euro_real_yen_delete_currency"),
    ]

    operations = [
        migrations.AddField(
            model_name="euro",
            name="iso_code",
            field=models.CharField(default="EUR", max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="real",
            name="iso_code",
            field=models.CharField(default="BRL", max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="yen",
            name="iso_code",
            field=models.CharField(default="JPY", max_length=3),
            preserve_default=False,
        ),
    ]
