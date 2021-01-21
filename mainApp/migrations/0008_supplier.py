# Generated by Django 2.0.2 on 2021-01-21 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0007_stockrequirement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('gst_no', models.CharField(blank=True, max_length=200, null=True)),
                ('pan_no', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
