# Generated by Django 3.2 on 2022-10-30 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dog_community_app', '0005_alter_events_event_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='events',
            name='event_description',
        ),
    ]
