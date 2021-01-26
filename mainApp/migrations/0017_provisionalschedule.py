# Generated by Django 2.0.2 on 2021-01-26 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0016_inventory_reserve_qty'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProvisionalSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provision_date', models.DateField()),
                ('qty', models.IntegerField()),
                ('is_finalised', models.BooleanField(default=False)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_data', to='mainApp.Job')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_data', to='mainApp.Order')),
            ],
        ),
    ]