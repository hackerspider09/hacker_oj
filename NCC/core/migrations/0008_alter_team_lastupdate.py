# Generated by Django 4.2.2 on 2023-08-21 14:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_team_lastupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='lastUpdate',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 21, 19, 32, 58, 439525)),
        ),
    ]