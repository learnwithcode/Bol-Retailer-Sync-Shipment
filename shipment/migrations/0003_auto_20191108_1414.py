# Generated by Django 2.2 on 2019-11-08 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipment', '0002_auto_20191108_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='shpiment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
