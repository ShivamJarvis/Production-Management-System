# Generated by Django 2.0.2 on 2021-01-24 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0013_order_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockrequirement',
            name='vendor_name',
        ),
    ]
