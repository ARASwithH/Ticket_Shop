# Generated by Django 5.2 on 2025-04-28 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='category',
        ),
        migrations.AddField(
            model_name='event',
            name='category',
            field=models.ManyToManyField(default=0, related_name='events', to='events.category'),
        ),
    ]
