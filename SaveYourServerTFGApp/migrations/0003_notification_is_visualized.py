# Generated by Django 3.2.3 on 2021-06-02 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SaveYourServerTFGApp', '0002_remove_notification_is_visualized'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_visualized',
            field=models.BooleanField(default=True),
        ),
    ]
