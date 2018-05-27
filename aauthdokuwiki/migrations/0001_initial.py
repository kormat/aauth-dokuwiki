# Generated by Django 2.0.4 on 2018-05-27 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='DokuwikiUser',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='dokuwiki', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('enabled', models.BooleanField()),
            ],
            options={
                'permissions': (('access_dokuwiki', 'Can access the Dokuwiki service'),),
            },
        ),
    ]
