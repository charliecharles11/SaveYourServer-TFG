# Generated by Django 3.2.3 on 2021-06-22 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SaveYourServerTFGApp', '0009_alter_file_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='upload_date',
        ),
    ]