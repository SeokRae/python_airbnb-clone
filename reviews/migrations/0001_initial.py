# Generated by Django 2.2.5 on 2020-03-11 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('review', models.TextField()),
                ('accuracy', models.IntegerField(default=0)),
                ('communication', models.IntegerField(default=0)),
                ('cleanliness', models.IntegerField(default=0)),
                ('location', models.IntegerField(default=0)),
                ('check_in', models.IntegerField(default=0)),
                ('value', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
