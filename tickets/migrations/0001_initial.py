# Generated by Django 5.1.3 on 2025-04-24 23:06

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='Event')),
                ('event_type', models.ManyToManyField(to='tickets.eventtype')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='Tickets')),
                ('stock', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('event', models.ManyToManyField(to='tickets.event')),
            ],
        ),
        migrations.CreateModel(
            name='BookingDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(blank=True, max_length=250, verbose_name='First Name')),
                ('l_name', models.CharField(blank=True, max_length=250, verbose_name='Last Name')),
                ('email', models.EmailField(blank=True, max_length=250, verbose_name='Email Address')),
                ('phone', models.PositiveIntegerField(blank=True, verbose_name='Phone Number')),
                ('ticket_type', models.CharField(choices=[('standard', 'Standard'), ('vip', 'VIP'), ('student', 'Student')], max_length=10)),
                ('row', models.CharField(blank=True, max_length=250, verbose_name='Row')),
                ('seat', models.PositiveIntegerField(blank=True, verbose_name='Seat')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookingdetails', to='tickets.ticket')),
            ],
        ),
    ]
