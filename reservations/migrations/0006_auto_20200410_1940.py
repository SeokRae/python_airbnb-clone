# Generated by Django 2.2.5 on 2020-04-10 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0002_auto_20200311_1413'),
        ('reservations', '0005_reservation_conversation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='conversation',
        ),
        migrations.AddField(
            model_name='reservation',
            name='conversation',
            field=models.ManyToManyField(blank=True, related_name='reservations', to='conversations.Conversation'),
        ),
    ]
