# Generated by Django 5.0.3 on 2024-03-18 04:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regional_name', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'ordering': ['regional_name'],
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_name', models.CharField(max_length=100)),
                ('bus_class', models.CharField(choices=[('O', 'Odinary'), ('S', 'Semi-luxury'), ('L', 'Luxury')], default='S', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terminal_name', models.CharField(max_length=15)),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('region', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Nauli.region')),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField()),
                ('via', models.CharField(blank=True, max_length=15, null=True)),
                ('dist_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_region', to='Nauli.region')),
                ('dist_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_region', to='Nauli.region')),
                ('stops', models.ManyToManyField(to='Nauli.terminal')),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Nauli.route')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Nauli.vehicle')),
            ],
        ),
    ]