# Generated by Django 2.0.2 on 2021-01-24 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0011_order_latest_partially_dispatched_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='completed_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_packaged_qty',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
