# Generated by Django 3.2.3 on 2021-06-03 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SaveYourServerTFGApp', '0005_notification_upload_date_not'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='id_file',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='id_notification',
        ),
    ]
