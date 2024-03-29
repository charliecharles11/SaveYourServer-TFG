# Generated by Django 3.2.3 on 2021-06-02 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_file', models.IntegerField(null=True, unique=True)),
                ('upload_date', models.DateTimeField(verbose_name='date uploaded')),
                ('is_malware', models.BooleanField(default=True)),
                ('file_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_notification', models.IntegerField(null=True, unique=True)),
                ('is_visualized', models.BooleanField(default=False)),
                ('message', models.TextField(blank=True, null=True)),
                ('notification_title', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, default='', max_length=255, verbose_name='email address')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('dni', models.CharField(default='', max_length=9, unique=True)),
                ('date_of_birth', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_systemadmin', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
    ]
