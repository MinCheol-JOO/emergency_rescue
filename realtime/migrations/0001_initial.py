# Generated by Django 3.2 on 2023-05-31 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Emergency_Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.CharField(blank=True, default='', max_length=250)),
                ('address', models.CharField(blank=True, default='', max_length=250)),
                ('phone', models.CharField(blank=True, default='', max_length=250)),
                ('bed_number', models.IntegerField(default=0)),
                ('bed_number_now', models.IntegerField(default=0)),
                ('distance_km', models.IntegerField(default=30)),
            ],
        ),
    ]
