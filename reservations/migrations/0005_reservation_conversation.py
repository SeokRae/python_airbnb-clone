# Generated by Django 2.2.5 on 2020-04-10 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0002_auto_20200311_1413'),
        ('reservations', '0004_auto_20200404_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='conversation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='conversations.Conversation'),
        ),
    ]
