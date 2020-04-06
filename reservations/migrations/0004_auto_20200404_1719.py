# Generated by Django 2.2.5 on 2020-04-04 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_bookedday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedday',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_day', to='reservations.Reservation'),
        ),
    ]
